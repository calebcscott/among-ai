import json
from typing import List
from simulation import Graph, Game
from test import load_graph
from pathfinder import Predict, Compare_paths, get_player
import sys
from pathlib import Path

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
            for i in range(len(self.goal) - 1):
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
        self.timelines.sort(key=lambda timeline: timeline.player)

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
    input_data = './graph-1/test_data/progress_report-10-1.json'
    nodes = "./graph-1/test_nodes.txt"
    edges = "./graph-1/test_edges.txt"
    all_event = './graph-1/test_data/progress_report-10-1-all-events.json'


    

    if len(sys.argv) > 1:
        input_data = sys.argv[1]
        all_event = sys.argv[1][:-5] + "-all-events.json"

    inputData: List[GameTimeline] = loadInputData(input_data)

    all_event_path = Path(all_event)

    if all_event_path.exists():
        all_event_games = loadInputData(all_event)

    graph = load_graph(nodes, edges)


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

    total = 0
    correct = 0

    index = 0
   
    game_metrics = []
    print(f'A* algorithm')
    for data in inputData:
        
        if all_event_path.exists():
            all_event_games[index].loadPlayerTimelines()
        
        predicted_killer, probability, output_paths = Predict(data, graph)
        print(f"Predicted: {predicted_killer}\tActual: {data.killer}\n\tWith probability: {probability}")

        total += 1
        if predicted_killer == data.killer:
            correct += 1

        game_output = (predicted_killer, data.killer)

        if all_event_path.exists():
            count = 10
            path_accrs = []
            path_corr = 0
            path_total = 0
            for predict_player in output_paths:
                truth = get_player(all_event_games[index].timelines, predict_player[0][1])

                corr, tot = Compare_paths(predict_player, truth.timeline)
                path_corr += corr
                path_total += tot

                path_accr = corr/tot
                path_accrs.append((predict_player[0][1], path_accr))

                print(f'Player {predict_player[0][1]} path accuracy: {round(path_accr*100, 2)}%')
                count -= 1
            game_output = (predicted_killer, data.killer, path_corr, path_total, path_accrs)
            print(f'Did not predict the paths for {count} players')

        index += 1
        game_metrics.append(game_output)

    print(f'Accuracy: {round((correct/total)*100, 2)}%')

    with open(f'{input_data[:-5]}-metrics.json', "w") as file:
        json.dump((game_metrics, correct/total), file)

    # Accuracy metrics = {
    #       List of all games : [
    #           "predicted",
    #           "actual",
    #           "total correct",
    #           "total path node predictions",
    #           "List of path accuracy percentages"
    #       ]  ,
    #       Accuracy of all games : 14%
    # }

    
    pass
