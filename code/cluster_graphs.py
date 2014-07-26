import numpy as np
import pandas as pd
import networkx as nx
import math
import matplotlib.pyplot as plt
import ipdb

def get_edge_weights(data, args):
	edge_dict = args
	cons_edges = data['consecutive_edges'].unique()
	times = np.zeros((len(cons_edges),))
	wait_times = np.zeros((len(cons_edges),))
	for i, cons_edge in enumerate(cons_edges):
		subdf = data[data['consecutive_edges'] == cons_edge]
		wait_times[i] = 4 * (len(subdf) - len(subdf[subdf['speed'] != 0]))
		times[i] = 4 * (len(subdf) - len(subdf[subdf['speed'] == 0]))

	wait_times = list(wait_times)
	times = list(times)

	times_dict = {}
	i = 0
	for j in xrange(len(data)-1):
		edge1 = data.iloc[j]['edge']
		edge2 = data.iloc[j+1]['edge']
		if edge1 != edge2:
			trans_edge = data.iloc[j]['trans_edge']
			if times[i] != 0.0:
				if trans_edge in times_dict:
					times_dict[trans_edge].append(times[i])
				else:
					times_dict[trans_edge] = [times[i]]
			if edge1[1] == edge2[0]:
				trans_edge = (data.iloc[j]['trans_edge'][1],data.iloc[j+1]['trans_edge'][0])
				if trans_edge in times_dict:
					times_dict[trans_edge].append(wait_times[i])
				else:
					times_dict[trans_edge] = [wait_times[i]]
			'''
			the following snippet adds wait time weights to all potential transitions in transition graph
			this can potentially allow illegal turns, which is currently prevented with a large prior weight
			'''
			# else:
			# 	for nodej in G.neighbors(edge1[1]):
			# 		trans_edge = (edge_trans_dict[edge1][1],nodej)
			# 		if trans_edge in times_dict:
			# 			times_dict[trans_edge].append(wait_times[i])
			# 		else:
			# 			times_dict[trans_edge] = [wait_times[i]]
			i += 1
	return times_dict

def make_cluster_graphs(centroids, transition_graph, uber_df, edge_dict, trans_dict):
	print 'making cluster graphs'
	nclusters = centroids.shape[0]
	cluster_graphs = []
	for i in xrange(nclusters):
		clone_graph = transition_graph
		df = uber_df[uber_df['cluster'] == i][['ride','speed','edge','consecutive_edges','trans_edge']]
		grouped = df.groupby('ride')
		times_group_dict = grouped[['edge','consecutive_edges','speed']].apply(get_edge_weights,
			args=(edge_dict)).to_dict()
		edge_weights_dict = {}
		for ride, times_dict in times_group_dict.iteritems():
			for edge, times in times_dict.iteritems():
				if edge in edge_weights_dict:
					edge_weights_dict[edge].extend(times)
				else:
					edge_weights_dict[edge] = times
		# print str(len(clone_graph.edges())) + ' total edges'
		# print str(len(edge_weights_dict.keys())) + ' updated edges'
		# ipdb.set_trace()
		plt.figure(figsize=(30,30))
		for edge, weights in edge_weights_dict.iteritems():
			# clone_graph[edge[0]][edge[1]]['weight'] = np.mean(weights)
			xvec = [trans_dict[edge]['start_coord'][0], trans_dict[edge]['stop_coord'][0]]
			yvec = [trans_dict[edge]['start_coord'][1], trans_dict[edge]['stop_coord'][1]]
			if trans_dict[edge]['trans_edge'] == 1:
				plt.plot(xvec,yvec,'r-')
			else:
				plt.plot(xvec,yvec,'g.')
		plt.axis('equal')
		plt.title(str(i))
		plt.show()

		cluster_graphs.append(clone_graph)
	ipdb.set_trace()
	return cluster_graphs