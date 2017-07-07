import networkx as nx
from networkx_viewer import Viewer
import json
import time
from networkx.readwrite import json_graph
import community

'''The main proposal for this script is to calculate some operations about graphs, given one.
    The graph will be imported from a json file and then, the next operations over each node will be calculated
    and added to each one:
    ** Centralities:
        * Betweeness
        * Degree
        * Closeness
        * PageRank
    ** Clustering Score
    ** Community detection

    The final graph will be export to a json file, in order to be visualized with 3djs with the script "visualization.html"'''

def get_centralities(g):
    '''This function calculates, for each connected component:
    # Degree
    # Closeness
    # Betweeness
    # PageRank
    '''

    centralities_data = {'degree': [], 'closeness':[], 'betweeness':[], 'pagerank':[]}
    max_conn_comp = None
    n=0
    print('Calculating centralities...')
    for conn_comp in nx.connected_component_subgraphs(g):
        if len(conn_comp) > 1:
            centralities_data['degree'].append(nx.degree_centrality(conn_comp))
            centralities_data['closeness'].append(nx.closeness_centrality(conn_comp))
            centralities_data['betweeness'].append(nx.betweenness_centrality(conn_comp))
            centralities_data['pagerank'].append(nx.pagerank(conn_comp))
            if (max_conn_comp is None) or (len(max_conn_comp) < len(conn_comp)):
                max_conn_comp = conn_comp
    return centralities_data

def clustering_score(g):
    '''This function calculates the clustering score'''

    print('The clustering score is: ' + str(nx.average_clustering(g)))


def add_centralities_tonodes(g, centralities_data):
    '''This function adds attributes to graphs'''

    print('Adding centralities to nodes..')
    centralities_types = centralities_data.keys()
    for cent_type in centralities_types:
        print('**Adding centrality type ' + cent_type)
        for conex_comp in centralities_data[cent_type]:
            for node_name in conex_comp.keys():
                g.node[node_name][cent_type] = conex_comp[node_name]
    return g

def see_graph(g):
    # Viewer

    app	=	Viewer(g)
    app.mainloop()

def import_graph_fromjson(path):
    '''This function import a graph from a json file'''

    with open(path, 'r') as f:
        json_data = json.load(f)
        g = json_graph.node_link_graph(json_data, directed=False)
    return g

def export_tojson(g, filename):
    '''This function export the graph to json file'''

    g_json = json_graph.node_link_data(g)

    with open(filename, 'w') as outfile:
        json.dump(g_json, outfile)

def community_detection(g):
    '''This function detects communities in a graph'''

    print('Detecting communities...')
    return community.best_partition(g)

def add_community_tonodes(g, communities):
    '''This function adds the community entity
     to each node in the graph as a attribute'''

    for node_name in communities.keys():
        g.node[node_name]['community'] = communities[node_name]
    return g

def get_subgraph(g, subgraph_size, feature, type):
    '''This function calculates a subgraph of subgraph_size artists theirs albums.
     In order to  filter the artist to be taken into account to, we need a feature to be filtered.
     subgraph_size best nodes will be displayed in the final subgraph'''

    # Extract the filter feature, node_name and node_type for each node
    gs = [(node_info[feature], node_name, node_info["type"]) for node_name, node_info in graph.node.items()]
    # Order nodes by feature in descending way
    sorted_gs = [(x[1],x[2]) for x in sorted(gs, key=lambda x: x[0], reverse=True)]
    # Extract only type nodes
    type_sorted_gs = [node[0] for node in sorted_gs if node[1] == type]
    # Get the subgraph_size first nodes
    type_sorted_gs = type_sorted_gs[:subgraph_size]
    # Add album_nodes
    artists_and_adjacencies = [(artist_name, g.neighbors(artist_name)) for artist_name in type_sorted_gs]
    # Get album adjacencies
    subgraph_node_list = list()
    for art_name, nbs in artists_and_adjacencies:
        subgraph_node_list.append(art_name)
        for nb_name in nbs:
            if g.node[nb_name]['type'] == 'album':
                subgraph_node_list.append(nb_name)
    # Get subgraph object
    subgraph = g.subgraph(subgraph_node_list)
    return subgraph

if __name__ == "__main__":

    # THE TOTAL EXECUTION TIME TAKES AROUND 9 MIN FOR BEING FINALIZED

    # Load graph
    path = 'data/graph.json'
    graph = import_graph_fromjson(path)

    # Environment
    init_time = time.time()

    # Number of artists in subgraph
    artist_subgraph_size = 50

    # Artists with major degree, will be taken into account as more important ones.
    # The more degree an artist have, with more artists has worked
    # and more albums has been released from him
    artist_subgraph_filter = 'degree'
    subgraph_type = 'artist'

    # Analysis
    # Centralities
    centralities_data = get_centralities(graph)
    graph = add_centralities_tonodes(graph, centralities_data)

    # Community detection
    communities = community_detection(graph)
    artist_subgraph = add_community_tonodes(graph, communities)

    # Get subgraph
    subgraph = get_subgraph(graph, artist_subgraph_size, artist_subgraph_filter, subgraph_type)

    # Clustering scores
    print('Clustering score of total graph')
    clustering_score(graph)
    print('Clustering score of artist graph')
    clustering_score(subgraph)

    # Export graph and subgraph to json. We will export the info in two different json.
    # Json file with all the graph information
    export_tojson(graph, filename = 'data/graph_analyzed.json')

    # Json file with the partial information of the graph, the subgraph. This graph will be represented with 3jds
    export_tojson(subgraph, filename = 'data/subgraph_analyzed.json')

    # Lapsed time in process
    print('Lapsed time: ' + str((time.time() - init_time)/60) + ' min')

