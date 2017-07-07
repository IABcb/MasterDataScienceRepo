# Get the information from spotify
1. python getGraph.py
   output: data/graph.json => output to be analyzed
   output: data/graph_indent.json => output indented for an easier understanding of the structure

# Get some calculations about the graph and
# the final subgraph to be represented with 3jds
2. python calcGraph.py
   output: data/subgraph_analyzed.json
   output: data/graph_analyzed.json

# Visualization with 3djs
# visualization.html will represent the data/subgraph_analyzed.json
# graph.css is the style sheet
