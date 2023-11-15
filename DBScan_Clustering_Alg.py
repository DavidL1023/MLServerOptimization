import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

df = pd.read_csv("exportforuconn.csv")
df = df.fillna(0)
df = df.iloc[0:1000, 2:4]
X_train = df[['Mem_Avg', 'Mem_Max']]


clustering = DBSCAN(eps=12.5, min_samples=4).fit(X_train)
DBSCAN_dataset = X_train.copy()
DBSCAN_dataset.loc[:,'Cluster'] = clustering.labels_ 

DBSCAN_dataset.Cluster.value_counts().to_frame()

outliers = DBSCAN_dataset[DBSCAN_dataset['Cluster']==-1]

fig2, axes = plt.subplots(1,figsize=(12,5))

sns.scatterplot(data=DBSCAN_dataset[DBSCAN_dataset['Cluster']!=-1], x='Mem_Avg', y='Mem_Max', hue=None, ax=axes, palette='Set2', legend='full', s=200)

axes.scatter(outliers['Mem_Avg'], outliers['Mem_Max'], s=10, label='outliers', c="k")

axes.legend()

plt.setp(axes.get_legend().get_texts(), fontsize='12')

plt.show()