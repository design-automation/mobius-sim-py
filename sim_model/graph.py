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
    FWD = 0
    REV = 1
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self):
        # nodes
        self._nodes = OrderedDict() # key is node name, value is dict of properties
        # edge_types, key is edge_type, value is x2x (M2M, M2O, O2M, O2O)
        self._edge_types = dict() 
        # edges, nested dictionaries four levels deep
        # first level is the snapshot dict, key is the ssid, value is an OrderedDict
        # second level for each ssid, key is the edge_type, value is an dict
        # third level for each edge type, key is FWD or REV, value is OrderedDict
        # fourth level, for each edge_type, key is a start node, value is a list of end nodes
        self._edges = dict()
        # init snapshot 0
        self._edges[0] = OrderedDict() 
        self._curr_ssid = 0
    # ==============================================================================================
    # METHODS
    # ==============================================================================================
    def add_node(self, node, **props):
        """
        Add a node to the graph. Throws an error if the node already exists.

        :param n: the name of the node, a string
        :param props: node properties, a dictionary of key-value pairs
        :return: No value.
        """
        if node in self._nodes:
            raise Exception('Node already exists.')
        self._nodes[node] = props
    # ----------------------------------------------------------------------------------------------
    def get_node_props(self, node):
        """
        Get the properties of a node in the graph. Throws an error is the node does not exist.

        :param n: the name of the node, a string
        :return: A dictionary of node properties.
        """
        if not node in self._nodes:
            raise Exception('Node does not exist.')
        return self._nodes[node]
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
        return self._edges[ssid][edge_type][Graph.FWD].keys()
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
        return self._edges[ssid][edge_type][Graph.REV].keys()
    # ----------------------------------------------------------------------------------------------
    def has_node(self, node):
        """
        Return True if the node n exists in the graph.

        :param n: the name of the node, a string
        :return: True or False
        """
        return node in self._nodes
    # ----------------------------------------------------------------------------------------------
    def add_edge(self, node0, node1, edge_type):
        """
        Add an edge to the graph, from node 0 to node 1.

        :param n0: the name of the start node
        :param n1: the name of the end node
        :param edge_type: the edge type
        :return: No value.
        """
        if not node0 in self._nodes and node1 in self._nodes:
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # add edge from n0 to n1
        if node0 in self._edges[self._curr_ssid][edge_type][Graph.FWD]:
            self._edges[self._curr_ssid][edge_type][Graph.FWD][node0].append( node1 )
        else:
            self._edges[self._curr_ssid][edge_type][Graph.FWD][node0] = [node1]
        # add rev edge from n1 to n0
        if node1 in self._edges[self._curr_ssid][edge_type][Graph.REV]:
            self._edges[self._curr_ssid][edge_type][Graph.REV][node1].append( node0 )
        else:
            self._edges[self._curr_ssid][edge_type][Graph.REV][node1] = [node0]
    # ----------------------------------------------------------------------------------------------
    def has_edge(self, node0, node1, edge_type, ssid = None):
        """
        Return True if an edge from n0 to n1 exists in the graph.

        :param n0: the name of the start node
        :param n1: the name of the end node
        :param edge_type: the edge type
        :return: True if the edge exists, false otherwise..
        """
        if not node0 in self._nodes and node1 in self._nodes:
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # check if edge exists
        if not node0 in self._edges[ssid][edge_type][Graph.FWD]:
            return False
        return node1 in self._edges[ssid][edge_type][Graph.FWD][node0]
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
        self._edges[self._curr_ssid][edge_type] = dict()
        self._edges[self._curr_ssid][edge_type][Graph.FWD] = OrderedDict()
        self._edges[self._curr_ssid][edge_type][Graph.REV] = OrderedDict()
    # ----------------------------------------------------------------------------------------------
    def has_edge_type(self, edge_type):
        """
        Return True if the edge type exists in the graph.

        :param edge_type: the edge type
        :return: True if the edge type exists, false otherwise.
        """
        return edge_type in self._edge_types
    # ----------------------------------------------------------------------------------------------
    def successor(self, node, edge_type, ssid = None):
        """
        Get one successor of a node in the graph.
        The node 'n' is linked to a successor by a forward edge of type 'edge_type'.

        If there are no successors, then None is returned.

        If the edge type ends in 'm' (i.e. 'm2m' or 'o2m'), then an error is thrown.

        :param n: the name of the node from which to find successors
        :param edge_type: the edge type
        :return: A single node name.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        if x2x in [Graph.M2M, Graph.O2M]:
            raise Exception('Edge type has multiple successors.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get successor
        if node not in self._edges[ssid][edge_type][Graph.FWD]:
            return None
        if len(self._edges[ssid][edge_type][Graph.FWD][node]) == 0:
            return None
        return self._edges[ssid][edge_type][Graph.FWD][node][0]
    # ----------------------------------------------------------------------------------------------
    def successors(self, node, edge_type, ssid = None):
        """
        Get multiple successors of a node in the graph.
        The node 'n' is linked to each successor by a forward edge of type 'edge_type'.

        If there are no successors, then an empty list is returned.

        If the edge type ends in 'o' (i.e. 'm2o' or 'o2o'), then an error is thrown.

        :param n: the name of the node from which to find successors
        :param edge_type: the edge type
        :return: A list of nodes names.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        if x2x in [Graph.M2O, Graph.O2O]:
            raise Exception('Edge type has one successor.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get successors
        if node not in self._edges[ssid][edge_type][Graph.FWD]:
            return []
        return self._edges[ssid][edge_type][Graph.FWD][node]
# ----------------------------------------------------------------------------------------------
    def predecessor(self, node, edge_type, ssid = None):
        """
        Get one predecessors of a node in the graph.
        The node 'n' is linked to a predecessor by a reverse edge of type 'edge_type'.

        If there are no predecessors, then None returned.

        If the edge type starts with 'm' (i.e. 'm2m' or 'm2o'), then an error is thrown.

        :param n: the name of the node from which to find predecessors
        :param edge_type: the edge type
        :return: A single node name.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        if x2x in [Graph.M2M, Graph.M2O]:
            raise Exception('Edge type has multiple predecessors.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get the predecessor
        if node not in self._edges[ssid][edge_type][Graph.REV]:
            return None
        if len(self._edges[ssid][edge_type][Graph.REV][node]) == 0:
            return None
        return self._edges[ssid][edge_type][Graph.REV][node][0]
    # ----------------------------------------------------------------------------------------------
    def predecessors(self, node, edge_type, ssid = None):
        """
        Get multiple predecessors of a node in the graph.
        The node 'n' is linked to each predecessor by a reverse edge of type 'edge_type'.

        If there are no predecessors, then an empty list is returned.

        If the edge type starts with 'o' (i.e. 'o2o' or 'o2m'), then an error is thrown.

        :param n: the name of the node from which to find predecessors
        :param edge_type: the edge type
        :return: A list of nodes names, or a single node name.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get the edge x2x
        x2x = self._edge_types[edge_type]
        if x2x in [Graph.O2M, Graph.O2O]:
            raise Exception('Edge type has one predecessor.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # get predecessors
        if node not in self._edges[ssid][edge_type][Graph.REV]:
            return []
        return self._edges[ssid][edge_type][Graph.REV][node]
    # ----------------------------------------------------------------------------------------------
    def degree_in(self, node, edge_type, ssid = None):
        """
        Count the the number of incoming edges.
        The 'in degree' is the number of reverse edges of type 'ent_type' linked to node 'n'.

        :param n: the name of the node for which to count incoming edges
        :param edge_type: the edge type
        :return: An integer, the number of incoming edges.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # calc reverse degree
        if node not in self._edges[ssid][edge_type][Graph.REV]:
            return 0
        return len(self._edges[ssid][edge_type][Graph.REV][node])
    # ----------------------------------------------------------------------------------------------
    def degree_out(self, node, edge_type, ssid = None):
        """
        Count the the number of outgoing edges.
        The 'out degree' is the number of forward edges of type 'ent_type' linked to node 'n'.

        :param n: the name of the node for which to count outgoing edges
        :param edge_type: the edge type
        :return: An integer, the number of outgoing edges.
        """        
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edge_types :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid == None: ssid = self._curr_ssid
        # calc forward degree
        if node not in self._edges[ssid][edge_type][Graph.FWD]:
            return 0
        return len(self._edges[ssid][edge_type][Graph.FWD][node])
    # ----------------------------------------------------------------------------------------------
    def degree(self, node, edge_type):
        """
        Count the the total number of incoming and outgoing edges.

        :param n: the name of the node for which to count edges
        :param edge_type: the edge type
        :return: An integer, the number of edges.
        """
        # return result
        return self.degree_in(node, edge_type) + self.degree_out(node, edge_type)
    # ----------------------------------------------------------------------------------------------
    def snapshot(self):
        """
        Takes a snapshot of the current set of edges in the graph.

        :return: An integer, the ssid of the current snapshot.
        """
        # return result
        prev_ssid = self._curr_ssid
        self._curr_ssid += 1
        self._edges[self._curr_ssid] = copy.deepcopy(self._edges[prev_ssid])
        return prev_ssid
# ==================================================================================================
# END GRAPH CLASS
# ==================================================================================================

