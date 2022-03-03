from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
class Graph():

    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================

    def __init__(self, edge_types):
        self.edge_types = edge_types
        self.nodes = {}
        self.edges = {}
        self.edges_rev = {}
        self.data = {}
        for edge_type in edge_types:
            self.edges[edge_type] = {}
            self.edges_rev[edge_type] = {}

    # ==============================================================================================
    # METHODS
    # ==============================================================================================

    def add_node(self, n: str, **attribs):
        self.nodes[n] = attribs
        for edge_type in self.edges.keys():
            self.edges[edge_type][n] = []
        for edge_type in self.edges_rev.keys():
            self.edges_rev[edge_type][n] = []

    def add_edge(self, n0: str, n1: str, edge_type: str):
        if not n0 in self.nodes and n1 in self.nodes:
            raise Exception('Node does not exist.')
        self.edges[edge_type][n0].append( n1 )
        self.edges_rev[edge_type][n1].append( n0 )

    def successors(self, n: str, edge_type: str):
        return self.edges[edge_type][n]

    def predecessors(self, n: str, edge_type: str):
        return self.edges_rev[edge_type][n]

    def degree(self, n: str, edge_type: str):
        return len(self.edges[edge_type][n]) + len(self.edges_rev[edge_type][n])
