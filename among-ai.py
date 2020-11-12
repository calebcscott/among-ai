import json
import pprint
import queue
from typing import List
from simulation import Graph, Game
from test import load_graph

"""

"""
class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

        # for popping an element based on Priority

    def get(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()

class State(object):
    def __init__(self, graph, name, parent, start = 0, goal = 0):
        self.graph = graph
        self.children = []
        self.parent = parent
        self.name = name
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(name)
            self.start = parent.start
            self.goal = self.goal
        else:
            self.path = [name]
            self.start = start
            self.goal = goal
    def GetDistance(self):
        pass
    def CreateChildren(self):
        pass

class State_String(State):
    def __init__(self, name, parent, start = 0, goal = 0):
        super(State_String, self).__init__(name, parent, start, goal)
        self.dist = self.GetDistance()

    """test distance function"""
    def GetDistance(self):
        if self.name == self.goal:
            return 0
        dist = 0
        for i in range(len(self.goal)):
            letter = self.goal[i]
            dist += abs(i - self.name.index(letter))
        return dist

    def CreateChildren(self):
        if not self.children:
            for i in xrange(len(self.goal) - 1):
                """add all possible states connected by"""

class AStar:
    def __init__(self, start, goal):
        self.path = []
        self.vistitedQueue = []
        self.priotiryQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def Solve(self):
        startState = State_String(self.start, 0, self.start, self.goal)
        count = 0
        self.priotiryQueue.insert(0, count, startState)
        while(not self.path and not self.priotiryQueue.isEmpty()):
            closestChild = self.priotiryQueue.get()[2] # not sure what the [2] does
            closestChild.CreateChilden()
            self.vistitedQueue.insert(closestChild.name)
            for child in closestChild.children:
                if child.name not in self.vistitedQueue:
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priotiryQueue.insert(child.dist, count, child)
        if not self.path:
            print(self.goal+" not possible to reach")
        return self.path




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
    with open(fileName, 'r') as file:
        data = json.load(file)
    for game, killer in data:
        inputData.append(GameTimeline(Game(game, ''), killer))
    return inputData


"""
MAIN METHOD BIOTCHES
"""
if __name__ == "__main__":
    inputData: List[GameTimeline] = loadInputData('./graph-1/test_data/testPrint-10-10.json')
    counter = 0
    for data in inputData:
        data.loadPlayerTimelines()
        coins = data.getCoincidences('Admin Hallway', 8, 1)
        print(f"Game: {counter}")
        counter += 1
        print(data)
        
        for coin in coins:
            print(f"player: {coin['player']}")
            print(f"location: {coin['location']}")
            print(f"time: {coin['time']}")

    """
    start = some node
    goal = some node
    graoh = loadGraph somhow
    a = AStar_Solver( start, goal)
    a.Solve()
    for i in range(len(a.path)):
        print(a.path[i]+" ")
    """
    pass
