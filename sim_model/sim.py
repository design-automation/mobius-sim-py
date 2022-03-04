from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from collections import OrderedDict
import json
from sim_model import graph
# ==================================================================================================
# Constants
# ==================================================================================================

# ENT_TYPE
class ENT_TYPE(object):
    """
    A class that defines a set of constants for different entity types. 
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

# DATA_TYPE
class DATA_TYPE(object):
    """
    A class that defines a set of constants for possible data types for attributes. 
    These types are used when adding an attrbute to the model.
    """
    NUM = 'number'
    STR =  'string'
    BOOL =  'boolean'
    LIST =  'list'
    DICT =  'dict'

# NODE TYPE
class _NODE_TYPE(object):
    ENT = 'entity'
    ATTRIB =  'attrib'
    ATTRIB_VAL =  'attrib_val'
    META = 'meta'

# EDGE TYPE
class _EDGE_TYPE(object):
    ENT = 'entity'
    ATTRIB =  'attrib'
    META = 'meta'

# ENT_TYPES FOR COLLECTIONS
_COLL_ENT_TYPES = [
    ENT_TYPE.POINTS, 
    ENT_TYPE.PLINES, 
    ENT_TYPE.PGONS, 
    ENT_TYPE.COLLS
]

# ENT PREFIX
_ENT_PREFIX = {
    'posis':  'ps',
    'verts': '_v',
    'edges': '_e',
    'wires': '_w',
    'points': 'pt',
    'plines': 'pl',
    'pgons': 'pg',
    'colls': 'co'
}

_ENT_SEQ = {
    ENT_TYPE.POSIS: 0,
    ENT_TYPE.VERTS: 1,
    ENT_TYPE.EDGES: 2,
    ENT_TYPE.WIRES: 3,
    ENT_TYPE.POINTS: 10,
    ENT_TYPE.PLINES: 20,
    ENT_TYPE.PGONS: 30,
    ENT_TYPE.COLLS: 40
}

# ==================================================================================================
# Class for reading and writing Spatial Information Models
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

    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================

    def __init__(self):
        """Constructor for creating a new empty model
        """

       # graph
        self.graph = graph.Graph([
            _EDGE_TYPE.ENT, _EDGE_TYPE.ATTRIB, _EDGE_TYPE.META
        ])

        # create meta nodes
        meta = [ENT_TYPE.POSIS, ENT_TYPE.VERTS, ENT_TYPE.EDGES, ENT_TYPE.WIRES, 
            ENT_TYPE.POINTS, ENT_TYPE.PLINES, ENT_TYPE.PGONS, ENT_TYPE.COLLS]
        for ent_type in meta:
            self.graph.add_node(ent_type, node_type = _NODE_TYPE.META)
            self.graph.add_node(ent_type + '_attribs', node_type = _NODE_TYPE.META)

        # add xyz attrib
        self._graph_add_attrib(ENT_TYPE.POSIS, 'xyz', DATA_TYPE.LIST)

    # ==============================================================================================
    # UTILITY 
    # ==============================================================================================

    def _check_type(self, value):
        val_type = type(value)
        if val_type == int or val_type == float:
            return DATA_TYPE.NUM
        if val_type == str:
            return DATA_TYPE.STR
        if val_type == bool:
            return DATA_TYPE.BOOL
        if val_type == list:
            return DATA_TYPE.LIST
        if val_type == dict:
            return DATA_TYPE.DICT
        raise Exception('Data type is not recognised.')

    # ==============================================================================================
    # PRIVATE GRAPH METHODS
    # ==============================================================================================

    def _graph_add_ent(self, enty_type):
        n = _ENT_PREFIX[enty_type] + str(self.graph.degree(enty_type, edge_type = _EDGE_TYPE.META))
        self.graph.add_node(n, node_type = _NODE_TYPE.ENT, ent_type = enty_type)
        self.graph.add_edge(enty_type, n, edge_type = _EDGE_TYPE.META)
        return n

    def _graph_attrib_node_name(self, ent_type, name):
        return 'att_' + ent_type + '_' + name

    def _graph_add_attrib(self, ent_type, name, data_type):
        n = self._graph_attrib_node_name(ent_type, name)
        self.graph.add_node(n, node_type = _NODE_TYPE.ATTRIB, ent_type = ent_type,
            name = name, data_type = data_type)
        self.graph.add_edge(ent_type + '_attribs', n, edge_type = _EDGE_TYPE.META)
        return n

    def _graph_attrib_val_node_name(self, value):
        return 'val_' + str(value)

    def _graph_add_attrib_val(self, att_n, value):
        att_val_n = self._graph_attrib_val_node_name(value)
        if not att_val_n in self.graph.nodes:
            self.graph.add_node(att_val_n, node_type = _NODE_TYPE.ATTRIB_VAL, value = value)
            self.graph.add_edge(att_val_n, att_n, edge_type = _EDGE_TYPE.ATTRIB) # att_val -> att
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

    def add_point(self, posi):
        """Add a point object to the model, specifying a single position.

        :param posi: A position ID.
        :return: The ID of the new point.
        """
        vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
        point_n = self._graph_add_ent(ENT_TYPE.POINTS)
        self.graph.add_edge(vert_n, posi, edge_type = _EDGE_TYPE.ENT)
        self.graph.add_edge(point_n, vert_n, edge_type = _EDGE_TYPE.ENT)
        return point_n

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
            self.graph.add_edge(vert_n, posi_n, edge_type = _EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, verts_n[i], edge_type = _EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, verts_n[i+1], edge_type = _EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        if closed:
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, verts_n[-1], edge_type = _EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, verts_n[0], edge_type = _EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graph_add_ent(ENT_TYPE.WIRES)
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], edge_type = _EDGE_TYPE.ENT)
        # pline
        pline_n = self._graph_add_ent(ENT_TYPE.PLINES)
        self.graph.add_edge(pline_n, wire_n, edge_type = _EDGE_TYPE.ENT)
        #  return
        return pline_n

    def add_pgon(self, posis):
        """Add a polygon object to the model, specifying a list of positions.

        :param posis: A list of position IDs.
        :return: The ID of the new polygon.
        """
        # vertices
        verts_n = []
        for posi_n in posis:
            vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
            self.graph.add_edge(vert_n, posi_n, edge_type = _EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, v0, edge_type = _EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, v1, edge_type = _EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graph_add_ent(ENT_TYPE.WIRES)
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], edge_type = _EDGE_TYPE.ENT)
        # pline
        pgon_n = self._graph_add_ent(ENT_TYPE.PGONS)
        self.graph.add_edge(pgon_n, wire_n, edge_type = _EDGE_TYPE.ENT)
        #  return
        return pgon_n

    def add_coll(self):
        """Add a new empty collection to the model.

        :return: The ID of the collection.
        """
        return self._graph_add_ent(ENT_TYPE.COLLS)

    def add_coll_ent(self, coll, ent):
        """Add an entity to an existing collection in the model.
        Collections can contain points, polylines, polygons, and other collections.
        Collections cannot contain positions, vertices, edges or wires.

        :param coll: The ID of the collection to which the entity will be added.
        :param ent: The ID of the entity to be added to the collection.
        :return: No value.
        """
        ent_type = self.graph.nodes[ent].get('ent_type')
        if ent_type not in _COLL_ENT_TYPES:
            raise Exception('Invalid entitiy for collections.')
        self.graph.add_edge(coll, ent, edge_type = _EDGE_TYPE.ENT)

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
        if self.graph.nodes.get(att_n) == None:
            self._graph_add_attrib(ent_type, att_name, att_data_type)
        elif self.graph.nodes[att_n].get('data_type') != att_data_type:
            raise Exception('Attribute already exists with different data type')
            
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
        ent_type = self.graph.nodes[ent].get('ent_type')
        att_n = self._graph_attrib_node_name(ent_type, att_name)
        if ent_type != self.graph.nodes[att_n].get('ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._check_type(att_value)
        if self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(att_value))
        att_val_n = self._graph_add_attrib_val(att_n, att_value)
        self.graph.add_edge(ent, att_val_n, edge_type = _EDGE_TYPE.ATTRIB) # ent -> att_val
        
    def get_attrib_val(self, ent, name):
        """Get an attribute value from an entity in the model, specifying the attribute name.

        :param ent: The ID of the entity for which to get the attribute value.
        :param name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        # TODO this look slow!
        ent_type = self.graph.nodes[ent].get('ent_type')
        att_n = self._graph_attrib_node_name(ent_type, name)
        att_vals_n = self.graph.successors(ent, _EDGE_TYPE.ATTRIB)
        for att_val_n in att_vals_n:
            atts_n = self.graph.successors(att_val_n, _EDGE_TYPE.ATTRIB)
            if atts_n and atts_n[0] == att_n:
                return self.graph.nodes[att_val_n].get('value')
        return None

    def set_model_attrib_val(self, att_name, att_value):
        """Set an attribute value from the model, specifying a name and value. Model attributes are
        top level attributes that apply to the whole model. As such, they are not attached to any
        specific entities.

        :param att_name: The name of the attribute.
        :param att_value: The attribute value to set.
        :return: No value.
        """
        self.graph.data[att_name] = att_value

    def get_model_attrib_val(self, att_name):
        """Get an attribute value from the model, specifying a name. Model attributes are
        top level attributes that apply to the whole model. As such, they are not attached to any
        specific entities.

        :param att_name: The name of the attribute.
        :return: The attribute value or None if no value.
        """
        return self.graph.data[att_name]

    # ==============================================================================================
    # GET METHODS FOR ENTITIES
    # ==============================================================================================

    def num_ents(self, ent_type):
        """Get the number of entities in the model of a specific type.  

        :param ent_type: The type of entity to search for in the model.
        :return: A number of entities of the specified type in the model.
        """
        return self.graph.degree(ent_type)

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
            return self.graph.successors(target_ent_type, _EDGE_TYPE.META)
        source_ents = source_ents if type(source_ents) is list else [source_ents]
        ents_set = OrderedDict() # ordered set
        for source_ent in source_ents:
            for target_ent in self._nav(target_ent_type, source_ent):
                ents_set[target_ent] = None # ordered set
        return list(ents_set.keys())

    def _nav(self, target_ent_type, source_ent):
        # TODO this method could be optimised
        source_ent_type = self.graph.nodes[source_ent].get('ent_type')
        if source_ent_type == target_ent_type:
            return ents
        dir = _ENT_SEQ[source_ent_type] - _ENT_SEQ[target_ent_type]
        navigate = self.graph.successors if dir > 0 else self.graph.predecessors
        ents = [source_ent]
        target_ents_set = OrderedDict()
        while ents:
            ent_set = OrderedDict()
            for ent in ents:
                for target_ent in navigate(ent, _EDGE_TYPE.ENT):
                    this_ent_type = self.graph.nodes[target_ent].get('ent_type')
                    if this_ent_type == target_ent_type:
                        target_ents_set[target_ent] = None # orderd set
                    else:
                        # TODO we may have passed the target already
                        ent_set[target_ent] = None # orderd set
            ents = ent_set.keys()
        return target_ents_set.keys()

    def get_point_posi(self, point):
        """Get the position ID for a point.

        :param point: A point ID from which to get the position.
        :return: A position ID. 
        """
        vert = self.get_ents(ENT_TYPE.VERTS, point)[0]
        return self.graph.successors(vert, _EDGE_TYPE.ENT)[0]

    def get_pline_posis(self, pline):
        """Get a list of position IDs for a polyline. If the polyline is closed, the first and last
        positions will be the same.

        :param pline: A polyline ID from which to get the positions.
        :return: A list of position IDs. The list may contain duplicates.
        """

        edges = self.get_ents(ENT_TYPE.EDGES, pline)
        verts = [self.graph.successors(edge, _EDGE_TYPE.ENT)[0] for edge in edges]
        posis = [self.graph.successors(vert, _EDGE_TYPE.ENT)[0] for vert in verts]
        last_vert = self.graph.successors(edges[-1], _EDGE_TYPE.ENT)[1]
        last_posi = self.graph.successors(last_vert, _EDGE_TYPE.ENT)[0]
        posis.append(last_posi)
        return posis

    def get_pgon_posis(self, pgon):
        """Get a list of lists of position IDs for an polygon. Each list represents one of the
        polygon wires. All wires are assumed to be closed. (The last position is not duplicated.)

        :param pgon: A polygon ID from which to get the positions.
        :return: A list of lists of position IDs. The lists may contain duplicates.
        """
        posis = []
        for wire in self.get_ents(ENT_TYPE.WIRES, pgon):
            verts = self.get_ents(ENT_TYPE.VERTS, wire)
            wire_posis = [self.graph.successors(vert, _EDGE_TYPE.ENT)[0] for vert in verts]
            posis.append(wire_posis)
        return posis


    # ==============================================================================================
    # QUERY
    # ==============================================================================================

    def pline_is_closed(self, pline):
        """Check if a polyline is open or closed.

        :param pline: A polyline ID.
        :return: True if closed, False if open.
        """
        edges = self.graph.successors(self.graph.successors(pline, _EDGE_TYPE.ENT)[0], _EDGE_TYPE.ENT)
        start = self.graph.successors(self.graph.successors(edges[0], _EDGE_TYPE.ENT)[0], _EDGE_TYPE.ENT)
        end = self.graph.successors(self.graph.successors(edges[-1], _EDGE_TYPE.ENT)[1], _EDGE_TYPE.ENT)
        return start == end

    # ==============================================================================================
    # EXPORT
    # ==============================================================================================

    def info(self):
        """Print information about the model. This is mainly used for debugging.
        
        :return: A string describing the data in the model.
        """
        nodes = map(lambda n: '- ' + n + ': ' + str(self.graph.nodes[n]), self.graph.nodes)
        nodes = '\n'.join(nodes)
        all_edges = ''
        for edge_type in self.graph.edge_types:
            edges = map(lambda e: '- ' + e + ': ' + str(self.graph.edges[edge_type][e]), self.graph.edges[edge_type])
            edges = '\n'.join(edges)
            all_edges = all_edges + '\n EDGES: ' + edge_type + '\n' + edges + '\n'
        return 'NODES: \n' + nodes + '\n' + all_edges + '\n\n\n'

    def to_json(self):
        """Return JSON representing that data in the model.
        
        :return: JSON data.
        """
        # get entities from graph
        posi_ents = self.graph.successors(ENT_TYPE.POSIS, _EDGE_TYPE.META)
        vert_ents = self.graph.successors(ENT_TYPE.VERTS, _EDGE_TYPE.META)
        edge_ents = self.graph.successors(ENT_TYPE.EDGES, _EDGE_TYPE.META)
        wire_ents = self.graph.successors(ENT_TYPE.WIRES, _EDGE_TYPE.META)
        point_ents = self.graph.successors(ENT_TYPE.POINTS, _EDGE_TYPE.META)
        pline_ents = self.graph.successors(ENT_TYPE.PLINES, _EDGE_TYPE.META)
        pgon_ents = self.graph.successors(ENT_TYPE.PGONS, _EDGE_TYPE.META)
        coll_ents = self.graph.successors(ENT_TYPE.COLLS, _EDGE_TYPE.META)
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
            'num_posis': self.graph.degree(ENT_TYPE.POSIS, _EDGE_TYPE.META),
            'points': [],
            'plines': [],
            'pgons': [],
            'coll_points': [],
            'coll_plines': [],
            'coll_pgons':  [],
            'coll_colls': []
        }
        for point_ent in point_ents:
            posi_i = self.get_point_posi(point_ent)
            geometry['points'].append(posis_dict[posi_i])
        for pline_ent in pline_ents:
            posis_i = self.get_pline_posis(pline_ent)
            geometry['plines'].append([posis_dict[posi_i] for posi_i in posis_i])
        for pgon_ent in pgon_ents:
            wires_posis_i = self.get_pgon_posis(pgon_ent)
            geometry['pgons'].append([[posis_dict[posi_i] for posi_i in posis_i] for posis_i in wires_posis_i])
        for coll_ent in coll_ents:
            geometry['coll_points'].append([])
            geometry['coll_plines'].append([])
            geometry['coll_pgons'].append([])
            geometry['coll_colls'].append([])
            for ent in self.graph.successors(coll_ent, _EDGE_TYPE.ENT):
                ent_type = self.graph.nodes[ent].get('ent_type')
                if ent_type == ENT_TYPE.POINTS:
                    geometry['coll_points'][-1].append(points_dict[ent])
                elif ent_type == ENT_TYPE.PLINES:
                    geometry['coll_plines'][-1].append(plines_dict[ent])
                elif ent_type == ENT_TYPE.PGONS:
                    geometry['coll_pgons'][-1].append(pgons_dict[ent])
                elif ent_type == ENT_TYPE.COLLS:
                    geometry['coll_colls'][-1].append(colls_dict[ent])
        # get attribs from graph
        posi_attribs = self.graph.successors(ENT_TYPE.POSIS + '_attribs', _EDGE_TYPE.META)
        vert_attribs = self.graph.successors(ENT_TYPE.VERTS + '_attribs', _EDGE_TYPE.META)
        edge_attribs = self.graph.successors(ENT_TYPE.EDGES + '_attribs', _EDGE_TYPE.META)
        wire_attribs = self.graph.successors(ENT_TYPE.WIRES + '_attribs', _EDGE_TYPE.META)
        point_attribs = self.graph.successors(ENT_TYPE.POINTS + '_attribs', _EDGE_TYPE.META)
        pline_attribs = self.graph.successors(ENT_TYPE.PLINES + '_attribs', _EDGE_TYPE.META)
        pgon_attribs = self.graph.successors(ENT_TYPE.PGONS + '_attribs', _EDGE_TYPE.META)
        coll_attribs = self.graph.successors(ENT_TYPE.COLLS + '_attribs', _EDGE_TYPE.META)
        # create the attribute data
        def _attribData(attribs, ent_dict):
            attribs_data = []
            for att_n in attribs:
                data = OrderedDict()
                att_vals_n = self.graph.predecessors(att_n, _EDGE_TYPE.ATTRIB)
                data['name'] = self.graph.nodes[att_n].get('name')
                data['data_type'] = self.graph.nodes[att_n].get('data_type')
                data['values'] = []
                data['entities'] = []
                for att_val_n in att_vals_n:
                    data['values'].append(self.graph.nodes[att_val_n].get('value'))
                    idxs = [ent_dict[ent] for ent in self.graph.predecessors(att_val_n, _EDGE_TYPE.ATTRIB)]
                    data['entities'].append(idxs)
                attribs_data.append(data)
            return attribs_data
        attributes = {
            'posis': _attribData(posi_attribs, posis_dict),
            'verts': _attribData(vert_attribs, verts_dict),
            'edges': _attribData(edge_attribs, edges_dict),
            'wires': _attribData(wire_attribs, wires_dict),
            'points': _attribData(point_attribs, points_dict),
            'plines': _attribData(pline_attribs, plines_dict),
            'pgons': _attribData(pgon_attribs, pgons_dict),
            'colls': _attribData(coll_attribs, colls_dict),
            'model': list(self.graph.data.items())
        }
        # create the json
        data = {
            'type': 'SIM',
            'version': '0.1',
            'geometry': geometry,
            'attributes': attributes
        }
        return data

    def to_json_str(self):
        """Return a JSON formatted string representing that data in the model.
        
        :return: A JSON string in the SIM format.
        """
        return json.dumps(self.to_json())