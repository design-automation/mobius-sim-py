import json
import networkx as nx

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

# ==================================================================================================
# Class for reading and writing Spatial Information Models
# ==================================================================================================

class SIM():
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================

    def __init__(self):

       # graph
        self.graph = nx.DiGraph()

        # graph view entity edges only
        def ent_filter_edge(n1, n2):
            return self.graph[n1][n2].get("edge_type") == EDGE_TYPE.ENT
        self.vw_ent_edges = nx.subgraph_view(self.graph, filter_edge=ent_filter_edge)

        # graph view attrib edges only
        def attrib_filter_edge(n1, n2):
            return self.graph[n1][n2].get("edge_type") == EDGE_TYPE.ATTRIB
        self.vw_attrib_edges = nx.subgraph_view(self.graph, filter_edge=attrib_filter_edge)

        # create meta nodes
        for ent_type in [ENT_TYPE.POSIS, ENT_TYPE.VERTS, ENT_TYPE.EDGES, ENT_TYPE.WIRES, 
            ENT_TYPE.POINTS, ENT_TYPE.PLINES, ENT_TYPE.PGONS, ENT_TYPE.COLLS ]:
            self.graph.add_node(ent_type, node_type = NODE_TYPE.META)
            self.graph.add_node(ent_type + '_attribs', node_type = NODE_TYPE.META)
            # self.graph.add_node(ent_type + '_attrib_vals', node_type = NODE_TYPE.META)

        # add xyz attrib
        self._graphAddAttrib(ENT_TYPE.POSIS, 'xyz', DATA_TYPE.LIST)

    # ==============================================================================================
    # UTILITY 
    # ==============================================================================================

    def _checkType(self, value):
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

    def _graphAddPosi(self):
        n = 'ps' + str(nx.degree(self.graph, ENT_TYPE.POSIS))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.POSIS)
        self.graph.add_edge(ENT_TYPE.POSIS, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddVert(self):
        n = '_v' + str(nx.degree(self.graph, ENT_TYPE.VERTS))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.VERTS)
        self.graph.add_edge(ENT_TYPE.VERTS, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddEdge(self):
        n = '_e' + str(nx.degree(self.graph, ENT_TYPE.EDGES))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.EDGES)
        self.graph.add_edge(ENT_TYPE.EDGES, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddWire(self):
        n = '_w' + str(nx.degree(self.graph, ENT_TYPE.WIRES))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.WIRES)
        self.graph.add_edge(ENT_TYPE.WIRES, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddPoint(self):
        n = 'pt' + str(nx.degree(self.graph, ENT_TYPE.POINTS))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.POINTS)
        self.graph.add_edge(ENT_TYPE.POINTS, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddPline(self):
        n = 'pl' + str(nx.degree(self.graph, ENT_TYPE.PLINES))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.PLINES)
        self.graph.add_edge(ENT_TYPE.PLINES, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddPgon(self):
        n = 'pg' + str(nx.degree(self.graph, ENT_TYPE.PGONS))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.PGONS)
        self.graph.add_edge(ENT_TYPE.PGONS, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAddColl(self):
        n = 'co' + str(nx.degree(self.graph, ENT_TYPE.COLLS))
        self.graph.add_node(n, node_type = NODE_TYPE.ENT, ent_type = ENT_TYPE.COLLS)
        self.graph.add_edge(ENT_TYPE.COLLS, n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAttribNodeName(self, ent_type, name):
        return 'att_' + ent_type + '_' + name

    def _graphAddAttrib(self, ent_type, name, data_type):
        n = self._graphAttribNodeName( ent_type, name)
        self.graph.add_node(n, node_type = NODE_TYPE.ATTRIB, ent_type = ent_type,
                name = name, data_type = data_type)
        self.graph.add_edge(ent_type + '_attribs', n, edge_type = EDGE_TYPE.META)
        return n

    def _graphAttribValNodeName(self, value):
        return 'val_' + str(value)

    def _graphAddAttribVal(self, value):
        n = self._graphAttribValNodeName(value)
        self.graph.add_node(n, node_type = NODE_TYPE.ATTRIB_VAL, value = value)
        self.graph.add_edge(ATTRIB_TYPE.ATTRIB_VALS, n, edge_type = EDGE_TYPE.META)
        return n

    # ==============================================================================================
    # ADD METHODS FOR ENT_TYPE
    # ==============================================================================================

    def addPosi(self, xyz: list):
        posi_n = self._graphAddPosi()
        self.setEntAttribVal(posi_n, POSIS_ATT_XYZ, xyz)
        return posi_n

    def addPoint(self, posi_n: str):
        vert_n = self._graphAddVert()
        point_n = self._graphAddPoint()
        self.graph.add_edge(vert_n, posi_n, edge_type = EDGE_TYPE.ENT)
        self.graph.add_edge(point_n, vert_n, edge_type = EDGE_TYPE.ENT)
        return point_n

    def addPline(self, posis_n: list, closed: bool):
        # vertices
        verts_n = []
        for posi_n in posis_n:
            vert_n = self._graphAddVert()
            self.graph.add_edge(vert_n, posi_n, edge_type = EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        if closed:
            verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graphAddEdge()
            self.graph.add_edge(edge_n, v0, i = 0, edge_type = EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, v1, i = 1, edge_type = EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graphAddWire()
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], i = i, edge_type = EDGE_TYPE.ENT)
        # pline
        pline_n = self._graphAddPline()
        self.graph.add_edge(pline_n, wire_n, edge_type = EDGE_TYPE.ENT)
        #  return
        return pline_n

    def addPgon(self, posis_n: list):
        # vertices
        verts_n = []
        for posi_n in posis_n:
            vert_n = self._graphAddVert()
            self.graph.add_edge(vert_n, posi_n, edge_type = EDGE_TYPE.ENT)
            verts_n.append(vert_n)
        verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graphAddEdge()
            self.graph.add_edge(edge_n, v0, i = 0, edge_type = EDGE_TYPE.ENT)
            self.graph.add_edge(edge_n, v1, i = 1, edge_type = EDGE_TYPE.ENT)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graphAddWire()
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], i = i, edge_type = EDGE_TYPE.ENT)
        # pline
        pgon_n = self._graphAddPgon()
        self.graph.add_edge(pgon_n, wire_n, i=0, edge_type = EDGE_TYPE.ENT)
        #  return
        return pgon_n

    def addColl(self):
        return self._graphAddColl()

    def addCollEnt(self, coll_n, ent_n):
        ent_type = self.graph.nodes[ent_n].get('ent_type')
        if ent_type not in COLL_ENT_TYPES:
            raise Exception('Invalid entitiy for collections.')
        self.graph.add_edge(coll_n, ent_n, edge_type = EDGE_TYPE.ENT)

    # ==============================================================================================
    # ATTRIBUTE METHODS
    # ==============================================================================================
        
    def getAttrib(self, ent_type, name):
        att_n = self._graphAttribNodeName(ent_type, name)
        return att_n

    def addAttrib(self, ent_type, name, data_type):
        att_n = self._graphAttribNodeName(ent_type, name)
        if self.graph.nodes.get(att_n) == None:
            self._graphAddAttrib(ent_type, name, data_type)
        elif self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute already exists with different data type')
        return att_n
            
    def setEntAttribVal(self, ent_n, att_n, value):
        if self.graph.nodes[ent_n].get('ent_type') != self.graph.nodes[att_n].get('ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._checkType(value)
        if self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(value))
        att_val_n = self._graphAddAttribVal(value)
        self.graph.add_edge(ent_n, att_val_n, edge_type = EDGE_TYPE.ATTRIB) # ent -> att_val
        self.graph.add_edge(att_val_n, att_n, edge_type = EDGE_TYPE.ATTRIB) # att_val -> att
        
    def getEntAttribVal(self, ent_n, att_n):
        att_vals_n = list(self.vw_attrib_edges.successors(ent_n))
        for att_val_n in att_vals_n:
            atts_n = list(self.vw_attrib_edges.successors(att_val_n))
            if atts_n and atts_n[0] == att_n:
                return self.graph.nodes[att_val_n].get('value')
        return None

    def setModelAttribVal(self, name, value):
        self.graph.graph[name] = value

    def getModelAttribVal(self, name):
        return self.graph.graph[name]

    # ==============================================================================================
    # GET METHODS FOR ENTITIES
    # ==============================================================================================

    def getEnts(self, ent_type):
        return list(self.graph.successors(ent_type))

    def numEnts(self, ent_type):
        return nx.degree(self.graph, ent_type)


    # ==============================================================================================
    # EXPORT
    # ==============================================================================================

    def info(self):
        nodes = map(lambda n: str(n), self.graph.nodes.data())
        nodes = '\n'.join(nodes)
        edges = map(lambda n: str(n), self.graph.edges.data())
        edges = '\n'.join(edges)
        return 'Nodes: \n' + nodes + '\n' + 'Edges: \n' + edges + '\n\n\n'

    def toStr(self):
        # entities
        posi_ents = list(self.graph.successors(ENT_TYPE.POSIS))
        vert_ents = list(self.graph.successors(ENT_TYPE.VERTS))
        edge_ents = list(self.graph.successors(ENT_TYPE.EDGES))
        wire_ents = list(self.graph.successors(ENT_TYPE.WIRES))
        point_ents = list(self.graph.successors(ENT_TYPE.POINTS))
        pline_ents = list(self.graph.successors(ENT_TYPE.PLINES))
        pgon_ents = list(self.graph.successors(ENT_TYPE.PGONS))
        coll_ents = list(self.graph.successors(ENT_TYPE.COLLS))
        # attribs
        posi_attribs = list(self.graph.successors(ATTRIB_TYPE.POSIS_ATTRIBS))
        vert_attribs = list(self.graph.successors(ATTRIB_TYPE.VERTS_ATTRIBS))
        edge_attribs = list(self.graph.successors(ATTRIB_TYPE.EDGES_ATTRIBS))
        wire_attribs = list(self.graph.successors(ATTRIB_TYPE.WIRES_ATTRIBS))
        point_attribs = list(self.graph.successors(ATTRIB_TYPE.POINTS_ATTRIBS))
        pline_attribs = list(self.graph.successors(ATTRIB_TYPE.PLINES_ATTRIBS))
        pgon_attribs = list(self.graph.successors(ATTRIB_TYPE.PGONS_ATTRIBS))
        coll_attribs = list(self.graph.successors(ATTRIB_TYPE.COLLS_ATTRIBS))
        # map for entity name -> entity index
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
            'num_posis': nx.degree(self.graph, ENT_TYPE.POSIS),
            'verts': [posis_dict[list(self.vw_ent_edges.successors(vert_ent))[0]] for vert_ent in vert_ents],
            'edges': [[verts_dict[vert] for vert in self.vw_ent_edges.successors(edge_ent)] for edge_ent in edge_ents],
            'wires': [[edges_dict[edge] for edge in self.vw_ent_edges.successors(wire_ent)] for wire_ent in wire_ents],
            'points': [verts_dict[list(self.vw_ent_edges.successors(point_ent))[0]] for point_ent in point_ents],
            'plines': [wires_dict[list(self.vw_ent_edges.successors(pline_ent))[0]] for pline_ent in pline_ents],
            'pgons': [[wires_dict[wire] for wire in self.vw_ent_edges.successors(pgon_ent)] for pgon_ent in pgon_ents],
            'coll_points': [],
            'coll_plines': [],
            'coll_pgons':  [],
            'coll_childs': []
        }
        for coll_ent in coll_ents:
            geometry['coll_points'].append([])
            geometry['coll_plines'].append([])
            geometry['coll_pgons'].append([])
            geometry['coll_childs'].append([])
            for ent in list(self.vw_ent_edges.successors(coll_ent)):
                ent_type = self.graph.nodes[ent].get('ent_type')
                if ent_type == ENT_TYPE.POINTS:
                    geometry['coll_points'][-1].append(points_dict[ent])
                elif ent_type == ENT_TYPE.PLINES:
                    geometry['coll_plines'][-1].append(plines_dict[ent])
                elif ent_type == ENT_TYPE.PGONS:
                    geometry['coll_pgons'][-1].append(pgons_dict[ent])
                elif ent_type == ENT_TYPE.COLLS:
                    geometry['coll_childs'][-1].append(colls_dict[ent])
        # create the attribute data
        def _attribData(attribs, ent_dict):
            data = {}
            for att_n in attribs:
                att_vals_n = list(self.vw_attrib_edges.predecessors(att_n))
                data['name'] = self.graph.nodes[att_n].get('name')
                data['data_type'] = self.graph.nodes[att_n].get('data_type')
                data['data_vals'] = []
                data['data_ents'] = []
                for att_val_n in att_vals_n:
                    data['data_vals'].append(self.graph.nodes[att_val_n].get('value'))
                    idxs = [ent_dict[ent] for ent in list(self.vw_attrib_edges.predecessors(att_val_n))]
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
            'colls': _attribData(coll_attribs, colls_dict)
        }
        # create the json
        # TODO Modle attributes
        data = {
            'type': 'SIM',
            'version': '0.9',
            'geometry': geometry,
            'attributes': attributes
        }
        return json.dumps(data)


