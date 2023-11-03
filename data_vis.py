import numpy as np
import pandas as pd

# for plotting
import matplotlib.pyplot as plt  # 3.3.2
import seaborn as sns  # 0.11.1
import folium  # 0.14.0
from folium import plugins

# for simple routing
import osmnx as ox


def map_visualisation_starting_points(df, mid_geoloc):
    # setup
    popup = "node_number"  # popup based on this column

    # base map
    map_ = folium.Map(location=mid_geoloc,
                      tiles="cartodbpositron", zoom_start=11)

    # add popup
    df.apply(lambda row:
             folium.CircleMarker(
                 location=[row["node_y"], row["node_x"]], popup=row[popup],
                 fill=True, radius=5).add_to(map_),
             axis=1)

    # add full-screen button
    plugins.Fullscreen(position="topright", title="Expand",
                       title_cancel="Exit", force_separate_button=True).add_to(map_)

    # show
    return map_


def map_visualisation_end_routes(start_geolocalisation, end_dataframe, graph, display_routes=False):
    color = "id"  # color based on this column
    lst_colors = ["blue", "red", 'black']
    popup = "tot_times"  # popup based on this column
    # base map
    map_ = folium.Map(location=start_geolocalisation,
                      tiles="cartodbpositron", zoom_start=10)

    lst_elements = sorted(list(end_dataframe[color].unique()))

    end_dataframe["color"] = end_dataframe[color].apply(
        lambda x: lst_colors[lst_elements.index(x)])

    end_dataframe.apply(lambda row: folium.CircleMarker(
        location=[row["node_y"], row["node_x"]], popup=row[popup],
        color=row["color"], fill=True, radius=5).add_to(map_),
        axis=1)

    # plotting the different routes
    if display_routes == True:
        for index, row in end_dataframe[['id', 'path_to_wpl1', 'path_to_wpl2']].iterrows():
            id_value = row['id']
            path_list1 = row['path_to_wpl1']
            path_list2 = row['path_to_wpl2']
            if id_value != 1 and id_value != 0:
                ox.plot_route_folium(graph, route=path_list1,
                                     route_map=map_, color="blue", weight=1)
                ox.plot_route_folium(graph, route=path_list2,
                                     route_map=map_, color="red", weight=1)

    # add full-screen button
    plugins.Fullscreen(position="topright", title="Expand",
                       title_cancel="Exit", force_separate_button=True).add_to(map_)

    # add map style config
    layers = ["cartodbpositron", "openstreetmap", "Stamen Terrain",
              "Stamen Water Color", "Stamen Toner", "cartodbdark_matter"]
    for tile in layers:
        folium.TileLayer(tile).add_to(map_)

    folium.LayerControl(position='bottomright').add_to(map_)

    # show
    return map_


def graph_visualisation(graph):
    fig, ax = ox.plot_graph(graph, bgcolor="black",
                            node_size=12, node_color="red", figsize=(32, 16))
    # return fig


def time_analysis(df):
    heatmap = df[['time_to_wpl1', 'time_to_wpl2']]

    for col in heatmap.columns:
        heatmap[col] = heatmap[col].apply(lambda x:
                                          # nan -> purple
                                          0.3 if pd.isnull(x) else
                                          (0.7 if np.isinf(x) else  # inf -> orange
                                           (0 if x != 0 else 1)))      # 0  -> white

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap, vmin=0, vmax=1, cbar=False, ax=ax)
    plt.show()


if __name__ == '__main__':
    pass
