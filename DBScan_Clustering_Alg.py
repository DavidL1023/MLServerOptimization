import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

day = input("Pick day\n").lower()

#change eps_value and groups based on day of week

df = pd.read_csv("/Users/angiemclean/Desktop/CSE 4939W/SDP Code/Data Cleaning/aggregated_days/hourly_aggregated_"+day+".csv")


df['_time'] = pd.to_datetime(df['_time'])

start_time = pd.to_datetime('09:00:00').time()
end_time = pd.to_datetime('15:00:00').time()

# Filter rows based on the time range
df = df[(df['_time'].dt.time >= start_time) & (df['_time'].dt.time <= end_time)]

# Convert dates to numerical representation (Unix timestamp)
df['_time'] = pd.to_datetime(df['_time']).astype(int) // 10**9
#5, 3
eps_value = 5
groups = 3

DBSCAN_data = df[['_time', 'CPU_95th_Perc']]

clustering = DBSCAN(eps=eps_value, min_samples=groups).fit(DBSCAN_data)
DBSCAN_dataset = DBSCAN_data.copy()
DBSCAN_dataset.loc[:,'Cluster'] = clustering.labels_ 

DBSCAN_dataset.Cluster.value_counts().to_frame()

outliers = DBSCAN_dataset[DBSCAN_dataset['Cluster']==-1]

fig2, axes = plt.subplots(1,figsize=(12,5))

set2_palette = sns.color_palette("Set2")

custom_palette = set2_palette + [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
]

sns.scatterplot(data=DBSCAN_dataset[DBSCAN_dataset['Cluster']!=-1], x='_time', y='CPU_95th_Perc', hue='Cluster', ax=axes, palette=custom_palette, legend='full', s=200)

plt.title('CPU 95th Percentile Over Time - '+day)

axes.scatter(outliers['_time'], outliers['CPU_95th_Perc'], s=10, label='outliers', c="k")

axes.legend()

plt.setp(axes.get_legend().get_texts(), fontsize='12')

tick_labels = [pd.to_datetime(t, unit='s').strftime('%H:%M') for t in axes.get_xticks()]
axes.set_xticklabels(tick_labels)

plt.show()

df['_time'] = pd.to_datetime(df['_time'], unit='s')

df['_time'] = df['_time'].dt.strftime('%H:%M')

'''
cluster_labels = clustering.labels_

cluster_dataframes = {}
for cluster_id in set(cluster_labels):
    if cluster_id != -1:  # Exclude outliers (cluster label = -1)
        cluster_df = df[cluster_labels == cluster_id]
        cluster_dataframes[cluster_id] = cluster_df

for cluster_id, cluster_df in cluster_dataframes.items():
    cluster_df.to_csv(f'cluster_{cluster_id}.csv', index=False)

'''


