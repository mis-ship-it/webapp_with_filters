
from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from io import BytesIO
import base64

app = Flask(__name__)

# Load your dataset
df = pd.read_csv('grouped_Dispatch.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    project_types = df['Proj_Type'].dropna().unique()
    filtered_df = df.copy()

    selected_type = request.form.get('proj_type')
    selected_month = request.form.get('proj_month')

    if selected_type:
        filtered_df = filtered_df[filtered_df['Proj_Type'] == selected_type]

    if selected_month:
        filtered_df['ProjectDate'] = pd.to_datetime(filtered_df['ProjectDate'], errors='coerce')
        filtered_df = filtered_df[filtered_df['ProjectDate'].dt.strftime('%Y-%m') == selected_month]

    map_obj = folium.Map(location=[23.2599, 77.4126], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(map_obj)

    for _, row in filtered_df.iterrows():
        if not pd.isna(row['Latitude']) and not pd.isna(row['Longitude']):
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=[row['City'],row['Dispatch_Count_Enq']]

            ).add_to(marker_cluster)

    map_html = map_obj._repr_html_()
    return render_template('index.html', project_types=project_types, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
