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
