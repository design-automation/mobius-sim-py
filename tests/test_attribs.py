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
        point1 = m.add_point( m.add_posi([1,2,3]) )
        point2 = m.add_point( m.add_posi([4,5,6]) )
        m.add_attrib(ENT_TYPE.POINTS, 'test', DATA_TYPE.STR)
        m.set_attrib_val(point1, 'test', 'hello')
        m.set_attrib_val(point2, 'test', 'hello')
        self.model = m

    def test_get_point(self):
        json = self.model.to_json()
        data = [{"name": "test", "data_type": "string", "values": ["hello"], "entities": [[0, 1]]}]
        self.assertEqual(json['attributes']['points'], data)

if __name__ == '__main__':
    unittest.main()