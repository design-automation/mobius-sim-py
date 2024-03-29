from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals
import unittest
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from sim_model import sim
ENT_TYPE = sim.ENT_TYPE
DATA_TYPE = sim.DATA_TYPE

class TestPolygons(unittest.TestCase):

    def setUp(self):
        m = sim.SIM()
        pgon = m.add_pgon(
            [m.add_posi([1,2,3]), m.add_posi([4,5,7]), m.add_posi([2,2,2])],
        )
        coll = m.add_coll()
        m.add_coll_ent(coll, pgon)
        self.model = m

    def test_get_pgon(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        self.assertEqual(list(pgons), ['pg0'])

    def test_pgon_to_posis(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        posis = self.model.get_ents(ENT_TYPE.POSI, pgons)
        self.assertEqual(list(posis), ['ps0', 'ps1', 'ps2'])

    def test_pgon_to_verts(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        verts = self.model.get_ents(ENT_TYPE.VERT, pgons)
        self.assertEqual(list(verts), ['_v0', '_v1', '_v2'])

    def test_pgon_to_edges(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        edges = self.model.get_ents(ENT_TYPE.EDGE, pgons)
        self.assertEqual(list(edges), ['_e0', '_e1', '_e2'])

    def test_pgon_to_wires(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        wires = self.model.get_ents(ENT_TYPE.WIRE, pgons)
        self.assertEqual(list(wires), ['_w0'])

    def test_pgon_to_colls(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        colls = self.model.get_ents(ENT_TYPE.COLL, pgons)
        self.assertEqual(list(colls), ['co0'])

    def test_posi_to_pgon(self):
        posis = self.model.get_ents(ENT_TYPE.POSI)
        pgon = self.model.get_ents(ENT_TYPE.PGON, posis[0])
        self.assertEqual(list(pgon), ['pg0'])

    def test_vert_to_pgon(self):
        verts = self.model.get_ents(ENT_TYPE.VERT)
        pgon = self.model.get_ents(ENT_TYPE.PGON, verts[0])
        self.assertEqual(list(pgon), ['pg0'])

    def test_edge_to_pgon(self):
        edges = self.model.get_ents(ENT_TYPE.EDGE)
        pgon = self.model.get_ents(ENT_TYPE.PGON, edges[0])
        self.assertEqual(list(pgon), ['pg0'])

    def test_wire_to_pgon(self):
        wires = self.model.get_ents(ENT_TYPE.WIRE)
        pgon = self.model.get_ents(ENT_TYPE.PGON, wires[0])
        self.assertEqual(list(pgon), ['pg0'])

    def test_coll_to_pgon(self):
        colls = self.model.get_ents(ENT_TYPE.COLL)
        pgon = self.model.get_ents(ENT_TYPE.PGON, colls[0])
        self.assertEqual(list(pgon), ['pg0'])

if __name__ == '__main__':
    unittest.main()