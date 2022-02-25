import json
import networkx as nx

# ==================================================================================================
# Constants
# ==================================================================================================

# ENT TYPE
class ENT():
    POSIS = 'posis'
    VERTS = 'verts'
    EDGES = 'edges'
    WIRES = 'wires'
    POINTS = 'points'
    PLINES = 'plines'
    PGONS = 'pgons'
    COLLS = 'colls'
    MODEL = 'model'

# DATA TYPE
class TYPE():
    NUM = 'number'
    STR =  'string'
    BOOL =  'boolean'
    LIST =  'list'
    DICT =  'dict'

# NODE TYPE
class NODE():
    ENT = 'entity'
    ATTRIB =  'attrib'
    ATTRIB_VAL =  'attrib_val'

# ENTS FOR COLLECTIONS
COLL_ENTS = [ENT.POINTS, ENT.PLINES, ENT.PGONS, ENT.COLLS]

# NAME OF XYZ ATTRIB NODE
POSIS_ATT_XYZ = 'att_posis_xyz'

# ==================================================================================================
# Class for reading and writing Spatial Information Models
# ==================================================================================================

class SIM():
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================

    def __init__(self):

        # counters
        self.num_posis = 0
        self.num_verts = 0
        self.num_edges = 0
        self.num_wires = 0
        self.num_points = 0
        self.num_plines = 0
        self.num_pgons = 0
        self.num_colls = 0

        # graph
        self.graph = nx.Graph()
        self.graph.add_node(POSIS_ATT_XYZ, 
            node = NODE.ATTRIB, ent_type = ENT.POSIS, name = 'xyz', data_type = TYPE.LIST)

        # graph view of entities without attribs
        self.vw_ents = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT)

        # graph view of specific ent types with attributes
        self.vw_posis_atts = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.POSIS)
        self.vw_verts_atts = nx.subgraph_view(self.graph,  
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.VERTS)
        self.vw_edges_atts = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.EDGES)
        self.vw_wires_atts = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.WIRES)
        self.vw_points_atts = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.POINTS)
        self.vw_plines_atts = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.PLINES)
        self.vw_pgons_atts = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.PGONS)
        self.vw_colls_atts = nx.subgraph_view(self.graph,  
            lambda n: self.graph.nodes[n].get('ent_type') == ENT.COLLS)
        
        # graph view of specific ent types with attributes
        self.vw_posis = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and 
                self.graph.nodes[n].get('ent_type') == ENT.POSIS)
        self.vw_verts = nx.subgraph_view(self.graph,  
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.VERTS)
        self.vw_edges = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.EDGES)
        self.vw_wires = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.WIRES)
        self.vw_points = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.POINTS)
        self.vw_plines = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.PLINES)
        self.vw_pgons = nx.subgraph_view(self.graph, 
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.PGONS)
        self.vw_colls = nx.subgraph_view(self.graph,  
            lambda n: self.graph.nodes[n].get('node') == NODE.ENT and
                self.graph.nodes[n].get('ent_type') == ENT.COLLS)

    # ==============================================================================================
    # UTILITY 
    # ==============================================================================================

    def _graphAttribNodeName(self, ent_type, name):
        return 'att_' + ent_type + '_' + name

    def _graphAttribValNodeName(self, value):
        return 'val_' + str(value)

    def _checkType(self, value):
        val_type = type(value)
        if val_type == int or val_type == float:
            return TYPE.NUM
        if val_type == str:
            return TYPE.STR
        if val_type == bool:
            return TYPE.BOOL
        if val_type == list:
            return TYPE.LIST
        if val_type == dict:
            return TYPE.DICT
        raise Exception('Data type is not recognised.')

    # ==============================================================================================
    # GRAPH METHODS
    # ==============================================================================================

    def _graphAddPosi(self):
        n = 'ps' + str(self.num_posis)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.POSIS)
        self.num_posis += 1
        return n

    def _graphAddVert(self):
        n = '_v' + str(self.num_verts)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.VERTS)
        self.num_verts += 1
        return n

    def _graphAddEdge(self):
        n = '_e' + str(self.num_edges)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.EDGES)
        self.num_edges += 1
        return n

    def _graphAddWire(self):
        n = '_w' + str(self.num_wires)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.WIRES)
        self.num_wires += 1
        return n

    def _graphAddPoint(self):
        n = 'pt' + str(self.num_points)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.POINTS)
        self.num_points += 1
        return n

    def _graphAddPline(self):
        n = 'pl' + str(self.num_plines)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.PLINES)
        self.num_plines += 1
        return n

    def _graphAddPgon(self):
        n = 'pg' + str(self.num_pgons)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.PGONS)
        self.num_pgons += 1
        return n

    def _graphAddColl(self):
        n = 'co' + str(self.num_colls)
        self.graph.add_node(n, node = NODE.ENT, ent_type = ENT.COLLS)
        self.num_colls += 1
        return n

    # ==============================================================================================
    # ADD METHODS FOR ENTITIES
    # ==============================================================================================

    def addPosi(self, xyz: list):
        posi_n = self._graphAddPosi()
        att_val_n = self.setEntAttribVal(posi_n, POSIS_ATT_XYZ, xyz)
        # return
        return posi_n

    def addPoint(self, posi_n: str):
        vert_n = self._graphAddVert()
        point_n = self._graphAddPoint()
        self.graph.add_edge(vert_n, posi_n)
        self.graph.add_edge(point_n, vert_n)
        # return
        return point_n

    def addPline(self, posis_n: list, closed: bool):
        # vertices
        verts_n = []
        for posi_n in posis_n:
            vert_n = self._graphAddVert()
            self.graph.add_edge(vert_n, posi_n)
            verts_n.append(vert_n)
        if closed:
            verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graphAddEdge()
            self.graph.add_edge(edge_n, v0, i = 0)
            self.graph.add_edge(edge_n, v1, i = 1)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graphAddWire()
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], i = i)
        # pline
        pline_n = self._graphAddPline()
        self.graph.add_edge(pline_n, wire_n)
        #  return
        return pline_n

    def addPgon(self, posis_n: list):
        # vertices
        verts_n = []
        for posi_n in posis_n:
            vert_n = self._graphAddVert()
            self.graph.add_edge(vert_n, posi_n)
            verts_n.append(vert_n)
        verts_n.append(verts_n[0])
        # edges
        edges_n = []
        for i in range(len(verts_n) - 1):
            v0 = verts_n[i]
            v1 = verts_n[i+1]
            edge_n = self._graphAddEdge()
            self.graph.add_edge(edge_n, v0, i = 0)
            self.graph.add_edge(edge_n, v1, i = 1)
            edges_n.append(edge_n)
        # wire
        wire_n = self._graphAddWire()
        for i in range(len(edges_n)):
            self.graph.add_edge(wire_n, edges_n[i], i = i)
        # pline
        pgon_n = self._graphAddPgon()
        self.graph.add_edge(pgon_n, wire_n, i=0)
        #  return
        return pgon_n

    def addColl(self):
        return self._graphAddColl()

    def addCollEnt(self, coll_n, ent_n):
        ent_type = self.graph.nodes[ent_n].get('ent_type')
        if ent_type not in COLL_ENTS:
            raise Exception('Invalid entitiy for collections.')
        self.graph.add_edge(coll_n, ent_n)

    # ==============================================================================================
    # GET METHODS FOR ENTITIES
    # ==============================================================================================

    def getPosis(self):
        return self.vw_posis.nodes()

    def getPoints(self):
        return self.vw_points.nodes()

    def getPlines(self):
        return self.vw_plines.nodes()

    def getPgons(self):
        return self.vw_pgons.nodes()

    def getColls(self):
        return self.vw_colls.nodes()

    def getEnts(self, ent_n, ent_type):
        # TODO
        # start at ent_n and search for linked entities
        raise Exception("Not Implemented")

    # ==============================================================================================
    # ATTRIBUTE METHODS
    # ==============================================================================================
        
    def getAttrib(self, ent_type, name):
        att_n = self._graphAttribNodeName(ent_type, name)
        return att_n

    def addAttrib(self, ent_type, name, data_type):
        att_n = self._graphAttribNodeName(ent_type, name)
        if self.graph.nodes.get(att_n) == None:
            self.graph.add_node(att_n, node = NODE.ATTRIB, ent_type = ent_type,
                name = name, data_type = data_type)
        elif self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute already exists with different data type')
        return att_n
            
    def setEntAttribVal(self, ent_n, att_n, value):
        if self.graph.nodes[ent_n].get('ent_type') != self.graph.nodes[att_n].get('ent_type'):
            raise Exception('Entity and attribute have different types.')
        data_type = self._checkType(value)
        if self.graph.nodes[att_n].get('data_type') != data_type:
            raise Exception('Attribute value has the wrong data type: ' + str(value))
        att_val_n = self._graphAttribValNodeName(value)
        self.graph.add_node(att_val_n, node = NODE.ATTRIB_VAL, value = value)
        self.graph.add_edge(ent_n, att_val_n)
        self.graph.add_edge(att_n, att_val_n)
            
    def getEntAttribVal(self, ent_n, att_n):
        neighbors = list(nx.common_neighbors(self.graph, ent_n, att_n))
        if len(neighbors) == 0:
            return None
        return self.graph.nodes[neighbors[0]].get('value')
        
    def setModelAttribVal(self, name, value):
        self.graph.graph[name] = value

    def getModelAttribVal(self, name):
        return self.graph.graph[name]

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
        print(">>>>>>>>", self.graph.nodes['ps0']['node'])
        # filter only positions
        ents = nx.subgraph_view(self.graph, lambda n: self.graph.nodes[n].get('node') == NODE.ENT)
        posis = nx.subgraph_view(ents, lambda n: self.graph.nodes[n].get('ent_type') == ENT.POSIS)
        nodes = posis.nodes.data()
        return 'Nodes: ' + str(nodes)

        # data = {
        #     'type': 'SIM',
        #     'version': '0.9',
        #     'geometry': self.geometry,
        #     'attributes': self.attributes
        # }
        # return json.dumps(data)