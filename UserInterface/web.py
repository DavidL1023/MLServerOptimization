from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

chunksize = 100000

# Generate Cluster Plot
def generate_plot(table_1, table_2, eps_value, groups):
    tfr = pd.read_csv("exportforuconn.csv", chunksize=chunksize, iterator=True)
    df = pd.concat(tfr, ignore_index=True)

    data = df.columns
    # Convert dates to numerical representation (Unix timestamp)
    df['_time'] = pd.to_datetime(df['_time']).astype('int64') // 10**9

    # Reshape data for clustering
    df['_time'] = StandardScaler().fit_transform(df[['_time']])

    string_to_int = {val: idx for idx, val in enumerate(df['host'].unique())}

    # Map strings to integers using the created mapping
    df['host'] = df['host'].map(string_to_int)


    df = df.fillna(0)
    df = df.iloc[0:30000, :]

    DBSCAN_data = df[[table_1, table_2]]

    clustering = DBSCAN(eps=eps_value, min_samples=groups).fit(DBSCAN_data)
    DBSCAN_dataset = DBSCAN_data.copy()
    DBSCAN_dataset.loc[:, 'Cluster'] = clustering.labels_

    DBSCAN_dataset.Cluster.value_counts().to_frame()

    outliers = DBSCAN_dataset[DBSCAN_dataset['Cluster'] == -1]

    fig2, axes = plt.subplots(1, figsize=(12, 5))

    sns.scatterplot(data=DBSCAN_dataset[DBSCAN_dataset['Cluster'] != -1], x=table_1, y=table_2, hue='Cluster', ax=axes, palette='Set2', legend='full', s=200)

    axes.scatter(outliers[table_1], outliers[table_2], s=10, label='outliers', c="k")

    axes.legend()

    plt.setp(axes.get_legend().get_texts(), fontsize='12')
    # Create BytesIO object to store plot image data
    plot_io = BytesIO()

    # Saves figure to the BytesIO obj in PNG format
    plt.savefig(plot_io, format='png')
    plot_io.seek(0)

    # Encode image data as base64 for transmission
    plot_base64 = base64.b64encode(plot_io.getvalue()).decode('utf-8')
    plt.close()

    return plot_base64

# Run Algorithm
@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    if request.method == 'POST':
        algorithm = request.json.get('algorithm')
        # Once I receive algorithm, it will be run here and displayed as the results 
        result = f"1. (Brief) {algorithm} Description\n" \
                 f"2. {algorithm} Prediction Results\n" \
                 f"3. {algorithm} Accuracy Analysis\n"
        return jsonify({'algorithm': algorithm, 'result': result})
    
@app.route('/choose_graph', methods=['POST'])
def choose_graph():
    if request.method == 'POST':
        graph = request.json.get('graph')
        return jsonify({'graph': graph})

@app.route('/run-cluster-graph', methods=['POST'])
def run_cluster_graph():
    if request.method == 'POST':
        xColumn = request.json.get('xColumn')
        yColumn = request.json.get('yColumn')
        eps = request.json.get('eps')
        groups = request.json.get('groups')
        plot_data = generate_plot(xColumn, yColumn, eps, groups)
        return jsonify({'plot_data': plot_data})

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('web.html')
if __name__ == '__main__':
    app.run(debug=True)      