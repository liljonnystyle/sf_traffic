#!/usr/bin/python
import pickle
from pygeocoder import Geocoder, GeocoderError
import numpy as np
import networkx as nx
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import requests
import random
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

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
	apikeys = ['AIzaSyBbKW7pUx7aE6PrBkBDhl3KYPyYufIzh0E']
	# ['AIzaSyBMTLIl73fU5XRJLvug1T_yVUhpJQQoNCw']

	source = source.replace(' ','+')
	source = source.replace(',','%2C')
	destination = destination.replace(' ','+')
	destination = destination.replace(',','%2C')

	keycount = 0
	dir_url = 'https://maps.googleapis.com/maps/api/directions/json?'
	dir_url += 'origin=' + source + '&'
	dir_url += 'destination=' + destination + '&'
	dir_url += 'key=' + apikeys[keycount]
	r = requests.get(dir_url)
	directions = r.json()

	coords = []
	eta = 0.0
	for step in directions['routes'][0]['legs'][0]['steps']:
		eta += step['duration']['value']
		coord = (step['start_location']['lat'], step['start_location']['lng'])
		coords.append(coord)
	coord = (step['end_location']['lat'], step['end_location']['lng'])
	coords.append(coord)
	return eta, coords

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

	return edge_trans_dict[edge], edge, frac

@app.after_request
def add_header(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

@app.route('/routing')
def routing():
	source, dest, time = request.args['source'], request.args['destination'], request.args['time']

	if time == 'morning':
		inds = [2, 3]
	elif time == 'afternoon':
		inds = [4, 5]
	else:
		inds = [0, 1]

	sc_transedge, sc_edge, sc_frac = get_edge(source, coord_lookup, node_coord_dict, edge_dict, edge_trans_dict)
	ds_transedge, ds_edge, ds_frac = get_edge(dest, coord_lookup, node_coord_dict, edge_dict, edge_trans_dict)

	if sc_frac > 0.5:
		sc_node = sc_transedge[1]
		sc_lng, sc_lat = node_coord_dict[sc_edge[1]]
	else:
		sc_node = sc_transedge[0]
		sc_lng, sc_lat = node_coord_dict[sc_edge[0]]

	if ds_frac > 0.5:
		ds_node = ds_transedge[1]
		ds_lng, ds_lat = node_coord_dict[ds_edge[1]]
	else:
		ds_node = ds_transedge[0]
		ds_lng, ds_lat = node_coord_dict[ds_edge[0]]

	ret = {'points': [], 'etas': []}
	ret['lat'] = (sc_lat+ds_lat)/2.0
	ret['lng'] = (sc_lng+ds_lng)/2.0
	etas = []
	stds = []
	for i in inds:
		transition_graph = cluster_graphs[i]
		path = nx.dijkstra_path(transition_graph,sc_node,ds_node)
		eta = 0.0
		sig2 = 0.0
		coords = []
		for j in xrange(len(path)-1):
			trans_edge = (path[j],path[j+1])
			if trans_edge in trans_edge_dict:
				edge = trans_edge_dict[trans_edge]
				coord = node_coord_dict[edge[0]]
				coord = (coord[1], coord[0])
				coords.append(coord)
				old_coord = node_coord_dict[edge[1]]
				old_coord = (old_coord[1], old_coord[0])
			else:
				coords.append(old_coord)
			eta += transition_graph[path[j]][path[j+1]]['weight']
			sig2 += transition_graph[path[j]][path[j+1]]['std']**2
		ret['points'].append(coords)
		ret['etas'].append(format(eta/60,'.2f'))
		etas.append(eta)
		stds.append((sig2**0.5)/60)

	xmin = min([etas[0]/60-3*stds[0], etas[1]/60-3*stds[1]])
	xmax = max([etas[0]/60+3*stds[0], etas[1]/60+3*stds[1]])
	x = np.linspace(xmin,xmax,num=100)
	y0 = mlab.normpdf(x,etas[0]/60,stds[0])
	y1 = mlab.normpdf(x,etas[1]/60,stds[1])
	ymax = max([max(y0),max(y1)])+0.1

	plt.figure(figsize=(18,8))
	ax = plt.subplot(111)
	plt.plot([min(x), max(x)], [0, 0], 'k-', linewidth=1)
	plt.plot(x,y0,'g', linewidth=4)
	plt.plot([etas[0], etas[0]], [0, ymax], 'g--', linewidth=2)
	plt.plot(x,y1,'r', linewidth=4)
	plt.plot([etas[1], etas[1]], [0, ymax], 'r--', linewidth=2)
	plt.ylim([-0.01, ymax])
	plt.xticks([xmin, etas[0], etas[1], xmax])
	plt.yticks([])
	plt.xlabel('ETA (minutes)')
	ax.set_frame_on(False)
	plt.savefig('static/norms0.png')

	plt.figure(figsize=(18,8))
	ax = plt.subplot(111)
	plt.plot([min(x), max(x)], [0, 0], 'k-', linewidth=1)
	plt.plot(x,y1,'r', linewidth=4)
	plt.plot([etas[1], etas[1]], [0, ymax], 'r--', linewidth=2)
	plt.plot(x,y0,'g', linewidth=4)
	plt.plot([etas[0], etas[0]], [0, ymax], 'g--', linewidth=2)
	plt.fill_between(x, 0, y0, facecolor='g', alpha=0.5)
	plt.ylim([-0.01, ymax])
	plt.xticks([xmin, etas[0], etas[1], xmax])
	plt.yticks([])
	plt.xlabel('ETA (minutes)')
	ax.set_frame_on(False)
	plt.savefig('static/norms1.png')

	plt.figure(figsize=(18,8))
	ax = plt.subplot(111)
	plt.plot([min(x), max(x)], [0, 0], 'k-', linewidth=1)
	plt.plot(x,y0,'g', linewidth=4)
	plt.plot([etas[0], etas[0]], [0, ymax], 'g--', linewidth=2)
	plt.plot(x,y1,'r', linewidth=4)
	plt.plot([etas[1], etas[1]], [0, ymax], 'r--', linewidth=2)
	plt.fill_between(x, 0, y1, facecolor='r', alpha=0.5)
	plt.ylim([-0.01, ymax])
	plt.xticks([xmin, etas[0], etas[1], xmax])
	plt.yticks([])
	plt.xlabel('ETA (minutes)')
	ax.set_frame_on(False)
	plt.savefig('static/norms1.png')

	eta, coords = get_gmaps_dirs(source,dest)

	etas.append(eta)
	ret['points'].append(coords)
	ret['etas'].append(format(eta/60,'.2f'))
	ret['max_eta'] = format(max(etas)/60,'.2f')
	return jsonify(ret)

@app.route('/', methods = ['GET'])
def start_page():
	return render_template('jrouting.html')

if __name__ == '__main__':
	cluster_graphs = pickle.load(open('../pickles/cgraphs.pkl'))
	trans_edge_dict = pickle.load(open('../pickles/trans_edge_dict.pkl'))
	edge_trans_dict = pickle.load(open('../pickles/edge_trans_dict.pkl'))
	coord_lookup = pickle.load(open('../pickles/coord_lookup.pkl'))
	edge_dict = pickle.load(open('../pickles/edge_dict.pkl'))
	node_coord_dict = pickle.load(open('../pickles/node_coord_dict.pkl'))

	print 'ready'
	app.run(host = '0.0.0.0', debug = True)