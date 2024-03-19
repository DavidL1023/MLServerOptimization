#IMPORTANT
#Needs to read from CSV file with the format server_name, _time, CPU_95th_Perc
#For better results, split up this csv files by the day of the week and averaged servers for each hour
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

#changes eps_value and groups to best value based on day of week
if day == 'monday':
    eps_value = 5
    groups = 3
elif day == 'tuesday':
    eps_value = 12
    groups = 2
elif day == 'wednesday':
    eps_value = 15
    groups = 2
elif day == 'thursday':
    eps_value = 10
    groups = 2
elif day == 'friday':
    eps_value = 13
    groups = 2
elif day == 'saturday':
    eps_value = 15
    groups = 2
elif day == 'sunday':
    eps_value = 15
    groups = 3

#read chosen day of the week file
df = pd.read_csv("/Users/angiemclean/Desktop/CSE 4939W/SDP Code/Data Cleaning/aggregated_days/hourly_aggregated_"+day+".csv")

#change time columns to datetime format
df['_time'] = pd.to_datetime(df['_time'])

#set a start time and end time for clustering graph
start_time = pd.to_datetime('09:00:00').time()
end_time = pd.to_datetime('15:00:00').time()

# Filter rows based on the times selected above
df = df[(df['_time'].dt.time >= start_time) & (df['_time'].dt.time <= end_time)]

# Convert dates to numerical representation (seconds)
df['_time'] = pd.to_datetime(df['_time']).astype(int) // 10**9

#take CPU percentile data and _time (only columns used for clustering)
DBSCAN_data = df[['_time', 'CPU_95th_Perc']]

#run DBScan algorithm on above columns
clustering = DBSCAN(eps=eps_value, min_samples=groups).fit(DBSCAN_data)
DBSCAN_dataset = DBSCAN_data.copy()
DBSCAN_dataset.loc[:,'Cluster'] = clustering.labels_ 

DBSCAN_dataset.Cluster.value_counts().to_frame()

outliers = DBSCAN_dataset[DBSCAN_dataset['Cluster']==-1]

#set up plots and color pallete
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

#chnage times back from seconds to HH:MM format
tick_labels = [pd.to_datetime(t, unit='s').strftime('%H:%M') for t in axes.get_xticks()]
axes.set_xticklabels(tick_labels)

plt.show()

df['_time'] = pd.to_datetime(df['_time'], unit='s')

df['_time'] = df['_time'].dt.strftime('%H:%M')

#following code takes the graph selected by user and creates seperate csv files of each cluster (used to see which servers belong to which groups)

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



