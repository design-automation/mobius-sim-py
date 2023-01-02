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

class TestPoints(unittest.TestCase):

    def setUp(self):
        m = sim.SIM()
        point = m.add_point( m.add_posi([1,2,3]) )
        coll = m.add_coll()
        m.add_coll_ent(coll, point)
        self.model = m

    def test_get_point(self):
        points = self.model.get_ents(ENT_TYPE.POINT)
        self.assertEqual(list(points), ['pt0'])

    def test_point_to_posis(self):
        points = self.model.get_ents(ENT_TYPE.POINT)
        posis = self.model.get_ents(ENT_TYPE.POSI, points)
        self.assertEqual(list(posis), ['ps0'])

    def test_point_to_verts(self):
        points = self.model.get_ents(ENT_TYPE.POINT)
        verts = self.model.get_ents(ENT_TYPE.VERT, points)
        self.assertEqual(list(verts), ['_v0'])

    def test_point_to_colls(self):
        points = self.model.get_ents(ENT_TYPE.POINT)
        colls = self.model.get_ents(ENT_TYPE.COLL, points)
        self.assertEqual(list(colls), ['co0'])

    def test_posi_to_point(self):
        posis = self.model.get_ents(ENT_TYPE.POSI)
        point = self.model.get_ents(ENT_TYPE.POINT, posis[0])
        self.assertEqual(list(point), ['pt0'])

    def test_vert_to_point(self):
        verts = self.model.get_ents(ENT_TYPE.VERT)
        point = self.model.get_ents(ENT_TYPE.POINT, verts[0])
        self.assertEqual(list(point), ['pt0'])

    def test_get_point_xyz(self):
        points = self.model.get_ents(ENT_TYPE.POINT)
        posis = self.model.get_ents(ENT_TYPE.POSI, points[0])
        vert_xyz = self.model.get_attrib_val(posis[0], 'xyz')
        self.assertEqual(list(vert_xyz), [1,2,3])
        point = self.model.get_ents(ENT_TYPE.POINT, posis[0])
        verts = self.model.get_ents(ENT_TYPE.VERT, point)
        posis = self.model.get_ents(ENT_TYPE.POSI, verts[0])
        posi_xyz = self.model.get_attrib_val(posis[0], 'xyz')
        self.assertEqual(list(posi_xyz), [1,2,3])

if __name__ == '__main__':
    unittest.main()