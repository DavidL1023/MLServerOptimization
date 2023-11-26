import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

chunksize = 100000

tfr = pd.read_csv("exportforuconn.csv", chunksize=chunksize, iterator=True)
df = pd.concat(tfr, ignore_index=True)

data = df.columns

# Convert dates to numerical representation (Unix timestamp)
df['_time'] = pd.to_datetime(df['_time']).astype(int) // 10**9

# Reshape data for clustering
df['_time'] = StandardScaler().fit_transform(df[['_time']]) 

string_to_int = {val: idx for idx, val in enumerate(df['host'].unique())}

# Map strings to integers using the created mapping
df['host'] = df['host'].map(string_to_int)


print("Options for columns are:")
str = '\n'
for item in data:
    str += item + ' '
print(str + '\n') 

table_1 = input("Enter a column from the data set to be clustered (X values): ")
while table_1 not in data:
    table_1 = input("This is not in the data set, enter a different column: ")
table_2 = input("Enter another column from the data set to be clustered (Y values): ")
while table_2 not in data:
    table_2 = input("This is not in the data set, enter a different column: ")

eps_value = float(input("Enter an eps value to cluseter by: "))
groups = int(input("Enter the number of clusters you would like: "))

df = df.fillna(0)
df = df.iloc[0:30000, :]

DBSCAN_data = df[[table_1, table_2]]

clustering = DBSCAN(eps=eps_value, min_samples=groups).fit(DBSCAN_data)
DBSCAN_dataset = DBSCAN_data.copy()
DBSCAN_dataset.loc[:,'Cluster'] = clustering.labels_ 

DBSCAN_dataset.Cluster.value_counts().to_frame()

outliers = DBSCAN_dataset[DBSCAN_dataset['Cluster']==-1]

fig2, axes = plt.subplots(1,figsize=(12,5))

sns.scatterplot(data=DBSCAN_dataset[DBSCAN_dataset['Cluster']!=-1], x=table_1, y=table_2, hue='Cluster', ax=axes, palette='Set2', legend='full', s=200)

axes.scatter(outliers[table_1], outliers[table_2], s=10, label='outliers', c="k")

axes.legend()

plt.setp(axes.get_legend().get_texts(), fontsize='12')

plt.show()
