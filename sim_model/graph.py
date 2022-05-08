from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict

# edge types
O2O = 'o2o' # one to one
M2M = 'm2m' # many to many
M2O = 'm2o' # many to one
O2M = 'o2m' # one to many

class Graph(object):

    # the graph is created using a sigle dict of nodes and multiple dicst of edges
    # 
    # for each edge type, there are two dicts, forward and reverse
    # these edges dicts vary based on the edge type
    # 
    # M2M forward: key is the start node, the value is a list of end nodes
    # M2M reverse: key is the start node, the value is a list of end nodes
    # 
    # M2O forward: key is the start node, the value is a single end node
    # M2O reverse: key is the start node, the value is a list of end nodes
    # 
    # O2M forward: key is the start node, the value is a list of end nodes
    # O2M reverse: key is the start node, the value is a single end node
    # 
    # O2O forward: key is the start node, the value is a single end node
    # O2O reverse: key is the start node, the value is a single end node

    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self):
        # nodes
        self.nodes = OrderedDict() # key is node name, value is dict of attributes
        # edges
        self.edge_types = OrderedDict() # key is edge_type, value is x2x
        self.edges_fwd = OrderedDict() # key is the edge_type, value is a dict of edges 
        self.edges_rev = OrderedDict() # key is the edge_type, value is a dict of edges 

    # ==============================================================================================
    # METHODS
    # ==============================================================================================

    def add_node(self, n, **attribs):
        self.nodes[n] = attribs

    def add_edge(self, n0, n1, edge_type):
        if not n0 in self.nodes and n1 in self.nodes:
            raise Exception('Node does not exist.')
        x2x = self.edge_types[edge_type]
        # add edge from n0 to n1
        if x2x in [M2M, O2M]:
            if n0 in self.edges_fwd[edge_type]:
                self.edges_fwd[edge_type][n0].append( n1 )
            else:
                self.edges_fwd[edge_type][n0] = [n1]
        else:
            self.edges_fwd[edge_type][n0] = n1
        # add rev edge from n1 to n0
        if x2x in [M2M, M2O]:
            if n1 in self.edges_rev[edge_type]:
                self.edges_rev[edge_type][n1].append( n0 )
            else:
                self.edges_rev[edge_type][n1] = [n0]
        else:
            self.edges_rev[edge_type][n1] = n0

    def add_edge_type(self, edge_type, x2x):
        self.edge_types[edge_type] = x2x
        self.edges_fwd[edge_type] = OrderedDict()
        self.edges_rev[edge_type] = OrderedDict()

    def successors(self, n, edge_type):
        x2x = self.edge_types[edge_type]
        if n not in self.edges_fwd[edge_type]:
            if x2x in [M2M, O2M]:
                return []
            else:
                return None
        return self.edges_fwd[edge_type][n]

    def predecessors(self, n, edge_type):
        x2x = self.edge_types[edge_type]
        if n not in self.edges_rev[edge_type]:
            if x2x in [M2M, M2O]:
                return []
            else:
                return None
        return self.edges_rev[edge_type][n]

    def degree(self, n, edge_type):
        if not n in self.nodes :
            raise Exception('Node does not exist.')
        x2x = self.edge_types[edge_type]
        # calc forward degree
        if n not in self.edges_fwd[edge_type]:
            fwd_deg = 0
        elif x2x in [M2M, O2M]:
            fwd_deg = len(self.edges_fwd[edge_type][n])
        else:
            fwd_deg = 1
        # calc reverse degree
        if n not in self.edges_rev[edge_type]:
            rev_deg = 0
        elif x2x in [M2M, M2O]:
            rev_deg = len(self.edges_rev[edge_type][n])
        else:
            rev_deg = 1
        # return result
        return fwd_deg + rev_deg
