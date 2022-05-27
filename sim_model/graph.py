from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
import copy
# ==================================================================================================
# GRAPH CLASS
# ==================================================================================================
class Graph(object):
    # the graph is created using a sigle dict of nodes and multiple dicts of edges
    # 
    # for each edge type, there are two dicts, forward and reverse
    # these edges dicts vary based on the edge type
    # 
    # M2M forward: key = start node, value = [end nodes]
    # M2M reverse: key = start node, value = [end nodes]
    # 
    # M2O forward: key = start node, value = single end node
    # M2O reverse: key = start node, value = [end nodes]
    # 
    # O2M forward: key = start node, value = [end nodes]
    # O2M reverse: key = start node, value = single end node
    # 
    # O2O forward: key = start node, value = single end node
    # O2O reverse: key = start node, value = single end node
    #
    O2O = 'o2o' # one to one
    M2M = 'm2m' # many to many
    M2O = 'm2o' # many to one
    O2M = 'o2m' # one to many
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self):
        # nodes
        self._nodes = OrderedDict() # key is node name, value is dict of properties
        # edge_types, key is edge_type, value is x2x (M2M, M2O, O2M, O2O)
        self._edge_types = dict() 
        # forward edges, nested dictionaries three levels deep
        # first level is the snapshot dict, key is the ssid, value is an OrderedDict
        # second level for each ssid, key is the edge_type, value is an OrderedDict
        # third level, for each edge_type, key is a start node, value is one or more end nodes
        # if x2x is either M2M or O2M, then the third level value is a list, otheriwse a single value
        self._edges_fwd = dict()
        self._edges_fwd[0] = OrderedDict() 
        # reverse edges, nested dictionaries three levels deep
        # first level is the snapshot dict, key is the ssid, value is an OrderedDict
        # second level for each ssid, key is the edge_type, value is an OrderedDict
        # third level for each edge_type, key is a start node, value is one or more end nodes
        # if x2x is either M2M or M2O, then the third level value is a list, otheriwse a single value
        self._edges_rev = dict()
        self._edges_rev[0] = OrderedDict() 
        # current snapshot
        self._curr_ssid = 0
    # ==============================================================================================
    # METHODS
    # ==============================================================================================
    def add_node(self, n, **props):
        """
        Add a node to the graph. Throws an error if the node already exists.

        :param n: the name of the node, a string
        :param props: node properties, a dictionary of key-value pairs
        :return: No value.
        """
        if n in self._nodes:
            raise Exception('Node already exists.')
        self._nodes[n] = props
    # ----------------------------------------------------------------------------------------------
    def get_node_props(self, n):
        """
        Get the properties of a node in the graph. Throws an error is the node does not exist.

        :param n: the name of the node, a string
        :return: A dictionary of node properties.
        """
        if not n in self._nodes:
            raise Exception('Node does not exist.')
        return self._nodes[n]
    # ----------------------------------------------------------------------------------------------
    def get_nodes_with_out_edge(self, edge_type, ssid = None):
        """
        Get a list of nodes that have an outgoing edge of type edge_type.

        :param edge_type: the edge type
        :return: A list of node names.
        """        
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the nodes
        return self._edges_fwd[ssid][edge_type].keys()
    # ----------------------------------------------------------------------------------------------
    def get_nodes_with_in_edge(self, edge_type, ssid = None):
        """
        Get a list of nodes that have an incoming edge of type edge_type.

        :param edge_type: the edge type
        :return: A list of node names.
        """        
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the nodes
        return self._edges_rev[ssid][edge_type].keys()
    # ----------------------------------------------------------------------------------------------
    def has_node(self, n):
        """
        Return True if the node n exists in the graph.

        :param n: the name of the node, a string
        :return: True or False
        """
        return n in self._nodes
    # ----------------------------------------------------------------------------------------------
    def add_edge(self, n0, n1, edge_type):
        """
        Add an edge to the graph, from node 0 to node 1.

        :param n0: the name of the start node
        :param n1: the name of the end node
        :param edge_type: the edge type
        :return: No value.
        """
        if not n0 in self._nodes and n1 in self._nodes:
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        # add edge from n0 to n1
        if x2x in [self.M2M, self.O2M]:
            if n0 in self._edges_fwd[self._curr_ssid][edge_type]:
                self._edges_fwd[self._curr_ssid][edge_type][n0].append( n1 )
            else:
                self._edges_fwd[self._curr_ssid][edge_type][n0] = [n1]
        else:
            self._edges_fwd[self._curr_ssid][edge_type][n0] = n1
        # add rev edge from n1 to n0
        if x2x in [self.M2M, self.M2O]:
            if n1 in self._edges_rev[self._curr_ssid][edge_type]:
                self._edges_rev[self._curr_ssid][edge_type][n1].append( n0 )
            else:
                self._edges_rev[self._curr_ssid][edge_type][n1] = [n0]
        else:
            self._edges_rev[self._curr_ssid][edge_type][n1] = n0
    # ----------------------------------------------------------------------------------------------
    def has_edge(self, n0, n1, edge_type, ssid = None):
        """
        Return True if an edge from n0 to n1 exists in the graph.

        :param n0: the name of the start node
        :param n1: the name of the end node
        :param edge_type: the edge type
        :return: True if the edge exists, false otherwise..
        """
        if not n0 in self._nodes and n1 in self._nodes:
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the edge x2x            
        x2x = self._edge_types[edge_type]
        if not n0 in self._edges_fwd[ssid][edge_type]:
            return False
        if x2x in [self.M2M, self.O2M]:
            return n1 in self._edges_fwd[ssid][edge_type][n0]
        else:
            return self._edges_fwd[ssid][edge_type][n0] == n1
    # ----------------------------------------------------------------------------------------------
    def add_edge_type(self, edge_type, x2x):
        """
        Add an edge type to the graph.

        :param edge_type: the edge type
        :param x2x: one of 'm2m', 'm2o', 'o2m', 'o2o'
        :return: No value.
        """
        if edge_type in self._edge_types:
            raise Exception('Edge type already exists.')
        self._edge_types[edge_type] = x2x
        self._edges_fwd[self._curr_ssid][edge_type] = OrderedDict()
        self._edges_rev[self._curr_ssid][edge_type] = OrderedDict()
    # ----------------------------------------------------------------------------------------------
    def has_edge_type(self, edge_type):
        """
        Return True if the edge type exists in the graph.

        :param edge_type: the edge type
        :return: True if the edge type exists, false otherwise.
        """
        return edge_type in self._edge_types
    # ----------------------------------------------------------------------------------------------
    def successors(self, n, edge_type, ssid = None):
        """
        Get the successors of a node in the graph.
        The node 'n' is linked to each successor by a forward edge of type 'edge_type'.

        If the edge type ends in 'm' (i.e. 'm2m' or 'o2m'), then a list of node names is returned.
        If there are no successors, then an empty list is returned.

        If the edge type ends in 'o' (i.e. 'm2o' or 'o2o'), then a single node name is returned.
        If there are no successors, then None is returned.

        :param n: the name of the node from which to find successors
        :param edge_type: the edge type
        :return: A list of nodes names, or a single node name.
        """
        if not n in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        if n not in self._edges_fwd[ssid][edge_type]:
            if x2x in [self.M2M, self.O2M]:
                return []
            else:
                return None
        return self._edges_fwd[ssid][edge_type][n]
    # ----------------------------------------------------------------------------------------------
    def predecessors(self, n, edge_type, ssid = None):
        """
        Get the predecessors of a node in the graph.
        The node 'n' is linked to each predecessor by a reverse edge of type 'edge_type'.

        If the edge type starts with 'm' (i.e. 'm2m' or 'm2o'), then a list of node names is returned.
        If there are no predecessors, then an empty list is returned.

        If the edge type starts with 'o' (i.e. 'o2o' or 'o2m'), then a single node name returned.
        If there are no predecessors, then None returned.

        :param n: the name of the node from which to find predecessors
        :param edge_type: the edge type
        :return: A list of nodes names, or a single node name.
        """
        if not n in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        if n not in self._edges_rev[ssid][edge_type]:
            if x2x in [self.M2M, self.M2O]:
                return []
            else:
                return None
        return self._edges_rev[ssid][edge_type][n]
    # ----------------------------------------------------------------------------------------------
    def degree_in(self, n, edge_type, ssid = None):
        """
        Count the the number of incoming edges.
        The 'in degree' is the number of reverse edges of type 'ent_type' linked to node 'n'.

        :param n: the name of the node for which to count incoming edges
        :param edge_type: the edge type
        :return: An integer, the number of incoming edges.
        """
        if not n in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        # calc reverse degree
        if n not in self._edges_rev[ssid][edge_type]:
            return 0
        elif x2x in [self.M2M, self.M2O]:
            return len(self._edges_rev[ssid][edge_type][n])
        else:
            return 1
    # ----------------------------------------------------------------------------------------------
    def degree_out(self, n, edge_type, ssid = None):
        """
        Count the the number of outgoing edges.
        The 'out degree' is the number of forward edges of type 'ent_type' linked to node 'n'.

        :param n: the name of the node for which to count outgoing edges
        :param edge_type: the edge type
        :return: An integer, the number of outgoing edges.
        """        
        if not n in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        # calc forward degree
        if n not in self._edges_fwd[ssid][edge_type]:
            return 0
        elif x2x in [self.M2M, self.O2M]:
            return len(self._edges_fwd[ssid][edge_type][n])
        else:
            return 1
    # ----------------------------------------------------------------------------------------------
    def degree(self, n, edge_type):
        """
        Count the the total number of incoming and outgoing edges.

        :param n: the name of the node for which to count edges
        :param edge_type: the edge type
        :return: An integer, the number of edges.
        """
        # return result
        return self.degree_in(n, edge_type) + self.degree_out(n, edge_type)
    # ----------------------------------------------------------------------------------------------
    def snapshot(self):
        """
        Takes a snapshot of the current set of edges in the graph.

        :return: An integer, the ssid of the current snapshot.
        """
        # return result
        prev_ssid = self._curr_ssid
        self._curr_ssid += 1
        self._edges_fwd[self._curr_ssid] = copy.deepcopy(self._edges_fwd[prev_ssid])
        self._edges_rev[self._curr_ssid] = copy.deepcopy(self._edges_rev[prev_ssid])
        return prev_ssid
# ==================================================================================================
# END GRAPH CLASS
# ==================================================================================================

