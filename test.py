from simulation import Graph, BaseNode
import random
import pprint
import sys
import json

class SecurityCamera(BaseNode):
    def __init__(self, name, camera, *args):
        self.camera = camera.lower() == 'true'
        super().__init__(name, args)

    def is_camera(self):
        return self.camera

def load_graph(node_file, edge_file, NodeType=SecurityCamera):

    g = Graph(NodeType)

    g.load_nodes(node_file, r'([\w ]+),([\w ]+)')
    g.load_edges(edge_file, r'([\w ]+),([\w ]+)')

    return g

def start_point(graph):
    choices = []
    for node, edges in graph:
        for e, _ in edges:
            if e.is_camera():
                choices.append(node.get_name())
                break
    
    return random.choice(choices)

def create_players(number, starting_node):
    players = {}
    print(f'Creating {number} of players for current game')
    for i in range(1, number+1):
        players[i] = starting_node
    return players


# def update_times(attributes, node_name, player, time):
#     print(f'Updating time for {player} in node {node_name}')
#     attributes[node_name].append( (player, time) )

def game(g, num_of_players, buffer=1):
    starting_node = start_point(g)
    attributes = {
        "Dead" : "",
        "Found" : False,
        "tFound" : 0,
        "Location" : "",
        "Events" : []
    }

    all_events  = {
        "Events" : []
    }

    

    players = create_players(num_of_players, starting_node)

    # if starting node camera set all times in beginning

    killer = random.choice(list(players))

    time = 1

    while not attributes["Found"]:
        # move all players and log times
        for player, node in players.items():
            # move players
            if player is attributes["Dead"]:
                print(f'Player: {player} is dead not moving')
                continue

            choice =  random.choice(g.edges[node])[0]
            players[player] = choice.get_name()

            # log movement
            if g.nodes[choice.get_name()].is_camera():
                attributes["Events"].append( (choice.get_name(), player, time))
                #update_times(attributes, choice.get_name(), player, time)
            all_events["Events"].append( (choice.get_name(), player, time))
            # check for body
            if attributes["Dead"] and choice.get_name() == players[attributes["Dead"]] and not attributes["Found"]:
                attributes["Found"] = True
                attributes["tFound"] = time 
                attributes["Location"] = choice.get_name()

                all_events["Found"] = True
                all_events["tFound"] = time
                all_events["Location"] = choice.get_name()
        
        # determine if killer can kill
        if time > buffer and not attributes["Dead"]:
            killer_node = players[killer]
            victims = []

            for player, node in players.items():
                if player != killer and node == killer_node:
                    victims.append(player)
            print(f'Possible victims for killer {victims}')
            if 0 < len(victims) < 2:
                print(f'Killed Player {victims[0]} at time {time}')
                attributes["Dead"] = victims[0]
                all_events["Dead"] = victims[0]
        
        # increment time
        time += 1

    return (attributes, killer, all_events)


if __name__ == "__main__":
    # test.py node_file.txt edge_file.txt out_file.txt {# of players} {# of games} buffer [--all]
    # for i in {5..10}; do python3 test.py ./graph-1/test_nodes.txt ./graph-1/test_edges.txt FILE_NAME $i 1000; done
    all = False
    game_output = []
    all_events = []
    buffer = 1
    output_folder = "."

    increment = 0
    
    if "--all" in sys.argv:
        all = True
        sys.argv.pop(sys.argv.index("--all"))

    if "--inc" in sys.argv:
        index = sys.argv.index("--inc")
        sys.argv.pop(index)
        increment = int(sys.argv.pop(index))

    

    node_file = sys.argv[1]
    edge_file = sys.argv[2]
    out_file = sys.argv[3]
    num_of_players = int(sys.argv[4])
    num_of_games = int(sys.argv[5])

    
    if len(sys.argv) > 6:
        buffer = int(sys.argv[6])
    
    graph = load_graph(node_file, edge_file)

    new_graph = False

    for i in range(num_of_games):
        game_out, killer, all_e = game(graph, num_of_players, buffer)
        game_output.append((game_out, killer))
        all_events.append((all_e, killer))

        if increment:
            buffer += increment

        if i > num_of_games/2 and "--compare" in sys.argv and not new_graph:
            graph = load_graph(sys.argv[sys.argv.index("--compare") + 1], sys.argv[sys.argv.index("--compare") + 2])
            new_graph = True

    pprint.pprint(game_output)

    with open(f'{output_folder}/{out_file}-{num_of_players}-{num_of_games}-{buffer}.json', "w") as file:
        json.dump(game_output, file)


    if all:
        with open(f'{output_folder}/{out_file}-{num_of_players}-{num_of_games}-{buffer}-all-events.json', "w") as file:
            json.dump(all_events, file)