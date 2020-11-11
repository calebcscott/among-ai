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

def create_players(number, starting_node):
    players = {}
    print(f'Creating {number} of players for current game')
    for i in range(1, number+1):
        players[i] = starting_node
    return players


def update_times(attributes, node_name, player, time):
    print(f'Updating time for {player} in node {node_name}')
    attributes[node_name].append( (player, time) )

def game(g, num_of_players):
    starting_node = random.choice(list(g.nodes))
    attributes = {
        "Dead" : "",
        "Found" : False,
        "tFound" : 0,
        "Location" : ""
    }

    camera_count = 0
    for node, _ in g :
        if node.is_camera():
            camera_count += 1
            attributes[node.get_name()] = []

    players = create_players(num_of_players, starting_node)

    # if starting node camera set all times in beginning
    if starting_node in attributes:
        for player, starting_node in players.items():
            update_times(attributes, starting_node, player, 1)

    killer = random.choice(list(players))

    buffer = 30
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
                update_times(attributes, choice.get_name(), player, time)

            # check for body
            if attributes["Dead"] and choice.get_name() == players[attributes["Dead"]] and not attributes["Found"]:
                attributes["Found"] = True
                attributes["tFound"] = time 
                attributes["Location"] = choice.get_name()
        
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
        
        # increment time
        time += 1

    return (attributes, killer)


if __name__ == "__main__":
    # test.py node_file.txt edge_file.txt out_file.txt {# of players} {# of games}
    node_file = sys.argv[1]
    edge_file = sys.argv[2]
    out_file = sys.argv[3]
    num_of_players = int(sys.argv[4])
    num_of_games = int(sys.argv[5])

    game_output = []
    print(node_file)
    graph = load_graph(node_file, edge_file)
    for i in range(num_of_games):
        game_out = game(graph, num_of_players)
        game_output.append(game_out)

    pprint.pprint(game_output)

    with open(f'{out_file}-{num_of_players}-{num_of_games}.json', "w") as file:
        json.dump(game_output, file)