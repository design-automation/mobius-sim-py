from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals
import unittest
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from sim_model import sim
from sim_model import io_sim
ENT_TYPE = sim.ENT_TYPE
DATA_TYPE = sim.DATA_TYPE

class TestAttribs(unittest.TestCase):

    def setUp(self):
        m = sim.SIM()
        point1 = m.add_point( m.add_posi([1,2,3]) )
        point2 = m.add_point( m.add_posi([4,5,6]) )
        m.add_attrib(ENT_TYPE.POINT, 'test', DATA_TYPE.STR)
        m.set_attrib_val(point1, 'test', 'hello1')
        m.set_attrib_val(point2, 'test', 'hello2')
        m.set_model_attrib_val("a_sting", "hello")
        m.set_model_attrib_val("a_number", 123)
        m.set_model_attrib_val("a_list", [1, "two", [3]])
        m.set_model_attrib_val("a_dict", { "a": 1, "b": "two", "c": [3]})
        self.model = m

    def test_get_attribs(self):
        atts1 = self.model.get_attribs(ENT_TYPE.POINT)
        atts2 = self.model.get_attribs(ENT_TYPE.POSI)
        atts3 = self.model.get_attribs(ENT_TYPE.PGON)
        self.assertEqual(list(atts1), ['test'])
        self.assertEqual(list(atts2), ['xyz'])
        self.assertEqual(list(atts3), [])

    def test_get_attrib_vals(self):
        att_vals1 = self.model.get_attrib_vals(ENT_TYPE.POINT, 'test')
        att_vals2 = self.model.get_attrib_vals(ENT_TYPE.POSI, 'xyz')
        self.assertEqual(list(att_vals1), ['hello1', 'hello2'])
        self.assertEqual(list(att_vals2), [[1,2,3], [4,5,6]])

    def test_get_point_attribs(self):
        points = self.model.get_ents(ENT_TYPE.POINT)
        str1 = self.model.get_attrib_val(points[0], 'test')
        str2 = self.model.get_attrib_val(points[1], 'test')
        self.assertEqual(str1, 'hello1')
        self.assertEqual(str2, 'hello2')

    def test_get_point_data(self):
        json = io_sim.export_sim_data(self.model)
        data = [{"name": "test", "data_type": "string", "values": ["hello1", "hello2"], "entities": [[0], [1]]}]
        self.assertEqual(json['attributes']['points'], data)

    def test_get_model_attribs(self):
        self.assertEqual( self.model.get_model_attrib_val("a_sting"), "hello")
        self.assertEqual( self.model.get_model_attrib_val("a_number"), 123)
        self.assertEqual( self.model.get_model_attrib_val("a_list"), [1, "two", [3]])
        self.assertEqual( self.model.get_model_attrib_val("a_dict"), { "a": 1, "b": "two", "c": [3]})

    def test_has_model_attrib(self):
        self.assertTrue( self.model.has_model_attrib("a_sting") )
        self.assertTrue( self.model.has_model_attrib("a_number") )
        self.assertTrue( self.model.has_model_attrib("a_list") )
        self.assertTrue( self.model.has_model_attrib("a_dict") )
        self.assertFalse( self.model.has_model_attrib("abc") )
       
if __name__ == '__main__':
    unittest.main()