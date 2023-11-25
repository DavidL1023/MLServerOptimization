import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("exportforuconn.csv")

data = df.columns

df['_time'] = pd.to_datetime(df['_time']).astype(int) // 10**9
df = df.fillna(0)
df = df.iloc[0:1000, :]

# Grouping by 'servers' column and creating separate DataFrames
server_groups = df.groupby('host')

# Creating separate DataFrames for each server
separate_dataframes = {server: group for server, group in server_groups}

print("Options for values are:")
str = '\n'
for item in data:
    str += item + ' '
print(str + '\n') 

value = input("Enter a column from the data to be plotted over time (for each server): ")
while value not in data:
    value = input("This is not in the data set, enter a different column: ")

for start in range(0, 286, 20): 
    end = min(start + 20, 286)
    fig, axs = plt.subplots(4, 5, figsize=(20, 10))
    axs = axs.flatten()

    for i, df in enumerate(separate_dataframes):
        if start + i < end:
            ax = axs[i]
            server = separate_dataframes[df]
            ax.plot(server['_time'], server[value], color='red', )
            title_font = {'family': 'serif', 'color': 'blue', 'weight': 'bold', 'size': 6}
            ax.set_title(df +': ' + value + ' Over Time', fontdict=title_font)

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.3, hspace=0.5)

# Adjusting layout
plt.tight_layout()

# Show plot
plt.show()
