import numpy as np
import pandas as pd
import networkx as nx
import math
import ipdb

def get_edge_weights(data, args):
	edge_dict, edge_trans_dict = args
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
			trans_edge = edge_trans_dict[edge1]
			if trans_edge in times_dict:
				if times[i] != 0.0:
					times_dict[trans_edge].append(times[i])
			else:
				times_dict[trans_edge] = [times[i]]
			if edge1[1] == edge2[0]:
				trans_edge = (edge_trans_dict[edge1][1],edge_trans_dict[edge2][0])
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

def make_cluster_graphs(centroids, transition_graph, uber_df, edge_dict, edge_trans_dict):
	nclusters = centroids.shape[0]
	cluster_graphs = []
	for i in xrange(nclusters):
		clone_graph = transition_graph
		df = uber_df[uber_df['cluster'] == i][['ride','speed','edge','consecutive_edges','trans_edge']]
		grouped = df.groupby('ride')
		times_group = grouped[['edge','consecutive_edges','speed']].apply(get_edge_weights, args=(edge_dict, edge_trans_dict))
		edge_weights_dict = {}
		for i in xrange(len(times_group)):
			for key, val in times_group.iloc[i].iteritems():
				if key in edge_weights_dict:
					edge_weights_dict[key].extend(val)
				else:
					edge_weights_dict[key] = val
		for edge, weights in edge_weights_dict.iteritems():
			# ipdb.set_trace()
			clone_graph[edge[0]][edge[1]]['weight'] = np.mean(weights)
		cluster_graphs.append(clone_graph)
	return cluster_graphs