#!/usr/bin/python
import project
from pygeocoder import Geocoder
from optparse import OptionParser
from googlemaps import GoogleMaps

def get_gmaps_dirs(source,destination):
	apikeys = [AIzaSyBMTLIl73fU5XRJLvug1T_yVUhpJQQoNCw]

	keycount = 0
	# try:
	directions = GoogleMaps(apikey[keycount]).directions(source,destination)
	# except:

	for step in directions['Directions']['Routes'][0]['Steps']:
		print step['descriptionHtml']

def get_edge(address):
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

	coord_lookup = pickle.load(open('../pickles/coord_lookup.pkl'))
	edge_dict = pickle.load(open('../pickles/edge_dict.pkl'))
	edge_trans_dict = pickle.load(open('../pickles/edge_trans_dict.pkl'))

	lookup_edges = coord_lookup[(format(lng,'.2f'),format(lat,'.2f'))]
	edge, frac, searching = project.find_nearest_street(lng, lat, lookup_edges, edge_dict)

	return edge_trans_dict[edge], frac

def main():
	p = OptionParser()
	p.add_option('-s', action="store", dest="source",
		type="str", default='San Francisco, CA',
		help="Address of Source")
	p.add_option('-d', action="store", dest="destination",
		type="str", default='San Francisco, CA',
		help="Address of Destination")
	p.add_option('-t', action="store", dest="time",
		type='str', default='morning',
		help="Time span. 'morning' = morning rush hour. 'afternoon' = afternoon rush hour. 'none' = otherwise")
	p.add_option('-c', action="store", dest="cluster",
		type='int', default="1",
		help="Behavior cluster")

	(options,args) = p.parse_args()

	source = options.source
	destination = options.destination
	time = options.time
	cluster = options.cluster

	if time == 'morning':
		inds = [0, 1, 2, 3]
	elif time == 'afternoon':
		inds = [4, 5, 6, 7]
	else:
		inds = [8, 9, 10, 11]

	cluster_graphs = pickle.load(open('../pickles/cluster_graphs.pkl'))
	trans_edge_dict = pickle.load(open('../pickles/trans_edge_dict.pkl'))
	edge_dict = pickle.load(open('../pickles/edge_dict.pkl'))
	node_coord_dict = pickle.load(open('../pickles/node_coord_dict.pkl'))
	sc_edge, sc_frac = get_edge(source)
	ds_edge, ds_frac = get_edge(destination)

	if sc_frac > 0.5:
		sc_node = sc_edge[1]
	else:
		sc_node = sc_edge[0]

	if ds_frac > 0.5:
		ds_node = ds_edge[1]
	else:
		ds_node = ds_edge[0]

	for i in inds:
		transition_graph = cluster_graphs[i]
		path = nx.astar_path(transition_graph,sc_node,ds_node)
		for j in xrange(len(path)-1):
			edge = trans_edge_dict[(path[j],path[j+1])]
			coord1 = node_coord_dict[edge[0]]
			coord2 = node_coord_dict[edge[1]]
			print edge_dict[edge][0] + ': ' + str(coord1)

	get_gmaps_dirs(source,destination)

if __name__ == '__main__':
	main()