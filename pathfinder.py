# Example Player timeline
# [{'time': 1, 'location': 'Admin Hallway'}, {'time': 5, 'location': 'Admin Hallway'}, {'time': 7, 'location': 'Admin Hallway'}]
from simulation import BaseNode



class AStarNode(BaseNode):
    def __init__(self, name, *args):
        self.distance = -1
        self.prev_node = None

        super().__init__(name, args)

    
    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def set_prev_node(self, prev_node):
        self.prev_node = prev_node

    def heuristic(self):
        return self.distance


        


class PathInfer():
    def __init__(self, Graph, Game, Player, end_loc=None):
        self._graph = Graph
        self._converted_graph = self._graph.as_NodeType(AStarNode)
        self._game = Game
        self._player = Player
        self._end_loc = end_loc
        self.path_root = {}

    """ costly as the as_NodeType method performs disk reads """
    def _reset_graph(self):
        self._converted_graph = self._graph.as_NodeType(AStarNode)

    def _convert_path(self, node):
        if node.prev_node:
            return f"{self._convert_path(node.prev_node)},{node.get_name()}"
        return node.get_name()

    def _find_path_between_nodes(self, loc1, loc2=None, last_time=None):
        self._reset_graph()
        # define depth limit of A*
        print(f"Test of loc2: {loc2}")
        c = 2

        # last time is not multiplied by constant to prevent over searching/predicting player path
        limit = c * (loc2["time"] - loc1["time"]) if loc2 else last_time - loc1["time"]
        print(f'Depth limit of {limit}')

        path = Path(self._converted_graph.nodes.get(loc1["location"])
                             ,self._converted_graph.edges.get(loc1["location"])
                             ,self._player.player)

        path.set_distance(loc1["time"])

        if not self.path_root:
            self.path_root = path

        prio_q = [path]
        visited = []
        found = False

        #print(f"Attempting to find path between {loc1['location']} and {loc2['location']}")

        while len(prio_q) > 0:
            current = prio_q.pop(0)
            
            if loc2 and current.get_name() != loc2["location"] or len(visited) != 0:
                visited.append(current)

            #print(f'Expanding node {current.get_name()}')

            if loc2 and current.get_name() == loc2["location"] and len(visited) > 0:
                print("Reached end node!")
                found = True
                return current

            for edge, weight in current.get_edges():
                # print(f'Testing current edge: {edge.get_name()}')
                cost = weight + current.get_distance()

                found = list(filter(lambda a : a.node == edge, visited))

                # cost and distance and time are equal in this case
                # need to offset the depth limit by the current time 
                # to ensure proper traversal
                if cost > (limit + loc1["time"]):
                    continue

                if not found or cost < edge.get_distance():
                    p = Path(edge
                            , self._converted_graph.edges.get(edge.get_name())
                            , self._player.player
                            , current)
                    p.set_distance(cost)
                    prio_q.append(p)

            
            prio_q.sort(key=lambda a: a.heuristic())

        return current

    def find_paths(self):
        path = None
        for i in range(len(self._player.timeline)-1):
            # print(f"Attempting to find path between {self._player.timeline[i]} and {self._player.timeline[i+1]}")
            tmp_path = self._find_path_between_nodes(self._player.timeline[i], self._player.timeline[i+1])

            if not path:
                path = tmp_path
            else:
                path = path.join(tmp_path)
        # print(f'Attempting to join last path for timeline {self._player.timeline[i+1]}')
        return path.join(self._find_path_between_nodes(self._player.timeline[i+1], last_time=int(self._game.time_found)))

        




class Path():
    def __init__(self, node, edges, player, parent_path_node=None):
        self.node = node
        self.edges = edges
        self.player = player
        self.distance = -1
        self.parent = parent_path_node

        # print(f'Creating Path node\n\tName: {self.node.get_name()}\n\tEdges: {self.edges}\n\tParent: {self.parent}')

    def get_edges(self):
        return self.edges
    
    def set_distance(self, cost):
        self.distance = cost

    def get_distance(self):
        return self.distance

    def set_prev_node(self, parent):
        self.parent = parent

    def get_name(self):
        return self.node.get_name()

    def heuristic(self):
        return self.node.heuristic()

    def convert_to_timeline(self):
        return [self.node.get_name(), self.player, self.distance]

    def path(self):
        if not self.parent:
            return [self.convert_to_timeline()]
        path = self.parent.path()
        path.append(self.convert_to_timeline())
        return path

    def str_path(self):
        if self.parent:
            return f'{self.parent.str_path()}, {self.node.get_name()}'
        return f'{self.node.get_name()}'

    def join(self, new_path):
        my_path = self.path()
        new_path = new_path.path()

        if new_path[0] == my_path[-1]:
            new_path.pop(0)

        my_path.extend(new_path)

        return my_path