import numpy as np
import pandas as pd
import pickle
import math
import ipdb

from collections import Counter
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from scipy.stats import mode
from sklearn.linear_model import LinearRegression
from sklearn import cluster, datasets 
from sklearn.preprocessing import StandardScaler

radius = 3963.1676
rad_x = 3963.1676*np.cos(37.7833*math.pi/180)

def cluster(uber_df):
	uber_df = filter_badrides(uber_df, pop=0)
	#compute speed and accel, filter out bad rides
	pickle.dump(uber_df, open('../pickles/uber_df_filtered.pkl','wb'))
	# uber_df = pickle.load(open('../pickles/uber_df_filtered.pkl'))

	uber_df = flag_rushhour(uber_df)
	tmp_dict = uber_df.groupby('ride')['rush_hour'].aggregate(lambda x: Counter(x).most_common(1)[0][0]).to_dict()
	uber_df['rush_hour'] = uber_df['ride'].map(tmp_dict)

	rush_hour_flags = ['none', 'morning', 'afternoon']
	# rush_hour_flags = ['none', 'yes']
	uber_df['cluster'] = None

	ride_cluster_dict = {}
	for i,flag in enumerate(rush_hour_flags):
		flag_df = uber_df[uber_df['rush_hour'] == flag]
		X = get_features(flag_df)
		scaler = StandardScaler()
		X_scaled = scaler.fit_transform(X)
		clusters, centers = get_clusters(X_scaled, n=2)
		centers = scaler.inverse_transform(centers)
		if centers[0,0] > centers[1,0]:
			centers = centers[::-1,:]
			clusters = np.where(clusters == 0, 1, 0)
		clusters += i*2
		if i == 0:
			centroids = centers
		else:
			centroids = np.vstack((centroids,centers))
		# ipdb.set_trace()
		ride_cluster_dict.update(dict(zip(X.index,clusters)))
	uber_df['cluster'] = uber_df['ride'].map(ride_cluster_dict)

	pickle.dump(uber_df, open('../pickles/uber_df_clustered.pkl','wb'))
	pickle.dump(centroids, open('../pickles/centroids.pkl','wb'))

	return uber_df, centroids

def from_pickle():
	uber_df = pickle.load(open('../pickles/uber_df_clustered.pkl','rb'))
	centroids = pickle.load(open('../pickles/centroids.pkl','rb'))

	return uber_df, centroids

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

def compute_speed(uber_df):
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

def filter_badrides(uber_df, pop=1):
	print 'computing speed'
	uber_df = uber_df.join(compute_speed(uber_df))
	print 'filtering bad speeds'
	bad_rides = uber_df[uber_df['speed'] > 100]['ride'].unique()
	uber_df = uber_df[~uber_df['ride'].isin(bad_rides)]

	print 'computing accel'
	uber_df = uber_df.join(compute_accel(uber_df))
	print 'filtering bad accels and decels'
	bad_rides = uber_df[uber_df['accel'] > 4]['ride'].unique()
	bad_rides = np.append(bad_rides, uber_df[uber_df['accel'] < -10]['ride'].unique())
	bad_rides = set(bad_rides)
	uber_df = uber_df[~uber_df['ride'].isin(bad_rides)]

	if pop == 1:
		uber_df.pop('speed')
		uber_df.pop('accel')

	return uber_df

'''
create rush hour flag column in Uber DataFrame
'''
def flag_rushhour(uber_df):
	print len(uber_df['ride'].unique())
	reindexed_df = uber_df.set_index('datetime')
	reindexed_df['rush_hour'] = 'none'

	morning_df = reindexed_df.ix['2007-01-01':'2007-01-06'].between_time('5:00','11:00')
	reindexed_df.ix[morning_df.index, 'rush_hour'] = 'morning'
	# reindexed_df.ix[morning_df.index, 'rush_hour'] = 'yes'
	afternoon_df = reindexed_df.ix['2007-01-01':'2007-01-06'].between_time('15:00','20:00')
	reindexed_df.ix[afternoon_df.index, 'rush_hour'] = 'afternoon'
	# reindexed_df.ix[afternoon_df.index, 'rush_hour'] = 'yes'

	return reindexed_df.reset_index()

def get_features(df):
	classes = {0,2,3,4,5}
	X = pd.DataFrame(df[(df['speed']>0) & (df['class'].isin(classes))].groupby('ride')['speed'].mean())
	X.columns = ['avg_speed']
	# X['avg_speed'] = df[(df['speed']>0) & (df['class'] != 1)].groupby('ride')['speed'].mean()
	# X['med_speed'] = df[df['speed']>0].groupby('ride')['speed'].median()
	# X['max_accel'] = df[(df['accel']>=0) & (df['class'].isin(classes))].groupby('ride')['accel'].max()
	X['avg_accel'] = df[(df['accel']>=0) & (df['class'].isin(classes))].groupby('ride')['accel'].mean()
	# X['med_accel'] = df[df['accel']>=0].groupby('ride')['accel'].median()
	# X['max_decel'] = df[(df['accel']<=0) & (df['class'].isin(classes))].groupby('ride')['accel'].min()
	X['avg_decel'] = df[(df['accel']<=0) & (df['class'].isin(classes))].groupby('ride')['accel'].mean()
	# X['med_decel'] = df[df['accel']<=0].groupby('ride')['accel'].median()

	'''
	mean free path: average time driving in between stops (aka zero velocity timestamps)
	'''
	def mfp(data):
		nz = np.where(np.append(0,data) == 0, 0, 1) # flag non-zeros
		if len(np.where(np.diff(nz) == 1)[0]) == 0:
			ipdb.set_trace()
		return 4.0*sum(nz)/len(np.where(np.diff(nz) == 1)[0]) #mean free path in seconds
	
	X['mfp'] = df[df['class'].isin(classes)].groupby('ride')['speed'].apply(mfp)

	X = X.fillna(X.mean())
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
