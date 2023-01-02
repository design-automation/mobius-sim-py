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

class TestPolygonHoles(unittest.TestCase):

    def setUp(self):
        m = sim.SIM()
        pgon = m.add_pgon(
            [m.add_posi([0,0,0]), m.add_posi([50,0,0]), m.add_posi([0,50,0])],
        )
        m.add_pgon_hole(pgon, 
            # [m.add_posi([10,10,0]), m.add_posi([30,10,0]), m.add_posi([10,30,0])]
            [m.add_posi([10,10,0]), m.add_posi([10,30,0]), m.add_posi([30,10,0])]
        )
        coll = m.add_coll()
        m.add_coll_ent(coll, pgon)
        self.model = m

    def test_get_pgon(self):
        pgons = self.model.get_ents(ENT_TYPE.PGON)
        self.assertEqual(list(pgons), ['pg0'])

    def test_get_pgon_hole(self):
        wires = self.model.get_ents(ENT_TYPE.WIRE)
        posis = self.model.get_ents(ENT_TYPE.POSI, wires[1])
        self.assertEqual(list(posis), ['ps3','ps4','ps5'])

 
if __name__ == '__main__':
    unittest.main()