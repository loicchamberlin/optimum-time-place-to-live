import requests, json

# for data input reading
import numpy as np
import pandas as pd

# for plotting (add functions to plot)
import matplotlib.pyplot as plt  #3.3.2
import seaborn as sns  #0.11.1
import folium  #0.14.0
from folium import plugins
import plotly.express as px  #5.1.0

# for simple routing
import osmnx as ox
import networkx as nx


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
    # converting the address
    address = address.replace(' ','+')

    r = requests.get(f'https://geocode.maps.co/search?q={address}')
    my_json = r.content.decode('utf-8')
    data = json.loads(my_json)

    return round(float(data[0]['lat']),2), round(float(data[0]['lon']),2)

def get_roadmap(input_geolocation, network_type='drive', distance=10000):
    graph = ox.graph_from_point(input_geolocation, dist=distance, simplify=True, network_type=network_type)  #'drive', 'bike', 'walk'
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)
    return graph

def get_close_nodes(graph, start_geolocation, end_geolocation):
    start_node = ox.distance.nearest_nodes(graph, Y=start_geolocation[0], X=start_geolocation[1])
    end_node = ox.distance.nearest_nodes(graph, Y=end_geolocation[0], X=end_geolocation[1])
    return start_node, end_node

def nodes_storage(graph):
    nodes_dtf = ox.graph_to_gdfs(graph, nodes=True, edges=False).reset_index()
    return nodes_dtf

def get_path(graph, input_node, input_address, method='travel_time'):
    try:
        path = nx.shortest_path(graph, source=input_node, target=input_address, method='dijkstra', weight=method) 
    except:
        path = np.nan

    try:
        path_distance = nx.shortest_path_length(graph, source=input_node, target=input_address, method='dijkstra', weight=method)
    except:
        path_distance = np.nan
    return path, path_distance

def get_all_path_and_times(workplace1, workplace2, distance):
    # get the geolocalisation of the two workplace
    geoloc_wpl1, geoloc_wpl2 = get_coordinates(workplace1.address), get_coordinates(workplace2.address)

    # create the network graph
    graph = get_roadmap(geoloc_wpl1, distance=distance)
    # get the closest nodes to the workplaces
    node_wpl1, node_wpl2 = get_close_nodes(graph, geoloc_wpl1, geoloc_wpl2)
    # store the nodes into a DataFrame
    nodes_dtf = nodes_storage(graph)

    lst = []
    # number of nodes
    print("nodes:", len(graph.nodes()))

    # logic to calculate the differents path from every nodes to both workplaces
    for row in nodes_dtf.itertuples():
        node = row.osmid
        x = row.x
        y = row.y

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

def top_10_fastest_routes(input_routes):
    input_routes['sum_times'] = input_routes['time_to_wpl1'] + input_routes['time_to_wpl2']
    input_routes['diff_times'] = abs(input_routes['time_to_wpl1'] - input_routes['time_to_wpl2'])
    input_routes['tot_times'] = input_routes['sum_times'] + input_routes['diff_times']

    # Find the index of the row with the lowest sum
    output_routes = input_routes.loc[input_routes['tot_times'].nsmallest(10).index]
    return output_routes

if __name__ == '__main__':
    workplace1 = address('52 Av. de Bordeaux', '42000', 'Mimizan','France')
    workplace2 = address('619 Av. du Maréchal Lyautey','40600','Biscarrosse','France')

    print('workplace1 : ', get_coordinates(workplace1.address))
    print('workplace2 : ', get_coordinates(workplace2.address))

    get_all_path_and_times(workplace1,workplace2)