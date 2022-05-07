from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from sim_model import sim
ENT_TYPE = sim.ENT_TYPE
DATA_TYPE = sim.DATA_TYPE

class TestClosedPolylines(unittest.TestCase):

    def setUp(self):
        m = sim.SIM()
        pline = m.add_pline(
            [m.add_posi([1,2,3]), m.add_posi([4,5,7]), m.add_posi([2,2,2])],
            True # closed
        )
        coll = m.add_coll()
        m.add_coll_ent(coll, pline)
        self.model = m

    def test_get_pline(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        self.assertEqual(list(plines), ['pl0'])

    def test_pline_to_posis(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        posis = self.model.get_ents(ENT_TYPE.POSIS, plines)
        self.assertEqual(list(posis), ['ps0', 'ps1', 'ps2'])

    def test_pline_to_verts(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        verts = self.model.get_ents(ENT_TYPE.VERTS, plines)
        self.assertEqual(list(verts), ['_v0', '_v1', '_v2'])

    def test_pline_to_edges(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        edges = self.model.get_ents(ENT_TYPE.EDGES, plines)
        self.assertEqual(list(edges), ['_e0', '_e1', '_e2'])

    def test_pline_to_wires(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        wires = self.model.get_ents(ENT_TYPE.WIRES, plines)
        self.assertEqual(list(wires), ['_w0'])

    def test_pline_to_colls(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        colls = self.model.get_ents(ENT_TYPE.COLLS, plines)
        self.assertEqual(list(colls), ['co0'])

    def test_posi_to_pline(self):
        posis = self.model.get_ents(ENT_TYPE.POSIS)
        pline = self.model.get_ents(ENT_TYPE.PLINES, posis[0])
        self.assertEqual(list(pline), ['pl0'])

    def test_vert_to_pline(self):
        verts = self.model.get_ents(ENT_TYPE.VERTS)
        pline = self.model.get_ents(ENT_TYPE.PLINES, verts[0])
        self.assertEqual(list(pline), ['pl0'])

    def test_edge_to_pline(self):
        edges = self.model.get_ents(ENT_TYPE.EDGES)
        pline = self.model.get_ents(ENT_TYPE.PLINES, edges[0])
        self.assertEqual(list(pline), ['pl0'])

    def test_wire_to_pline(self):
        wires = self.model.get_ents(ENT_TYPE.WIRES)
        pline = self.model.get_ents(ENT_TYPE.PLINES, wires[0])
        self.assertEqual(list(pline), ['pl0'])

    def test_coll_to_pline(self):
        colls = self.model.get_ents(ENT_TYPE.COLLS)
        pline = self.model.get_ents(ENT_TYPE.PLINES, colls[0])
        self.assertEqual(list(pline), ['pl0'])

if __name__ == '__main__':
    unittest.main()