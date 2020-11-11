import json
import pprint
from typing import List
from simulation import Graph, Game
from test import load_graph

"""

"""
class Search():
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal

    """

    """
    def searchGoal(self):

        currentNode =self.graph.nodes[self.start]
        goalNode = self.graph.nodes[self.goal]

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


"""
    Object that hold timelines and details for players in a given game
"""
class GameTimeline():
    def __init__(self, game: Game, killer):
        self.timelines: List[self.Player] = []
        self.game = game
        self.killer = killer

    """
        Loads individual player timelines from game data
    """
    def loadPlayerTimelines(self):
        self.timelines = []
        for location, player, time in self.game.events:
            if player in list(map((lambda player: player.player), self.timelines)):
                index = list(map(lambda player: player.player, self.timelines)).index(player)
                self.timelines[index].timeline.append({
                    'time': time,
                    'location': location
                })
            else:
                data = self.Player(player)
                data.timeline.append({
                    'time': time,
                    'location': location
                })
                self.timelines.append(data)

    """
        finds players at a specified location within a given time range
    """
    def getCoincidences(self, location, time, timeRange) -> list:
        returnList = []
        for player in self.timelines:
            if location in list(map(lambda time: time['location'], player.timeline)):
                indexes = [i for i, x in enumerate(list(map(lambda time: time['location'], player.timeline))) if x == location]
                for index in indexes:
                    for time in range(time - timeRange, time + timeRange + 1):
                        if time == player.timeline[index]['time']:
                            returnList.append({
                                'player': player.player,
                                'time': time,
                                'location': location
                            })
        
        return returnList
            
    """
    Object to hold a player identifier and their timeline
    """
    class Player():
            def __init__(self, player):
                self.player = player
                self.timeline = []
            
            def __str__(self) -> str:
                returnString = 'Player:\t' + str(self.player) + '\n'
                for time in self.timeline:
                    returnString += '\tTime: ' + str(time['time']) + ' Location: ' + time['location'] + '\n'
                return returnString

    def __str__(self) -> str:
        returnString = 'Killer: ' + str(self.killer) + ' Victim: ' + str(self.game.dead_player) + '\n'
        for player in self.timelines:
            returnString += str(player)

        return returnString

"""
Function to load input data into GameTimeline objects
"""
def loadInputData(fileName) -> List[GameTimeline]:
    inputData = []
    with open(f'time_graph_test-10-1.json', 'r') as file:
        data = json.load(file)
    for game, killer in data:
        inputData.append(GameTimeline(Game(game, ''), killer))
    return inputData


"""
MAIN METHOD BIOTCHES
"""
if __name__ == "__main__":
    inputData: List[GameTimeline] = loadInputData('time_graph_test-10-1.json')

    for data in inputData:
        data.loadPlayerTimelines()
        coins = data.getCoincidences('Admin Hallway', 8, 1)
        print(data)
        for coin in coins:
            print(f"player: {coin['player']}")
            print(f"location: {coin['location']}")
            print(f"time: {coin['time']}")

