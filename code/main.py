#!/usr/bin/python

import load_data
import pickle
import project
import cluster
import cluster_graphs
import ipdb

def main():
	data_from_pickle = 1
	projection_from_pickle = 1
	clusters_from_pickle = 1

	if data_from_pickle:
		uber_df, street_df, street_graph, node_coord_dict, coord_node_dict, \
			edge_dict, coord_lookup, transition_graph, trans_edge_dict, \
			edge_trans_dict, trans_dict = load_data.from_pickle()
	else:
		uber_df, street_df, street_graph, node_coord_dict, coord_node_dict, \
			edge_dict, coord_lookup, transition_graph, trans_edge_dict, \
			edge_trans_dict, trans_dict = load_data.load_fresh()

	''' apply Kalman filter first pass here, fix large errors '''

	if projection_from_pickle:
		print 'reading in projected uber_df from pickle...'
		uber_df = pickle.load(open('../pickles/uber_df_projected.pkl'))
		print 'read projected uber_df'
	else:
		uber_df = project.project(uber_df, street_graph, transition_graph, 
			node_coord_dict, edge_dict, edge_trans_dict, coord_lookup)
		pickle.dump(uber_df, open('../pickles/uber_df_projected.pkl','wb'))

	''' apply Kalman filter second pass here? fix small errors and re-project onto edges? '''

	# TODO: put this into load_data above
	edge_class_dict = {edge:val[1] for edge,val in edge_dict.iteritems()}
	uber_df['class'] = uber_df['edge'].map(edge_class_dict)

	if clusters_from_pickle:
		uber_df, centroids = cluster.from_pickle()
	else:
		uber_df, centroids = cluster.cluster(uber_df)

	cgraphs = cluster_graphs.make_cluster_graphs(centroids, 
		transition_graph, uber_df, edge_dict, trans_dict)
	pickle.dump(cgraphs, open('../pickles/cgraphs.pkl','wb'))

if __name__ == '__main__':
	main()