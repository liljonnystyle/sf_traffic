#!/usr/bin/python
import pickle
from pygeocoder import Geocoder, GeocoderError
from optparse import OptionParser
from googlemaps import GoogleMaps
import numpy as np
import networkx as nx
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import requests
import random

app = Flask(__name__)

def edge_eval(start, stop):
	'''
	INPUT: start and stop coordinates of a vector
	OUTPUT: length and unit vector
	'''
	length = ((start[0] - stop[0])**2 + (start[1] - stop[1])**2)**0.5
	unit_vec = np.array([(stop[0] - start[0])/length, (stop[1] - start[1])/length])
	return length, unit_vec

def point_to_line(point, start, stop, edge_len, edge_vec):
	'''
	find perpendicular distance from point to line
	find fraction along vector of projected point
	'''
	startpoint_len, startpoint_vec = edge_eval(start, point)
	cosang = np.dot(edge_vec, startpoint_vec)
	sinang = np.linalg.norm(np.cross(edge_vec, startpoint_vec))
	# angle = np.arctan2(sinang, cosang)
	dist = startpoint_len * sinang
	frac = startpoint_len * cosang / edge_len
	return dist, frac

def find_nearest_street(x, y, edges, node_dict, edge_dict):
	min_dist = 9999
	for edge in edges:
		coord1 = node_dict[edge[0]]
		coord2 = node_dict[edge[1]]
		dist, frac = point_to_line((x, y), coord1, coord2, edge_dict[edge][2], edge_dict[edge][3])
		if dist < min_dist and (frac >= 0 and frac <= 1):
			min_dist = dist
			min_edge = edge
			min_frac = frac
	if min_dist == 9999:
		return (-1,-1), 0, 1
	else:
		return min_edge, min_frac, 0

def get_gmaps_dirs(source,destination):
	apikeys = ['AIzaSyBMTLIl73fU5XRJLvug1T_yVUhpJQQoNCw']

	keycount = 0
	# try:
	directions = GoogleMaps(apikey[keycount]).directions(source,destination)
	# except:

	print 'Google Maps Directions:\n'
	for step in directions['Directions']['Routes'][0]['Steps']:
		print step['descriptionHtml']

def get_edge(address, coord_lookup, node_coord_dict, edge_dict, edge_trans_dict):
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

	keycount = 0
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

	if lat == -1.0 or lng == -1.0:
		pass

	lookup_edges = coord_lookup[(format(lng,'.2f'),format(lat,'.2f'))]
	edge, frac, searching = find_nearest_street(lng, lat, lookup_edges, node_coord_dict, edge_dict)

	return edge_trans_dict[edge], frac

@app.route('/routing')
def routing():
	source, dest, time = request.args['source'], request.args['destination'], request.args['time']

	if time == 'morning':
		inds = [0, 1, 2, 3]
	elif time == 'afternoon':
		inds = [4, 5, 6, 7]
	else:
		inds = [8, 9, 10, 11]

	# sc_edge, sc_frac = get_edge(source, coord_lookup, node_coord_dict, edge_dict, edge_trans_dict)
	# ds_edge, ds_frac = get_edge(dest, coord_lookup, node_coord_dict, edge_dict, edge_trans_dict)

	# if sc_frac > 0.5:
	# 	sc_node = sc_edge[1]
	# else:
	# 	sc_node = sc_edge[0]

	# if ds_frac > 0.5:
	# 	ds_node = ds_edge[1]
	# else:
	# 	ds_node = ds_edge[0]

	sc_lat,sc_lng = Geocoder().geocode(source)[0].coordinates
	ds_lat,ds_lng = Geocoder().geocode(dest)[0].coordinates

	ret = {'points': [], 'etas': []}
	for i in inds:
		coords = []
		coords.append((sc_lat, sc_lng))
		coords.append((sc_lat+0.05*(0.5-random.random()),sc_lng+0.05*(0.5-random.random())))
		coords.append((ds_lat+0.05*(0.5-random.random()),ds_lng+0.05*(0.5-random.random())))
		coords.append((ds_lat, ds_lng))
		# transition_graph = cluster_graphs[i]
		# path = nx.astar_path(transition_graph,sc_node,ds_node)
		# eta = 0
		# coords = []
		# for j in xrange(len(path)-1):
		# 	edge = trans_edge_dict[(path[j],path[j+1])]
		# 	coords.append(node_coord_dict[edge[0]])
		# 	eta += transition_graph[path[j]][path[j+1]]['weight']
		ret['points'].append(coords)
		ret['etas'].append(5+i)
	return jsonify(ret)

@app.route('/', methods = ['GET'])
def start_page():
	return render_template('jrouting.html')

# 	get_gmaps_dirs(source,destination)

if __name__ == '__main__':
	cluster_graphs = pickle.load(open('../pickles/cluster_graphs.pkl'))
	trans_edge_dict = pickle.load(open('../pickles/trans_edge_dict.pkl'))
	edge_trans_dict = pickle.load(open('../pickles/edge_trans_dict.pkl'))
	coord_lookup = pickle.load(open('../pickles/coord_lookup.pkl'))
	edge_dict = pickle.load(open('../pickles/edge_dict.pkl'))
	node_coord_dict = pickle.load(open('../pickles/node_coord_dict.pkl'))

	app.run(host = '0.0.0.0', debug = True)