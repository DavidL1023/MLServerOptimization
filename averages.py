import pandas as pd
import numpy as np
df = pd.read_csv('export.csv')
df = df.fillna(0)
timestamps = {}
for index, row in df.iterrows():
    if row["host"] in timestamps:
        timestamps[row["host"]].append(row["CPU_95th_Perc"])
    else:
        timestamps[row["host"]] = [row["CPU_95th_Perc"]]
with open("average_cpus.csv","a") as f:
    for k,v in timestamps.items():
        timestamps[k] = np.mean(v)
        ln = str(k[0:16])+","+str(timestamps[k]) + "\n"
        f.write(ln)

    
