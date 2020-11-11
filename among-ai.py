import json
import pprint
from simulation import Graph
from test import load_graph

input_data = {}
num_of_players = 3




with open(f"./graph-1/au-test-{num_of_players}-1000.json", "r") as file:
    input_data = json.load(file)


graph = load_graph("./graph-1/test_nodes.txt", "./graph-1/test_edges.txt")
    
for game in input_data:
    pprint.pprint(game)
    break