import numpy as np
import scipy
import pandas as pd
import datetime
import networkx as nx
import json
import pickle
import cluster
import ipdb

from datetime import timedelta

'''
load uber_df from csv
load street_df from json
assemble street graph
assemble transition graph
'''
def load_fresh():
	print 'loading uber_df from csv...'
	xmax = -122.36
	xmin = -122.4
	ymax = 37.75
	ymin = 37.71
	# xmax = -122.36
	# xmin = -122.50
	# ymax = 37.82
	# ymin = 37.71
	uber_df = load_uber()
	uber_df = uber_df[uber_df['x'] >= xmin]
	uber_df = uber_df[uber_df['x'] <= xmax]
	uber_df = uber_df[uber_df['y'] >= ymin]
	uber_df = uber_df[uber_df['y'] <= ymax]
	
	uber_df = uber_df[uber_df.groupby(['ride'])['ride'].transform('count') >= 3]
	uber_df = uber_df.groupby('ride').apply(fill_timeseries)
	uber_df = uber_df.drop(['ride'],axis=1).reset_index().drop(['level_1'],axis=1)
	uber_df = uber_df.dropna()
	
	uber_df = uber_df.join(cluster.compute_speed(uber_df))
	bad_rides = uber_df[uber_df['speed'] > 100]['ride'].unique()
	uber_df = uber_df[~uber_df['ride'].isin(bad_rides)]

	uber_df = uber_df.join(cluster.compute_accel(uber_df))
	bad_rides = uber_df[uber_df['accel'] > 4]['ride'].unique()
	bad_rides = np.append(bad_rides, uber_df[uber_df['accel'] < -10]['ride'].unique())
	bad_rides = set(bad_rides)
	uber_df = uber_df[~uber_df['ride'].isin(bad_rides)]

	uber_df.pop('speed')
	uber_df.pop('accel')

	print str(len(uber_df)) + ' timestamps'
	print str(len(uber_df['ride'].unique())) + ' rides'
	print 'loaded uber_df'
	pickle.dump(uber_df,open('../pickles/uber_df.pkl','wb'))

	print 'loading street df from json...'
	street_df = load_streets(n=1)
	pickle.dump(street_df,open('../pickles/street_df.pkl','wb'))
	# street_df = street_df = street_df[(street_df['xstart'] >= xmin) & (street_df['xstart'] <= xmax) &
	# 	(street_df['xstop'] >= xmin) & (street_df['xstop'] <= xmax) &
	# 	(street_df['ystart'] >= ymin) & (street_df['ystart'] <= ymax) &
	# 	(street_df['ystop'] >= ymin) & (street_df['ystop'] <= ymax)]
	print 'loaded street df'

	print 'assembling street graph...'
	street_graph, node_coord_dict, coord_node_dict, edge_dict, coord_lookup = create_graph(street_df)
	pickle.dump(street_graph,open('../pickles/street_graph.pkl','wb'))
	pickle.dump(node_coord_dict,open('../pickles/node_coord_dict.pkl','wb'))
	pickle.dump(coord_node_dict,open('../pickles/coord_node_dict.pkl','wb'))
	pickle.dump(edge_dict,open('../pickles/edge_dict.pkl','wb'))
	pickle.dump(coord_lookup,open('../pickles/coord_lookup.pkl','wb'))
	print 'assembled street graph'

	print 'assembling transition graph...'
	transition_graph, trans_edge_dict, edge_trans_dict, transnode_node_dict = create_transition_graph(street_graph, node_coord_dict, edge_dict)
	pickle.dump(transition_graph,open('../pickles/transition_graph.pkl','wb'))
	pickle.dump(trans_edge_dict,open('../pickles/trans_edge_dict.pkl','wb'))
	pickle.dump(edge_trans_dict,open('../pickles/edge_trans_dict.pkl','wb'))
	print 'assembled transition graph'

	return uber_df, street_df, street_graph, node_coord_dict, coord_node_dict, edge_dict, coord_lookup, transition_graph, trans_edge_dict, edge_trans_dict

'''
read uber_df from pickle
read street_df from pickle
read street graph from pickle
read transition graph from pickle
'''
def from_pickle():
	print 'reading uber_df from pickle...'
	uber_df = pickle.load(open('../pickles/uber_df.pkl'))
	print 'read uber_df'
	uber_df = uber_df.groupby('ride').apply(fill_timeseries)

	print 'reading street df from pickle...'
	street_df = pickle.load(open('../pickles/street_df.pkl','rb'))
	print 'read street df'
	# street_df = street_df = street_df[(street_df['xstart'] >= xmin) & (street_df['xstart'] <= xmax) &
	# 	(street_df['xstop'] >= xmin) & (street_df['xstop'] <= xmax) &
	# 	(street_df['ystart'] >= ymin) & (street_df['ystart'] <= ymax) &
	# 	(street_df['ystop'] >= ymin) & (street_df['ystop'] <= ymax)]

	print 'reading street graph from pickle...'
	street_graph = pickle.load(open('../pickles/street_graph.pkl','rb'))
	node_coord_dict = pickle.load(open('../pickles/node_coord_dict.pkl','rb'))
	coord_node_dict = pickle.load(open('../pickles/coord_node_dict.pkl','rb'))
	edge_dict = pickle.load(open('../pickles/edge_dict.pkl','rb'))
	coord_lookup = pickle.load(open('../pickles/coord_lookup.pkl','rb'))
	print 'read street graph'

	print 'reading transition graph from pickle...'
	transition_graph = pickle.load(open('../pickles/transition_graph.pkl','rb'))
	trans_edge_dict = pickle.load(open('../pickles/trans_edge_dict.pkl','rb'))
	edge_trans_dict = pickle.load(open('../pickles/edge_trans_dict.pkl','rb'))
	print 'read transition graph'

	return uber_df, street_df, street_graph, node_coord_dict, coord_node_dict, edge_dict, coord_lookup, transition_graph, trans_edge_dict, edge_trans_dict

def dparser(datestring):
	return datetime.datetime.strptime(datestring,'%Y-%m-%dT%H:%M:%S+00:00')

'''
load uber coord data from csv into DataFrame
'''
def load_uber(nlines=-1):
	column_names = ['ride', 'datetime', 'y', 'x']
	uber_df = pd.read_csv('../uber_data/all.tsv', sep='\t', header=None, names=column_names,
		parse_dates=[1], date_parser=dparser)

	# some rides have duplicated datapoints
	uber_df.drop_duplicates(inplace=True)

	uber_df = uber_df[(uber_df['x'] >= -123) & (uber_df['x'] <= -122) &
			(uber_df['y'] >= 37) & (uber_df['y'] <= 38)]

	# remove remaining rides that are shorter than 5 minutes
	uber_df = uber_df[uber_df.groupby(['ride'])['ride'].transform('count') >= 3] 
	# should actually do this by filtering trip duration, rather than value counts

	return uber_df.iloc[:nlines]

def fill_timeseries(data):
	return data.set_index('datetime').resample('4000L',fill_method='pad').reset_index()

'''
load street geo data from json into DataFrame
'''
def load_streets(n=0):
	with open('../street_centerlines/stclines_streets.json') as f:
		streets = json.loads(f.read())

	df = pd.DataFrame()
	for street in streets['features']:
		df = pd.concat([df, pd.DataFrame([
			street['properties']['STREETNAME'],
			street['properties']['ONEWAY'],
			int(street['properties']['CLASSCODE']),
			float(street['geometry']['coordinates'][0][0]),
			float(street['geometry']['coordinates'][0][1]),
			float(street['geometry']['coordinates'][-1][0]),
			float(street['geometry']['coordinates'][-1][1])
			]).T],axis=0)
	colnames = ['name','oneway','class','xstart','ystart','xstop','ystop']
	df.columns = colnames
	df.reset_index(inplace=True)
	df.pop('index')
	nstreets = len(df)
	# xstarts = np.zeros((nstreets,1))
	# ystarts = np.zeros((nstreets,1))
	# xstops = np.zeros((nstreets,1))
	# ystops = np.zeros((nstreets,1))
	
	if n == 0:
		'''
		prepare input file for fortran program to convert state plane
		coordinates to lat long coordinates
		'''
		file81 = open('../nad83/input.81','wb')
		for i, row in df.iterrows():
			xstart = int(row['xstart']*304.80061)
			ystart = int(row['ystart']*304.80061)
			xstop = int(row['xstop']*304.80061)
			ystop = int(row['ystop']*304.80061)
			output = '      *81*                                  %10d%11d0403\n' % (xstart, ystart)
			file81.write(output)
			output = '      *81*                                  %10d%11d0403\n' % (xstop, ystop)
			file81.write(output)
	else:
		'''
		parse fortran program output of lat long coordinates
		write into DataFrame
		'''
		file80 = open('../nad83/output.80','rb')
		for i, row in df.iterrows():
			line = file80.readline()
			lat = float(line[44:46]) + float(line[46:48])/60 + float(line[48:50] + '.' + line[50:55])/3600
			lng = -(float(line[56:59]) + float(line[59:61])/60 + float(line[61:63] + '.' + line[63:68])/3600)
			row['xstart'] = lng
			row['ystart'] = lat
			line = file80.readline()
			lat = float(line[44:46]) + float(line[46:48])/60 + float(line[48:50] + '.' + line[50:55])/3600
			lng = -(float(line[56:59]) + float(line[59:61])/60 + float(line[61:63] + '.' + line[63:68])/3600)
			row['xstop'] = lng
			row['ystop'] = lat

	# apikeys = ['AIzaSyDFKC9RzHpgfCdnslTL0QXNHO_JpWcYXuQ',
	# 		'AIzaSyBTO9qExEKhrwT4lr8g0t3-B99wOWdPZ50',
	# 		'AIzaSyBxH0Ddo3jA5hs4S2K4p97gOFGTd_JenUo',
	# 		'AIzaSyDvRO-SXSI4O5k-JuwMimjUysI6-E2Xfp4',
	# 		'AIzaSyDWrMtTB22XPpHqW1izt86W-IRerEpsa4s',
	# 		'AIzaSyCRr-NOee3V0leRNBw_INQqiCsvBLf-2sQ',
	# 		'AIzaSyDYd4vMnyBr55xWb4FVwedgvGOuEHKKAJw',
	# 		'AIzaSyAnwR8-ENkEK8yJlF9akU6n1PknorTY_wY',
	# 		'AIzaSyBbKW7pUx7aE6PrBkBDhl3KYPyYufIzh0E',
	# 		'AIzaSyC7RykRoFJY_fgBDt-vG_JPjDc3BmECCWQ',
	# 		'AIzaSyD_KHdVxL_r3s2JLFeu-qFG7dhiYsrTISU']

	# conn = psycho.connect(dbname ='coords')
	# cur = conn.cursor()
	# cur.execute('create table coords (id serial primary key, intersection varchar(100), lat real, lng real)')
	# conn.commit()

	# keycount = 0
	# for i, row in df.iterrows():
	# 	xstarti = row[2]
	# 	ystarti = row[3]
	# 	streeti = str(row[0])
	# 	inds_j = df[ (df['xstop'] == xstarti) & (df['ystop'] == ystarti) ].index
	# 	if len(inds_j) != 0:
	# 		streetj = str(df.ix[inds_j[0],'name'])
	# 		intersection = streeti + ' & ' + streetj + ', San Francisco, CA'
	# 		try:
	# 			lat,lng = Geocoder(apikeys[keycount]).geocode(intersection)[0].coordinates
	# 		except GeocoderError, e:
	# 			if e[0] == 'ZERO_RESULTS':
	# 				lat,lng = -1,-1
	# 			else:
	# 				time.sleep(1)
	# 				try:
	# 					lat,lng = Geocoder(apikeys[keycount]).geocode(intersection)[0].coordinates
	# 				except GeocoderError:
	# 					keycount += 1
	# 					lat,lng = Geocoder(apikeys[keycount]).geocode(intersection)[0].coordinates
	# 		except ConnectionError:
	# 			lat,lng = -1,-1
	# 		cur.execute("""INSERT INTO coords(intersection, lat, lng) VALUES ('%s', '%s', '%s')""" % (intersection, lat, lng))
	# 		conn.commit()
	# 	else:
	# 		address = streeti + ', San Francisco, CA'
	# 		try:
	# 			lat,lng = Geocoder(apikeys[keycount]).geocode(address)[0].coordinates
	# 		except GeocoderError, e:
	# 			if e[0] == 'ZERO_RESULTS':
	# 				lat,lng = -1,-1
	# 			else:
	# 				time.sleep(1)
	# 				try:
	# 					lat,lng = Geocoder(apikeys[keycount]).geocode(address)[0].coordinates
	# 				except GeocoderError:
	# 					keycount += 1
	# 					lat,lng = Geocoder(apikeys[keycount]).geocode(address)[0].coordinates
	# 		except ConnectionError:
	# 			lat,lng = -1,-1
	# 		cur.execute("""INSERT INTO coords(intersection, lat, lng) VALUES ('%s', '%s', '%s')""" % (address, lat, lng))
	# 		conn.commit()

	# 	xstarts[i] = lng
	# 	ystarts[i] = lat
	# 	for j in inds_j:
	# 		xstops[j] = lng
	# 		ystops[j] = lat

	# for i in xrange(nstreets):
	# 	if xstarts[i] == 0:
	# 		xstarts[i] = xstops[i]
	# 		ystarts[i] = ystops[i]
	# 	if xstops[i] == 0:
	# 		xstops[i] = xstarts[i]
	# 		ystops[i] = ystarts[i]

	# df['xstart'] = xstarts
	# df['ystart'] = ystarts
	# df['xstop'] = xstops
	# df['ystop'] = ystops

	# df = df[df['xstart'] != -1]
	# # df = df[ (df['xstop'] != 0) & (df['ystop'] != 0) ]
	
	df = df[(df['xstart'] >= -123) & (df['xstart'] <= -122) &
			(df['xstop'] >= -123) & (df['xstop'] <= -122) &
			(df['ystart'] >= 37) & (df['ystart'] <= 38) &
			(df['ystop'] >= 37) & (df['ystop'] <= 38)]

	return df

'''
Create directed street network graph from street DataFrame
'''
def create_graph(df):
	G=nx.DiGraph().to_directed()
	edge_dict = {}
	node_count = 0
	node_coord_dict = {}
	coord_node_dict = {}
	coord_lookup = {}

	class_wt_dict = {}
	class_wt_dict[0] = 1./20
	class_wt_dict[1] = 1./65
	class_wt_dict[2] = 1./45
	class_wt_dict[3] = 1./35
	class_wt_dict[4] = 1./35
	class_wt_dict[5] = 1./25
	class_wt_dict[6] = 1./45
	
	for i, street in df.iterrows():
		xstart = street['xstart']
		ystart = street['ystart']
		xstop = street['xstop']
		ystop = street['ystop']

		if (xstart,ystart) not in coord_node_dict.keys():
			start_node = node_count
			node_coord_dict[start_node] = (xstart,ystart)
			coord_node_dict[(xstart,ystart)] = node_count
			node_count += 1
		else:
			start_node = coord_node_dict[(xstart,ystart)]

		if (xstop,ystop) not in coord_node_dict.keys():
			stop_node = node_count
			node_coord_dict[stop_node] = (xstop,ystop)
			coord_node_dict[(xstop,ystop)] = node_count
			node_count += 1
		else:
			stop_node = coord_node_dict[(xstop,ystop)]

		xstart_trunc = format(xstart,'.2f')
		xstart_truncp = format(xstart+0.01,'.2f')
		xstart_truncm = format(xstart-0.01,'.2f')
		ystart_trunc = format(ystart,'.2f')
		ystart_truncp = format(ystart+0.01,'.2f')
		ystart_truncm = format(ystart-0.01,'.2f')
		xstop_trunc = format(xstop,'.2f')
		xstop_truncp = format(xstop+0.01,'.2f')
		xstop_truncm = format(xstop-0.01,'.2f')
		ystop_trunc = format(ystop,'.2f')
		ystop_truncp = format(ystop+0.01,'.2f')
		ystop_truncm = format(ystop-0.01,'.2f')

		keys = [(xstart_trunc,ystart_trunc),
				(xstart_truncm,ystart_truncm),
				(xstart_truncm,ystart_trunc),
				(xstart_truncm,ystart_truncp),
				(xstart_trunc,ystart_truncp),
				(xstart_truncp,ystart_truncp),
				(xstart_truncp,ystart_trunc),
				(xstart_truncp,ystart_truncm),
				(xstart_trunc,ystart_truncm),
				(xstart_trunc,ystart_trunc),
				(xstop_truncm,ystop_truncm),
				(xstop_truncm,ystop_trunc),
				(xstop_truncm,ystop_truncp),
				(xstop_trunc,ystop_truncp),
				(xstop_truncp,ystop_truncp),
				(xstop_truncp,ystop_trunc),
				(xstop_truncp,ystop_truncm),
				(xstop_trunc,ystop_truncm)]

		if node_coord_dict[start_node] != node_coord_dict[stop_node]:
			if street['oneway'] != 'T':
				wt = class_wt_dict[street['class']]
				G.add_path([start_node, stop_node])
				edge_dict[(start_node, stop_node)] = [street['name'],street['class']]
				for key in keys:
					if key in coord_lookup.keys():
						coord_lookup[key].add((start_node, stop_node))
					else:
						coord_lookup[key] = set([(start_node, stop_node)])

			if street['oneway'] != 'F':
				wt = class_wt_dict[street['class']]
				G.add_path([stop_node, start_node])
				edge_dict[(stop_node, start_node)] = [street['name'],street['class']]
				for key in keys:
					if key in coord_lookup.keys():
						coord_lookup[key].add((stop_node, start_node))
					else:
						coord_lookup[key] = set([(stop_node, start_node)])

	for edge in G.edges_iter():
		node1 = node_coord_dict[edge[0]]
		node2 = node_coord_dict[edge[1]]
		edge_len, edge_vec = edge_eval(node1,node2)
		edge_dict[edge].append(edge_len)
		edge_dict[edge].append(edge_vec)
		wt = edge_dict[edge][1]*edge_dict[edge][2]
		G[edge[0]][edge[1]]['weight'] = wt

	'''
	edge_dict keyed on node-node tuple
	values are list of street name, street class, edge length, edge unit vec
	'''
	return G, node_coord_dict, coord_node_dict, edge_dict, coord_lookup

'''
INPUT: start and stop coordinates of a vector
OUTPUT: length and unit vector
'''
def edge_eval(start, stop):
	length = ((start[0] - stop[0])**2 + (start[1] - stop[1])**2)**0.5
	unit_vec = np.array([(stop[0] - start[0])/length, (stop[1] - start[1])/length])
	return length, unit_vec

'''
INPUT: start/stop coordinates (as a tuple), length, and unit vector
OUTPUT: new vector shortened to 1%-90% of original vector
'''
def shorten_edge(coord, length, unit_vec):
	# could actually just compute full vector here...
	# but length and unit_vec give more flexibility for later changes
	start_coord = (coord[0]+unit_vec[0]*length*0.01, coord[1]+unit_vec[1]*length*0.01)
	stop_coord = (coord[0]+unit_vec[0]*length*0.9, coord[1]+unit_vec[1]*length*0.9)
	return start_coord, stop_coord

'''
INPUT: original street graph, node-to-coordinates dictionary, edge dictionary
OUTPUT: new directed graph with shortened street edges and new transition edges
'''
def create_transition_graph(G, node_dict, edge_dict):
	newG = nx.DiGraph().to_directed()
	start_dict = {}
	stop_dict = {}
	trans_edge_dict = {}
	edge_trans_dict = {}
	node_count = 0
	transnode_node_dict = {}
	for edge in G.edges_iter():
		new_edge_coords = shorten_edge(node_dict[edge[0]], edge_dict[edge][2], edge_dict[edge][3])
		wt = G[edge[0]][edge[1]]['weight']
		newG.add_path([node_count, node_count+1], weight=wt)
		new_edge = (node_count, node_count+1)
		node_count += 2
		trans_edge_dict[new_edge] = edge
		edge_trans_dict[edge] = new_edge
		transnode_node_dict[new_edge[0]] = edge[0]
		transnode_node_dict[new_edge[1]] = edge[1]
		if edge[0] in start_dict:
			start_dict[edge[0]].append(new_edge[0])
		else:
			start_dict[edge[0]] = [new_edge[0]]
		stop_dict[new_edge[1]] = edge[1]

	for newstop, oldstop in stop_dict.iteritems():
		if oldstop in start_dict:
			for newstart in start_dict[oldstop]:
				newG.add_path([newstop, newstart], weight=9999)

	# for edge in newG.edges():
	# 	if edge not in trans_edge_dict:
	# 		oldedge1 = (transnode_node_dict[edge[0]], transnode_node_dict[edge[0]])
	# 		oldedge2 = (transnode_node_dict[edge[1]], transnode_node_dict[edge[1]])

	return newG, trans_edge_dict, edge_trans_dict, transnode_node_dict