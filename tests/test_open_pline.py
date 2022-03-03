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
            [m.add_posi([1,0,0]), m.add_posi([2,0,0]), m.add_posi([3,0,0]), m.add_posi([4,0,0])],
            False # open
        )
        coll = m.add_coll()
        m.add_coll_ent(coll, pline)
        self.model = m

    def test_get_pline(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        self.assertEqual(plines, ['pl0'])

    def test_pline_to_posis(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        posis = self.model.get_ents(ENT_TYPE.POSIS, plines)
        self.assertEqual(posis, ['ps0', 'ps1', 'ps2', 'ps3'])

    def test_pline_to_verts(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        verts = self.model.get_ents(ENT_TYPE.VERTS, plines)
        self.assertEqual(verts, ['_v0', '_v1', '_v2', '_v3'])

    def test_pline_to_edges(self):
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        edges = self.model.get_ents(ENT_TYPE.EDGES, plines)
        self.assertEqual(edges, ['_e0', '_e1', '_e2'])

if __name__ == '__main__':
    unittest.main()