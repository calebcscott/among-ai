import json
import pprint
from typing import List
from simulation import Graph, Game
from test import load_graph

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



class PlayerTimelines():
    def __init__(self, game: Game, killer):
        self.timelines: List[self.Player] = []
        self.game = game
        self.killer = killer

    def loadPlayerTimelines(self):
        self.timelines = []
        for location, player, time in self.game.events:
            if player in list(map((lambda player: player.player), self.timelines)):
                index = list(map(lambda player: player.player, self.timelines)).index(player)
                self.timelines[index].Timeline.append({
                    time: time,
                    location: location
                })
            else:
                data = self.Player(player)
                data.Timeline.append({
                    time: time,
                    location: location
                })
                self.timelines.append(data)
            

    class Player():
            def __init__(self, player):
                self.player = player
                self.Timeline = []
            
            def __str__(self) -> str:
                returnString = 'Player:\t' + str(self.player) + '\n'
                for time, location in self.Timeline:
                    returnString += '\tTime: ' + str(time) + ' Location: ' + location + '\n'
                return returnString

    def __str__(self) -> str:
        returnString = 'Killer: ' + str(self.killer) + ' Victim:' + str(self.game.dead_player) + '\n'
        for player in self.timelines:
            returnString += str(player)

        return returnString

def loadInputData(fileName) -> List[PlayerTimelines]:
    inputData = []
    with open(f'time_graph_test-10-1.json', 'r') as file:
        data = json.load(file)
    for game, killer in data:
        inputData.append(PlayerTimelines(Game(game, ''), killer))
    return inputData



if __name__ == "__main__":
    inputData: List[PlayerTimelines] = loadInputData('time_graph_test-10-1.json')
    graph = load_graph("./graph-1/test_nodes.txt", "./graph-1/test_edges.txt")

    for data in inputData:
        data.loadPlayerTimelines()
        print(data)

