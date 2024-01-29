import pandas as pd
import numpy as np
df = pd.read_csv('export.csv')
df = df.fillna(0)
timestamps = {}
#print(df.iloc[1]['Disk_Avg'])
for index, row in df.iterrows():
    if row["_time"] in timestamps:
        timestamps[row["_time"]].append(row["CPU_95th_Perc"])
    else:
        timestamps[row["_time"] ] = []

with open("aggregated2.csv","a") as f:
    for k,v in timestamps.items():
        timestamps[k] = np.mean(v)
        ln = str(k[0:16])+","+str(timestamps[k]) + "\n"
        f.write(ln)
    
