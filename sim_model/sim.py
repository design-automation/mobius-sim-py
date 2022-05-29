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
    POSIS = 'posis'
    VERTS = 'verts'
    EDGES = 'edges'
    WIRES = 'wires'
    POINTS = 'points'
    PLINES = 'plines'
    PGONS = 'pgons'
    COLLS = 'colls'
    MODEL = 'model'
# --------------------------------------------------------------------------------------------------
class DATA_TYPE(object):
    """
    An Enum class that defines a set of constants for possible data types for attributes. 
    These types are used when adding an attrbute to the model.
    """
    NUM = 'number'
    STR =  'string'
    BOOL =  'boolean'
    LIST =  'list'
    DICT =  'dict'
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
    # ----------------------------------------------------------------------------------------------
    # types of edges in the graph
    class _GRAPH_EDGE_TYPE(object):
        ENT = 'entity'
        ATTRIB =  'attrib'
        META = 'meta'
    # ----------------------------------------------------------------------------------------------
    # Node in the graph that links to all ents
    _GRAPH_ENTS_NODE = {
        ENT_TYPE.POSIS: '_ents_posis',
        ENT_TYPE.VERTS: '_ents_verts',
        ENT_TYPE.EDGES: '_ents_edges',
        ENT_TYPE.WIRES: '_ents_wires',
        ENT_TYPE.POINTS: '_ents_points',
        ENT_TYPE.PLINES: '_ents_plines',
        ENT_TYPE.PGONS: '_ents_pgons',
        ENT_TYPE.COLLS: '_ents_colls',
    }
    # ----------------------------------------------------------------------------------------------
    # node in the graph that links to all attribs
    _GRAPH_ATTRIBS_NODE = {
        ENT_TYPE.POSIS: '_atts_posis',
        ENT_TYPE.VERTS: '_atts_verts',
        ENT_TYPE.EDGES: '_atts_edges',
        ENT_TYPE.WIRES: '_atts_wires',
        ENT_TYPE.POINTS: '_atts_points',
        ENT_TYPE.PLINES: '_atts_plines',
        ENT_TYPE.PGONS: '_atts_pgons',
        ENT_TYPE.COLLS: '_atts_colls',
    }
    # ----------------------------------------------------------------------------------------------
    # ENT PREFIX
    _ENT_PREFIX = {
        ENT_TYPE.POSIS:  'ps',
        ENT_TYPE.VERTS: '_v',
        ENT_TYPE.EDGES: '_e',
        ENT_TYPE.WIRES: '_w',
        ENT_TYPE.POINTS: 'pt',
        ENT_TYPE.PLINES: 'pl',
        ENT_TYPE.PGONS: 'pg',
        ENT_TYPE.COLLS: 'co'
    }
    # ----------------------------------------------------------------------------------------------
    # ENT_TYPES FOR COLLECTIONS
    _COLL_ENT_TYPES = [
        ENT_TYPE.POINTS, 
        ENT_TYPE.PLINES, 
        ENT_TYPE.PGONS, 
        ENT_TYPE.COLLS
    ]
    # ==============================================================================================
    # CONSTRUCTOR FOR SIM CLASS
    # ==============================================================================================
    def __init__(self):
        """Constructor for creating a new empty model
        """
        # graph
        self.graph = Graph()
        self.graph.add_edge_type(self._GRAPH_EDGE_TYPE.ENT, Graph.M2M) # many to many
        self.graph.add_edge_type(self._GRAPH_EDGE_TYPE.ATTRIB, Graph.M2O) # many to one
        self.graph.add_edge_type(self._GRAPH_EDGE_TYPE.META, Graph.O2M) # one to many
        # create nodes for ents and attribs
        for ent_type in [ENT_TYPE.POSIS, ENT_TYPE.VERTS, ENT_TYPE.EDGES, ENT_TYPE.WIRES, 
            ENT_TYPE.POINTS, ENT_TYPE.PLINES, ENT_TYPE.PGONS, ENT_TYPE.COLLS]:
            self.graph.add_node(
                self._GRAPH_ENTS_NODE[ent_type]
            )
            self.graph.add_node(
                self._GRAPH_ATTRIBS_NODE[ent_type]
            )
        # add xyz attrib
        self._graph_add_attrib(ENT_TYPE.POSIS, 'xyz', DATA_TYPE.LIST)
        # add empty model attrbutes
        self.model_attribs = {}
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
    # ==============================================================================================
    # PRIVATE GRAPH METHODS
    # ==============================================================================================
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
    # ----------------------------------------------------------------------------------------------
    def _graph_attrib_node_name(self, ent_type, att_name):
        """Create the name for an attrib node.
        It will be something like this: '_att_pgons_area'.
        """
        return '_att_' + ent_type + '_' + att_name
    # ----------------------------------------------------------------------------------------------
    def _graph_attrib_val_node_name(self, att_val, att_n):
        """Create the name for an attrib value node.
        It will be something like this: '_val_[1,2,3]'.
        """
        data_type = self.graph.get_node_props(att_n).get('data_type')
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
        ent_type_n = self._GRAPH_ENTS_NODE[ent_type]
        # create the node name, from prefix and then next count number
        ent_i = self.graph.degree_out(ent_type_n, edge_type = self._GRAPH_EDGE_TYPE.META)
        ent = self._ENT_PREFIX[ent_type] + str(ent_i)
        # add a node with name `n`
        # the new node has 1 property
        self.graph.add_node(ent, 
            ent_type = ent_type  # the type of entity, `posi`, `vert`, etc
        )
        # create an edge from the node `ent_type` to the new node
        # the new edge is given the attribute `meta`
        # this edge is so that later the node can be found
        self.graph.add_edge(ent_type_n, ent, 
            edge_type = self._GRAPH_EDGE_TYPE.META
        )
        # return the name of the new entity node
        return ent
    # ----------------------------------------------------------------------------------------------
    def _graph_add_attrib(self, ent_type, name, data_type):
        """Add an attribute node to the graph.
        """
        # create the node name, from the entity type and attribute name
        att_n = self._graph_attrib_node_name(ent_type, name)
        # add the node to the graph
        # the new node has 4 properties
        self.graph.add_node(
            att_n, 
            ent_type = ent_type, # the `entity_type` for this attribute, `posi`, `vert`, etc
            name = name,  # the name of the attribute
            data_type = data_type # the data type of this attribute
        )
        # create an edge from the node `ent_type_attribs` (e.g. posis_attribs) to the new attrib node
        # the edge type is `meta`
        self.graph.add_edge(
            self._GRAPH_ATTRIBS_NODE[ent_type], 
            att_n, 
            edge_type = self._GRAPH_EDGE_TYPE.META
        )
        # create a new edge type for this attrib
        self.graph.add_edge_type(att_n, Graph.M2O) # many to one
        # return the name of the new attrib node
        return att_n
    # ----------------------------------------------------------------------------------------------
    def _graph_add_attrib_val(self, att_n, att_val):
        """
        Add an attribute value node to the graph.

        :param att_n: the name of the attribute node
        :param value: the value of the attribute
        """
        # get the name of the attribute value node
        att_val_n = self._graph_attrib_val_node_name(att_val, att_n)
        # make sure that no node with the name already exists
        if not self.graph.has_node(att_val_n):
            # add the attrib value node
            # the new node has 1 property
            self.graph.add_node(att_val_n, 
                value = att_val # the node value
            )
            # add an edge from the attrib value to the attrib
            self.graph.add_edge(att_val_n, att_n, 
                edge_type = self._GRAPH_EDGE_TYPE.ATTRIB
            ) # att_val -> att
        # return the name of the attrib value node
        return att_val_n
    # ==============================================================================================
    # ADD METHODS FOR ENTITIES
    # ==============================================================================================
    def add_posi(self, xyz):
        """Add a position to the model, specifying the XYZ coordinates.

        :param xyz: The XYZ coordinates, a list of three numbers.
        :return: The ID of the new position.
        """
        posi_n = self._graph_add_ent(ENT_TYPE.POSIS)
        self.set_attrib_val(posi_n, "xyz", xyz)
        return posi_n
    # ----------------------------------------------------------------------------------------------
    def add_point(self, posi):
        """Add a point object to the model, specifying a single position.

        :param posi: A position ID.
        :return: The ID of the new point.
        """
        vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
        point_n = self._graph_add_ent(ENT_TYPE.POINTS)
        self.graph.add_edge(vert_n, posi, edge_type = self._GRAPH_EDGE_TYPE.ENT)
        self.graph.add_edge(point_n, vert_n, edge_type = self._GRAPH_EDGE_TYPE.ENT)
        return point_n
    # ----------------------------------------------------------------------------------------------
    def add_pline(self, posis, closed):
        """Add a polyline object to the model, specifying a list of positions.

        :param posis: A list of position IDs.
        :param closed: A boolean indicating if the polyline is closed or open.
        :return: The ID of the new polyline.
        """
        # vertices
        verts_n = []
        for posi_n in posis:
            vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
            self.graph.add_edge(vert_n, posi_n, edge_type = self._GRAPH_EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, verts_n[i], edge_type = self._GRAPH_EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, verts_n[i+1], edge_type = self._GRAPH_EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        if closed:
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, verts_n[-1], edge_type = self._GRAPH_EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, verts_n[0], edge_type = self._GRAPH_EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graph_add_ent(ENT_TYPE.WIRES)
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], edge_type = self._GRAPH_EDGE_TYPE.ENT)
        # pline
        pline_n = self._graph_add_ent(ENT_TYPE.PLINES)
        self.graph.add_edge(pline_n, wire_n, edge_type = self._GRAPH_EDGE_TYPE.ENT)
        #  return
        return pline_n
    # ----------------------------------------------------------------------------------------------
    def add_pgon(self, posis):
        """Add a polygon object to the model, specifying a list of positions.

        :param posis: A list of position IDs.
        :return: The ID of the new polygon.
        """
        # vertices
        verts_n = []
        for posi_n in posis:
            vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
            self.graph.add_edge(vert_n, posi_n, edge_type = self._GRAPH_EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, v0, edge_type = self._GRAPH_EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, v1, edge_type = self._GRAPH_EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graph_add_ent(ENT_TYPE.WIRES)
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], edge_type = self._GRAPH_EDGE_TYPE.ENT)
        # pline
        pgon_n = self._graph_add_ent(ENT_TYPE.PGONS)
        self.graph.add_edge(pgon_n, wire_n, edge_type = self._GRAPH_EDGE_TYPE.ENT)
        #  return
        return pgon_n
    # ----------------------------------------------------------------------------------------------
    def add_coll(self):
        """Add a new empty collection to the model.

        :return: The ID of the collection.
        """
        return self._graph_add_ent(ENT_TYPE.COLLS)
    # ----------------------------------------------------------------------------------------------
    def add_coll_ent(self, coll, ent):
        """Add an entity to an existing collection in the model.
        Collections can contain points, polylines, polygons, and other collections.
        Collections cannot contain positions, vertices, edges or wires.

        :param coll: The ID of the collection to which the entity will be added.
        :param ent: The ID of the entity to be added to the collection.
        :return: No value.
        """
        ent_type = self.graph.get_node_props(ent).get('ent_type')
        if ent_type not in self._COLL_ENT_TYPES:
            raise Exception('Invalid entitiy for collections.')
        self.graph.add_edge(coll, ent, edge_type = self._GRAPH_EDGE_TYPE.ENT)
    # ==============================================================================================
    # ATTRIBUTE METHODS
    # ==============================================================================================
    def add_attrib(self, ent_type, att_name, att_data_type):
        """Create a new attribute in the model, specifying the entity type, the attribute name, and
        the data type. Note that for each entity type, the attribute name must be a unique name.

        :param ent_type: The entity type for the attribute. (See ENT_TYPE)
        :param att_name: The name of the attribute to create. 
        :param att_data_type: The data type for the attribute values. (See DATA_TYPE)
        :return: No value.
        """
        att_n = self._graph_attrib_node_name(ent_type, att_name)
        if not self.graph.has_node(att_n):
            self._graph_add_attrib(ent_type, att_name, att_data_type)
        elif self.graph.get_node_props(att_n).get('data_type') != att_data_type:
            raise Exception('Attribute already exists with different data type')
    # ----------------------------------------------------------------------------------------------
    def has_attrib(self, ent_type, att_name):
        """Returns true if an attribute exists with the specified entity type and name.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param att_name: The name of the attribute. 
        :return: True is the attribute exists, false otherwise.
        """
        att_n = self._graph_attrib_node_name(ent_type, att_name)
        return self.graph.has_node(att_n)
    # ----------------------------------------------------------------------------------------------
    def get_attribs(self, ent_type):
        """Get a list of attribute names in the model, specifying the entity type.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :return: A list of attrib names.
        """
        return map(
            lambda att_n: self.graph.get_node_props(att_n).get('name'), 
            self.graph.successors(
                self._GRAPH_ATTRIBS_NODE[ent_type],
                self._GRAPH_EDGE_TYPE.META
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
        ent_type = self.graph.get_node_props(ent).get('ent_type')
        att_n = self._graph_attrib_node_name(ent_type, att_name)
        if ent_type != self.graph.get_node_props(att_n).get('ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._check_type(att_value)
        if self.graph.get_node_props(att_n).get('data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(att_value))
        att_val_n = self._graph_add_attrib_val(att_n, att_value)
        self.graph.add_edge(ent, att_val_n, att_n) # ent -> att_val
    # ----------------------------------------------------------------------------------------------
    def get_attrib_val(self, ent, name):
        """Get an attribute value from an entity in the model, specifying the attribute name.

        :param ent: The ID of the entity for which to get the attribute value.
        :param name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        ent_type = self.graph.get_node_props(ent).get('ent_type')
        att_n = self._graph_attrib_node_name(ent_type, name)
        att_vals_n = self.graph.successor(ent, att_n)
        if att_vals_n == None:
            return None
        return self.graph.get_node_props(att_vals_n).get('value')
    # ----------------------------------------------------------------------------------------------
    def get_attrib_vals(self, ent_type, name):
        """Get a list of all the attribute values for the specified attribute.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param name: The name of the attribute.
        :return: A list of all attribute values.
        """
        att_n = self._graph_attrib_node_name(ent_type, name)
        att_vals_n = self.graph.predecessors(att_n, self._GRAPH_EDGE_TYPE.ATTRIB)
        values = []
        for att_val_n in att_vals_n:
            values.append(self.graph.get_node_props(att_val_n).get('value'))
        return values
    # ----------------------------------------------------------------------------------------------
    def get_attrib_datatype(self, ent_type, name):
        """Get an attribute datatype, specifying the attribute entity type and attribute name.

        :param ent_type: The entity type for getting attributes. (See ENT_TYPE)
        :param name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        att_n = self._graph_attrib_node_name(ent_type, name)
        return self.graph.get_node_props(att_n).get('data_type')
    # ----------------------------------------------------------------------------------------------
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
    def get_model_attribs(self):
        """Get a list of attribute names from the model. Model attributes are
        top level attributes that apply to the whole model. As such, they are not attached to any
        specific entities.

        :return: A list of attribute names.
        """
        return self.model_attribs.keys()
    # ==============================================================================================
    # GET METHODS FOR ENTITIES
    # ==============================================================================================
    _ENT_SEQ = {
        ENT_TYPE.POSIS: 0,
        ENT_TYPE.VERTS: 1,
        ENT_TYPE.EDGES: 2,
        ENT_TYPE.WIRES: 3,
        ENT_TYPE.POINTS: 4,
        ENT_TYPE.PLINES: 4,
        ENT_TYPE.PGONS: 4,
        ENT_TYPE.COLLS: 6
    }
    # ----------------------------------------------------------------------------------------------
    _ENT_SEQ_COLL_POINT_POSI = {
        ENT_TYPE.POSIS: 0,
        ENT_TYPE.VERTS: 1,
        ENT_TYPE.POINTS: 2,
        ENT_TYPE.COLLS: 6
    }
    # ----------------------------------------------------------------------------------------------
    _ENT_SEQ_COLL_PLINE_POSI = {
        ENT_TYPE.POSIS: 0,
        ENT_TYPE.VERTS: 1,
        ENT_TYPE.EDGES: 2,
        ENT_TYPE.WIRES: 3,
        ENT_TYPE.PLINES: 4,
        ENT_TYPE.COLLS: 6
    }
    # ----------------------------------------------------------------------------------------------
    _ENT_SEQ_COLL_PGON_POSI = {
        ENT_TYPE.POSIS: 0,
        ENT_TYPE.VERTS: 1,
        ENT_TYPE.EDGES: 2,
        ENT_TYPE.WIRES: 3,
        ENT_TYPE.PGONS: 4,
        ENT_TYPE.COLLS: 6
    }
    # ----------------------------------------------------------------------------------------------
    def _get_ent_seq(self, target_ent_type, source_ent_type):
        if (target_ent_type == ENT_TYPE.POINTS or source_ent_type == ENT_TYPE.POINTS):
            return self._ENT_SEQ_COLL_POINT_POSI
        elif (target_ent_type == ENT_TYPE.PLINES or source_ent_type == ENT_TYPE.PLINES):
            return self._ENT_SEQ_COLL_PLINE_POSI
        elif (target_ent_type == ENT_TYPE.PGONS or source_ent_type == ENT_TYPE.PGONS):
            return self._ENT_SEQ_COLL_PGON_POSI
        return self._ENT_SEQ
    # ----------------------------------------------------------------------------------------------
    # TODO more tests needed
    def _nav(self, target_ent_type, source_ent):
        source_ent_type = self.graph.get_node_props(source_ent).get('ent_type')
        ent_seq = self._get_ent_seq(target_ent_type, source_ent_type)
        if source_ent_type == target_ent_type:
            if source_ent_type == ENT_TYPE.COLLS:
                return [] # TODO nav colls of colls
            return [source_ent]
        dist = ent_seq[source_ent_type] - ent_seq[target_ent_type]
        if dist == 1:
            return self.graph.successors(source_ent, self._GRAPH_EDGE_TYPE.ENT)
        if dist == -1:
            return self.graph.predecessors(source_ent, self._GRAPH_EDGE_TYPE.ENT)
        # get the function to navigate
        navigate = self.graph.successors if dist > 0 else self.graph.predecessors
        ents = [source_ent]
        target_ents_set = OrderedDict() # to be used as an ordered set
        while ents:
            ent_set = OrderedDict() # to be used as an ordered set
            for ent in ents:
                for target_ent in navigate(ent, self._GRAPH_EDGE_TYPE.ENT):
                    this_ent_type = self.graph.get_node_props(target_ent).get('ent_type')
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
    def num_ents(self, ent_type):
        """Get the number of entities in the model of a specific type.  

        :param ent_type: The type of entity to search for in the model.
        :return: A number of entities of the specified type in the model.
        """
        return self.graph.degree_out(
            self._GRAPH_ENTS_NODE[ent_type], 
            self._GRAPH_EDGE_TYPE.META
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
        :param source_ents: None, or a single entity ID or a list of entity IDs from which to get the target entities.
        :return: A list of unique entity IDs.
        """
        if source_ents == None:
            return self.graph.successors(
                self._GRAPH_ENTS_NODE[target_ent_type], 
                self._GRAPH_EDGE_TYPE.META
            )
        # not a list
        if not type(source_ents) is list:
            return self._nav(target_ent_type, source_ents)
        # a list with one item
        if len(source_ents) == 1:
            return self._nav(target_ent_type, source_ents[0])
        # a list with multiple items
        ents_set = OrderedDict() # ordered set
        for source_ent in source_ents:
            for target_ent in self._nav(target_ent_type, source_ent):
                ents_set[target_ent] = None # ordered set
        return list(ents_set.keys())
    # ----------------------------------------------------------------------------------------------
    def get_point_posi(self, point):
        """Get the position ID for a point.

        :param point: A point ID from which to get the position.
        :return: A position ID. 
        """
        vert = self.graph.successors(point, self._GRAPH_EDGE_TYPE.ENT)[0]
        return self.graph.successors(vert, self._GRAPH_EDGE_TYPE.ENT)[0]
    # ----------------------------------------------------------------------------------------------
    def get_pline_posis(self, pline):
        """Get a list of position IDs for a polyline. If the polyline is closed, the first and last
        positions will be the same.

        :param pline: A polyline ID from which to get the positions.
        :return: A list of position IDs. The list may contain duplicates.
        """
        wire = self.graph.successors(pline, self._GRAPH_EDGE_TYPE.ENT)[0]
        edges = self.graph.successors(wire, self._GRAPH_EDGE_TYPE.ENT)
        verts = [self.graph.successors(edge, self._GRAPH_EDGE_TYPE.ENT)[0] for edge in edges]
        posis = [self.graph.successors(vert, self._GRAPH_EDGE_TYPE.ENT)[0] for vert in verts]
        last_vert = self.graph.successors(edges[-1], self._GRAPH_EDGE_TYPE.ENT)[1]
        last_posi = self.graph.successors(last_vert, self._GRAPH_EDGE_TYPE.ENT)[0]
        posis.append(last_posi)
        return posis
    # ----------------------------------------------------------------------------------------------
    def get_pgon_posis(self, pgon):
        """Get a list of lists of position IDs for an polygon. Each list represents one of the
        polygon wires. All wires are assumed to be closed. (The last position is not duplicated.)

        :param pgon: A polygon ID from which to get the positions.
        :return: A list of lists of position IDs. The lists may contain duplicates.
        """
        posis = []
        for wire in self.graph.successors(pgon, self._GRAPH_EDGE_TYPE.ENT):
            edges = self.graph.successors(wire, self._GRAPH_EDGE_TYPE.ENT)
            verts = [self.graph.successors(edge, self._GRAPH_EDGE_TYPE.ENT)[0] for edge in edges]
            wire_posis = [self.graph.successors(vert, self._GRAPH_EDGE_TYPE.ENT)[0] for vert in verts]
            posis.append(wire_posis)
        return posis
    # ----------------------------------------------------------------------------------------------
    def get_posi_coords(self, posi):
        """Get the XYZ coordinates of a position

        :param posi: A position ID.
        :return: A list of three numbers, the XYZ coordinates.
        """
        att_n = self._graph_attrib_node_name(ENT_TYPE.POSIS, 'xyz')
        att_vals_n = self.graph.successor(posi, att_n)
        return self.graph.get_node_props(att_vals_n).get('value')
    # ==============================================================================================
    # QUERY
    # ==============================================================================================
    def pline_is_closed(self, pline):
        """Check if a polyline is open or closed.

        :param pline: A polyline ID.
        :return: True if closed, False if open.
        """
        edges = self.graph.successors(self.graph.successors(pline, self._GRAPH_EDGE_TYPE.ENT)[0], self._GRAPH_EDGE_TYPE.ENT)
        start = self.graph.successors(self.graph.successors(edges[0], self._GRAPH_EDGE_TYPE.ENT)[0], self._GRAPH_EDGE_TYPE.ENT)
        end = self.graph.successors(self.graph.successors(edges[-1], self._GRAPH_EDGE_TYPE.ENT)[1], self._GRAPH_EDGE_TYPE.ENT)
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
        att_n = self._graph_attrib_node_name(ent_type, att_name)
        if not self.graph.has_node(att_n):
            raise Exception("The attribute does not exist: '" + att_name + "'.")
        # val == None
        if comparator == '==' and att_val == None:
            set_with_val = set(self.graph.get_nodes_with_out_edge(att_n))
            set_all = set(self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META))
            return list(set_all - set_with_val)
        # val != None
        if comparator == '!=' and att_val == None:
            return self.graph.get_nodes_with_out_edge(att_n)
        # val == att_val
        if comparator == '==':
            att_val_n = self._graph_attrib_val_node_name(att_val, att_n)
            if not self.graph.has_node(att_val_n):
                return []
            return self.graph.predecessors(att_val_n, att_n)
        # val != att_val
        if comparator == '!=':
            att_val_n = self._graph_attrib_val_node_name(att_val, att_n)
            if not self.graph.has_node(att_val_n):
                return self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META)
            ents_equal = self.graph.predecessors(att_val_n, att_n)
            if len(ents_equal) == 0:
                return self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META)
            set_equal = set(ents_equal)
            set_all = set(self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META))
            return list(set_all - set_equal)
        # other cases, data_type must be a number
        data_type = self.graph.get_node_props(att_n).get('data_type')
        if data_type != DATA_TYPE.NUM:
            raise Exception("The '" + comparator +
                "' comparator cannot be used with attributes of type '" + data_type + "'.")
        result = []
        # val < att_val
        if comparator == '<':
            result = []
            for ent in self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META):
                val_n = self.graph.successor(ent, att_n)
                if val_n != None and self.graph.get_node_props(val_n).get('value') < att_val:
                    result.append(ent)
        # val <= att_val
        if comparator == '<=':
            result = []
            for ent in self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META):
                val_n = self.graph.successor(ent, att_n)
                if val_n != None and self.graph.get_node_props(val_n).get('value') <= att_val:
                    result.append(ent)
        # val > att_val
        if comparator == '>':
            result = []
            for ent in self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META):
                val_n = self.graph.successor(ent, att_n)
                if val_n != None and self.graph.get_node_props(val_n).get('value') > att_val:
                    result.append(ent)
        # val >= att_val
        if comparator == '>=':
            result = []
            for ent in self.graph.successors(self._GRAPH_ENTS_NODE[ent_type], self._GRAPH_EDGE_TYPE.META):
                val_n = self.graph.successor(ent, att_n)
                if val_n != None and self.graph.get_node_props(val_n).get('value') >= att_val:
                    result.append(ent)
        # return list of entities
        # TODO handle queries sub-entities in lists and dicts
        return result
# ==================================================================================================
# END SIM CLASS
# ==================================================================================================