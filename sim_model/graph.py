from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
class Graph(object):

    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================

    def __init__(self, edge_types):
        self.edge_types = edge_types
        self.nodes = OrderedDict()
        self.edges = OrderedDict()
        self.edges_rev = OrderedDict()
        self.data = OrderedDict()
        for edge_type in edge_types:
            self.edges[edge_type] = OrderedDict()
            self.edges_rev[edge_type] = OrderedDict()

    # ==============================================================================================
    # METHODS
    # ==============================================================================================

    def add_node(self, n, **attribs):
        self.nodes[n] = attribs
        for edge_type in self.edges.keys():
            self.edges[edge_type][n] = []
        for edge_type in self.edges_rev.keys():
            self.edges_rev[edge_type][n] = []

    def add_edge(self, n0, n1, edge_type):
        if not n0 in self.nodes and n1 in self.nodes:
            raise Exception('Node does not exist.')
        self.edges[edge_type][n0].append( n1 )
        self.edges_rev[edge_type][n1].append( n0 )

    def successors(self, n, edge_type):
        return self.edges[edge_type][n]

    def predecessors(self, n, edge_type):
        return self.edges_rev[edge_type][n]

    def degree(self, n, edge_type):
        return len(self.edges[edge_type][n]) + len(self.edges_rev[edge_type][n])
