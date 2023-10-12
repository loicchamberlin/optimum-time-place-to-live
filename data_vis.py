# for plotting
import matplotlib.pyplot as plt  #3.3.2
import seaborn as sns  #0.11.1
import folium  #0.14.0
from folium import plugins
import plotly.express as px  #5.1.0

# for simple routing
import osmnx as ox


def map_visualisation(start_geolocalisation, end_dataframe):
        color = "id"  #color based on this column
        lst_colors = ["blue", "red", 'black']
        popup = "id" #popup based on this column
        # base map
        map_ = folium.Map(location=start_geolocalisation, tiles="cartodbpositron", zoom_start=10)

        lst_elements = sorted(list(end_dataframe[color].unique()))
        print(lst_elements)
        end_dataframe["color"] = end_dataframe[color].apply(lambda x: lst_colors[lst_elements.index(x)])

        end_dataframe.apply(lambda row: folium.CircleMarker(
                                    location=[row["node_y"],row["node_x"]], popup=row[popup],
                                    color=row["color"], fill=True, radius=5).add_to(map_), 
                                axis=1)

        # add full-screen button
        plugins.Fullscreen(position="topright", title="Expand", title_cancel="Exit", force_separate_button=True).add_to(map_)

        # add map style config
        layers = ["cartodbpositron", "openstreetmap", "Stamen Terrain", "Stamen Water Color", "Stamen Toner", "cartodbdark_matter"]
        for tile in layers:
            folium.TileLayer(tile).add_to(map_)
            
        folium.LayerControl(position='bottomright').add_to(map_)

        # show
        return map_

def graph_visualisation(graph):
    fig, ax = ox.plot_graph(graph, bgcolor="black", node_size=12, node_color="red", figsize=(32,16))
    # return fig

if __name__ == '__main__':
    pass