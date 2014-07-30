import numpy as np
import pandas as pd
import networkx as nx
import ipdb

def project(uber_df, G, transG, node_dict, edge_dict, trans_dict, coord_lookup):
	'''
	project coordinates onto street graph, and then onto transition graph
	'''
	
	def get_lookup_edges(G,node,radius):
		''' does what set(nx.ego_graph(G,node,radius).edges()) should do '''
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
		for i in xrange(len(data)):
			row = data.iloc[i]
			# if i == 28:
			# 	ipdb.set_trace()
			if broken_chain[i] == 1:
				lookup_edges = coord_lookup[(format(row['x'],'.2f'),format(row['y'],'.2f'))]
				edge1, frac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges, edge_dict)
				if searching == 1:
					broken_chain[i] = -1
				else:
					if i < len(data)-2:
						x2 = data.iloc[i+1]['x']
						y2 = data.iloc[i+1]['y']

						searching = 1
						radius = 1
						checked_edges = set()
						while searching:
							radius += 1
							if radius <= 4:
								lookup_edges = get_lookup_edges(G,edge1[1],radius)
								lookup_edges = lookup_edges.union(get_lookup_edges(G,edge1[0],radius))
							else:
								lookup_edges = coord_lookup[(format(x2,'.2f'),format(y2,'.2f'))]
							lookup_edges = lookup_edges.difference(checked_edges)
							checked_edges = checked_edges.union(lookup_edges)
							edge2, frac2, searching = find_nearest_street(x2, y2, lookup_edges, edge_dict)
							if (radius == 5) and (searching == 1):
								searching = 0
								broken_chain[i+1] = -1

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
						elif edge1[0] == edge2[0]:
							proposed_edge1 = (edge1[1], edge1[0])
							if proposed_edge1 in edge_dict:
								broken_chain[i+1] = 0
								edges.append(proposed_edge1)
								fracs.append(1-frac1)
							else:
								edges.append(edge1)
								fracs.append(frac1)
						elif edge1[0] == edge2[1]:
							proposed_edge1 = (edge1[1], edge1[0])
							proposed_edge2 = (edge2[1], edge2[0])
							if (proposed_edge1 in edge_dict) and (proposed_edge2 in edge_dict):
								broken_chain[i+1] = 0
								edges.append(proposed_edge1)
								fracs.append(1-frac1)
							else:
								edges.append(edge1)
								fracs.append(frac1)
						elif edge1[1] == edge2[0]:
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						elif (edge1[1] == edge2[1]) and ((edge2[1],edge2[0]) in edge_dict):
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						else:
							lookup_edges = set()
							if (edge1[0], edge2[0]) in edge_dict:
								lookup_edges.add((edge1[0], edge2[0]))
							if (edge1[0], edge2[1]) in edge_dict:
								lookup_edges.add((edge1[0], edge2[1]))
							lookup_edges.discard(edge1)
							newedge1, newfrac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges, edge_dict)
							if searching == 1:
								edges.append(edge1)
								fracs.append(frac1)
							else:
								if (newedge1[1] == edge2[1]) and ((edge2[1],edge2[0]) in edge_dict):
									broken_chain[i+1] = 0
									edges.append(newedge1)
									fracs.append(newfrac1)
								elif (newedge1[1] == edge2[1]) and ((edge2[1],edge2[0]) not in edge_dict):
									edges.append(edge1)
									fracs.append(frac1)
								else:
									broken_chain[i+1] = 0
									edges.append(newedge1)
									fracs.append(newfrac1)
					else:
						edges.append(edge1)
						fracs.append(frac1)
			elif broken_chain[i] == -1:
				continue
			else: # not broken chain, can be confident in start node if correct for directionality
				edge0 = edges[-1]
				frac0 = fracs[-1]
				
				lookup_edges = get_lookup_edges(G,edge0[1],1)
				lookup_edges.add(edge0)
				edge_reverse = (edge0[1], edge0[0])
				lookup_edges.discard(edge_reverse)
				edge1, frac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges, edge_dict)

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
					if startnode == -1:
						print i
					lookup_edges = get_lookup_edges(G,startnode,1)
					edge1, frac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges, edge_dict)

				if stopnode == -1:
					if i <= len(data)-2:
						x2 = data.iloc[i+1]['x']
						y2 = data.iloc[i+1]['y']
						
						searching = 1
						radius = 1
						edge_reverse = (edge1[1], edge1[0])
						checked_edges = set([edge_reverse])
						while searching:
							radius += 1
							if radius <= 4:
								lookup_edges = get_lookup_edges(G,startnode,radius)
							else:
								lookup_edges = coord_lookup[(format(x2,'.2f'),format(y2,'.2f'))]
							lookup_edges = lookup_edges.difference(checked_edges)
							checked_edges = checked_edges.union(lookup_edges)
							edge2, frac2, searching = find_nearest_street(x2, y2, lookup_edges, edge_dict)
							if (radius == 5) and (searching == 1):
								searching = 0
								broken_chain[i+1] = -1
						if edge1 == edge2:
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						elif edge1[1] == edge2[0]:
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						elif (edge1[1] == edge2[1]) and ((edge2[1],edge2[0]) in edge_dict):
							broken_chain[i+1] = 0
							edges.append(edge1)
							fracs.append(frac1)
						else:
							lookup_edges = set()
							if (startnode, edge2[0]) in edge_dict:
								lookup_edges.add((startnode, edge2[0]))
							if (startnode, edge2[1]) in edge_dict:
								lookup_edges.add((startnode, edge2[1]))
							lookup_edges.discard(edge1)
							newedge1, newfrac1, searching = find_nearest_street(row['x'], row['y'], lookup_edges, edge_dict)
							if searching == 1:
								edges.append(edge1)
								fracs.append(frac1)
							else:
								if (newedge1[1] == edge2[1]) and ((edge2[1],edge2[0]) in edge_dict):
									broken_chain[i+1] = 0
									edges.append(newedge1)
									fracs.append(newfrac1)
								elif (newedge1[1] == edge2[1]) and ((edge2[1],edge2[0]) not in edge_dict):
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
						checked_edges = set([edge_reverse])
						while searching:
							radius += 1
							if radius <= 4:
								lookup_edges = get_lookup_edges(G,stopnode,radius)
							else:
								lookup_edges = coord_lookup[(format(x2,'.2f'),format(y2,'.2f'))]
							lookup_edges.add(edge1)
							lookup_edges = lookup_edges.difference(checked_edges)
							checked_edges = checked_edges.union(lookup_edges)
							edge2, frac2, searching = find_nearest_street(x2, y2, lookup_edges, edge_dict)
							if (radius == 5) and (searching == 1):
								searching = 0
								broken_chain[i+1] = -1

						if edge1 == edge2:
							broken_chain[i+1] = 0
						elif edge1[1] == edge2[0]:
							broken_chain[i+1] = 0
						elif (edge1[1] == edge2[1]) and ((edge2[1],edge2[0]) in edge_dict):
							broken_chain[i+1] = 0

		data = data.iloc[np.where(broken_chain != -1)[0]]
		data['edge'] = edges
		data['fraction'] = fracs

		ride = data.iloc[0]['ride']
		if ride%50 == 0:
			print ride
		return data

	def find_nearest_street(x, y, edges, edge_dict):
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

	print 'projecting uber onto streets...'
	# uber_df = uber_df[uber_df['ride'] >= 21100].groupby('ride').apply(mapping)
	uber_df = uber_df.groupby('ride').apply(mapping)
	print 'found nearest edges'

	uber_df = consecutive_edges(uber_df)
	newy, newx = update_loc(uber_df['edge'], uber_df['fraction'])
	uber_df.ix[:,['y','x']] = np.vstack([newy, newx]).T

	uber_df['trans_edge'] = uber_df['edge'].apply(lambda x: trans_dict[x])
	print 'converted to transition edges'

	uber_df = uber_df.drop(['ride'],axis=1).reset_index().drop(['level_1'],axis=1)
	
	edge_class_dict = {edge:val[1] for edge,val in edge_dict.iteritems()}
	uber_df['class'] = uber_df['edge'].map(edge_class_dict)

	return uber_df

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

def consecutive_edges(df):
	'''
	create label for consecutive edges
	'''
	nrows = len(df)
	cons_edges = np.zeros((nrows,1))
	edgecount = 0
	for i in xrange(1, nrows):
		edge1 = df.iloc[i - 1]['edge']
		edge2 = df.iloc[i]['edge']
		if edge1 != edge2:
			edgecount += 1
		cons_edges[i] = edgecount
	df['consecutive_edges'] = cons_edges
	return df