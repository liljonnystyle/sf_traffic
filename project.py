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
import math
import ipdb
# import psycopg2 as psycho

from pygeocoder import Geocoder, GeocoderError
from collections import Counter
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
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
	if n > 1:
		d[0] = (x.iloc[1]-x.iloc[0])/(x.index[1]-x.index[0]).total_seconds()
		d[n-1] = (x.iloc[n-1]-x.iloc[n-2])/(x.index[n-1]-x.index[n-2]).total_seconds()
	return d

def dparser(datestring):
	return datetime.datetime.strptime(datestring,'%Y-%m-%dT%H:%M:%S+00:00')

'''
load uber coord data from csv into DataFrame
'''
def load_uber(nlines=-1):
	column_names = ['ride', 'datetime', 'y', 'x']
	uber_df = pd.read_csv('uber_data/all.tsv', sep='\t', header=None, names=column_names,
		parse_dates=[1], date_parser=dparser)

	# some rides have duplicated datapoints
	uber_df.drop_duplicates(inplace=True)

	# remove remaining rides that are shorter than 5 minutes
	uber_df = uber_df[uber_df.groupby(['ride'])['ride'].transform('count') >= 3] 
	# should actually do this by filtering trip duration, rather than value counts

	# resample to every 2 seconds?
	return uber_df.iloc[:nlines]

'''
load street geo data from json into DataFrame
'''
def load_streets(n=0):
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
	# xstarts = np.zeros((nstreets,1))
	# ystarts = np.zeros((nstreets,1))
	# xstops = np.zeros((nstreets,1))
	# ystops = np.zeros((nstreets,1))

	if n == 0:
		'''
		prepare input file for fortran program to convert state plane
		coordinates to lat long coordinates
		'''
		file81 = open('nad83/input.81','wb')
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
		file80 = open('nad83/output.80','rb')
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
Truncates/pads a float f to n decimal places without rounding
'''
def trunc(f, n=2):
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

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

		xstart_trunc = trunc(xstart,2)
		xstart_truncp = trunc(xstart+0.01,2)
		xstart_truncm = trunc(xstart-0.01,2)
		ystart_trunc = trunc(ystart,2)
		ystart_truncp = trunc(ystart+0.01,2)
		ystart_truncm = trunc(ystart-0.01,2)
		xstop_trunc = trunc(xstop,2)
		xstop_truncp = trunc(xstop+0.01,2)
		xstop_truncm = trunc(xstop-0.01,2)
		ystop_trunc = trunc(ystop,2)
		ystop_truncp = trunc(ystop+0.01,2)
		ystop_truncm = trunc(ystop-0.01,2)

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
				G.add_path([start_node, stop_node])
				edge_dict[(start_node, stop_node)] = [street['name']]
				for key in keys:
					if key in coord_lookup.keys():
						coord_lookup[key].add((start_node, stop_node))
					else:
						coord_lookup[key] = set([(start_node, stop_node)])

			if street['oneway'] != 'F':
				G.add_path([stop_node, start_node])
				edge_dict[(stop_node, start_node)] = [street['name']]
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
	'''
	edge_dict keyed on node-node tuple
	values are list of street name, edge length, edge unit vec
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
	trans_dict = {}
	node_count = 0
	trans_node_dict = {}
	for edge in G.edges_iter():
		new_edge = shorten_edge(node_dict[edge[0]], edge_dict[edge][1], edge_dict[edge][2])
		trans_dict[edge] = new_edge
		newG.add_path([new_edge[0], new_edge[1]], weight=9999)
		if edge[0] in start_dict:
			start_dict[edge[0]].append(new_edge[0])
		else:
			start_dict[edge[0]] = [new_edge[0]]
		stop_dict[new_edge[1]] = edge[1]

	for newstop, oldstop in stop_dict.iteritems():
		if oldstop in start_dict:
			for newstart in start_dict[oldstop]:
				newG.add_path([newstop, newstart], weight=0)

	return newG, trans_dict

'''
find perpendicular distance from point to line
find fraction along vector of projected point
'''
def point_to_line(point, start, stop, edge_len, edge_vec):
	startpoint_len, startpoint_vec = edge_eval(start, point)
	cosang = np.dot(edge_vec, startpoint_vec)
	sinang = np.linalg.norm(np.cross(edge_vec, startpoint_vec))
	# angle = np.arctan2(sinang, cosang)
	dist = startpoint_len * sinang
	frac = startpoint_len * cosang / edge_len
	return dist, frac

'''
project coordinates onto street graph, and then onto transition graph
'''
def project(uber_df, G, transG, node_dict, edge_dict, trans_dict, coord_lookup):

	''' does what set(nx.ego_graph(G,node,radius).edges()) should do '''
	def get_lookup_edges(G,node,radius):
		if radius == 1:
			return set([(node, neigh) for neigh in G.neighbors(node)])
		if radius > 1:
			lookup_edges = set([(node, neigh) for neigh in G.neighbors(node)])
			for neigh in G.neighbors(node):
				tmp = get_lookup_edges(G,neigh,radius-1)
				lookup_edges = lookup_edges.union(tmp)
			return lookup_edges
		else:
			return set()

	def mapping(data):
		broken_chain = np.ones(len(data))
		edges = []
		fracs = []
		# if data.iloc[0]['ride'] == 14:
		# 	ipdb.set_trace()
		for i in xrange(len(data)):
			row = data.iloc[i]
			if broken_chain[i] == 1:
				lookup_edges = coord_lookup[(trunc(row['x'],2),trunc(row['y'],2))]
				edge1, frac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges)
				if i < len(data)-2:
					x2 = data.iloc[i+1]['x']
					y2 = data.iloc[i+1]['y']

					searching = 1
					radius = 1
					checked_edges = set()
					while searching:
						radius += 1
						lookup_edges = get_lookup_edges(G,edge1[1],radius)
						lookup_edges = lookup_edges.union(get_lookup_edges(G,edge1[0],radius))
						lookup_edges = lookup_edges.difference(checked_edges)
						checked_edges = checked_edges.union(lookup_edges)
						edge2, frac2, searching = find_nearest_street(x2, y2, lookup_edges)

					if edge1 == edge2:
						broken_chain[i+1] = 0
						if frac1 < frac2:
							edges.append(edge1)
							fracs.append(frac1)
						else:
							proposed_edge1 = (edge1[1], edge1[0])
							if proposed_edge1 in edge_dict:
								edges.append(proposed_edge1)
								fracs.append(1-frac1)
							else:
								edges.append(edge1)
								fracs.append(frac1)
					elif edge1 == (edge2[1], edge2[0]):
						broken_chain[i+1] = 0
						if frac1 < 1-frac2:
							edges.append(edge1)
							fracs.append(frac1)
						else:
							proposed_edge1 = (edge1[1], edge1[0])
							if proposed_edge1 in edge_dict:
								edges.append(proposed_edge1)
								fracs.append(1-frac1)
					elif (edge1[0] == edge2[0]) or (edge1[0] == edge2[1]):
						proposed_edge1 = (edge1[1], edge1[0])
						if proposed_edge1 in edge_dict:
							broken_chain[i+1] = 0
							edges.append(proposed_edge1)
							fracs.append(1-frac1)
						else:
							edges.append(edge1)
							fracs.append(frac1)
					elif (edge1[1] == edge2[0]) or (edge1[1] == edge2[1]):
						broken_chain[i+1] = 0
						edges.append(edge1)
						fracs.append(frac1)
					else:
						edges.append(edge1)
						fracs.append(frac1)
				else:
					edges.append(edge1)
					fracs.append(frac1)
			else: # not broken chain, can be confident in start node if correct for directionality
				edge0 = edges[i-1]
				frac0 = fracs[i-1]
				
				lookup_edges = get_lookup_edges(G,edge0[1],1)
				lookup_edges.add(edge0)
				edge_reverse = (edge0[1], edge0[0])
				lookup_edges.discard(edge_reverse)
				edge1, frac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges)
				stopnode = -1
				if edge0 == edge1:
					edges.append(edge1)
					fracs.append(frac1)
					startnode = edge1[0]
					stopnode = edge1[1]
				elif edge0 == (edge1[1],edge1[0]):
					edges.append(edge0)
					fracs.append(1-frac1)
					startnode = edge1[1]
					stopnode = edge1[0]
					edge1 = (startnode, stopnode)
				elif edge0[1] == edge1[0]:
					startnode = edge1[0]
				else:
					startnode = edge1[1]
					lookup_edges = get_lookup_edges(G,startnode,1)
					edge1, frac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges)

				if stopnode == -1:
					if i <= len(data)-2:
						x2 = data.iloc[i+1]['x']
						y2 = data.iloc[i+1]['y']
						
						searching = 1
						radius = 1
						edge_reverse = (edge1[1], edge1[0])
						checked_edges = set(edge_reverse)
						while searching:
							radius += 1
							lookup_edges = get_lookup_edges(G,startnode,radius)
							lookup_edges = lookup_edges.difference(checked_edges)
							checked_edges = checked_edges.union(lookup_edges)
							edge2, frac2, searching = find_nearest_street(x2, y2, lookup_edges)

						if edge1 == edge2:
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						elif edge1[1] == edge2[0]:
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						elif edge1[1] == edge2[1]:
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						else:
							proposed_edges1 = set()
							if (startnode, edge2[0]) in edge_dict:
								proposed_edges1.add((startnode, edge2[0]))
							if (startnode, edge2[1]) in edge_dict:
								proposed_edges1.add((startnode, edge2[1]))
							newedge1, newfrac1, searching = find_nearest_street(row['x'], row['y'], proposed_edges1)
							if searching == 1:
								edges.append(edge1)
								fracs.append(frac1)
							else:
								broken_chain[i+1] = 0
								edges.append(newedge1)
								fracs.append(newfrac1)
					else:
						edges.append(edge1)
						fracs.append(frac1)
				else:
					if i <= len(data)-2:
						x2 = data.iloc[i+1]['x']
						y2 = data.iloc[i+1]['y']
						
						searching = 1
						radius = 1
						edge_reverse = (edge1[1], edge1[0])
						checked_edges = set(edge_reverse)
						while searching:
							radius += 1
							lookup_edges = get_lookup_edges(G,stopnode,radius)
							lookup_edges.add(edge1)
							lookup_edges = lookup_edges.difference(checked_edges)
							checked_edges = checked_edges.union(lookup_edges)
							edge2, frac2, searching = find_nearest_street(x2, y2, lookup_edges)

						if edge1 == edge2:
							broken_chain[i+1] = 0
						elif edge1[1] == edge2[0]:
							broken_chain[i+1] = 0
						elif edge1[1] == edge2[1]:
							broken_chain[i+1] = 0


		data['edge'] = edges
		data['fraction'] = fracs
		return data

	def find_nearest_street(x, y, edges):
		min_dist = 9999
		for edge in edges:
			coord1 = node_dict[edge[0]]
			coord2 = node_dict[edge[1]]
			dist, frac = point_to_line((x, y), coord1, coord2, edge_dict[edge][1], edge_dict[edge][2])
			if dist < min_dist and (frac >= 0 and frac <= 1):
				min_dist = dist
				min_edge = edge
				min_frac = frac
		if min_dist == 9999:
			return (0,0), 0, 1
		else:
			return min_edge, min_frac, 0

	# def voting(edges, fracs):
	# 	broken_chain = np.ones(len(edges))
	# 	troublemakers = set()
	# 	for i, edge in enumerate(edges[:-1]):
	# 		if broken_chain[i]:
	# 			if (edge == edges[i+1]):
	# 				broken_chain[i+1] = 0
	# 				if fracs[i] > fracs[i+1]: # if subsequent edges match, but going wrong direction
	# 					if (edges[i][1], edges[i][0]) in edge_dict:
	# 						edges[i] = (edges[i][1], edges[i][0])
	# 						fracs[i] = 1-fracs[i]
	# 						edges[i+1] = edges[i]
	# 						fracs[i+1] = 1-fracs[i+1]
	# 					else:
	# 						troublemakers.add(i)
	# 						troublemakers.add(i+1)
	# 			elif (edge[0] == edges[i+1][1]) & (edge[1] == edges[i+1][0]): # if subsequent edges flip/flop
	# 				broken_chain[i+1] = 0
	# 				if fracs[i] > 1-fracs[i+1]: # 0 is wrong, 1 is right
	# 					edges[i] = edges[i+1]
	# 					fracs[i] = 1-fracs[i]
	# 			else:
	# 				for j in xrange(i+1,len(edges)):
	# 					if edge[0] == edges[j][0]:
	# 						broken_chain[j] = 0
	# 						if (edges[i][1], edges[i][0]) in edge_dict:
	# 							edges[i] = (edges[i][1], edges[i][0])
	# 							fracs[i] = 1-fracs[i]
	# 						else:
	# 							troublemakers.add(i)
	# 						break
	# 					elif edge[0] == edges[j][1]:
	# 						broken_chain[j] = 0
	# 						if (edges[i][1], edges[i][0]) in edge_dict:
	# 							edges[i] = (edges[i][1], edges[i][0])
	# 							fracs[i] = 1-fracs[i]
	# 						else:
	# 							troublemakers.add(i)
	# 						if (edges[j][1], edges[j][0]) in edge_dict:
	# 							edges[j] = (edges[j][1], edges[j][0])
	# 							fracs[j] = 1-fracs[j]
	# 						else:
	# 							troublemakers.add(j)
	# 						break
	# 					elif edge[1] == edges[j][1]:
	# 						broken_chain[j] = 0
	# 						if (edges[j][1], edges[j][0]) in edge_dict:
	# 							edges[j] = (edges[j][1], edges[j][0])
	# 							fracs[j] = 1-fracs[j]
	# 						else:
	# 							troublemakers.add(j)
	# 						break
	# 		else:
	# 			for j in xrange(i+1,len(edges)):
	# 				if edge != edges[j]:
	# 					if (edge[0] == edges[i+1][1]) & (edge[1] == edges[i+1][0]): # if subsequent edges flip/flop
	# 						broken_chain[j] = 0
	# 						edges[j] = edges[i]
	# 						fracs[j] = 1-fracs[j]
	# 					else:
	# 						if edge[1] == edges[j][1]:
	# 							broken_chain[j] = 0
	# 							if (edges[j][1], edges[j][0]) in edge_dict:
	# 								edges[j] = (edges[j][1], edges[j][0])
	# 								fracs[j] = 1-fracs[j]
	# 							else:
	# 								troublemakers.add(j)
	# 							break
	# 						else:
	# 							break
	# 	return edges, fracs, troublemakers

	# def check_edges(edges, fracs, ride):
	# 	error = 0
	# 	lr = LinearRegression()

	# 	newedges = np.array(edges)
	# 	newfracs = np.array(fracs)
	# 	for i, edge in enumerate(edges):
	# 		if i != 0:
	# 			if edge == oldedge:
	# 				curr_inds.append(i)
	# 			else:
	# 				inds = np.where(edges == oldedge)[0]
	# 				x = np.arange(len(inds))[:,np.newaxis]
	# 				y = np.array(np.array(fracs)[inds])
	# 				try:
	# 					lr.fit(x,y)
	# 				except AttributeError:
	# 					print x, type(x)
	# 					print y, type(y)
	# 				if lr.coef_[0] < 0:
	# 					newedge = (oldedge[1], oldedge[0])
	# 					if newedge in G.nodes():
	# 						for j in curr_inds:
	# 							newedges[j] = newedge
	# 							newfracs[j] = 1 - fracs[j]
	# 					else:
	# 						print 'ride ' + str(ride) + ' can not reverse edge ' + str(edge)
	# 						error = 1
	# 						return edges, fracs, error
	# 				oldedge = edge
	# 				curr_inds = [i]
	# 		else:
	# 			oldedge = edge
	# 			curr_inds = [i]

	# 	for i, edge in enumerate(newedges):
	# 		if i != 0:
	# 			if edge != oldedge:
	# 				if edge[0] != oldedge[1]:
	# 					print 'ride ' + str(ride) + ' node match error:'
	# 					print '\t' + str(oldedge) + ' & ' + str(edge)
	# 					error = 1
	# 					return edges, fracs, error
	# 		oldedge = edge
	# 	return newedges, newfracs, error

	# def get_trans_edges(edges, fracs, ride):
	# 	transedges = np.array(edges)
	# 	error = 0
	# 	for i, frac in enumerate(fracs):
	# 		tmp = trans_dict[edges[i]]
	# 		if frac < 0.01: # beginning of edge, go backwards to find previous edge
	# 			check = 0
	# 			for j in xrange(i-1, 0, -1):
	# 				if edges[i] != edges[j]:
	# 					transedges[i] = (trans_dict[edges[j]][1],tmp[0])
	# 					check = 1
	# 					break
	# 			if check == 0: # got to beginning of series with no previous edge, assign any trans edge that matches
	# 				for edge_it in G.edges_iter():
	# 					if edge_it[1] == edges[i][0]:
	# 						transedges[i] = (trans_dict[edge_it][1],tmp[0])
	# 						break
	# 		elif frac > 0.9: # end of edge, go forwards to find next edge
	# 			check = 0
	# 			for j in xrange(i+1, len(edges)):
	# 				if edges[i] != edges[j]:
	# 					transedges[i] = (tmp[1],trans_dict[edges[j]][0])
	# 					check = 1
	# 					break
	# 			if check == 0: # got to end of series with no next edge, assign any trans edge that matches
	# 				for edge_it in G.edges_iter():
	# 					if edge_it[0] == edges[i][1]:
	# 						transedges[i] = (tmp[1],trans_dict[edge_it][0])
	# 						break
	# 		else:
	# 			transedges[i] = tmp

	# 		if transedges[i] not in transG.edges():
	# 			print 'ride ' + str(ride) + ' transition edge mismatch'
	# 			print 'transition ' + str(transedges[i]) + ' does not exist'
	# 			error = 1
	# 			break
	# 	return transedges, error

	def update_loc(edges, fracs):
		newx = np.zeros((len(edges),))
		newy = np.zeros((len(edges),))
		for i in xrange(len(edges)):
		#for i, edge in enumerate(edges):
			length, unit_vec = edge_eval(node_dict[edges.iloc[i][0]], node_dict[edges.iloc[i][1]])
			vec = unit_vec*length*fracs.iloc[i]
			newx[i] = node_dict[edges.iloc[i][0]][0] + vec[0]
			newy[i] = node_dict[edges.iloc[i][0]][1] + vec[1]
		return newy, newx

	# def dftransform(subdf):
	# 	error = 0
	# 	edges, fracs, troublemakers = voting(subdf['edge'].values, subdf['fraction'].values)
	# 	# edges, fracs, error = check_edges(edges, fracs, subdf['ride'].iloc[0])
	# 	# if error == 1:
	# 		# return subdf, edges, error
	# 	newy, newx = update_loc(edges, fracs)

	# 	transedges, error = get_trans_edges(edges, fracs, subdf['ride'].iloc[0])
	# 	# if error == 1:
	# 		# return subdf, edges, error

	# 	return np.vstack([newy, newx, edges, fracs]).T, transedges, error, troublemakers

	uber_df = uber_df.groupby('ride').apply(mapping)
	print 'found nearest edges'
	newy, newx = update_loc(uber_df['edge'], uber_df['fraction'])
	uber_df.ix[:,['y','x']] = np.vstack([newy, newx]).T

	# for ride in rides:
	# tmp = uber_df[['x','y']].apply(find_nearest_street, axis=1)
	# uber_df['edge'] = tmp[0]
	# uber_df['fraction'] = tmp[1]
	# uber_df['street'] = uber_df['edge'].apply(lambda x: edge_dict[x][0])

	# rides = uber_df['ride'].unique()
	# transedges_array = np.array([])
	# for ride in rides:
	# 	if len(uber_df[uber_df['ride'] == ride]) > 1:
	# 		tmp, transedges, error, troublemakers = dftransform(uber_df[uber_df['ride'] == ride])
	# 		uber_df.ix[uber_df['ride'] == ride,['y','x','edge','fraction']] = tmp
	# 		# tmp['troublemakers'] = False
	# 		# for i in troublemakers:
	# 		# 	tmp.ix[i,'troublemakers'] = True
	# 		# uber_df = uber_df[tmp['troublemakers'] == False]
	# 		if error == 1:
	# 			uber_df = uber_df[uber_df['ride'] != ride]
	# 		else:
	# 			transedges_array = np.hstack([transedges_array,transedges])
	# 	else:
	# 		transedges_array = np.hstack([transedges_array, trans_dict[uber_df['edge']]])
	# uber_df['trans_edge'] = transedges_array
	uber_df['trans_edge'] = uber_df['edge'].apply(lambda x: trans_dict[x])
	print 'converted to transition edges'

	return uber_df

def compute_speed(uber_df):
	radius = 3963.1676
	rad_x = 3963.1676*np.cos(37.7833*math.pi/180)

	grouped = uber_df.groupby(['ride'])
	count = 0
	for ride, group in grouped:
		speedx = deriv(group.set_index('datetime')['x']) * 2 * math.pi * rad_x * 10
		speedy = deriv(group.set_index('datetime')['y']) * 2 * math.pi * radius * 10
		# speeds in miles per hour
		if count == 0:
			speeddf = pd.DataFrame(np.sqrt(speedx**2 + speedy**2),index=[group.index],columns=['speed'])
		else:
			speeddf = pd.concat([speeddf,pd.DataFrame(np.sqrt(speedx**2 + speedy**2),index=[group.index],columns=['speed'])])
		count += 1
	return speeddf

def compute_accel(uber_df):
	grouped = uber_df.groupby(['ride'])
	count = 0
	for ride, group in grouped:
		accel = deriv(group.set_index('datetime')['speed']) * 1609.34 / 3600
		# compute acceleration in meter/s/s
		if count == 0:
			acceldf = pd.DataFrame(accel,index=[group.index],columns=['accel'])
		else:
			acceldf = pd.concat([acceldf,pd.DataFrame(accel,index=[group.index],columns=['accel'])])
		count += 1
	return acceldf

'''
create rush hour flag column in Uber DataFrame
'''
def flag_rushhour(uber_df):
	reindexed_df = uber_df.set_index('datetime')
	reindexed_df['rush_hour'] = 'none'

	morning_df = reindexed_df.ix['2007-01-02':'2007-01-07'].between_time('6:00','10:00')
	reindexed_df.ix[morning_df.index, 'rush_hour'] = 'morning'
	afternoon_df = reindexed_df.ix['2007-01-02':'2007-01-07'].between_time('15:00','19:00')
	reindexed_df.ix[afternoon_df.index, 'rush_hour'] = 'afternoon'

	return reindexed_df.reset_index()

def get_features(df):
	X = pd.DataFrame(df.groupby('ride')['speed'].max())
	X.columns = ['max_speed']
	X['avg_speed'] = df.groupby('ride')['speed'].mean()
	X['med_speed'] = df.groupby('ride')['speed'].median()
	X['max_accel'] = df[df['accel']>=0].groupby('ride')['accel'].max()
	X['avg_accel'] = df[df['accel']>=0].groupby('ride')['accel'].mean()
	X['med_accel'] = df[df['accel']>=0].groupby('ride')['accel'].median()
	X['max_decel'] = df[df['accel']<=0].groupby('ride')['accel'].min()
	X['avg_decel'] = df[df['accel']<=0].groupby('ride')['accel'].mean()
	X['med_decel'] = df[df['accel']<=0].groupby('ride')['accel'].median()

	'''
	mean free path: average time driving in between stops (aka zero velocity timestamps)
	'''
	def mfp(data):
		nz = np.where(np.append(0,data) == 0, 0, 1) # flag non-zeros
		return 4.0*sum(nz)/len(np.where(np.diff(nz) == 1)[0]) #mean free path in seconds
	
	X['mfp'] = df.groupby('ride')['speed'].apply(mfp)
	return X

'''
compute kmeans clusters
'''
def get_clusters(X, n=4):
	# distxy = squareform(pdist(X_scaled, metric='euclidean'))
	# linkage(distxy, method='complete')
	model = KMeans(n,n_jobs=-1)
	model.fit(X)

	return model.predict(X), model.cluster_centers_

# def compute_edge_weight(df,edge):
# 	grouped = df.groupby('trans_edge')
# 	for edge,group in grouped:

def main():
	from_pickle = 1

	xmax = -122.417
	xmin = -122.420
	ymin = 37.76181
	ymax = 37.7655

	uber_df = load_uber()
	print 'loaded uber_df'

	uber_df = uber_df[uber_df['x'] >= xmin]
	uber_df = uber_df[uber_df['x'] <= xmax]
	uber_df = uber_df[uber_df['y'] >= ymin]
	uber_df = uber_df[uber_df['y'] <= ymax]

	# resample to fill in gaps, need to implement my own interpolation function
	# uber_df.set_index('datetime').resample('4000L').reset_index(inplace=True)

	if from_pickle:
		street_df = pickle.load(open('pickles/street_df.pkl','rb'))
		print 'read street df'
		# street_df = street_df = street_df[(street_df['xstart'] >= xmin) & (street_df['xstart'] <= xmax) &
		# 	(street_df['xstop'] >= xmin) & (street_df['xstop'] <= xmax) &
		# 	(street_df['ystart'] >= ymin) & (street_df['ystart'] <= ymax) &
		# 	(street_df['ystop'] >= ymin) & (street_df['ystop'] <= ymax)]

		street_graph = pickle.load(open('pickles/street_graph.pkl','rb'))
		node_coord_dict = pickle.load(open('pickles/node_coord_dict.pkl','rb'))
		coord_node_dict = pickle.load(open('pickles/coord_node_dict.pkl','rb'))
		edge_dict = pickle.load(open('pickles/edge_dict.pkl','rb'))
		coord_lookup = pickle.load(open('pickles/coord_lookup.pkl','rb'))
		print 'read street graph'

		transition_graph = pickle.load(open('pickles/transition_graph.pkl','rb'))
		trans_dict = pickle.load(open('pickles/trans_dict.pkl','rb'))
		print 'read transition graph'

		uber_df = pickle.load(open('pickles/uber_df_projected.pkl'))
		print 'read projected uber data'
	else:
		# street_df = load_streets(n=0)
		street_df = pickle.load(open('pickles/street_df.pkl','rb'))
		# street_df = street_df = street_df[(street_df['xstart'] >= xmin) & (street_df['xstart'] <= xmax) &
		# 	(street_df['xstop'] >= xmin) & (street_df['xstop'] <= xmax) &
		# 	(street_df['ystart'] >= ymin) & (street_df['ystart'] <= ymax) &
		# 	(street_df['ystop'] >= ymin) & (street_df['ystop'] <= ymax)]
		print 'loaded street df'

		street_graph, node_coord_dict, coord_node_dict, edge_dict, coord_lookup = create_graph(street_df)
		pickle.dump(street_graph,open('pickles/street_graph.pkl','wb'))
		pickle.dump(node_coord_dict,open('pickles/node_coord_dict.pkl','wb'))
		pickle.dump(coord_node_dict,open('pickles/coord_node_dict.pkl','wb'))
		pickle.dump(edge_dict,open('pickles/edge_dict.pkl','wb'))
		pickle.dump(coord_lookup,open('pickles/coord_lookup.pkl','wb'))
		print 'computed street graph'
	
		transition_graph, trans_dict = create_transition_graph(street_graph, node_coord_dict, edge_dict)
		pickle.dump(transition_graph,open('pickles/transition_graph.pkl','wb'))
		pickle.dump(trans_dict,open('pickles/trans_dict.pkl','wb'))
		print 'computed transition graph'

		''' apply Kalman filter first pass here, fix large errors '''

		uber_df = project(uber_df, street_graph, transition_graph, node_coord_dict, edge_dict, trans_dict, coord_lookup)
		pickle.dump(uber_df,open('pickles/uber_df_projected.pkl','wb'))
		print 'projected uber onto streets'
		
		''' apply Kalman filter second pass here? fix small errors and re-project onto edges? '''
	
	uber_df = uber_df[uber_df.groupby(['ride'])['ride'].transform('count') >= 3]
	uber_df = uber_df.join(compute_speed(uber_df))
	uber_df = uber_df.join(compute_accel(uber_df))

	uber_df = flag_rushhour(uber_df)

	rush_hour_flags = ['none', 'morning', 'afternoon']
	uber_df['cluster'] = None

	for i,flag in enumerate(rush_hour_flags):
		flag_df = uber_df[uber_df['rush_hour'] == flag]
		X = get_features(flag_df)
		clusters, centers = get_clusters(X, n=4)
		clusters += i*4
		if i == 0:
			centroids = centers
		else:
			centroids = np.vstack((centroids,centers))
		ride_cluster_dict = dict(zip(X.index,clusters))
		uber_df.ix[flag_df.index,'cluster'] = uber_df.ix[flag_df.index,'ride'].apply(lambda x: ride_cluster_dict[x])

	pickle.dump(uber_df, open('pickles/uber_df_clustered.pkl','wb'))
	pickle.dump(centroids, open('pickles/centroids.pkl','wb'))

	'''
	xx, yy = np.meshgrid(rush_hour_flags,np.arange(4))
	for flag, cluster in zip(flatten(xx),flatten(yy)):
		clone_graph = transition_graph
		df = uber_df[(uber_df['rush_hour'] == flag) & (uber_df['cluster'] == cluster)][['speed','trans_edge']]
		edge_speed_df = df.groupby('trans_edge')['speed'].mean() * trans_edge_len(???)
		edges = df['trans_edge'].unique()
		for edge in edges:
			i = some_trans_graph_dictionary(???)[edge]
			clone_graph.edges()[i]['weight'] = edge_speed_df[edge]
	'''
	# 		for i, edge in clone_graph.edges_iter():
	# 			edge['weight'] = compute_edge_weight(flag_df,edge)
	
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