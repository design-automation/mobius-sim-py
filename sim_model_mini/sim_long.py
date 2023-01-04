from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals
from collections import OrderedDict
import copy
import json
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

# ==================================================================================================
# ENUMS
# ==================================================================================================
class ENT_TYPE(object):
    """
    An Enum class that defines a set of constants for different entity types. 
    These types are used when adding an attrbute to the model.
    """
    POSI = 'ps'
    VERT = '_v'
    EDGE = '_e'
    WIRE = '_w'
    TRI = '_t'
    POINT = 'pt'
    PLINE = 'pl'
    PGON = 'pg'
    COLL = 'co'
    COLL_PRED = 'cp'
    COLL_SUCC = 'cs'
    MODEL = 'mo'
# --------------------------------------------------------------------------------------------------
class VERT_TYPE(object):
    """
    An Enum class that defines three vertex types
    """
    PLINE = 'pl'
    PGON = 'pg'
    PGON_HOLE = 'pgh'
# --------------------------------------------------------------------------------------------------
class DATA_TYPE(object):
    """
    An Enum class that defines data types for attributes.
    """
    NUM = 'number'
    STR =  'string'
    BOOL =  'boolean'
    LIST =  'list'
    DICT =  'dict'
# --------------------------------------------------------------------------------------------------
class COMPARATOR(object):
    """
    An Enum class that defines operators that can be used in a filter.
    """
    IS_EQUAL = '=='
    IS_NOT_EQUAL = '!='
    IS_GREATER_OR_EQUAL = '>='
    IS_LESS_OR_EQUAL = '<='
    IS_GREATER = '>'
    IS_LESS = '<'
# ==================================================================================================
# GRAPH NAMES
# ==================================================================================================
# Node in the graph that links to all ents
_GR_ENTS_NODE = {
    ENT_TYPE.POSI: '_ents_posis',
    ENT_TYPE.VERT: '_ents_verts',
    ENT_TYPE.EDGE: '_ents_edges',
    ENT_TYPE.WIRE: '_ents_wires',
    ENT_TYPE.TRI:  '_ents_tris',
    ENT_TYPE.POINT: '_ents_points',
    ENT_TYPE.PLINE: '_ents_plines',
    ENT_TYPE.PGON: '_ents_pgons',
    ENT_TYPE.COLL: '_ents_colls',
}
# --------------------------------------------------------------------------------------------------
# node in the graph that links to all attribs
_GR_ATTRIBS_NODE = {
    ENT_TYPE.POSI: '_atts_posis',
    ENT_TYPE.VERT: '_atts_verts',
    ENT_TYPE.EDGE: '_atts_edges',
    ENT_TYPE.WIRE: '_atts_wires',
    ENT_TYPE.POINT: '_atts_points',
    ENT_TYPE.PLINE: '_atts_plines',
    ENT_TYPE.PGON: '_atts_pgons',
    ENT_TYPE.COLL: '_atts_colls',
}
# --------------------------------------------------------------------------------------------------
_GR_XYZ_NODE = '_att_ps_xyz';
# --------------------------------------------------------------------------------------------------
# types of edges in the graph
class _GR_EDGE_TYPE(object):
    ENT = 'entity'
    ATT =  'attrib'
    META = 'meta'
    TRI = 'tri'
# ==================================================================================================
# ENT SEQUENCES
# ==================================================================================================
_ENT_SEQ = {
    ENT_TYPE.POSI:  0, # {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.VERT:  1, # {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.EDGE:  2, # {'idx': 2, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.WIRE:  3, # {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.POINT: 4, # {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PLINE: 4, # {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PGON:  4, # {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL:  6, # {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PT_PO = {
    ENT_TYPE.POSI:  0, # {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.VERT:  1, # {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, #  TODO remove
    ENT_TYPE.POINT: 2, # {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL:  6, # {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PL_PO = {
    ENT_TYPE.POSI:  0, # {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.VERT:  1, # {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.EDGE:  2, # {'idx': 2, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.WIRE:  3, # {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PLINE: 4, # {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.COLL:  6, # {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PG_PO = {
    ENT_TYPE.POSI: 0, # {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.VERT: 1, # {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.EDGE: 2, # {'idx': 2, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.WIRE: 3, # {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PGON: 4, # {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL: 6, # {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
# _ENT_SEQ_CO_PG_TRI_PO = {
#     ENT_TYPE.POSI: {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
#     ENT_TYPE.VERT: {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.TRI},
#     ENT_TYPE.TRI:  {'idx': 2, 'succ': _GR_EDGE_TYPE.TRI,    'pred': _GR_EDGE_TYPE.TRI},
#     ENT_TYPE.PGON: {'idx': 3, 'succ': _GR_EDGE_TYPE.TRI,    'pred': _GR_EDGE_TYPE.ENT},
#     ENT_TYPE.COLL: {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
# }
# ==================================================================================================
# ENT SETS
# ==================================================================================================
# ENT_TYPES FOR COLLECTIONS
_COLL_ENT_TYPES = {
    ENT_TYPE.POINT, 
    ENT_TYPE.PLINE, 
    ENT_TYPE.PGON, 
    ENT_TYPE.COLL
}
# --------------------------------------------------------------------------------------------------
#  ENT_TYPES FOR OBJECTS
_OBJ_ENT_TYPES = {
    ENT_TYPE.POINT, 
    ENT_TYPE.PLINE, 
    ENT_TYPE.PGON, 
}
# --------------------------------------------------------------------------------------------------
#  ENT_TYPES FOR TOPOLOGY
_TOPO_ENT_TYPES = {
    ENT_TYPE.VERT, 
    ENT_TYPE.EDGE, 
    ENT_TYPE.WIRE
}
# --------------------------------------------------------------------------------------------------
# ENT_TYPES
_ALL_ENT_TYPES = {
    ENT_TYPE.POSI,
    ENT_TYPE.VERT, 
    ENT_TYPE.EDGE, 
    ENT_TYPE.WIRE, 
    ENT_TYPE.POINT, 
    ENT_TYPE.PLINE, 
    ENT_TYPE.PGON, 
    ENT_TYPE.COLL
}
# ==================================================================================================
# SIM CLASS
# ==================================================================================================
class SIM(object):
    """
    A class for creating Spatial Information Models (SIM models).

    The model can contain three types of objects: points, polyline, and polygons.

    Objects are creating by specifing positions, which have XYZ coordinates.

    Objects can be groouped into collections. Collections can contain heterogeneous sets of points,
    polylines, polygons and other collections.

    Objects have sub-entities that define their topology. The three types of sub-entities are
    vertices, edges, and wires. Attributes can also be attached to these sub-emtities. 

    - Point objects contain just one vertex.
    - Polyline objects contain vertices, edges, and one wire.
    - Polygon objects cotain vertices, edges and multiple wires. The first wire specifies the 
      polygon boundary. Subsequent wires spcify the polygon holes.
    """
    """
    === NODES ===

    The nodes for entities are:
    
    - entity nodes
      - e.g. 'ps01', '_v123'
      - have a property, 'ent_type', e.g. 'ps', '_v'
      - vertices have an additional property, 'vert_type', can be 'pl', 'pg', 'pgh'

    - entity type nodes 
      - e.g. '_ents_posis', '_ents_verts'

    The nodes for attribs are:

    - attribute entity type nodes 
      - e.g.'_atts_pgons'

    - attribute name nodes 
      - e.g. '_att_pgons_area' (i.e. the attribute name is 'area')

    - _att_val nodes 
      - e.g. '[1,2,3]'
    
    === EDGES ===

    Edges of type 'entity':

    - ent -> sub_ents 
      - e.g. pg0 -> [_w0, _w1]
      - edge_type = 'entity'
      - many to many

    For each 'entity' forward edge, there is an equivalent reverse edge.

    Edges of type 'meta':

    - ent_type -> ents
      - e.g. pgons -> pg0
      - edge_type = 'meta'
      - one to many

    - ent_type_attribs -> att_ent_type_name 
      - e.g. pgons_attribs -> att_pgons_area
      - edge_type = 'meta'
      - one to many

    For 'meta' forward edges, there is __no__ reverse edge.

    Edges of type 'attrib':

    - attrib_val -> att_ent_type_name 
      - e.g. val_123 -> att_pgons_area
      - edge_type = 'attrib' 
      - many to one

    For each 'attrib' forward edge, there is an equivalent reverse edge.

    Edges with a type specific to the attribute:

    - ent -> attrib_val 
      - pg0 -> val_123
      - edge_type = att_ent_type_name e.g. '_att_pgons_area'
      - many to one

    For each attribute specific forward edge, there is an equivalent reverse edge.

    """

    # Triangulation is not yet implemented.

    # ==============================================================================================
    # CONSTRUCTOR FOR SIM CLASS
    # ==============================================================================================
    def __init__(self):
        """Constructor for creating a new empty model
        """
        # graph
        self.graph = Graph()

        # edge types
        self.graph.add_edge_type(_GR_EDGE_TYPE.ENT, True)
        self.graph.add_edge_type(_GR_EDGE_TYPE.ATT, True)
        self.graph.add_edge_type(_GR_EDGE_TYPE.META, False)
        self.graph.add_edge_type(_GR_EDGE_TYPE.TRI, True)

        # create nodes for ents (incl TRI)
        for ent_type in [ENT_TYPE.POSI, ENT_TYPE.VERT, ENT_TYPE.EDGE, ENT_TYPE.WIRE, ENT_TYPE.TRI, 
                ENT_TYPE.POINT, ENT_TYPE.PLINE, ENT_TYPE.PGON, ENT_TYPE.COLL]:
            self.graph.add_node( _GR_ENTS_NODE[ent_type] )

        # create nodes for attribs (not incl TRI)
        for ent_type in [ENT_TYPE.POSI, ENT_TYPE.VERT, ENT_TYPE.EDGE, ENT_TYPE.WIRE, 
                ENT_TYPE.POINT, ENT_TYPE.PLINE, ENT_TYPE.PGON, ENT_TYPE.COLL]:
            self.graph.add_node( _GR_ATTRIBS_NODE[ent_type] )

        # add xyz attrib
        self._graph_add_attrib(ENT_TYPE.POSI, 'xyz', DATA_TYPE.LIST)

        # add empty model attrbutes
        self.model_attribs = dict()

    # ==============================================================================================
    # CREATE NEW ENTITIES
    # ==============================================================================================
    def add_posi(self, xyz = None):
        """Add a position to the model, specifying the XYZ coordinates.

        :param xyz: The XYZ coordinates, a list of three numbers.
        :return: The ID of the new position.
        """
        posi = self._graph_add_ent(ENT_TYPE.POSI)
        if xyz is not None:
            self.set_posi_coords(posi, xyz)
        return posi
    # ----------------------------------------------------------------------------------------------
    def add_point(self, posi):
        """Add a point object to the model, specifying a single position.

        :param posi: A position ID.
        :return: The ID of the new point.
        """
        # TODO removed vertex
        vert = self._graph_add_ent(ENT_TYPE.VERT)
        point = self._graph_add_ent(ENT_TYPE.POINT)
        self.graph.add_edge(vert, posi, _GR_EDGE_TYPE.ENT)
        self.graph.add_edge(point, vert, _GR_EDGE_TYPE.ENT)
        return point
    # ----------------------------------------------------------------------------------------------
    def add_pline(self, posis, closed):
        """Add a polyline object to the model, specifying a list of positions.

        :param posis: A list of position IDs.
        :param closed: A boolean indicating if the polyline is closed or open.
        :return: The ID of the new polyline.
        """
        if len(posis) < 2:
            raise Exception('Too few positions for polyline.');
        # TODO removed wire
        # pline and wire
        pline = self._graph_add_ent(ENT_TYPE.PLINE)
        wire = self._graph_add_ent(ENT_TYPE.WIRE)
        self.graph.add_edge(pline, wire, _GR_EDGE_TYPE.ENT)
        # verts and edges
        self._add_edge_seq(posis, closed, VERT_TYPE.PLINE, wire)
        # return
        return pline
    # ----------------------------------------------------------------------------------------------
    def add_pgon(self, posis):
        """Add a polygon object to the model, specifying a list of positions.

        :param posis: A list of position IDs.
        :return: The ID of the new polygon.
        """
        posis = posis if type(posis[0]) is list else [posis]
        if len(posis[0]) < 3:
            raise Exception('Too few positions for polygon.')
        # pgon and wire
        pgon = self._graph_add_ent(ENT_TYPE.PGON)
        wire = self._graph_add_ent(ENT_TYPE.WIRE)
        self.graph.add_edge(pgon, wire, _GR_EDGE_TYPE.ENT)
        # verts and edges
        self._add_edge_seq(posis[0], True, VERT_TYPE.PGON, wire)
        # make holes
        for i in range(1, len(posis)):
            self.add_pgon_hole(pgon, posis[i])
        # triangulate
        # self.tri.triangulatePgon(pgon) TODO
        # return
        return pgon
    # ----------------------------------------------------------------------------------------------
    def add_pgon_hole(self, pgon, posis):
        """Create a hole in a polygon.

        :param pgon: The polygon ID.
        :param posis: A list of position IDs for the hole.
        :return: The ID of the new hole wire.
        """
        if len(posis) < 3:
            raise Exception('Too few positions for polygon hole.')
        # wire
        wire = self._graph_add_ent(ENT_TYPE.WIRE)
        self.graph.add_edge(pgon, wire, _GR_EDGE_TYPE.ENT)
        # verts and edges
        self._add_edge_seq(posis, True, VERT_TYPE.PGON_HOLE, wire)
        # triangulate
        # self.tri.triangulatePgon(pgon) TODO
        # return
        return wire
    # ----------------------------------------------------------------------------------------------
    def _add_edge_seq(self, posis, closed, vert_type, parent):
        """Add a sequnce of edges. Use by add_pgon(), add_pgon_hole(), add_pline().

        :param posis: The list of posis.
        :param closed: If true, then the last edge loops back to the first vertex.
        :param vert_type: The vertex type, see VERT_TYPE
        :param parent: The parent of the new edges. Wither a wire or a pline.
        """
        edges = []
        v0 = None
        v1 = None
        # v0
        v_start = self._graph_add_ent(ENT_TYPE.VERT)
        self.graph.set_node_prop(v_start, 'vert_type', vert_type)
        self.graph.add_edge(v_start, posis[0], _GR_EDGE_TYPE.ENT)
        v0 = v_start
        for i in range(1, len(posis)):
            # v1
            v1 = self._graph_add_ent(ENT_TYPE.VERT)
            self.graph.set_node_prop(v1, 'vert_type', vert_type)
            self.graph.add_edge(v1, posis[i], _GR_EDGE_TYPE.ENT)
            # edge
            edge = self._graph_add_ent(ENT_TYPE.EDGE)
            self.graph.add_edge(parent, edge, _GR_EDGE_TYPE.ENT)
            self.graph.add_edge(edge, v0, _GR_EDGE_TYPE.ENT)
            self.graph.add_edge(edge, v1, _GR_EDGE_TYPE.ENT)
            v0 = v1
            edges.append(edge)
        # last edge
        if closed:
            last_edge = self._graph_add_ent(ENT_TYPE.EDGE)
            self.graph.add_edge(parent, last_edge, _GR_EDGE_TYPE.ENT)
            self.graph.add_edge(last_edge, v1, _GR_EDGE_TYPE.ENT)
            self.graph.add_edge(last_edge, v_start, _GR_EDGE_TYPE.ENT)
            # re-order the predecessors of the start vertex
            # the order should be [last_edge, first_edge]
            self.graph.set_predecessors(v_start, [last_edge, edges[0]], _GR_EDGE_TYPE.ENT)
    # ----------------------------------------------------------------------------------------------
    def triangulate_pgon(self, pgon):
        """Triangulate a polygon.

        :param pgon: The polygon ID.
        :return: No value.
        """
        raise Exception('Not implements.')
    # ----------------------------------------------------------------------------------------------
    def copy_ents(self, ents, vec = None):
        """Make a copy of an list of entities. For objects, the object positions are also copied. For 
        collections, the contents of the collection is also copied. 
        TODO Raise error for deleted ents ???

        :param ents: A list of entity IDs.
        :param vec: Optional vector specifying the transplation of the positions.
        :return: A list of IDs of the copied entities.
        """
        raise Exception('Not implements.')
    # ----------------------------------------------------------------------------------------------
    def clone_ents(self, ents):
        """Triangulate a polygon.l.

        :param ents: A list of entity IDs.
        :return: A list of IDs of the cloned entities.
        """
        raise Exception('Not implements.')
    # ==============================================================================================
    # COLLECTIONS 
    # ==============================================================================================
    def add_coll(self):
        """Add a new empty collection to the model.

        :return: The ID of the collection.
        """
        return self._graph_add_ent(ENT_TYPE.COLL)
    # ----------------------------------------------------------------------------------------------
    def add_coll_ent(self, coll, ent):
        """Add an entity to an existing collection in the model.
        Collections can contain points, polylines, polygons, and other collections.
        Collections cannot contain positions, vertices, edges or wires.

        :param coll: The ID of the collection to which the entity will be added.
        :param ent: The ID of the entity to be added to the collection.
        :return: No value.
        """
        ent_type = self.graph.get_node_prop(ent, 'ent_type')
        if ent_type not in _COLL_ENT_TYPES:
            raise Exception('Invalid entitiy for collections.')
        self.graph.add_edge(coll, ent, _GR_EDGE_TYPE.ENT)
    # ----------------------------------------------------------------------------------------------
    def rem_coll_ent(self, coll, ent):
        """Remove an entity from an existing collection in the model.
        Collections can contain points, polylines, polygons, and other collections.
        If the entity is not in the collection, no error is thrown.

        :param coll: The ID of the collection from which the entity will be removed.
        :param ent: The ID of the entity to be removed from the collection.
        :return: No value.
        """
        self.graph.del_edge(coll, ent, _GR_EDGE_TYPE.ENT)
    # ==============================================================================================
    # ENTITY ATTRIBUTES
    # ==============================================================================================
    def add_attrib(self, ent_type, att_name, att_data_type):
        """Create a new attribute in the model, specifying the entity type, the attribute name, and
        the data type. Note that for each entity type, the attribute name must be a unique name.

        :param ent_type: The entity type for the attribute. (See ENT_TYPE)
        :param att_name: The name of the attribute to create. 
        :param att_data_type: The data type for the attribute values. (See DATA_TYPE)
        :return: No value.
        """
        att = self._graph_attrib_node_name(ent_type, att_name)
        if not self.graph.has_node(att):
            self._graph_add_attrib(ent_type, att_name, att_data_type)
        elif self.graph.get_node_prop(att, 'data_type') != att_data_type:
            raise Exception('Attribute already exists with different data type')
    # ----------------------------------------------------------------------------------------------
    def has_attrib(self, ent_type, att_name):
        """Returns true if an attribute exists with the specified entity type and name.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute. 
        :return: True is the attribute exists, false otherwise.
        """
        att = self._graph_attrib_node_name(ent_type, att_name)
        return self.graph.has_node(att)
    # ----------------------------------------------------------------------------------------------
    def get_attribs(self, ent_type):
        """Get a list of attribute names in the model, specifying the entity type.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :return: A list of attrib names.
        """
        return map(
            lambda att: self.graph.get_node_prop(att, 'name'), 
            self.graph.successors(
                _GR_ATTRIBS_NODE[ent_type],
                _GR_EDGE_TYPE.META
            )
        )
    # ----------------------------------------------------------------------------------------------
    def set_attrib_val(self, ent, att_name, att_value):
        """Set the value of an attribute, specifying the entity in the model, the attribute name and
        the attribute value. 
        
        Note that an attribute with the specified name must already exist in 
        the model. If the attribute does not exist, an exception will be thrown. In addition, the 
        attribute value and the data type for the attribute must match.

        :param ent: The ID of the entity.
        :param att_name: The name of the attribute.
        :param att_value: The attribute value to set.
        :return: No value.
        """
        ent_type = self.graph.get_node_prop(ent, 'ent_type')
        att_node = self._graph_attrib_node_name(ent_type, att_name)
        if ent_type != self.graph.get_node_prop(att_node, 'ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._check_type(att_value)
        if self.graph.get_node_prop(att_node, 'data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(att_value) +
                'The data type is a "' + data_type + '". ' + 
                'The data type should be a "' + self.graph.get_node_prop(att_node, 'data_type') + '".' )
        # get the name of the attribute value node
        att_val_node = self._graph_attrib_val_node_name(att_value, att_node)
        # make the att_val_node exists
        if not self.graph.has_node(att_val_node):
            # add the att_val_node
            self.graph.add_node(att_val_node)
            self.graph.set_node_prop(att_val_node, 'value', att_value)
        # add an edge from the att_val_node to the attrib: att_val -> att
        self.graph.add_edge(att_val_node, att_node, _GR_EDGE_TYPE.ATT)
        # add and edge from the ent to the att_val_node
        self.graph.del_edge(ent, None, att_node)
        # ent -> att_val, ent <- att_val
        self.graph.add_edge(ent, att_val_node, att_node)
    # ----------------------------------------------------------------------------------------------
    def get_attrib_val(self, ent, att_name):
        """Get an attribute value from an entity in the model, specifying the attribute name.
        If the entity has no value for that attribute, then `None` is returned.

        :param ent: The ID of the entity for which to get the attribute value.
        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        ent_type = self.graph.get_node_prop(ent, 'ent_type')
        att_node = self._graph_attrib_node_name(ent_type, att_name)
        succs = self.graph.successors(ent, att_node)
        if len(succs) == 0:
            return None
        return self.graph.get_node_prop(succs[0], 'value')
    # ----------------------------------------------------------------------------------------------
    def del_attrib_val(self, ent, att_name):
        """Delete an attribute value from an entity in the model, specifying the attribute name.
        TODO Raise error for deleted ents ???

        :param ent: The ID of the entity for which to get the attribute value
        :param att_name: The name of the attribute to delete.
        :return: No value.
        """
        ent_type = self.graph.get_node_prop(ent, 'ent_type')
        att_node = self._graph_attrib_node_name(ent_type, att_name)
        succs = self.graph.successors(ent, att_node)
        if len(succs) == 0:
            return
        self.graph.del_edge(ent, succs[0], att_node)
    # ----------------------------------------------------------------------------------------------
    def get_attrib_vals(self, ent_type, att_name):
        """Get a list of all the attribute values for the specified attribute.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute.
        :return: A list of all attribute values.
        """
        att_node = self._graph_attrib_node_name(ent_type, att_name)
        att_val_nodes = self.graph.predecessors(att_node, _GR_EDGE_TYPE.ATT)
        values = []
        for att_val_node in att_val_nodes:
            values.append(self.graph.get_node_prop(att_val_node, 'value'))
        return values
    # ----------------------------------------------------------------------------------------------
    def get_attrib_datatype(self, ent_type, att_name):
        """Get an attribute datatype, specifying the attribute entity type and attribute name.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        att_node = self._graph_attrib_node_name(ent_type, att_name)
        return self.graph.get_node_prop(att_node, 'data_type')
    # ----------------------------------------------------------------------------------------------
    def rename_attrib(self, ent_type, att_name, new_name):
        """Rename an attribute.

        :param ent_type: The entity type for the attribute. (See ENT_TYPE)
        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        old_att_node = self._graph_attrib_node_name(ent_type, att_name)
        att_data_type = self.graph.get_node_prop(old_att_node, 'data_type')
        new_att_node = self._graph_add_attrib(ent_type, new_name, att_data_type)
        for pred in self.graph.predecessors(old_att_node, _GR_EDGE_TYPE.ATT):
            self.graph.del_edge(pred, old_att_node, _GR_EDGE_TYPE.ATT)
            self.graph.add_edge(pred, new_att_node, _GR_EDGE_TYPE.ATT)
    # ==============================================================================================
    # MODEL ATTRIBUTES
    # ==============================================================================================
    def has_model_attrib(self, att_name):
        """Returns true if a model attribute exists with the specified name.

        :param att_name: The name of the attribute. 
        :return: True is the attribute exists, false otherwise.
        """
        return att_name in self.model_attribs
    # ----------------------------------------------------------------------------------------------
    def set_model_attrib_val(self, att_name, att_value):
        """Set an attribute value from the model, specifying a name and value. Model attributes are
        top level attributes that apply to the whole model. As such, they are not attached to any
        specific entities.

        :param att_name: The name of the attribute.
        :param att_value: The attribute value to set.
        :return: No value.
        """
        self.model_attribs[att_name] = att_value
    # ----------------------------------------------------------------------------------------------
    def get_model_attrib_val(self, att_name):
        """Get an attribute value from the model, specifying a name. Model attributes are
        top level attributes that apply to the whole model. As such, they are not attached to any
        specific entities.

        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        return self.model_attribs[att_name]
    # ----------------------------------------------------------------------------------------------
    def del_model_attrib_val(self, att_name):
        """Delete an attribute value from the model..

        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        del self.model_attribs[att_name]
    # ----------------------------------------------------------------------------------------------
    def get_model_attribs(self):
        """Get a list of attribute names from the model. Model attributes are
        top level attributes that apply to the whole model. As such, they are not attached to any
        specific entities.

        :return: A list of attribute names.
        """
        return self.model_attribs.keys()
    # ==============================================================================================
    # ENTITIES
    # ==============================================================================================
    def num_ents(self, ent_type):
        """Get the number of entities in the model of a specific type.  

        :param ent_type: The type of entity to search for in the model.
        :return: A number of entities of the specified type in the model.
        """
        return self.graph.degree_out(
            _GR_ENTS_NODE[ent_type], 
            _GR_EDGE_TYPE.META
        )
    # ----------------------------------------------------------------------------------------------
    def get_ents(self, target_ent_type, source_ents = None):
        """Get entities of a specific type. A list of entity IDs is returned.

        If source_ents is None, then all entities of the specified type in the model are returned.
        If there are no entities of that type in the model, then an empty list is returned. 

        If source_ents contains a list of entities, then entities will be extracted from the source
        ents. For example, if ent_type is 'posis' and 'source_ents' is a polyline and a polygon,
        then a list containing the positions used in the polyline and polygon are returned. 
        Similarly, if ent_type is 'pgons' and 'source_ents' is a list of positions,
        then a list of polygons is returned, of polygons that make use of the specified positions.

        :param target_ent_type: The type of entity to get from the model.
        :param source_ents: None, or a single entity ID or a list of entity IDs from which to get 
        the target entities.
        :return: A list of unique entity IDs.
        """
        if source_ents == None:
            return self.graph.successors(
                _GR_ENTS_NODE[target_ent_type], 
                _GR_EDGE_TYPE.META
            )
        # get ents from one ent
        if not type(source_ents) is list:
            return self._nav(target_ent_type, source_ents)
        # a list with multiple items
        ents_set = OrderedDict() # ordered set
        for source_ent in source_ents:
            for target_ent in self._nav(target_ent_type, source_ent):
                ents_set[target_ent] = None # ordered set
        return list(ents_set.keys())
    # ----------------------------------------------------------------------------------------------
    def _get_ent_seq(self, target_ent_type, source_ent_type):
            # if (target_ent_type == ENT_TYPE.TRI or source_ent_type == ENT_TYPE.TRI):
            #     return _ENT_SEQ_CO_PG_TRI_PO
            if (target_ent_type == ENT_TYPE.POINT or source_ent_type == ENT_TYPE.POINT):
                return _ENT_SEQ_CO_PT_PO
            elif (target_ent_type == ENT_TYPE.PLINE or source_ent_type == ENT_TYPE.PLINE):
                return _ENT_SEQ_CO_PL_PO
            elif (target_ent_type == ENT_TYPE.PGON or source_ent_type == ENT_TYPE.PGON):
                return _ENT_SEQ_CO_PG_PO
            return _ENT_SEQ
    # ----------------------------------------------------------------------------------------------
    # TODO more tests needed
    def _nav(self, target_ent_type, source_ent):
        source_ent_type = self.graph.get_node_prop(source_ent, 'ent_type')
        ent_seq = self._get_ent_seq(target_ent_type, source_ent_type)
        if source_ent_type == target_ent_type:
            if source_ent_type == ENT_TYPE.COLL:
                return [] # TODO nav colls of colls
            return [source_ent]
        dist = ent_seq[source_ent_type] - ent_seq[target_ent_type]
        if dist == 1:
            return self.graph.successors(source_ent, _GR_EDGE_TYPE.ENT)
        if dist == -1:
            return self.graph.predecessors(source_ent, _GR_EDGE_TYPE.ENT)
        # get the function to navigate
        navigate = self.graph.successors if dist > 0 else self.graph.predecessors
        ents = [source_ent]
        target_ents_set = OrderedDict() # to be used as an ordered set
        while ents:
            ent_set = OrderedDict() # to be used as an ordered set
            for ent in ents:
                for target_ent in navigate(ent, _GR_EDGE_TYPE.ENT):
                    this_ent_type = self.graph.get_node_prop(target_ent, 'ent_type')
                    if this_ent_type == target_ent_type:
                        target_ents_set[target_ent] = None # add to orderd set
                    elif this_ent_type in ent_seq:
                        if dist > 0 and ent_seq[this_ent_type] > ent_seq[target_ent_type]:
                            ent_set[target_ent] = None # add to orderd set
                        elif dist < 0 and ent_seq[this_ent_type] < ent_seq[target_ent_type]:
                            ent_set[target_ent] = None # add to orderd set
            ents = ent_set.keys()
        return list(target_ents_set.keys())


    # ----------------------------------------------------------------------------------------------
    def get_ent_posis(self, ent):
        """Get a position ID or list the position IDs for an entity.

        If the entity is a point, vertex, or position, then a single position is returned.
        If the entity is a polyline, a list of positions will be returned.
        For a closed polyline, the first and last positions will be the same.
        If the entity is a polygon, a nested list of positions is returned.
        If the entity is a collection, ... not mplemented

        :param point: An entity ID from which to get the position.
        :return: A list of position IDs. 
        """
        ent_type = self.graph.get_node_prop(ent, 'ent_type')
        if ent_type == ENT_TYPE.POSI:
            return ent
        elif ent_type == ENT_TYPE.VERT:
            return self.graph.successors(ent, _GR_EDGE_TYPE.ENT)[0]
        elif ent_type == ENT_TYPE.EDGE:
            verts = self.graph.successors(ent, _GR_EDGE_TYPE.ENT)
            return [self.graph.successors(vert, _GR_EDGE_TYPE.ENT)[0] for vert in verts]
        elif ent_type == ENT_TYPE.WIRE:
            edges = self.graph.successors(ent, _GR_EDGE_TYPE.ENT)
            verts = [self.graph.successors(edge, _GR_EDGE_TYPE.ENT)[0] for edge in edges]
            posis = [self.graph.successors(vert, _GR_EDGE_TYPE.ENT)[0] for vert in verts]
            last_vert = self.graph.successors(edges[-1], _GR_EDGE_TYPE.ENT)[1]
            last_posi = self.graph.successors(last_vert, _GR_EDGE_TYPE.ENT)[0]
            posis.append(last_posi)
            return posis
        elif ent_type == ENT_TYPE.POINT:
            vert = self.graph.successors(ent, _GR_EDGE_TYPE.ENT)[0]
            return self.graph.successors(vert, _GR_EDGE_TYPE.ENT)[0]
        elif ent_type == ENT_TYPE.PLINE:
            wire = self.graph.successors(ent, _GR_EDGE_TYPE.ENT)[0]
            edges = self.graph.successors(wire, _GR_EDGE_TYPE.ENT)
            verts = [self.graph.successors(edge, _GR_EDGE_TYPE.ENT)[0] for edge in edges]
            posis = [self.graph.successors(vert, _GR_EDGE_TYPE.ENT)[0] for vert in verts]
            last_vert = self.graph.successors(edges[-1], _GR_EDGE_TYPE.ENT)[1]
            last_posi = self.graph.successors(last_vert, _GR_EDGE_TYPE.ENT)[0]
            posis.append(last_posi)
            return posis
        elif ent_type == ENT_TYPE.PGON:
            posis = []
            for wire in self.graph.successors(ent, _GR_EDGE_TYPE.ENT):
                edges = self.graph.successors(wire, _GR_EDGE_TYPE.ENT)
                verts = [self.graph.successors(edge, _GR_EDGE_TYPE.ENT)[0] for edge in edges]
                wire_posis = [self.graph.successors(vert, _GR_EDGE_TYPE.ENT)[0] for vert in verts]
                posis.append(wire_posis)
            return posis
        elif ent_type == ENT_TYPE.COLL:
            raise Exception('Not implemented') # TODO

    # ----------------------------------------------------------------------------------------------
    def get_vert_coords(self, vert):
        """Get the XYZ coordinates of a vertex.

        :param posi: A vertex ID.
        :return: A list of three numbers, the XYZ coordinates.
        """
        posi = self.graph.successors(vert, _GR_EDGE_TYPE.ENT)[0]
        att_val_node = self.graph.successors(posi, _GR_XYZ_NODE)[0]
        return self.graph.get_node_prop(att_val_node, 'value')
    # ----------------------------------------------------------------------------------------------
    def get_posi_coords(self, posi):
        """Get the XYZ coordinates of a position.

        :param posi: A position ID.
        :return: A list of three numbers, the XYZ coordinates.
        """
        att_val_node = self.graph.successors(posi, _GR_XYZ_NODE)[0]
        return self.graph.get_node_prop(att_val_node, 'value')
# ----------------------------------------------------------------------------------------------
    def set_posi_coords(self, posi, xyz):
        """Set the XYZ coordinates of a position.

        :param posi: A position ID.
        :return: The ID of the attrib value node.
        """
        # get the name of the attribute value node
        att_val_node = self._graph_attrib_val_node_name(xyz, _GR_XYZ_NODE)
        # make sure that no node with the name already exists
        if (not self.graph.has_node(att_val_node)) :
            # add the attrib value node
            self.graph.add_node(att_val_node)
            self.graph.set_node_prop(att_val_node, 'value', xyz)
        # add an edge from the att_val_node to the attrib att_val -> att
        self.graph.add_edge(att_val_node, _GR_XYZ_NODE, _GR_EDGE_TYPE.ATT)
        # add and edge from the ent to the att_val_node: ent -> att_val, ent <- att_val
        self.graph.del_edge(posi, None, _GR_XYZ_NODE)
        self.graph.add_edge(posi, att_val_node, _GR_XYZ_NODE) 
        # return att_val_node
        return att_val_node
    # ==============================================================================================
    # QUERY
    # ==============================================================================================
    def is_pline_closed(self, pline):
        """Check if a polyline is open or closed.

        :param pline: A polyline ID.
        :return: True if closed, False if open.
        """
        edges = self.graph.successors(self.graph.successors(pline, _GR_EDGE_TYPE.ENT)[0], _GR_EDGE_TYPE.ENT)
        start = self.graph.successors(self.graph.successors(edges[0], _GR_EDGE_TYPE.ENT)[0], _GR_EDGE_TYPE.ENT)
        end = self.graph.successors(self.graph.successors(edges[-1], _GR_EDGE_TYPE.ENT)[1], _GR_EDGE_TYPE.ENT)
        return start == end
    # ----------------------------------------------------------------------------------------------
    def query(self, ent_type, att_name, comparator, att_val):
        """Find entities in the model that satisy the query condition.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute. 
        :param comparator: The operator to use to compare value, can be:
        '==', '!=', '<', '<=', '>', '>='.
        :param att_val: The value of the attribute. 
        :return: A list of entities.
        """
        #if attrib does not exist, throw error
        att_node = self._graph_attrib_node_name(ent_type, att_name)
        if not self.graph.has_node(att_node):
            raise Exception("The attribute does not exist: '" + att_name + "'.")
        # val == None
        if comparator == '==' and att_val == None:
            set_with_val = set(self.graph.get_nodes_with_out_edge(att_node))
            set_all = set(self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META))
            return list(set_all - set_with_val)
        # val != None
        if comparator == '!=' and att_val == None:
            return self.graph.get_nodes_with_out_edge(att_node)
        # val == att_val
        if comparator == '==':
            att_val_node = self._graph_attrib_val_node_name(att_val, att_node)
            if not self.graph.has_node(att_val_node):
                return []
            return self.graph.predecessors(att_val_node, att_node)
        # val != att_val
        if comparator == '!=':
            att_val_node = self._graph_attrib_val_node_name(att_val, att_node)
            if not self.graph.has_node(att_val_node):
                return self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META)
            ents_equal = self.graph.predecessors(att_val_node, att_node)
            if len(ents_equal) == 0:
                return self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META)
            set_equal = set(ents_equal)
            set_all = set(self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META))
            return list(set_all - set_equal)
        # other cases, data_type must be a number
        data_type = self.graph.get_node_prop(att_node, 'data_type')
        if data_type != DATA_TYPE.NUM:
            raise Exception("The '" + comparator +
                "' comparator cannot be used with attributes of type '" + data_type + "'.")
        result = []
        # val < att_val
        if comparator == '<':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att_node)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0], 'value') < att_val:
                    result.append(ent)
        # val <= att_val
        if comparator == '<=':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att_node)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0],'value') <= att_val:
                    result.append(ent)
        # val > att_val
        if comparator == '>':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att_node)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0], 'value') > att_val:
                    result.append(ent)
        # val >= att_val
        if comparator == '>=':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att_node)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0], 'value') >= att_val:
                    result.append(ent)
        # return list of entities
        # TODO handle queries sub-entities in lists and dicts
        return result
    # ==============================================================================================
    # PRIVATE GRAPH METHODS
    # ==============================================================================================
    # ----------------------------------------------------------------------------------------------
    def _graph_attrib_node_name(self, ent_type, att_name):
        """Create the name for an attrib node.
        It will be something like this: '_att_pgons_area'.
        """
        # TODO create a dict for fast lookup
        return '_att_' + ent_type + '_' + att_name
    # ----------------------------------------------------------------------------------------------
    def _graph_attrib_val_node_name(self, att_val, att_node):
        """Create the name for an attrib value node.
        If the attrib value is a number or string, then the value is returned.
        Otherwise, the value is converted into a string.
        For a list, it will be something like this: '[1,2,3]'.
        """
        data_type = self.graph.get_node_prop(att_node, 'data_type')
        if data_type == DATA_TYPE.NUM or data_type == DATA_TYPE.STR:
            return att_val
        return str(att_val)
    # ----------------------------------------------------------------------------------------------
    def _graph_add_ent(self, ent_type):
        """Add an entity node to the graph. 
        The entity can be a posi, vert, edge, wire, point, pline, pgon, coll.
        The entity node will have a name.
        The entity_type node wil be connected to the entity node.
        """
        ent_type_n = _GR_ENTS_NODE[ent_type]
        # create the node name, from prefix and then next count number
        ent_i = self.graph.degree_out(ent_type_n, edge_type = _GR_EDGE_TYPE.META)
        ent = ent_type + str(ent_i)
        # add a node with name `n`
        self.graph.add_node(ent)
        # set entity type, `posi`, `vert`, etc
        self.graph.set_node_prop(ent, 'ent_type', ent_type)  
        # create an edge from the node `ent_type` to the new node
        # the new edge is given the attribute `meta`
        # this edge is so that later the node can be found
        self.graph.add_edge(ent_type_n, ent, _GR_EDGE_TYPE.META)
        # return the name of the new entity node
        return ent
    # ----------------------------------------------------------------------------------------------
    def _graph_add_attrib(self, ent_type, name, data_type):
        """Add an attribute node to the graph.
        """
        # create the node name, from the entity type and attribute name
        att_node = self._graph_attrib_node_name(ent_type, name)
        # add the node to the graph
        self.graph.add_node(att_node)
        # set node properties
        self.graph.set_node_prop(att_node, 'ent_type', ent_type) # the `entity_type` for this attribute, `posi`, `vert`, etc
        self.graph.set_node_prop(att_node, 'name', name) # the name of the attribute
        self.graph.set_node_prop(att_node, 'data_type', data_type) # the data type of this attribute
        # create an edge from the node `ent_type_attribs` (e.g. posis_attribs) to the new attrib node
        # the edge type is `meta`
        self.graph.add_edge(_GR_ATTRIBS_NODE[ent_type], att_node, _GR_EDGE_TYPE.META)
        # create a new edge type for this attrib
        self.graph.add_edge_type(att_node, rev = True) # many to one
        # return the name of the new attrib node
        return att_node
    # ----------------------------------------------------------------------------------------------
    def _graph_add_attrib_val(self, att_node, att_val):
        """
        Add an attribute value node to the graph.

        :param att_node: the name of the attribute node
        :param value: the value of the attribute
        """
        # get the name of the attribute value node
        att_val_node = self._graph_attrib_val_node_name(att_val, att_node)
        # make sure that no node with the name already exists
        if not self.graph.has_node(att_val_node):
            # add the attrib value node
            # the new node has 1 property
            self.graph.add_node(att_val_node)
            self.graph.set_node_prop(att_val_node, 'value', att_val) # the node value
            # add an edge from the attrib value to the attrib
            self.graph.add_edge(att_val_node, att_node, _GR_EDGE_TYPE.ATT) # att_val -> att
        # return the name of the attrib value node
        return att_val_node
    # ==============================================================================================
    # UTILITY 
    # ==============================================================================================
    def _check_type(self, value):
        val_type = type(value)
        if val_type == int or val_type == float:
            return DATA_TYPE.NUM
        if val_type == str or val_type == unicode:
            return DATA_TYPE.STR
        if val_type == bool:
            return DATA_TYPE.BOOL
        if val_type == list:
            return DATA_TYPE.LIST
        if val_type == dict:
            return DATA_TYPE.DICT
        raise Exception('Data type is not recognised:', str(value), type(value))
    # ----------------------------------------------------------------------------------------------
    def to_string(self):
        """
        Creates a human-readable string representation of the graph, for debugging.

        :return: A string representation of the graph.
        """
        return self.graph.to_string()

# ==================================================================================================
# END SIM CLASS
# ==================================================================================================

# ==================================================================================================
# Functions for importing and exporting models in the SIM file format.
# ==================================================================================================
# ==================================================================================================
# EXPORT
# ==================================================================================================
def export_sim_data(sim_model):
    """Return JSON representing that data in the SIM model.
    
    :return: JSON data.
    """
    # get entities from graph
    posi_ents = sim_model.get_ents(ENT_TYPE.POSI)
    vert_ents = sim_model.get_ents(ENT_TYPE.VERT)
    edge_ents = sim_model.get_ents(ENT_TYPE.EDGE)
    wire_ents = sim_model.get_ents(ENT_TYPE.WIRE)
    point_ents = sim_model.get_ents(ENT_TYPE.POINT)
    pline_ents = sim_model.get_ents(ENT_TYPE.PLINE)
    pgon_ents = sim_model.get_ents(ENT_TYPE.PGON)
    coll_ents = sim_model.get_ents(ENT_TYPE.COLL)
    # create maps for entity name -> entity index
    posis_dict = dict( zip(posi_ents, range(len(posi_ents))) )
    verts_dict = dict( zip(vert_ents, range(len(vert_ents))) )
    edges_dict = dict( zip(edge_ents, range(len(edge_ents))) )
    wires_dict = dict( zip(wire_ents, range(len(wire_ents))) )
    points_dict = dict( zip(point_ents, range(len(point_ents))) )
    plines_dict = dict( zip(pline_ents, range(len(pline_ents))) )
    pgons_dict = dict( zip(pgon_ents, range(len(pgon_ents))) )
    colls_dict = dict( zip(coll_ents, range(len(coll_ents))) )
    # create the geometry data
    geometry = {
        'num_posis': sim_model.num_ents(ENT_TYPE.POSI),
        'points': [],
        'plines': [],
        'pgons': [],
        'coll_points': [],
        'coll_plines': [],
        'coll_pgons':  [],
        'coll_colls': []
    }
    for point_ent in point_ents:
        posi_i = sim_model.get_ent_posis(point_ent)
        geometry['points'].append(posis_dict[posi_i])
    for pline_ent in pline_ents:
        posis_i = sim_model.get_ent_posis(pline_ent)
        geometry['plines'].append([posis_dict[posi_i] for posi_i in posis_i])
    for pgon_ent in pgon_ents:
        wires_posis_i = sim_model.get_ent_posis(pgon_ent)
        geometry['pgons'].append([[posis_dict[posi_i] for posi_i in posis_i] for posis_i in wires_posis_i])
    for coll_ent in coll_ents:
        # points
        coll_points = sim_model.get_ents(ENT_TYPE.POINT, coll_ent)
        geometry['coll_points'].append([points_dict[point] for point in coll_points])
        # plines
        coll_plines = sim_model.get_ents(ENT_TYPE.PLINE, coll_ent)
        geometry['coll_plines'].append([plines_dict[pline] for pline in coll_plines])
        # pgons
        coll_pgons = sim_model.get_ents(ENT_TYPE.PGON, coll_ent)
        geometry['coll_pgons'].append([pgons_dict[pgon] for pgon in coll_pgons])
        # colls
        coll_colls = sim_model.get_ents(ENT_TYPE.COLL, coll_ent)
        geometry['coll_colls'].append([colls_dict[coll] for coll in coll_colls])
    # create the attribute data
    def _attribData(ent_type, ent_dict):
        attribs_data = []
        for att_name in sim_model.get_attribs(ent_type):
            data = dict()
            data['name'] = att_name
            data['data_type'] = sim_model.get_attrib_datatype(ent_type, att_name)
            data['values'] = []
            data['entities'] = []
            for att_val in sim_model.get_attrib_vals(ent_type, att_name):
                data['values'].append(att_val)
                ents = sim_model.query(ent_type, att_name, '==', att_val)
                ents_i = [ent_dict[ent] for ent in ents]
                data['entities'].append(ents_i)
            attribs_data.append(data)
        return attribs_data
    attributes = {
        'posis': _attribData(ENT_TYPE.POSI, posis_dict),
        'verts': _attribData(ENT_TYPE.VERT, verts_dict),
        'edges': _attribData(ENT_TYPE.EDGE, edges_dict),
        'wires': _attribData(ENT_TYPE.WIRE, wires_dict),
        'points': _attribData(ENT_TYPE.POINT, points_dict),
        'plines': _attribData(ENT_TYPE.PLINE, plines_dict),
        'pgons': _attribData(ENT_TYPE.PGON, pgons_dict),
        'colls': _attribData(ENT_TYPE.COLL, colls_dict),
        'model': [
            [att_name, sim_model.get_model_attrib_val(att_name)] 
            for att_name in sim_model.get_model_attribs()
        ]
    }
    # create the json
    data = {
        'type': 'SIM',
        'version': '0.1',
        'geometry': geometry,
        'attributes': attributes
    }
    return data
# ----------------------------------------------------------------------------------------------
def export_sim(sim_model):
    """Return a JSON formatted string representing that data in the model.
    
    :return: A JSON string in the SIM format.
    """
    return json.dumps(export_sim_data(sim_model))
# ----------------------------------------------------------------------------------------------
def export_sim_file(sim_model, filepath):
    """Import SIM file.
    
    :return: No value.
    """
    with open(filepath, 'w') as f:
        f.write( json.dumps(export_sim_data(sim_model)) )
# ==================================================================================================
# IMPORT
# ==================================================================================================
def import_sim_data(sim_model, json_data):
    """Import SIM JSON data.
    
    :return: No value.
    """
    # positions
    posis = []
    for i in range(json_data['geometry']['num_posis']):
        posis.append(sim_model.add_posi([0,0,0]))
    # points
    for posi_i in json_data['geometry']['points']:
        sim_model.add_point(posis[posi_i])
    # polylines
    for posis_i in json_data['geometry']['plines']:
        closed = posis_i[0] == posis_i[-1]
        sim_model.add_pline(map(lambda posi_i: posis[posi_i], posis_i), closed)
    # polygons
    for posi_lists_i in json_data['geometry']['pgons']:
        boundary = map(lambda posi_i: posis[posi_i], posi_lists_i[0])
        pgon = sim_model.add_pgon(boundary)
        for hole_posis_i in posi_lists_i[1:]:
            sim_model.add_pgon_hole(pgon, map(lambda posi_i: posis[posi_i], hole_posis_i))

    # collections
    num_colls = len(json_data['geometry']['coll_points'])
    for i in range(num_colls):
        coll = sim_model.add_coll()
        for point_i in json_data['geometry']['coll_points'][i]:
            sim_model.add_coll_ent(coll, 'pt' + str(point_i))
        for pline_i in json_data['geometry']['coll_plines'][i]:
            sim_model.add_coll_ent(coll, 'pl' + str(pline_i))
        for pgon_i in json_data['geometry']['coll_pgons'][i]:
            sim_model.add_coll_ent(coll, 'pg' + str(pgon_i))
        for child_coll_i in json_data['geometry']['coll_colls'][i]:
            sim_model.add_coll_ent(coll, 'co' + str(child_coll_i))
    # entity attribs
    ent_type_strs = [
        ['posis', ENT_TYPE.POSI],
        ['verts', ENT_TYPE.VERT],
        ['edges', ENT_TYPE.EDGE],
        ['wires', ENT_TYPE.WIRE],
        ['points', ENT_TYPE.POINT],
        ['plines', ENT_TYPE.PLINE],
        ['pgons', ENT_TYPE.PGON],
        ['colls', ENT_TYPE.COLL]
    ]
    
    for sim_ent_type, ent_type in ent_type_strs:
        for attrib in json_data['attributes'][sim_ent_type]:
            att_name = attrib['name']
            if sim_model.has_attrib(ent_type, att_name): 
                if (attrib['data_type'] != sim_model.get_attrib_datatype(ent_type, att_name)):
                    # if attrib already exists but with different datatype, then rename attrib
                    att_name = att_name + '_' + attrib['data_type']
            else:
                sim_model.add_attrib(ent_type, att_name, attrib['data_type'])
            for i in range(len(attrib['values'])):
                att_value = attrib['values'][i]
                for ent_i in attrib['entities'][i]:
                    ent = ent_type + str(ent_i)
                    sim_model.set_attrib_val(ent, att_name, att_value)
    # model attributes
    for [attrib_name, attrib_val] in json_data['attributes']['model']:
        sim_model.set_model_attrib_val(attrib_name, attrib_val)
# ----------------------------------------------------------------------------------------------
def import_sim(sim_model, json_str):
    """Import SIM string.
    
    :return: No value.
    """
    import_sim_data(sim_model, json.loads(json_str))
# ----------------------------------------------------------------------------------------------
def import_sim_file(sim_model, filepath):
    """Import SIM file.
    
    :return: No value.
    """
    with open(filepath, 'r') as f:
        import_sim_data(sim_model, json.loads(f.read()))
# ==================================================================================================
