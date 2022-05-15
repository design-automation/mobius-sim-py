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

class TestAttribs(unittest.TestCase):

    def setUp(self):
        m = sim.SIM()
        point0 = m.add_point( m.add_posi([1,2,3]) )
        point1 = m.add_point( m.add_posi([4,5,6]) )
        point2 = m.add_point( m.add_posi([7,8,9]) )
        m.add_attrib(ENT_TYPE.POINTS, 'some_str', DATA_TYPE.STR)
        m.set_attrib_val(point0, 'some_str', 'hello1')
        m.add_attrib(ENT_TYPE.POINTS, 'some_number', DATA_TYPE.NUM)
        m.set_attrib_val(point1, 'some_number', 55)
        self.model = m

    def test_query_string(self):
        result = self.model.query(ENT_TYPE.POINTS, 'some_str', '==', 'hello1')
        self.assertEqual(result, ['pt0'])
        result = self.model.query(ENT_TYPE.POINTS, 'some_str', '!=', 'hello1')
        result.sort()
        self.assertEqual(list(result), ['pt1', 'pt2'])

    def test_query_number(self):
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '==', 55)
        self.assertEqual(list(result), ['pt1'])
        
    def test_query_xyz(self):
        result = self.model.query(ENT_TYPE.POSIS, 'xyz', '==', [1,2,3])
        self.assertEqual(list(result), ['ps0'])
        result = self.model.query(ENT_TYPE.POSIS, 'xyz', '!=', [1,2,3])
        result.sort()
        self.assertEqual(list(result), ['ps1', 'ps2'])

    def test_query_lt_gt(self):
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '>', 50)
        self.assertEqual(list(result), ['pt1'])
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '>=', 55)
        self.assertEqual(list(result), ['pt1'])
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '<', 50)
        self.assertEqual(list(result), [])
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '<=', 50)
        self.assertEqual(list(result), [])
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '<=', 60)
        self.assertEqual(list(result), ['pt1'])

        
    def test_query_none(self):
        result = self.model.query(ENT_TYPE.POSIS, 'xyz', '==', None)
        self.assertEqual(list(result), [])
        result = self.model.query(ENT_TYPE.POINTS, 'some_str', '!=', None)
        self.assertEqual(list(result), ['pt0'])
        result = self.model.query(ENT_TYPE.POINTS, 'some_str', '==', None)
        result.sort()
        self.assertEqual(list(result), ['pt1', 'pt2'])
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '!=', None)
        self.assertEqual(list(result), ['pt1'])
        result = self.model.query(ENT_TYPE.POINTS, 'some_number', '==', None)
        result.sort()
        self.assertEqual(list(result), ['pt0', 'pt2'])

if __name__ == '__main__':
    unittest.main()