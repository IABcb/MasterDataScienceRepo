import spotipy
import json
import sys
import spotipy.util as util
import time

'''The proposal for this script is to get information from the Spotfy API about an artist
   and his relations and albums and then compose a graph exported into a json file.

   This starts getting the friends of an artist, until a certain level of deepness. The chosen artist is David Guetta
   and the level is 3.  After that, the albums of all relations will be extracted too.

   All this information will be exported into a json file, following the necessary structure
   in order to be read for the script calcGraph.py, in wich some calculations about graphs will be made.'''

def get_id(uri):
    '''This function split the uri of an artist and gets the id'''

    id = uri.split(':')[2]
    return id

def extract_info_artist(artist, curr_level):
    '''This function gets the info we mind for this exercise'''

    artist_new = dict()
    artist_new['id'] = artist['name']
    artist_new['uri'] = artist['uri']
    artist_new['popularity'] = artist['popularity']
    artist_new['followers'] = artist['followers']['total']
    try:
        artist_new['image'] = artist['images'][0]
    except IndexError:
        artist_new['image'] = None

    artist_new['type'] = artist['type']
    artist_new['friendship_level'] = curr_level
    return artist_new

def query_discos_artist_more_50(artist_id):
    '''This function gets the discs of a given artist aid'''

    # For more than 50 results, to see them all
    sp = spotipy.Spotify()
    count = sys.maxint
    offset = 0
    limit = 1
    discos = []
    analyzed_albums = list()
    while True:
        try:
            artist_info = sp.artist_albums(artist_id, album_type='album', offset=offset, limit=limit)
            print('############# ARTIST INFO \n')
            print(artist_info)
            print()
            offset += len(artist_info['items'])
            try:
                album_name = artist_info['items'][0]['name']
                if album_name not in analyzed_albums:
                    album_image = artist_info['items'][0]['images'][0]['url']
                    album_uri = get_id(artist_info['items'][0]['uri'])
                    disco = {'name': album_name, 'uri': album_uri, 'image': album_image}
                    discos.append(disco)
                    analyzed_albums.append(album_name)
            except IndexError:
                if len(artist_info['items']) < limit:
                    break
        except ValueError:
            pass
    print('\n')
    print(discos)
    print('##############################################')
    print('\n')
    return discos

def add_main_artist(artist_id, dicc_artists):
    '''This function add the main artist info with the rest of artists'''

    sp = spotipy.Spotify()
    main_artist_info = sp.artist(artist_id)
    curr_level = 0
    dicc_artists[str(curr_level)] = []
    dicc_artists[str(curr_level)].append(extract_info_artist(main_artist_info, curr_level))
    return dicc_artists

def init_graph_data():
    '''This function initialize the dictionary of nodes'''

    graph = dict()
    graph["directed"] = False
    graph['graph'] = {}
    graph["nodes"] = list()
    graph["links"] = list()
    graph["multigraph"] = False
    return graph


def create_edge(init, end):
    '''This function create an edge in a specific way'''

    edge = dict()
    edge["source"] = init
    edge["target"] = end
    return edge

def add_node(graph, node):
    '''This function add a node in a list of nodes'''

    graph["nodes"].append(node)
    return graph

def create_album_node(album):
    '''This function creates an album node'''

    node = dict()
    node['id'] = album['name']
    node['type'] = 'album'
    node['image'] = album['image']
    node['uri'] = album['uri']
    return node

def add_edge(graph, edge):
    '''This function add an edge in a list of edges'''

    graph["links"].append(edge)
    return graph

def add_nodes(graph, list_nodes):
    '''This function add all nodes'''

    for node in list_nodes:
        graph = add_node(graph, node)
    return graph


def extract_main_artist(artist_id):
    '''This function converts info into the format we mind'''

    sp = spotipy.Spotify()
    artist_info = sp.artist(artist_id)
    artist_info = extract_info_artist(artist_info, 0)
    artist_info["name"] = artist_info["id"]
    return artist_info

def artists_related_with_one_given(artist_id, curr_level, prev_artist, nivel, dicc_artists,dicc_edges):
    '''This function gives the levels of related friends in a clean visualization '''

    curr_level += 1
    # The max. level will be nivel, for our case, level 3
    if curr_level <= nivel:
        dicc_artists.setdefault(str(curr_level), [])
        # We get the direct relations from the spotify API
        sp = spotipy.Spotify()
        artist_info = sp.artist_related_artists(artist_id)

        prev_artist = sp.artist(artist_id)
        prev_artist = prev_artist["name"]
        dicc_edges.setdefault(prev_artist, [])

        # We check every relation of every relation of the main artist
        for artist in artist_info['artists']:

            # Check if the current relation is in an upper level, same or lower.
            # If upper or same, removes the relation and gets the current relation
            # If it  lower, doesn't take the current relation because it is already in a better position
            # (the lower the better)
            analyze = True
            for level in dicc_artists.keys():
                for art in dicc_artists[level]:
                    if artist['name'] == art['id']:
                        if int(level) >= int(curr_level):
                            index_to_delete = dicc_artists[level].index(art)
                            del dicc_artists[level][index_to_delete]
                        else:
                            analyze = False

            # If we have to analyze the artist..
            if analyze:
                # We get the id
                artist_id = get_id(artist['uri'])
                # We keep the artist info
                dicc_artists[str(curr_level)].append(extract_info_artist(artist, curr_level))
                # We keep the edge
                if artist["name"] not in dicc_edges[prev_artist]:
                    dicc_edges[prev_artist].append(artist["name"])
                # We analyze the relations of this current relation
                artists_related_with_one_given(artist_id,
                                                    curr_level, prev_artist,
                                                    nivel,
                                                    dicc_artists,dicc_edges)

def add_relations(graph, dicc_artists):
    '''This function add all relation nodes into complete graph'''

    for level in dicc_artists.keys():
        graph = add_nodes(graph, dicc_artists[level])
    return graph

def get_node_pos(graph_data, name):
    '''This function gets the position of the node in json file in order
    to create the edge between two nodes'''

    for node in graph_data['nodes']:
        if name == node['id']:
            pos = graph_data['nodes'].index(node)
    return pos

def add_edges(graph_data, dicc_edges):
    '''This function gets the position of related nodes and adds the edge between them'''

    for artist in dicc_edges.keys():
        main_pos = get_node_pos(graph_data, artist)
        for friend_artist in dicc_edges[artist]:
            end_pos = get_node_pos(graph_data, friend_artist)
            edge = create_edge(main_pos, end_pos)
            add_edge(graph_data, edge)
    return graph_data

def add_discos_artists(graph_data, dicc_artists):
    '''This function gets the albums of all artists and adds them to the graph, nodes and edges'''

    for friendship_level in dicc_artists.keys():
        for artist in dicc_artists[friendship_level]:
            artist_id = get_id(artist['uri'])
            discos = query_discos_artist_more_50(artist_id)
            for disco in discos:
                node = create_album_node(disco)
                graph_data = add_node(graph_data, node)
                album_pos = get_node_pos(graph_data, node['id'])
                artist_pos = get_node_pos(graph_data, artist['id'])
                edge = create_edge(artist_pos, album_pos)
                add_edge(graph_data, edge)
    return graph_data

def export_graph_tojson(filename, graph):
    '''This function export the graph into a json file. We will export
    the info in two different files, in order to have one indented for an easier
    understanding of the structure'''

    # Json file with indented information
    with open(final_graph_filename.split('.')[0] + '_indent.json', 'w') as outfile:
        json.dump(graph_data, outfile, indent=1)

    # Json file without indented information. This will be read for calcGraph.py script
    with open(final_graph_filename, 'w') as outfile:
        json.dump(graph_data, outfile)

if __name__ == '__main__':

    # THE TOTAL EXECUTION TIME TAKES AROUND 65 MIN FOR BEING FINALIZED

    init = time.time()
    # David Guetta Id
    artist_id = '1Cs0zKBU1kc0i8ypK3B9ai'
    # File to export
    final_graph_filename = 'data/graph.json'
    # Max. Deep friendship level
    deepest_level = 3

    # Some initialization
    curr_level = 0
    prev_artist = None
    dicc_artists = dict()
    dicc_edges = dict()
    graph_data =  init_graph_data()

    # Get nodes and relations from spotify
    print("Getting nodes and relations...")
    artists_related_with_one_given(artist_id, curr_level, prev_artist, deepest_level, dicc_artists, dicc_edges)
    dicc_artists = add_main_artist(artist_id, dicc_artists)

    # Add artist nodes to graph
    print('Adding artists to graph...')
    graph_data = add_relations(graph_data, dicc_artists)

    # Get album for furthest relations
    print('Getting albumns of relations...')
    graph_data = add_discos_artists(graph_data, dicc_artists)

    # Add edges to graph
    print('Adding edges to graph...')
    graph_data = add_edges(graph_data, dicc_edges)

    # Export graph to json file
    print('Exporting to json file...')
    export_graph_tojson(final_graph_filename, graph_data)

    # Lapsed time in process
    print('Total time: ' + str((time.time() - init)/60) + ' min')