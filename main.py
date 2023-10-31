import requests
import json

# for data input reading
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

# for plotting (add functions to plot)
import matplotlib.pyplot as plt  # 3.3.2
import seaborn as sns  # 0.11.1
import folium  # 0.14.0
from folium import plugins
import plotly.express as px  # 5.1.0

# for simple routing
import osmnx as ox
import networkx as nx

# for distance calculation
import geopy.distance as gd
import math as m


class address:
    def __init__(self, road, postal_code, city, country) -> None:
        self.road = road
        self.postal_code = postal_code
        self.city = city
        self.country = country
        self.address = road + ', ' + postal_code + ' ' + city + ' ' + country

    def display_address(self) -> str:
        print('My address is {}'.format(self.address))


def get_coordinates(address) -> (float, float):
    """
    This function get a string that corresponds to a real address. 
    It uses geocode api to retrieve the corresponding geolocalisation (longitude, lattitude)

    :param address: string.
    :return tuple: (longitude, lattitude).
    """
    # converting the address
    address = address.replace(' ', '+')

    r = requests.get(f'https://geocode.maps.co/search?q={address}')
    my_json = r.content.decode('utf-8')
    data = json.loads(my_json)

    return float(data[0]['lat']), float(data[0]['lon'])


def get_roadmap(input_geolocation, output_geolocalisation, network_type='drive'):
    """
    This function creates a numbered bi-directionnal graph based of two geolocalisation and the network type.

    :param input_geolocation: (longitude: float, lattitude: float).
    :param output_geolocation: (longitude: float, lattitude: float).
    :return graph: graph.
    """
    # get informations to create a centered graph
    distance = get_realdistance(input_geolocation, output_geolocalisation)
    mid_geolocalisation = get_mid_geolocalisation(
        input_geolocation, output_geolocalisation)

    graph = ox.graph_from_point(mid_geolocalisation, dist=distance,
                                simplify=True, network_type=network_type)  # 'drive', 'bike', 'walk'
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)
    return graph


def get_close_node(graph, geolocalisation) -> int:
    """
    This function find the nearest node of the graph for a geolocalisation.

    :param graph: graph.
    :param geolocation: (longitude: float, lattitude: float).
    :return node: (int, int).
    """
    node = ox.distance.nearest_nodes(
        graph, Y=geolocalisation[0], X=geolocalisation[1])

    return node


def nodes_storage(graph) -> pd.DataFrame:
    """
    This function stores the nodes into a dataframe.

    :param graph: graph.
    :return nodes_dtf: DataFrame.
    """
    nodes_dtf = ox.graph_to_gdfs(graph, nodes=True, edges=False).reset_index()
    return nodes_dtf


def get_path(graph, input_node, input_node_address, method='travel_time') -> (list[int], float):
    """
    This function find the fastest route between two nodes on a graph and gives the time for the method chosen.

    :param graph: graph.
    :param input_node: (longitude: float, lattitude: float).
    :param input_node_address: (longitude: float, lattitude: float).
    :param method: string.
    :return (path, path_distance): (list[int], float).
    """
    try:
        path = nx.shortest_path(
            graph, source=input_node, target=input_node_address, method='dijkstra', weight=method)
    except:
        path = np.nan

    try:
        path_distance = nx.shortest_path_length(
            graph, source=input_node, target=input_node_address, method='dijkstra', weight=method)
    except:
        path_distance = np.nan
    return path, path_distance


def get_all_path_and_times(workplace1, workplace2, min_samples=2) -> pd.DataFrame:
    """
    This function is the logic to create a DataFrame that contains informations about the routes for one node,
    such as : 
        - node_number,
        - node_x,
        - node_y,
        - path_to_wpl1
        - time_to_wpl1
        - path_to_wpl2
        - time_to_wpl2

    :param workplace1: string.
    :param workplace2: string.
    :return df: DataFrame.
    """
    # get the geolocalisation of the two workplace
    geoloc_wpl1, geoloc_wpl2 = get_coordinates(
        workplace1.address), get_coordinates(workplace2.address)

    # create the network graph
    graph = get_roadmap(geoloc_wpl1, geoloc_wpl2)
    # get the closest nodes to the workplaces
    node_wpl1, node_wpl2 = get_close_node(
        graph, geoloc_wpl1), get_close_node(graph, geoloc_wpl2)
    # store the nodes into a DataFrame
    nodes_dtf = nodes_storage(graph)

    # creation of the centroids to combine close areas
    centroids_dtf = cluster_close_nodes(nodes_dtf, min_samples=min_samples)

    lst = []
    # logic to calculate the differents path from every nodes to both workplaces
    for row in centroids_dtf.itertuples():
        x = row.node_x
        y = row.node_y

        node = get_close_node(graph, (y, x))

        path_to_wpl1, time_to_wpl1 = get_path(graph, node, node_wpl1)
        path_to_wpl2, time_to_wpl2 = get_path(graph, node, node_wpl2)

        data = {
            'node_number': node,
            'node_x': x,
            'node_y': y,
            'path_to_wpl1': path_to_wpl1,
            'time_to_wpl1': time_to_wpl1,
            'path_to_wpl2': path_to_wpl2,
            'time_to_wpl2': time_to_wpl2
        }

        lst.append(data)

    df = pd.DataFrame(lst)
    return df


def cluster_close_nodes(nodes, epsilon=0.01, min_samples=2):
    """
    add a description
    """
    coordinates = nodes[['x', 'y']].values

    # Define the epsilon (maximum distance between two samples) and minimum samples for DBSCAN

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples,
                    metric='euclidean').fit(coordinates)

    # Get the labels and unique clusters identified by DBSCAN
    labels = dbscan.labels_
    unique_labels = np.unique(labels)

    # Find the centroids of each cluster
    centroids = []
    for label in unique_labels:
        if label != -1:  # Ignoring noise points (label -1)
            cluster_points = coordinates[labels == label]
            cluster_centroid = np.mean(cluster_points, axis=0)
            centroids.append(cluster_centroid)

    '''print("Cluster Centroids:")
    for idx, centroid in enumerate(centroids):
        print(f"Cluster {idx + 1}: {centroid}")'''

    centroids_dtf = pd.DataFrame(data={'id': [i for i in range(0, len(centroids))],
                                       'node_y': [arr[1] for arr in centroids],
                                       'node_x': [arr[0] for arr in centroids]})
    return centroids_dtf


def top_fastest_routes(input_routes, number) -> pd.DataFrame:
    """
    This function calculates the sum and the absolute difference of times for each node in order to find
    the first 10th fastest routes available in the graph. 
    It is important to take into account the fact that these routes are optimised to be almost equals. This aims
    to have a real split and equal time to work.

    :param input_routes: DataFrame.
    :return output_routes: DataFrame.
    """
    input_routes['sum_times'] = input_routes['time_to_wpl1'] + \
        input_routes['time_to_wpl2']
    input_routes['diff_times'] = abs(
        input_routes['time_to_wpl1'] - input_routes['time_to_wpl2'])
    input_routes['tot_times'] = input_routes['sum_times'] + \
        input_routes['diff_times']

    # Find the index of the row with the lowest sum
    output_routes = input_routes.loc[input_routes['tot_times'].nsmallest(
        number).index]

    output_routes["id"] = 2
    return output_routes


def get_realdistance(geoloc1, geoloc2) -> int:
    """
    This function calculates the real distance between two geolocalisation in meters.

    :param geoloc1: (float, float).
    :param geoloc2: (float, float).
    :return distance: int.
    """
    return int(gd.geodesic(geoloc1, geoloc2).m)


def get_mid_geolocalisation(geoloc1, geoloc2) -> (float, float):
    """
    This function finds the mid geolocalisation between to geolocalisation

    :param geoloc1: (float, float).
    :param geoloc2: (float, float).
    :return out_geolocalisation: (float,float).
    """
    Bx = m.cos(geoloc2[1]) * m.cos(geoloc2[0]-geoloc1[0])
    By = m.cos(geoloc2[1]) * m.sin(geoloc2[0]-geoloc1[0])

    mid_lattitude = m.atan2(m.sin(geoloc1[1]) + m.sin(geoloc2[1]), m.sqrt(
        (m.cos(geoloc1[1])+Bx)*(m.cos(geoloc1[1])+Bx) + By*By))
    mid_longitude = geoloc1[0] + m.atan2(By, m.cos(geoloc1[1]) + Bx)

    return (mid_longitude, mid_lattitude)


if __name__ == '__main__':
    pass
