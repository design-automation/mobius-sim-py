import json
from sim_model import graph

# ==================================================================================================
# Constants
# ==================================================================================================

# ENT_TYPE
class ENT_TYPE():
    POSIS = 'posis'
    VERTS = 'verts'
    EDGES = 'edges'
    WIRES = 'wires'
    POINTS = 'points'
    PLINES = 'plines'
    PGONS = 'pgons'
    COLLS = 'colls'
    MODEL = 'model'

# Attribs
class ATTRIB_TYPE():
    POSIS_ATTRIBS = 'posis_attribs'
    VERTS_ATTRIBS = 'verts_attribs'
    EDGES_ATTRIBS = 'edges_attribs'
    WIRES_ATTRIBS = 'wires_attribs'
    POINTS_ATTRIBS = 'points_attribs'
    PLINES_ATTRIBS = 'plines_attribs'
    PGONS_ATTRIBS = 'pgons_attribs'
    COLLS_ATTRIBS = 'colls_attribs'
    ATTRIB_VALS = 'attrib_vals'

# DATA_TYPE
class DATA_TYPE():
    NUM = 'number'
    STR =  'string'
    BOOL =  'boolean'
    LIST =  'list'
    DICT =  'dict'

# NODE_TYPE
class NODE_TYPE():
    ENT = 'entity'
    ATTRIB =  'attrib'
    ATTRIB_VAL =  'attrib_val'
    META = 'meta'

# EDGE TYPE
class EDGE_TYPE():
    ENT = 'entity'
    ATTRIB =  'attrib'
    META = 'meta'

# ENT_TYPES FOR COLLECTIONS
COLL_ENT_TYPES = [ENT_TYPE.POINTS, ENT_TYPE.PLINES, ENT_TYPE.PGONS, ENT_TYPE.COLLS]

# NAME OF XYZ ATTRIB NODE_TYPE
POSIS_ATT_XYZ = 'att_posis_xyz'

# ENT PREFIX
ENT_PREFIX = {
    'posis':  'ps',
    'verts': '_v',
    'edges': '_e',
    'wires': '_w',
    'points': 'pt',
    'plines': 'pl',
    'pgons': 'pg',
    'colls': 'co'
}

# ==================================================================================================
# Class for reading and writing Spatial Information Models
# ==================================================================================================

class SIM():

    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================

    def __init__(self):

       # graph
        self.graph = graph.Graph([EDGE_TYPE.ENT,EDGE_TYPE.ATTRIB, EDGE_TYPE.META])

        # create meta nodes
        meta = [ENT_TYPE.POSIS, ENT_TYPE.VERTS, ENT_TYPE.EDGES, ENT_TYPE.WIRES, 
            ENT_TYPE.POINTS, ENT_TYPE.PLINES, ENT_TYPE.PGONS, ENT_TYPE.COLLS]
        for ent_type in meta:
            self.graph.add_node(ent_type, node_type = NODE_TYPE.META)
            self.graph.add_node(ent_type + '_attribs', node_type = NODE_TYPE.META)
            # self.graph.add_node(ent_type + '_attrib_vals', node_type = NODE_TYPE.META)

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
        n = ENT_PREFIX[enty_type] + str(self.graph.degree(enty_type, edge_type = EDGE_TYPE.META))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = enty_type)
        self.graph.add_edge(enty_type, n, edge_type = EDGE_TYPE.META)
        return n

    def _graph_attrib_node_name(self, ent_type, name):
        return 'att_' + ent_type + '_' + name

    def _graph_add_attrib(self, ent_type, name, data_type):
        n = self._graph_attrib_node_name( ent_type, name)
        self.graph.add_node(n, node_type = NODE_TYPE.ATTRIB, ent_type = ent_type,
                name = name, data_type = data_type)
        self.graph.add_edge(ent_type + '_attribs', n, edge_type = EDGE_TYPE.META)
        return n

    def _graph_attrib_val_node_name(self, value):
        return 'val_' + str(value)

    def _graph_add_attrib_val(self, value):
        n = self._graph_attrib_val_node_name(value)
        self.graph.add_node(n, node_type = NODE_TYPE.ATTRIB_VAL, value = value)
        return n

    # ==============================================================================================
    # ADD METHODS FOR ENTITIES
    # ==============================================================================================

    def add_posi(self, xyz: list):
        posi_n = self._graph_add_ent(ENT_TYPE.POSIS)
        self.set_attrib_val(posi_n, POSIS_ATT_XYZ, xyz)
        return posi_n

    def add_point(self, posi_n: str):
        vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
        point_n = self._graph_add_ent(ENT_TYPE.POINTS)
        self.graph.add_edge(vert_n, posi_n, edge_type = EDGE_TYPE.ENT)
        self.graph.add_edge(point_n, vert_n, edge_type = EDGE_TYPE.ENT)
        return point_n

    def add_pline(self, posis_n: list, closed: bool):
        # vertices
        verts_n = []
        for posi_n in posis_n:
            vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
            self.graph.add_edge(vert_n, posi_n, edge_type = EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        if closed:
            verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, v0, edge_type = EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, v1, edge_type = EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graph_add_ent(ENT_TYPE.WIRES)
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], edge_type = EDGE_TYPE.ENT)
        # pline
        pline_n = self._graph_add_ent(ENT_TYPE.PLINES)
        self.graph.add_edge(pline_n, wire_n, edge_type = EDGE_TYPE.ENT)
        #  return
        return pline_n

    def add_pgon(self, posis_n: list):
        # vertices
        verts_n = []
        for posi_n in posis_n:
            vert_n = self._graph_add_ent(ENT_TYPE.VERTS)
            self.graph.add_edge(vert_n, posi_n, edge_type = EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graph_add_ent(ENT_TYPE.EDGES)
            self.graph.add_edge(edge_n, v0, edge_type = EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, v1, edge_type = EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graph_add_ent(ENT_TYPE.WIRES)
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], edge_type = EDGE_TYPE.ENT)
        # pline
        pgon_n = self._graph_add_ent(ENT_TYPE.PGONS)
        self.graph.add_edge(pgon_n, wire_n, edge_type = EDGE_TYPE.ENT)
        #  return
        return pgon_n

    def add_coll(self):
        return self._graph_add_ent(ENT_TYPE.COLLS)

    def add_coll_ent(self, coll_n, ent_n):
        ent_type = self.graph.nodes[ent_n].get('ent_type')
        if ent_type not in COLL_ENT_TYPES:
            raise Exception('Invalid entitiy for collections.')
        self.graph.add_edge(coll_n, ent_n, edge_type = EDGE_TYPE.ENT)

    # ==============================================================================================
    # ATTRIBUTE METHODS
    # ==============================================================================================
        
    def get_attrib(self, ent_type, name):
        att_n = self._graph_attrib_node_name(ent_type, name)
        return att_n

    def add_attrib(self, ent_type, name, data_type):
        att_n = self._graph_attrib_node_name(ent_type, name)
        if self.graph.nodes.get(att_n) == None:
            self._graph_add_attrib(ent_type, name, data_type)
        elif self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute already exists with different data type')
        return att_n
            
    def set_attrib_val(self, ent_n, att_n, value):
        if self.graph.nodes[ent_n].get('ent_type') != self.graph.nodes[att_n].get('ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._check_type(value)
        if self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(value))
        att_val_n = self._graph_add_attrib_val(value)
        self.graph.add_edge(ent_n, att_val_n, edge_type = EDGE_TYPE.ATTRIB) # ent -> att_val
        self.graph.add_edge(att_val_n, att_n, edge_type = EDGE_TYPE.ATTRIB) # att_val -> att
        
    def get_attrib_val(self, ent_n, att_n):
        att_vals_n = self.graph.successors(ent_n, EDGE_TYPE.ATTRIB)
        for att_val_n in att_vals_n:
            atts_n = self.graph.successors(att_val_n, EDGE_TYPE.ATTRIB)
            if atts_n and atts_n[0] == att_n:
                return self.graph.nodes[att_val_n].get('value')
        return None

    def set_model_attrib_val(self, name, value):
        self.graph.data[name] = value

    def get_model_attrib_val(self, name):
        return self.graph.data[name]

    # ==============================================================================================
    # GET METHODS FOR ENTITIES
    # ==============================================================================================

    def get_ents(self, ent_type):
        return self.graph.successors(ent_type)

    def num_ents(self, ent_type):
        return self.graph.degree(ent_type)

    # ==============================================================================================
    # EXPORT
    # ==============================================================================================

    def info(self):
        nodes = map(lambda n: '- ' + n + ': ' + str(self.graph.nodes[n]), self.graph.nodes)
        nodes = '\n'.join(nodes)
        all_edges = ''
        for edge_type in self.graph.edge_types:
            edges = map(lambda e: '- ' + e + ': ' + str(self.graph.edges[edge_type][e]), self.graph.edges[edge_type])
            edges = '\n'.join(edges)
            all_edges = all_edges + '\n EDGES: ' + edge_type + '\n' + edges + '\n'
        return 'NODES: \n' + nodes + '\n' + all_edges + '\n\n\n'

    def json_str(self):
        # get entities from graph
        posi_ents = self.graph.successors(ENT_TYPE.POSIS, EDGE_TYPE.META)
        vert_ents = self.graph.successors(ENT_TYPE.VERTS, EDGE_TYPE.META)
        edge_ents = self.graph.successors(ENT_TYPE.EDGES, EDGE_TYPE.META)
        wire_ents = self.graph.successors(ENT_TYPE.WIRES, EDGE_TYPE.META)
        point_ents = self.graph.successors(ENT_TYPE.POINTS, EDGE_TYPE.META)
        pline_ents = self.graph.successors(ENT_TYPE.PLINES, EDGE_TYPE.META)
        pgon_ents = self.graph.successors(ENT_TYPE.PGONS, EDGE_TYPE.META)
        coll_ents = self.graph.successors(ENT_TYPE.COLLS, EDGE_TYPE.META)
        # get attribs from graph
        posi_attribs = self.graph.successors(ATTRIB_TYPE.POSIS_ATTRIBS, EDGE_TYPE.META)
        vert_attribs = self.graph.successors(ATTRIB_TYPE.VERTS_ATTRIBS, EDGE_TYPE.META)
        edge_attribs = self.graph.successors(ATTRIB_TYPE.EDGES_ATTRIBS, EDGE_TYPE.META)
        wire_attribs = self.graph.successors(ATTRIB_TYPE.WIRES_ATTRIBS, EDGE_TYPE.META)
        point_attribs = self.graph.successors(ATTRIB_TYPE.POINTS_ATTRIBS, EDGE_TYPE.META)
        pline_attribs = self.graph.successors(ATTRIB_TYPE.PLINES_ATTRIBS, EDGE_TYPE.META)
        pgon_attribs = self.graph.successors(ATTRIB_TYPE.PGONS_ATTRIBS, EDGE_TYPE.META)
        coll_attribs = self.graph.successors(ATTRIB_TYPE.COLLS_ATTRIBS, EDGE_TYPE.META)
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
            'num_posis': self.graph.degree(ENT_TYPE.POSIS, EDGE_TYPE.META),
            'verts': [posis_dict[self.graph.successors(vert_ent, EDGE_TYPE.ENT)[0]] for vert_ent in vert_ents],
            'edges': [[verts_dict[vert] for vert in self.graph.successors(edge_ent, EDGE_TYPE.ENT)] for edge_ent in edge_ents],
            'wires': [[edges_dict[edge] for edge in self.graph.successors(wire_ent, EDGE_TYPE.ENT)] for wire_ent in wire_ents],
            'points': [verts_dict[self.graph.successors(point_ent, EDGE_TYPE.ENT)[0]] for point_ent in point_ents],
            'plines': [wires_dict[self.graph.successors(pline_ent, EDGE_TYPE.ENT)[0]] for pline_ent in pline_ents],
            'pgons': [[wires_dict[wire] for wire in self.graph.successors(pgon_ent, EDGE_TYPE.ENT)] for pgon_ent in pgon_ents],
            'coll_points': [],
            'coll_plines': [],
            'coll_pgons':  [],
            'coll_colls': []
        }
        for coll_ent in coll_ents:
            geometry['coll_points'].append([])
            geometry['coll_plines'].append([])
            geometry['coll_pgons'].append([])
            geometry['coll_colls'].append([])
            for ent in self.graph.successors(coll_ent, EDGE_TYPE.ENT):
                ent_type = self.graph.nodes[ent].get('ent_type')
                if ent_type == ENT_TYPE.POINTS:
                    geometry['coll_points'][-1].append(points_dict[ent])
                elif ent_type == ENT_TYPE.PLINES:
                    geometry['coll_plines'][-1].append(plines_dict[ent])
                elif ent_type == ENT_TYPE.PGONS:
                    geometry['coll_pgons'][-1].append(pgons_dict[ent])
                elif ent_type == ENT_TYPE.COLLS:
                    geometry['coll_colls'][-1].append(colls_dict[ent])
        # create the attribute data
        def _attribData(attribs, ent_dict):
            data = {}
            for att_n in attribs:
                att_vals_n = self.graph.predecessors(att_n, EDGE_TYPE.ATTRIB)
                data['name'] = self.graph.nodes[att_n].get('name')
                data['data_type'] = self.graph.nodes[att_n].get('data_type')
                data['data_vals'] = []
                data['data_ents'] = []
                for att_val_n in att_vals_n:
                    data['data_vals'].append(self.graph.nodes[att_val_n].get('value'))
                    idxs = [ent_dict[ent] for ent in self.graph.predecessors(att_val_n, EDGE_TYPE.ATTRIB)]
                    data['data_ents'].append(idxs)
            return data
        attributes = {
            'posis': _attribData(posi_attribs, posis_dict),
            'verts': _attribData(vert_attribs, verts_dict),
            'edges': _attribData(edge_attribs, edges_dict),
            'wires': _attribData(wire_attribs, wires_dict),
            'points': _attribData(point_attribs, points_dict),
            'plines': _attribData(pline_attribs, plines_dict),
            'pgons': _attribData(pgon_attribs, pgons_dict),
            'colls': _attribData(coll_attribs, colls_dict),
            'model': self.graph.data
        }
        # create the json
        data = {
            'type': 'SIM',
            'version': '0.1',
            'geometry': geometry,
            'attributes': attributes
        }
        return json.dumps(data)


