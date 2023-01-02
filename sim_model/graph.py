from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals
from collections import OrderedDict
import copy
# ==================================================================================================
# GRAPH CLASS
# ==================================================================================================
class Graph(object):
    # the graph is created using a sigle dict of nodes and multiple dicts of edges
    # 
    # for each edge type, there are two dicts, forward and reverse
    FWD = 0
    REV = 1
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self):
        # nodes
        self._nodes = OrderedDict() # key is node name, value is dict of properties
        # edge_types, key is edge_type, value is boolean
        self._edges_reversed = dict() 
        # edges, nested dictionaries four levels deep
        # first level is the snapshot dict, key is the ssid, value is an OrderedDict
        # second level for each ssid, key is the edge_type, value is an dict
        # third level for each edge type, key is FWD or REV, value is OrderedDict
        # fourth level, for each edge_type, key is a start node, value is a list of end nodes
        self._edges = dict()
        # init snapshot 0
        self._edges[0] = OrderedDict() #TODO does this need to be ordered?
        self._curr_ssid = 0
    # ==============================================================================================
    # METHODS
    # ==============================================================================================
    def add_node(self, node):
        """
        Add a node to the graph. Throws an error if the node already exists.

        :param node: (str) The name of the node.
        :return: No value.
        """
        if node in self._nodes:
            raise Exception('Node already exists.')
        self._nodes[node] = dict()
    # ----------------------------------------------------------------------------------------------
    def set_node_prop(self, node, prop_name, prop_value):
        """
        Set the value of a property of a node. 
        Throws an error if the node does not exist.

        :param node: (str) The name of the node.
        :param prop_name: (str) The name of the property.
        :param prop_value (any) The value of the property.
        :return: No value
        """
        if not node in self._nodes:
            raise Exception('Node does not exist.')
        self._nodes[node][prop_name] = prop_value
    # ----------------------------------------------------------------------------------------------
    def get_node_prop(self, node, prop_name):
        """
        Get the value of a property of a node . 
        Throws an error if the node does not exist.

        :param node: (string) The name of the node.
        :param prop_name: (string) The name of the property.
        :return: (any) The value of the property.
        """
        if not node in self._nodes:
            raise Exception('Node does not exist.')
        return self._nodes[node][prop_name]
    # ----------------------------------------------------------------------------------------------
    def get_node_prop_names(self, node):
        """
        Get the names of all the properties of a node in the graph. 
        Throws an error if the node does not exist.

        :param node: (string) The name of the node.
        :return: (string[]) A list of property names.
        """
        if not node in self._nodes:
            raise Exception('Node does not exist.')
        return list(self._nodes[node].keys())
    # ----------------------------------------------------------------------------------------------
    def get_nodes(self):
        """
        Get a list of all nodes.

        :return: (str[]) A list of node names.
        """        
        # get the nodes
        return list(self._nodes.keys())
    # ----------------------------------------------------------------------------------------------
    def get_nodes_with_out_edge(self, edge_type, ssid = None):
        """
        Get a list of nodes that have an outgoing edge of type edge_type.

        :param edge_type: (str) The edge type.
        :return: (str[]) A list of node names.
        """        
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # get the nodes
        return list(self._edges[ssid][edge_type][Graph.FWD].keys())
    # ----------------------------------------------------------------------------------------------
    def get_nodes_with_in_edge(self, edge_type, ssid = None):
        """
        Get a list of nodes that have an incoming edge of type edge_type.

        :param edge_type: (str) The edge type.
        :return: (str[]) A list of node names.
        """        
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # get the nodes
        return list(self._edges[ssid][edge_type][Graph.REV].keys())
    # ----------------------------------------------------------------------------------------------
    def has_node(self, node):
        """
        Return True if the node n exists in the graph.

        :param node: (string) The name of the node.
        :return: (bool) True or False.
        """
        return node in self._nodes
    # ----------------------------------------------------------------------------------------------
    def add_edge(self, node0, node1, edge_type, ssid = None):
        """
        Add an edge to the graph, from node 0 to node 1.

        :param node0: (str) The name of the start node.
        :param node1: (str) The name of the end node.
        :param edge_type: (str) The edge type.
        :return: No value.
        """
        if not node0 in self._nodes and node1 in self._nodes:
            raise Exception('Node does not exist.')
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # get the edges
        if edge_type not in self._edges[ssid]:
            edges = dict()
            edges[Graph.FWD] = OrderedDict()
            if (self._edges_reversed[edge_type]):
                edges[Graph.REV] = OrderedDict()
            self._edges.get(ssid)[edge_type] = edges
        edges = self._edges[ssid][edge_type]
        # =====
        # Prior to 3.7 sets in python do not maintain order.
        # We can use the keys in an ordered dict as an ordered set.
        # We set the value to None.
        # =====
        # add edge from node0 to node1
        edge_fwd = self._edges[ssid][edge_type][Graph.FWD]
        if node0 not in edge_fwd:
            edge_fwd[node0] = OrderedDict() # ORDERED DICT
        edge_fwd[node0][node1] = None # ADD TO ORDERED DICT
        
        # add rev edge from node1 to node0
        if self._edges_reversed[edge_type]:
            edge_rev = self._edges[ssid][edge_type][Graph.REV]
            if node1 not in edge_rev:
                edge_rev[node1] = OrderedDict() # ORDERED DICT
            edge_rev[node1][node0] = None # ADD TO ORDERED DICT
    # ----------------------------------------------------------------------------------------------
    def del_edge(self, node0, node1, edge_type, ssid = None):
        """
        Delete the edge from node0 to node1.
        If `node0` is null, then all edges ending at `node1` will be deleted.
        If `node1` is null, then all edges starting at `node0` will be deleted.
        If the edge does not exists, then no error is thrown. 

        :param node0: (str) The name of the start node.
        :param node1: (str) The name of the end node.
        :param edge_type: (str) The edge type.
        :return: No value.
        """
        # error check
        if not edge_type in self._edges_reversed:
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid 
        rev = self._edges_reversed[edge_type]
        # check there are edges of edge)type
        if edge_type not in self._edges[ssid]:
            return
        # get edges
        edges = self._edges[ssid][edge_type]
        # None cases, del all edges which end at node1
        if node0 is None:
            if not rev:
                raise Exception('Edge type "' + edge_type + '" does not have reverse edges.')
            if node1 in edges[Graph.REV]:
                for node in edges[Graph.REV][node1]:
                    edges[Graph.FWD][node].pop(node1)
                edges[Graph.REV][node1].clear()
            return
        # None cases, del all edges which start at node0
        if node1 is None:
            if node0 in edges[Graph.FWD]:
                if rev:
                    for node in edges[Graph.FWD][node0]:
                        edges[Graph.REV][node].pop(node0)
                edges[Graph.FWD][node0].clear()
            return
        # error check
        if node0 not in self._nodes or node1 not in self._nodes:
            raise Exception('Node does not exist: ' + str(node0) + ', ' + str(node1) + '.')
        if (node0 == node1) :
            raise Exception('Nodes cannot be the same.')
        # check if edge_type has any edges
        if edge_type not in self._edges[ssid]:
            return
        # if no edge, silently return
        if node0 not in edges[Graph.FWD] or node1 not in edges[Graph.FWD][node0]:
            return
        # del fwd edge from n0 to n1
        edges[Graph.FWD][node0].pop(node1)
        # del rev edge from n1 to n0
        if (rev) :
            edges[Graph.REV][node1].pop(node0)
    # ----------------------------------------------------------------------------------------------
    def has_edge(self, node0, node1, edge_type, ssid = None):
        """
        Return True if an edge from node0 to node1 exists in the graph.

        :param node0: (str) The name of the start node.
        :param node1: (str) The name of the end node.
        :param edge_type: (str) The edge type.
        :return: (bool) True if the edge exists, false otherwise.
        """
        if not node0 in self._nodes and node1 in self._nodes:
            raise Exception('Node does not exist.')
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # check if no edges of edge_type
        if edge_type not in self._edges[ssid]:
            return False
        # get edges
        edges_fwd = self._edges[ssid][edge_type][Graph.FWD]
        # check if edge exists
        if node0 not in edges_fwd:
            return False
        return node1 in edges_fwd[node0]
    # ----------------------------------------------------------------------------------------------
    def add_edge_type(self, edge_type, rev, ssid = None):
        """
        Add an edge type to the graph.

        :param edge_type: (str) The edge type.
        :param rev: (bool) If True, reverse edges are geenrated.
        :return: No value.
        """
        if edge_type in self._edges_reversed:
            raise Exception('Edge type already exists.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # add edge type
        self._edges_reversed[edge_type] = rev
        # self._edges[ssid][edge_type] = dict()
    # ----------------------------------------------------------------------------------------------
    def has_edge_type(self, edge_type):
        """
        Return True if the edge type exists in the graph.

        :param edge_type: (str) The edge type.
        :return: (bool) True if the edge type exists, false otherwise.
        """
        return edge_type in self._edges_reversed
    # ----------------------------------------------------------------------------------------------
    def successors(self, node, edge_type, ssid = None):
        """
        Get multiple successors of a node in the graph.
        The 'node' is linked to each successor by a forward edge of type 'edge_type'.

        If there are no successors, then an empty list is returned.

        :param node: (str) The name of the node from which to find successors.
        :param edge_type: (str) The edge type.
        :return: (str[]) A list of nodes names.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # check if no edges of edge_type
        if edge_type not in self._edges[ssid]:
            return []
        # get edges
        edges = self._edges[ssid][edge_type]
        # get successors
        if node not in edges[Graph.FWD]:
            return []
        return list(edges[Graph.FWD][node])
    # ----------------------------------------------------------------------------------------------
    def predecessors(self, node, edge_type, ssid = None):
        """
        Get multiple predecessors of a node in the graph.
        The node 'n' is linked to each predecessor by a reverse edge of type 'edge_type'.

        If there are no predecessors, then an empty list is returned.

        If the edge type starts with 'o' (i.e. 'o2o' or 'o2m'), then an error is thrown.

        :param node: (str) The name of the node from which to find predecessors.
        :param edge_type: (str) The edge type.
        :return: (str[]) A list of nodes names, or a single node name.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        if not self._edges_reversed[edge_type] :
            raise Exception('Edge types "' + edge_type + '" does not have reverse edges.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # check if no edges of edge_type
        if edge_type not in self._edges[ssid]:
            return []
        # get edges
        edges = self._edges[ssid][edge_type]
        # get predecessors
        if node not in edges[Graph.REV]:
            return []
        return list(edges[Graph.REV][node])
    # ----------------------------------------------------------------------------------------------
    def set_successors(self, node0, nodes1, edge_type, ssid = None):
        """
        Advanced low level method - this can break graph consistency. Creates multiple edges by
        manually specifying the successors of a node. An existing successors will be overwritten. If
        this edge_type has reverse edges, then care needs to be taken to also update the
        predecessors.

        :param node0: (str) The name of the start node
        :param nodes1: (str) A list of names of sucessor nodes.
        :param edge_type: (str) The edge type.
        :return: No value.
        """
        if node0 not in self._nodes:
            raise Exception('Node does not exist: ' + node0 + '.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # get successors
        if edge_type not in self._edges[ssid]:
            edges = dict()
            edges[Graph.FWD] = OrderedDict()
            if self._edges_reversed[edge_type]:
                edges[Graph.REV] = OrderedDict()
            self._edges[ssid][edge_type] = edges
        # get edges
        edges = self._edges[ssid][edge_type]
        # set successors
        edges[Graph.FWD][node0].clear()
        for node1 in nodes1:
            edges[Graph.FWD][node0][node1] = None # ORDERED SET
    # ----------------------------------------------------------------------------------------------
    def set_predecessors(self, node1, nodes0, edge_type, ssid = None):
        """
        Advanced low level method - this can break graph consistency. Creates multiple edges by
        manually specifying the successors of a node. An existing successors will be overwritten. If
        this edge_type has reverse edges, then care needs to be taken to also update the
        predecessors.

        :param node1: (str) The name of the end node
        :param nodes0: (str) A list of names of predecessor nodes.
        :param edge_type: (str) The edge type.
        :return: No value.
        """
        if node1 not in self._nodes:
            raise Exception('Node does not exist: ' + node1 + '.')
        if not self._edges_reversed.get(edge_type):
            raise Exception('Edge types "' + edge_type + '" does not have reverse edges.');
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # check if edges of edge_type exist
        if edge_type not in self._edges[ssid]:
            edges = dict()
            edges[Graph.FWD] = OrderedDict()
            if self._edges_reversed.get(edge_type):
                edges[Graph.REV] = OrderedDict()
            self._edges[ssid][edge_type] = edges
        # get edges
        edges = self._edges[ssid][edge_type]
        # set predecessors
        edges[Graph.REV][node1].clear()
        for node0 in nodes0:
            edges[Graph.REV][node1][node0] = None # ORDERED SET
    # ----------------------------------------------------------------------------------------------
    def degree_in(self, node, edge_type, ssid = None):
        """
        Count the the number of incoming edges.
        The 'in degree' is the number of reverse edges of type 'ent_type' linked to node 'n'.

        :param node: (str) The name of the node for which to count incoming edges.
        :param edge_type: (str) The edge type.
        :return: (int) The number of incoming edges.
        """
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        if not self._edges_reversed[edge_type] :
            raise Exception('Edge types "' + edge_type + '" does not have reverse edges.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # check if no edges of edge_type
        if edge_type not in self._edges[ssid]:
            return 0
        # get edges
        edges = self._edges[ssid][edge_type]
        # calc reverse degree
        if node not in edges[Graph.REV]:
            return 0
        return len(edges[Graph.REV][node])
    # ----------------------------------------------------------------------------------------------
    def degree_out(self, node, edge_type, ssid = None):
        """
        Count the the number of outgoing edges.
        The 'out degree' is the number of forward edges of type 'ent_type' linked to node 'n'.

        :param node: (str) The name of the node for which to count outgoing edges
        :param edge_type: (str) The edge type.
        :return: (int) The number of outgoing edges.
        """        
        if not node in self._nodes :
            raise Exception('Node does not exist.')
        if not edge_type in self._edges_reversed :
            raise Exception('Edge type does not exist.')
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # check if no edges of edge_type
        if edge_type not in self._edges[ssid]:
            return 0
        # get edges
        edges = self._edges[ssid][edge_type]
        # calc forward degree
        if node not in edges[Graph.FWD]:
            return 0
        return len(edges[Graph.FWD][node])
    # ----------------------------------------------------------------------------------------------
    def degree(self, node, edge_type):
        """
        Count the the total number of incoming and outgoing edges.

        :param node: (str) The name of the node for which to count edges
        :param edge_type: (str) The edge type.
        :return: (int) The number of edges.
        """
        # return result
        return self.degree_in(node, edge_type) + self.degree_out(node, edge_type)
    # ----------------------------------------------------------------------------------------------
    def new_snapshot(self, ssid = None):
        """
        Start a new snapshot of the edges .
        If `ssid` is None, the the new snapshot will be empty.

        :param: (int | None) The ID of an existing snapshot, or None.
        :return:(int) The ssid of the current snapshot.
        """
        self._curr_ssid += 1
        if ssid is None:
            # create a new empty snapshot
            self._edges[self._curr_ssid] =  OrderedDict()
        else:
            # create a deep copy of the edge in an existing snapshot
            self._edges[self._curr_ssid] = copy.deepcopy(self._edges.get(ssid))
        return self._curr_ssid
    # ----------------------------------------------------------------------------------------------
    def get_active_snapshot(self):
        """
        Get the ID of the current active snapshot.

        :return: (int) The ssid of the current snapshot.
        """
        return self._curr_ssid
    # ----------------------------------------------------------------------------------------------
    def set_active_snapshot(self, ssid):
        """
        Set the ID of the current active snapshot.
        If the snapshot ID does not exist, an error will be thrown.

        :param ssid: (int) The ssid of an existing snapshot.
        :return: No value.
        """
        if not ssid in self._edges:
            raise Exception('Snapshot ID does not exist.');
        self._curr_ssid = ssid
    # ----------------------------------------------------------------------------------------------
    def clear_snapshot(self, ssid = None):
        """
        Clear all edges in the current active snapshot.

        :return: No value.
        """
        # get ssid
        if ssid is None: ssid = self._curr_ssid
        # create a new dict
        self._edges[self._curr_ssid] = OrderedDict()
        
    # ----------------------------------------------------------------------------------------------
    def to_string(self):
        """
        Creates a human-readable string representation of the graph, for debugging.

        :return: A string representation of the graph.
        """
        info = '\n\n=GRAPH=\n'
        info += 'NODES = ' + str(self.get_nodes()) + '\n'
        for ssid, edge_types_map in self._edges.items():
            info += 'SSID = ' + str(ssid) + '\n'
            for edge_type, fr_edges_map in edge_types_map.items():
                info += '    EDGE TYPE = ' + edge_type + ', reverse = ' + \
                    str(self._edges_reversed[edge_type]) + '\n'
                if Graph.FWD in fr_edges_map:
                    # fwd edges
                    for start, end in fr_edges_map[Graph.FWD].items():
                        info += '      FWD EDGE: ' + start + ' -> '
                        type_end = type(end)
                        if type_end is set or type_end is OrderedDict:
                            info += str(list(end)) + '\n'
                        else:
                            info += str(end) + '\n'
                    # rev edges
                    if self._edges_reversed[edge_type]:
                        for start, end in fr_edges_map[Graph.REV].items():
                            info += '      REV EDGE: '
                            type_end = type(end)
                            if type_end is set or type_end is OrderedDict:
                                info += str(list(end))
                            else:
                                info += end
                            info += ' <- ' + start + '\n'
        return info
# ==================================================================================================
# END GRAPH CLASS
# ==================================================================================================

