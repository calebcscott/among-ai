import re


# Define Base Node Class
""" Node object to contain information of the current Node i.e. Name, Position(x,y), attributes, etc. 
        Edges not an attribute of Node but Attribute of Graph
"""
class BaseNode():
    def __init__(self,
        name,
        *args
    ):
        self.name = name
        self.args = args

    def get_name(self):
        return self.name


# Define Graph Class

class Graph():
    def __init__(self, NodeType=BaseNode):
        self.nodes = {}
        self.edges = {}
        self.NodeType = NodeType
        pass
        # Nodes: Name of Node -> Node Object
        # Edges: Name of Node -> List of Connected Nodes in form (Node, weight)
        # iter returns (Current Node, List of Edges)   

    def add_node(self, name, node):
        self.nodes[name] = node
    
    def add_edge(self, name_base_node, edge_node, weight=1):
        if self.edges.get(name_base_node, None):
            self.edges[name_base_node].append((edge_node, weight))
        else:
            self.edges[name_base_node] = [(edge_node, weight)]


    def load_nodes(self, filename, re_format):
        pat = re.compile(re_format)
        with open(filename, "r") as node_file:
            for line in node_file:
                match = pat.match(line.rstrip())
                if match:
                    self.add_node(match.group(1), self.NodeType(*match.groups()))
                


    def load_edges(self, filename, re_format):
        pat = re.compile(re_format)
        with open(filename, "r") as edge_file:
            for line in edge_file:
                match = pat.match(line.rstrip())
                if match: 
                    self.add_edge(match.group(1), self.nodes[match.group(2)], int(match.group(3)) if len(match.groups()) > 2 else 1)
                    self.add_edge(match.group(2), self.nodes[match.group(1)], int(match.group(3)) if len(match.groups()) > 2 else 1)


    def write_graph(self, filename):
        """ possibly write out graph structure to file (i.e. Nodes and Edges) """
        pass


    def __iter__(self):
        for _, node in self.nodes.items():
            yield (node, self.edges.get(node.get_name(), []))

# Graph Class will read in Nodes from serialized file
# Allows for dynamic Graph generation
# Graph Class will read in Edges from file
# Allows for dynamic changes to Graph without changing Code