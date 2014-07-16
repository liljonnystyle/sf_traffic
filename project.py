#!/usr/bin/python
import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import networkx as nx
import json
import ast
import time
import sys
import pickle
import psycopg2 as psycho

from pygeocoder import Geocoder, GeocoderError
from collections import Counter
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform
from scipy.stats import mode
from sklearn.linear_model import LinearRegression
from sklearn import cluster, datasets 
from sklearn.preprocessing import StandardScaler

# Central finite difference function to estimate derivatives
def deriv(x):
	"Finite difference derivative of the function f"
	n = len(x)
	d = np.zeros(n,'float') # assume float
	# Use centered differences for the interior points, one-sided differences for the ends
	for i in xrange(1,n-1):
		d[i] = (x.iloc[i+1]-x.iloc[i])/(x.index[i+1]-x.index[i]).total_seconds()
	d[0] = (x.iloc[1]-x.iloc[0])/(x.index[1]-x.index[0]).total_seconds()
	d[n-1] = (x.iloc[n-1]-x.iloc[n-2])/(x.index[n-1]-x.index[n-2]).total_seconds()
	return d

def dparser(datestring):
	return datetime.datetime.strptime(datestring,'%Y-%m-%dT%H:%M:%S+00:00')

def load_uber(nlines=-1):
	column_names = ['ride', 'datetime', 'y', 'x']
	uber_df = pd.read_csv('uber_data/all.tsv', sep='\t', header=None, names=column_names,
		parse_dates=[1], date_parser=dparser)

	# some rides have duplicated datapoints
	uber_df.drop_duplicates(inplace=True)

	# remove remaining rides that are shorter than 5 minutes
	#df = df[df.groupby(['ride'])['ride'].transform('count') >= 75] 
	# should actually do this by filtering trip duration, rather than value counts

	# resample to every 2 seconds
	return uber_df.iloc[:nlines]

def load_streets():
	with open('street_centerlines/stclines_streets.json') as f:
		streets = json.loads(f.read())

	df = pd.DataFrame()
	for street in streets['features']:
		df = pd.concat([df, pd.DataFrame([
			street['properties']['STREETNAME'],
			street['properties']['ONEWAY'],
			street['geometry']['coordinates'][0][0],
			street['geometry']['coordinates'][0][1],
			street['geometry']['coordinates'][-1][0],
			street['geometry']['coordinates'][-1][1]
			]).T],axis=0)
	colnames = ['name','oneway','xstart','ystart','xstop','ystop']
	df.columns = colnames
	df.reset_index(inplace=True)
	df.pop('index')
	nstreets = len(df)
	xstarts = np.zeros((nstreets,1))
	ystarts = np.zeros((nstreets,1))
	xstops = np.zeros((nstreets,1))
	ystops = np.zeros((nstreets,1))

	apikeys = ['AIzaSyDFKC9RzHpgfCdnslTL0QXNHO_JpWcYXuQ',
			'AIzaSyBTO9qExEKhrwT4lr8g0t3-B99wOWdPZ50',
			'AIzaSyBxH0Ddo3jA5hs4S2K4p97gOFGTd_JenUo',
			'AIzaSyDvRO-SXSI4O5k-JuwMimjUysI6-E2Xfp4',
			'AIzaSyDWrMtTB22XPpHqW1izt86W-IRerEpsa4s',
			'AIzaSyCRr-NOee3V0leRNBw_INQqiCsvBLf-2sQ',
			'AIzaSyDYd4vMnyBr55xWb4FVwedgvGOuEHKKAJw',
			'AIzaSyAnwR8-ENkEK8yJlF9akU6n1PknorTY_wY',
			'AIzaSyBbKW7pUx7aE6PrBkBDhl3KYPyYufIzh0E',
			'AIzaSyC7RykRoFJY_fgBDt-vG_JPjDc3BmECCWQ',
			'AIzaSyD_KHdVxL_r3s2JLFeu-qFG7dhiYsrTISU']

	conn = psycho.connect(dbname ='coords')
	cur = conn.cursor()
	cur.execute('create table coords (id serial primary key, intersection varchar(100), lat real, lng real)')
	conn.commit()

	keycount = 0
	for i, row in df.iterrows():
		xstarti = row[2]
		ystarti = row[3]
		streeti = str(row[0])
		inds_j = df[ (df['xstop'] == xstarti) & (df['ystop'] == ystarti) ].index
		if len(inds_j) != 0:
			streetj = str(df.ix[inds_j[0],'name'])
			intersection = streeti + ' & ' + streetj + ', San Francisco, CA'
			try:
				lat,lng = Geocoder(apikeys[keycount]).geocode(intersection)[0].coordinates
			except GeocoderError, e:
				if e[0] == 'ZERO_RESULTS':
					lat,lng = -1,-1
				else:
					time.sleep(1)
					try:
						lat,lng = Geocoder(apikeys[keycount]).geocode(intersection)[0].coordinates
					except GeocoderError:
						keycount += 1
						lat,lng = Geocoder(apikeys[keycount]).geocode(intersection)[0].coordinates
			except ConnectionError:
				lat,lng = -1,-1
			cur.execute("""INSERT INTO coords(intersection, lat, lng) VALUES ('%s', '%s', '%s')""" % (intersection, lat, lng))
			conn.commit()
		else:
			address = streeti + ', San Francisco, CA'
			try:
				lat,lng = Geocoder(apikeys[keycount]).geocode(address)[0].coordinates
			except GeocoderError, e:
				if e[0] == 'ZERO_RESULTS':
					lat,lng = -1,-1
				else:
					time.sleep(1)
					try:
						lat,lng = Geocoder(apikeys[keycount]).geocode(address)[0].coordinates
					except GeocoderError:
						keycount += 1
						lat,lng = Geocoder(apikeys[keycount]).geocode(address)[0].coordinates
			except ConnectionError:
				lat,lng = -1,-1
			cur.execute("""INSERT INTO coords(intersection, lat, lng) VALUES ('%s', '%s', '%s')""" % (address, lat, lng))
			conn.commit()

		xstarts[i] = lng
		ystarts[i] = lat
		for j in inds_j:
			xstops[j] = lng
			ystops[j] = lat

	for i in xrange(nstreets):
		if xstarts[i] == 0:
			xstarts[i] = xstops[i]
			ystarts[i] = ystops[i]
		if xstops[i] == 0:
			xstops[i] = xstarts[i]
			ystops[i] = ystarts[i]

	df['xstart'] = xstarts
	df['ystart'] = ystarts
	df['xstop'] = xstops
	df['ystop'] = ystops

	df = df[df['xstart'] != -1]
	# df = df[ (df['xstop'] != 0) & (df['ystop'] != 0) ]
	#pickle.dump(df, open('pickles/street_df.pkl','wb'))
	return df

def create_graph(df):
	G=nx.DiGraph()
	for street in df.iterrows():
		street = street[1]
		start_node = (street['xstart'],street['ystart'])
		stop_node = (street['xstop'],street['ystop'])
		if start_node != stop_node:
			if street['oneway'] != 'T':
				G.add_edge(start_node, stop_node)
			if street['oneway'] != 'F':
				G.add_edge(stop_node, start_node)
	return G

def edge_eval(start, stop):
	length = ((start[0] - stop[0])**2 + (start[1] - stop[1])**2)**0.5
	unit_vec = np.array([(stop[0] - start[0])/length, (stop[1] - start[1])/length])
	return length, unit_vec

def shorten_edge(edge):
	length, unit_vec = edge_eval(edge[0], edge[1])
	# could actually just compute full vector here...
	# but length and unit_vec give more flexibility for later changes
	start_node = (edge[0][0]+unit_vec[0]*length*0.01, edge[0][1]+unit_vec[1]*length*0.01)
	stop_node = (edge[0][0]+unit_vec[0]*length*0.9, edge[0][1]+unit_vec[1]*length*0.9)
	return start_node, stop_node

def create_transition_graph(G):
	newG = nx.DiGraph()
	starts = []
	stops = []
	trans_dict = {}
	for edge in G.edges_iter():
		new_edge = shorten_edge(edge)
		trans_dict[edge] = new_edge
		newG.add_edge(*new_edge, weight=9999)
		starts.append([edge[0], new_edge[0]])
		stops.append([new_edge[1], edge[1]])
	for stop in stops:
		newstops = [start[1] for start in starts if start[0] == stop[1]]
		for newstop in newstops:
			newG.add_edge(stop[0], newstop, weight=9999)
	return newG, trans_dict

def point_to_line(point, start, stop):
	startstop_len, startstop_vec = edge_eval(start, stop)
	startpoint_len, startpoint_vec = edge_eval(start, point)
	cosang = np.dot(startstop_vec, startpoint_vec)
	sinang = np.linalg.norm(np.cross(startstop_vec, startpoint_vec))
	# angle = np.arctan2(sinang, cosang)
	dist = startpoint_len * sinang
	frac = startpoint_len * cosang / startstop_len
	return dist, frac

def project(uber_df, G, transG, trans_dict):
	def find_nearest_street(data):
		min_dist = 9999
		for edge in G.edges_iter():
			dist, frac = point_to_line(data, edge[0], edge[1])
			if dist < min_dist and (frac >= 0 and frac <= 1):
				min_dist = dist
				min_edge = edge
				min_frac = frac

		return pd.Series([min_edge, min_frac])
		
	tmp = uber_df[['x','y']].apply(find_nearest_street, axis=1)
	uber_df['edge'] = tmp[0]
	uber_df['fraction'] = tmp[1]

	def voting(edges, fracs):
		edges_str = edges.apply(str)
		for i, edge in enumerate(edges_str):
			# set the beginning and end of moving window
			if i == 0:
				edgemode = edge
			elif i == 1:
				edgemode, freq = Counter(edges_str.iloc[i-1:i+2]).most_common(1)[0]
				if freq == 0:
					edgemode = edge
			elif i == len(edges) - 2:
				edgemode, freq = Counter(edges_str.iloc[i-1:i+2]).most_common(1)[0]
				if freq == 0:
					edgemode = edge
			elif i == len(edges) - 1:
				edgemode = edge
			else:
				edgemode, freq = Counter(edges_str.iloc[i-2:i+3]).most_common(1)[0]
				if freq == 0:
					edgemode = edge
			# print str(i) + ': ' + edgemode
			if edge != edgemode:
				# reset edge column to match mode of moving window
				edges.iloc[i] = ast.literal_eval(edgemode)
				# then adjust frac column..
				fracs.iloc[i] = np.mean(fracs.iloc[i-1:i+1])
		return edges, fracs

	def check_edges(edges, fracs, ride):
		error = 0
		lr = LinearRegression()

		newedges = np.array(edges)
		newfracs = np.array(fracs)
		for i, edge in enumerate(edges):
			if i != 0:
				if edge == oldedge:
					curr_inds.append(i)
				else:
					inds = np.where(edges == oldedge)[0]
					x = np.arange(len(inds))[:,np.newaxis]
					y = np.array(np.array(fracs)[inds])
					try:
						lr.fit(x,y)
					except AttributeError:
						print x, type(x)
						print y, type(y)
					if lr.coef_[0] < 0:
						newedge = (oldedge[1], oldedge[0])
						if newedge in G.nodes():
							for j in curr_inds:
								newedges[j] = newedge
								newfracs[j] = 1 - fracs[j]
						else:
							print 'ride ' + str(ride) + ' can not reverse edge ' + str(edge)
							error = 1
							return edges, fracs, error
					oldedge = edge
					curr_inds = [i]
			else:
				oldedge = edge
				curr_inds = [i]

		for i, edge in enumerate(newedges):
			if i != 0:
				if edge != oldedge:
					if edge[0] != oldedge[1]:
						print 'ride ' + str(ride) + ' node match error:'
						print '\t' + str(oldedge) + ' & ' + str(edge)
						error = 1
						return edges, fracs, error
			oldedge = edge
		return newedges, newfracs, error

	def get_trans_edges(edges, fracs, ride):
		transedges = np.array(edges)
		error = 0
		for i, frac in enumerate(fracs):
			tmp = trans_dict[edges[i]]
			if frac < 0.01: # beginning of edge, go backwards to find previous edge
				check = 0
				for j in xrange(i-1, 0, -1):
					if edges[i] != edges[j]:
						transedges[i] = (trans_dict[edges[j]][1],tmp[0])
						check = 1
						break
				if check == 0: # got to beginning of series with no previous edge, assign any trans edge that matches
					for edge_it in G.edges_iter():
						if edge_it[1] == edges[i][0]:
							transedges[i] = (trans_dict[edge_it][1],tmp[0])
							break
			elif frac > 0.9: # end of edge, go forwards to find next edge
				check = 0
				for j in xrange(i+1, len(edges)):
					if edges[i] != edges[j]:
						transedges[i] = (tmp[1],trans_dict[edges[j]][0])
						check = 1
						break
				if check == 0: # got to end of series with no next edge, assign any trans edge that matches
					for edge_it in G.edges_iter():
						if edge_it[0] == edges[i][1]:
							transedges[i] = (tmp[1],trans_dict[edge_it][0])
							break
			else:
				transedges[i] = tmp

			if transedges[i] not in transG.edges:
				print 'ride ' + str(ride) + ' transition edge mismatch'
				print 'transition ' + str(transedges[i]) + ' does not exist'
				error = 1
				break
		return transedges, error

	def update_loc(edges, fracs):
		newx = np.zeros((len(edges),))
		newy = np.zeros((len(edges),))
		for i, edge in enumerate(edges):
			length, unit_vec = edge_eval(edge[0], edge[1])
			vec = unit_vec*length*fracs[i]
			newx[i] = edge[0][0] + vec[0]
			newy[i] = edge[0][1] + vec[1]
		return newy, newx

	def dftransform(subdf):
		error = 0
		edges, fracs = voting(subdf['edge'],subdf['fraction'])
		edges, fracs, error = check_edges(edges, fracs, subdf['ride'].iloc[0])
		# if error == 1:
			# return subdf, edges, error
		transedges, error = get_trans_edges(edges, fracs, subdf['ride'].iloc[0])
		# if error == 1:
			# return subdf, edges, error
		newy, newx = update_loc(edges, fracs)

		return np.vstack([newy, newx, edges, fracs]).T, transedges, error

	rides = uber_df['ride'].unique()
	transedges_array = np.array([])
	for ride in rides:
		tmp, transedges, error = dftransform(uber_df[uber_df['ride'] == ride])
		uber_df.ix[uber_df['ride'] == ride,['y','x','edge','fraction']] = tmp
		if error == 1:
			uber_df = uber_df[uber_df['ride'] != ride]
		else:
			transedges_array = np.hstack([transedges_array,transedges])
	uber_df['trans_edge'] = transedges_array
	# update x and y
	return uber_df

def compute_speed(uber_df):
	grouped = uber_df.groupby(['ride'])
	count = 0
	for ride, group in grouped:
		speedx = deriv(group.set_index('datetime')['x'])
		speedy = deriv(group.set_index('datetime')['y'])
		if count == 0:
			speeddf = pd.DataFrame(np.sqrt(speedx**2 + speedy**2),index=[group.index],columns=['speed'])
		else:
			speeddf = pd.concat([speeddf,pd.DataFrame(np.sqrt(speedx**2 + speedy**2),index=[group.index],columns=['speed'])])
		count += 1
	return speeddf

def compute_accel(uber_df):
	count = 0
	for ride, group in df.groupby(['ride']):
		accel = deriv(group.set_index('datetime')['speed']) # compute acceleration in meter/s/s
		if count == 0:
			acceldf = pd.DataFrame(accel,index=[group.index],columns=['accel'])
		else:
			acceldf = pd.concat([acceldf,pd.DataFrame(accel,index=[group.index],columns=['accel'])])
		count += 1
	return acceldf

def subset_flag_df(uber_df):
	reindexed_df = uber_df.set_index('datetime')
	reindexed_df['rush_hour'] = None

	morning_df = reindexed_df.ix['2007-01-02':'2007-01-07'].between_time('6:00','10:00')
	reindexed_df[morning_df.index]['rush_hour'] = 'morning'
	afternoon_df = reindexed_df.ix['2007-01-02':'2007-01-07'].between_time('15:00','19:00')
	reindexed_df[afternoon_df.index]['rush_hour'] = 'afternoon'
	return reindexed_df

def get_features(df):
	X = pd.DataFrame(df.groupby('ride')['speed'].max())
	X.columns = ['max_speed']
	X['avg_speed'] = df.groupby('ride')['speed'].mean()
	X['med_speed'] = df.groupby('ride')['speed'].median()
	X['max_accel'] = df[df['accel']>0].groupby('ride')['accel'].max()
	X['avg_accel'] = df[df['accel']>0].groupby('ride')['accel'].mean()
	X['med_accel'] = df[df['accel']>0].groupby('ride')['accel'].median()
	X['max_decel'] = df[df['accel']<0].groupby('ride')['accel'].min()
	X['avg_decel'] = df[df['accel']<0].groupby('ride')['accel'].mean()
	X['med_decel'] = df[df['accel']<0].groupby('ride')['accel'].median()

	def mfp(data):
		nz = np.nonzero(np.append(0,data['speed']))
		return 4.0*sum(nz)/len(np.where(np.diff(nz) == 1)[0]) #mean free path in seconds
	X['mfp'] = df[['ride','speed','time']].groupby('ride').apply(mfp)
	return X

# def get_clusters(X, n=4):
# 	distxy = squareform(pdist(X_scaled, metric='euclidean'))
# 	linkage(distxy, method='complete')

# 	return clusters

# def compute_edge_weight(df,edge):
# 	grouped = df.groupby('trans_edge')
# 	for edge,group in grouped:

def main():
	uber_df = load_uber() # resample to every 2 seconds

	# street_df = load_streets(n=0)
	street_df = pickle.load(open('pickles/street_df.pkl','rb'))

	street_graph = create_graph(street_df)
	transition_graph, trans_dict = create_transition_graph(street_graph)

	uber_df = project(uber_df, street_graph, transition_graph, trans_dict)

	uber_df = uber_df.join(compute_speed(uber_df))
	uber_df = uber_df.join(compute_accel(uber_df))

	uber_df = subset_flag_df(uber_df)

	rush_hour_flags = [None,'morning','afternoon']

	for flag in rush_hour_flags:
		flag_df = uber_df[uber_df['rush_hour'] == flag]
		X = get_features(flag_df)
		clusters = get_clusters(X, n=4)
		for cluster in clusters:
			clone_graph = transition_graph
			for i, edge in clone_graph.edges_iter():
				edge['weight'] = compute_edge_weight(flag_df,edge)
	
	'''
	nx.astar_path(transition_graph,source,target)

	for edge in graph:
		group drivers by edge
		compute average velocity at location on edge
		compute average acceleration at location on edge
		# integrate velocity over edge
		# integrate acceleration over edge
	'''
	# for ride:
		# for edge:
			# subtract average from velocity at location on edge
			# subtract average from acceleraton at location on edge
			# integrate velocity (per location) over edge 
			# integrate acceleration (per location) over edge

if __name__ == '__main__':
	main()