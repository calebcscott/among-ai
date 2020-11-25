from test import load_graph
from pathfinder import PathInfer
from amongAI import GameTimeline, loadInputData

def print_player(timelines, player_num):
    for player in timelines:
        if player.player == player_num:
            print(player)
            return player

games = loadInputData("./a-start-test-10-1.json")
all_event_games = loadInputData("./a-start-test-10-1-all-events.json")
graph = load_graph("./graph-1/test_nodes.txt", "./graph-1/test_edges.txt")

g = games[0]
g.loadPlayerTimelines()
print(g.game)

all_g = all_event_games[0]
all_g.loadPlayerTimelines()



player3 = print_player(g.timelines, 3)

path = PathInfer(graph, g.game, player3)

p = path._find_path_between_nodes(player3.timeline[1], last_time=5)
# print(f"Path predicted player {g.timelines[1].player}")
# print(p.str_path())

print(f'Path truth for player 3')
print_player(all_g.timelines, 3)

# print(p.path())

p = path.find_paths()
print(p)