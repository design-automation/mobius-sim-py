from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import with_statement
# generators, generator_stop, nested_scopes 
import sys
print("PYTHON Version: ", sys.version_info)
if sys.version_info[0] >= 3:
    unicode = str
from collections import OrderedDict
import json
from sim_model.graph import Graph
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
    ENT_TYPE.POSI:  {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.VERT:  {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.EDGE:  {'idx': 2, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.WIRE:  {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.POINT: {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PLINE: {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PGON:  {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL:  {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PT_PO = {
    ENT_TYPE.POSI:  {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.POINT: {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL:  {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PL_PO = {
    ENT_TYPE.POSI:  {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.VERT:  {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.EDGE:  {'idx': 2, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.PLINE: {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}, 
    ENT_TYPE.COLL:  {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PG_PO = {
    ENT_TYPE.POSI: {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.VERT: {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.EDGE: {'idx': 2, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.WIRE: {'idx': 3, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.PGON: {'idx': 4, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL: {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
# --------------------------------------------------------------------------------------------------
_ENT_SEQ_CO_PG_TRI_PO = {
    ENT_TYPE.POSI: {'idx': 0, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.VERT: {'idx': 1, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.TRI},
    ENT_TYPE.TRI:  {'idx': 2, 'succ': _GR_EDGE_TYPE.TRI,    'pred': _GR_EDGE_TYPE.TRI},
    ENT_TYPE.PGON: {'idx': 3, 'succ': _GR_EDGE_TYPE.TRI,    'pred': _GR_EDGE_TYPE.ENT},
    ENT_TYPE.COLL: {'idx': 6, 'succ': _GR_EDGE_TYPE.ENT, 'pred': _GR_EDGE_TYPE.ENT}
}
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
    The nodes for entities are:
    
    - ent nodes
      - e.g. 'ps01', '_v123'

    - ent_type nodes 
      - e.g. 'posis', 'verts'

    The nodes for attribs are:

    - _atts_ent_type nodes 
      - e.g.'_atts_pgons'

    - _att_ent_type_name nodes 
      - e.g. '_att_pgons_area'

    - _att_val nodes 
      - e.g. '[1,2,3]'

    The forward edges are as follows:
    
    Edges of type 'entity':

    - ent -> sub_ents 
      - e.g. pg0 -> [w0, w1]
      - edge_type = 'entity'
      - many to many

    Edges of type 'meta':

    - ent_type -> ents
      - e.g. pgons -> pg0
      - edge_type = 'meta'
      - one to many

    - ent_type_attribs -> att_ent_type_name 
      - e.g. pgons_attribs -> att_pgons_area) 
      - edge_type = 'meta'
      - one to many

    Edges of type 'att':

    - attrib_val -> att_ent_type_name 
      - e.g. val_123 -> att_pgons_area
      - edge_type = 'attrib' 
      - many to one

    Edges of with a type specific to the attribute:

    - ent -> attrib_val 
      - pg0 -> val_123
      - edge_type = att_ent_type_name e.g. '_att_pgons_area'
      - many to one

    For each forward edge, there is an equivalent reverse edge.

    """
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

        # create nodes for attribs (not TRI)
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
        # pline
        pline = self._graph_add_ent(ENT_TYPE.PLINE)
        closed = posis[0] == posis[-1]
        self._add_edge_seq(posis, len(posis) - 1, closed, VERT_TYPE.PLINE, pline)
        # return entity
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
        self._add_edge_seq(posis[0], len(posis[0]), True, VERT_TYPE.PGON, wire)
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
        self._add_edge_seq(posis, len(posis), True, VERT_TYPE.PGON_HOLE, wire)
        # triangulate
        # self.tri.triangulatePgon(pgon) TODO
        # return
        return wire
    # ----------------------------------------------------------------------------------------------
    def _add_edge_seq(self, posis, num_edges, closed, vert_type, parent):
        """Add a sequnce of edges. Use by addPgon(), add_pgon_hole(), addPline().

        :param posis: The list of posis.
        :param num_edges: The number of edges to add.
        :param closed: If true, and additional edge is added to close the loop.
        :param vert_type: The vertex type, see VERT_TYPE
        :param parent: The parent of the new edges. Wither a wire or a pline.
        """
        num_verts = num_edges if closed else num_edges + 1
        edges = []
        v0 = None
        v1 = None
        # v0
        v_start = self._graph_add_ent(ENT_TYPE.VERT)
        self.graph.set_node_prop(v_start, 'vert_type', vert_type)
        self.graph.add_edge(v_start, posis[0], _GR_EDGE_TYPE.ENT)
        v0 = v_start
        for i in range(1, len(num_verts)):
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
            edges.push(edge)
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
        att = self._graph_attrib_node_name(ent_type, att_name)
        if ent_type != self.graph.get_node_prop(att, 'ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._check_type(att_value)
        if self.graph.get_node_prop(att, 'data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(att_value) +
                'The data type is a "' + data_type + '". ' + 
                'The data type should be a "' + self.graph.get_node_prop(att, 'data_type') + '".' )
        # get the name of the attribute value node
        att_val_node = self._graph_attrib_val_node_name(att_value)
        # make sure that no node with the name already exists
        if not self.graph.has_node(att_val_node):
            # add the attrib value node
            self.graph.add_node(att_val_node)
            self.graph.set_node_prop(att_val_node, 'value', att_value)
        # add an edge from the att_val_node to the attrib: att_val -> att
        self.graph.add_edge(att_val_node, att, _GR_EDGE_TYPE.ATT)
        # add and edge from the ent to the att_val_node
        self.graph.del_edge(ent, None, att)
        # ent -> att_val, ent <- att_val
        self.graph.add_edge(ent, att_val_node, att)
    # ----------------------------------------------------------------------------------------------
    def get_attrib_val(self, ent, att_name):
        """Get an attribute value from an entity in the model, specifying the attribute name.
        If the entity has no value for that attribute, then `None` is returned.

        :param ent: The ID of the entity for which to get the attribute value.
        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        ent_type = self.graph.get_node_prop(ent, 'ent_type')
        att = self._graph_attrib_node_name(ent_type, att_name)
        succs = self.graph.successors(ent, att)
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
        att = self._graph_attrib_node_name(ent_type, att_name)
        succs = self.graph.successors(ent, att)
        if len(succs) == 0:
            return
        self.graph.del_edge(ent, succs[0], att)
    # ----------------------------------------------------------------------------------------------
    def get_attrib_vals(self, ent_type, att_name):
        """Get a list of all the attribute values for the specified attribute.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute.
        :return: A list of all attribute values.
        """
        att = self._graph_attrib_node_name(ent_type, att_name)
        att_vals = self.graph.predecessors(att, _GR_EDGE_TYPE.ATT)
        values = []
        for att_val_n in att_vals:
            values.append(self.graph.get_node_prop(att_val_n, 'value'))
        return values
    # ----------------------------------------------------------------------------------------------
    def get_attrib_datatype(self, ent_type, att_name):
        """Get an attribute datatype, specifying the attribute entity type and attribute name.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        att = self._graph_attrib_node_name(ent_type, att_name)
        return self.graph.get_node_prop(att, 'data_type')
    # ----------------------------------------------------------------------------------------------
    def rename_attrib(self, ent_type, att_name, new_name):
        """Rename an attribute.

        :param ent_type: The entity type for the attribute. (See ENT_TYPE)
        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        old_att = self._graph_attrib_node_name(ent_type, att_name)
        att_data_type = self.graph.get_node_prop(old_att, 'data_type')
        new_att = self._graph_add_attrib(ent_type, new_name, att_data_type)
        for pred in self.graph.predecessors(old_att, _GR_EDGE_TYPE.ATT):
            self.graph.del_edge(pred, old_att, _GR_EDGE_TYPE.ATT)
            self.graph.add_edge(pred, new_att, _GR_EDGE_TYPE.ATT)
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
            if (target_ent_type == ENT_TYPE.TRI or source_ent_type == ENT_TYPE.TRI):
                return _ENT_SEQ_CO_PG_TRI_PO
            elif (target_ent_type == ENT_TYPE.POINT or source_ent_type == ENT_TYPE.POINT):
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
        att_val_n = self.graph.successors(posi, _GR_XYZ_NODE)[0]
        return self.graph.get_node_prop(att_val_n, 'value')
    # ----------------------------------------------------------------------------------------------
    def get_posi_coords(self, posi):
        """Get the XYZ coordinates of a position.

        :param posi: A position ID.
        :return: A list of three numbers, the XYZ coordinates.
        """
        att_val_n = self.graph.successors(posi, _GR_XYZ_NODE)[0]
        return self.graph.get_node_prop(att_val_n, 'value')
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
        att = self._graph_attrib_node_name(ent_type, att_name)
        if not self.graph.has_node(att):
            raise Exception("The attribute does not exist: '" + att_name + "'.")
        # val == None
        if comparator == '==' and att_val == None:
            set_with_val = set(self.graph.get_nodes_with_out_edge(att))
            set_all = set(self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META))
            return list(set_all - set_with_val)
        # val != None
        if comparator == '!=' and att_val == None:
            return self.graph.get_nodes_with_out_edge(att)
        # val == att_val
        if comparator == '==':
            att_val_n = self._graph_attrib_val_node_name(att_val, att)
            if not self.graph.has_node(att_val_n):
                return []
            return self.graph.predecessors(att_val_n, att)
        # val != att_val
        if comparator == '!=':
            att_val_n = self._graph_attrib_val_node_name(att_val, att)
            if not self.graph.has_node(att_val_n):
                return self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META)
            ents_equal = self.graph.predecessors(att_val_n, att)
            if len(ents_equal) == 0:
                return self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META)
            set_equal = set(ents_equal)
            set_all = set(self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META))
            return list(set_all - set_equal)
        # other cases, data_type must be a number
        data_type = self.graph.get_node_prop(att, 'data_type')
        if data_type != DATA_TYPE.NUM:
            raise Exception("The '" + comparator +
                "' comparator cannot be used with attributes of type '" + data_type + "'.")
        result = []
        # val < att_val
        if comparator == '<':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0], 'value') < att_val:
                    result.append(ent)
        # val <= att_val
        if comparator == '<=':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0],'value') <= att_val:
                    result.append(ent)
        # val > att_val
        if comparator == '>':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att)
                if len(succs) != 0 and self.graph.get_node_prop(succs[0], 'value') > att_val:
                    result.append(ent)
        # val >= att_val
        if comparator == '>=':
            result = []
            for ent in self.graph.successors(_GR_ENTS_NODE[ent_type], _GR_EDGE_TYPE.META):
                succs = self.graph.successors(ent, att)
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
    def _graph_attrib_val_node_name(self, att_val, att):
        """Create the name for an attrib value node.
        It will be something like this: '_val_[1,2,3]'.
        """
        data_type = self.graph.get_node_prop(att, 'data_type')
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
        att = self._graph_attrib_node_name(ent_type, name)
        # add the node to the graph
        self.graph.add_node(att)
        # set node properties
        self.graph.set_node_prop(att, 'ent_type', ent_type) # the `entity_type` for this attribute, `posi`, `vert`, etc
        self.graph.set_node_prop(att, 'name', name) # the name of the attribute
        self.graph.set_node_prop(att, 'data_type', data_type) # the data type of this attribute
        # create an edge from the node `ent_type_attribs` (e.g. posis_attribs) to the new attrib node
        # the edge type is `meta`
        self.graph.add_edge(_GR_ATTRIBS_NODE[ent_type], att, _GR_EDGE_TYPE.META)
        # create a new edge type for this attrib
        self.graph.add_edge_type(att, rev = True) # many to one
        # return the name of the new attrib node
        return att
    # ----------------------------------------------------------------------------------------------
    def _graph_add_attrib_val(self, att_name, att_val):
        """
        Add an attribute value node to the graph.

        :param att_name: the name of the attribute node
        :param value: the value of the attribute
        """
        # get the name of the attribute value node
        att_val_n = self._graph_attrib_val_node_name(att_val, att_name)
        # make sure that no node with the name already exists
        if not self.graph.has_node(att_val_n):
            # add the attrib value node
            # the new node has 1 property
            self.graph.add_node(att_val_n)
            self.graph.set_node_prop(att_val_n, 'value', att_val) # the node value
            # add an edge from the attrib value to the attrib
            self.graph.add_edge(att_val_n, att_name, _GR_EDGE_TYPE.ATT) # att_val -> att
        # return the name of the attrib value node
        return att_val_n
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