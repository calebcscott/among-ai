import json
import pprint
from typing import List
from simulation import Graph
from test import load_graph

input_data = []
num_of_players = 3




with open(f"./graph-1/au-test-{num_of_players}-1000.json", "r") as file:
    input_data = json.load(file)


graph = load_graph("./graph-1/test_nodes.txt", "./graph-1/test_edges.txt")
    
for game in input_data:
    pprint.pprint(game)
    break

def loadInputData(fileName):
    file = open(fileName)

class PlayerTimelines():
    def __init__(self, game):
        self.timelines: list[self.Player] = []
        self.game = game

        self.loadPlayerTimelines()

    def loadPlayerTimelines(self):
        self.timelines = []
        for location, player, time in game[0].Events:
            if player in map(lambda player: player.player, self.timelines):
                index = self.timelines.index(player, map(lambda player: player.player, self.timelines))
                self.timelines[index].Timeline.append({
                    time: time,
                    location: location
                })
            

    class Player():
            def __init__(self, player):
                self.player = player
                self.Timeline = []

class Search():
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal

    def searchGoal(self):

        currentNode = graph.nodes[self.start]
        goalNode = graph.nodes[self.goal]

        visited = []
        frontier = []
        path = {}

        frontier.append(currentNode)

        while len(frontier) > 0:

            currentNode = frontier.pop(0)

            if currentNode in visited:
                continue

            for node, weight in graph.nodes[currentNode.get_name()]:
                if goalNode == node:
                    return path
                frontier.append(node)

            visited.append(currentNode)


