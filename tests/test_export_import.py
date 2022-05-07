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

def create_geom(model):
    # make some geom
    posis = [
        model.add_posi([1,2,3]), 
        model.add_posi([4,-5,7]), 
        model.add_posi([2,2,2]), 
        model.add_posi([-10,0,-10])
    ]
    pgon = model.add_pgon(posis)
    pline_open = model.add_pline([
        posis[0], 
        posis[2]
    ], False)
    pline_closed = model.add_pline([
        posis[1], 
        posis[3], 
        posis[0]
    ], True)
    coll = model.add_coll()
    model.add_coll_ent(coll, pgon)
    model.add_coll_ent(coll, pline_open)
    model.add_coll_ent(coll, pline_closed)

class TestImport(unittest.TestCase):
    
    def setUp(self):
        m = sim.SIM()
        self.model = m

    def test_import_file(self):
        # import a file
        self.model.import_sim_file('./pgons_18.sim')
        # check 
        pgons = self.model.get_ents(ENT_TYPE.PGONS)
        self.assertEqual(len(pgons), 18)

    def test_export_import_sim_data(self):
        # make some geom
        create_geom(self.model)
        # export
        sim_data = self.model.export_sim_data()
        # import
        self.model.import_sim_data(sim_data)
        # check
        posis = self.model.get_ents(ENT_TYPE.POSIS)
        self.assertEqual(len(posis), 8)
        pgons = self.model.get_ents(ENT_TYPE.PGONS)
        self.assertEqual(len(pgons), 2)
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        self.assertEqual(len(plines), 4)
        colls = self.model.get_ents(ENT_TYPE.COLLS)
        self.assertEqual(len(colls), 2)

    def test_export_import_sim_str(self):
        # make some geom
        create_geom(self.model)
        # export
        sim_str = self.model.export_sim()
        # import
        self.model.import_sim(sim_str)
        # check
        posis = self.model.get_ents(ENT_TYPE.POSIS)
        self.assertEqual(len(posis), 8)
        pgons = self.model.get_ents(ENT_TYPE.PGONS)
        self.assertEqual(len(pgons), 2)
        plines = self.model.get_ents(ENT_TYPE.PLINES)
        self.assertEqual(len(plines), 4)
        colls = self.model.get_ents(ENT_TYPE.COLLS)
        self.assertEqual(len(colls), 2)

    def test_import_model_attribs(self):
        # create a model with some modle attributes
        m2 = sim.SIM()
        m2.set_model_attrib_val("a_sting", "hello")
        m2.set_model_attrib_val("a_number", 123)
        m2.set_model_attrib_val("a_list", [1, "two", [3]])
        m2.set_model_attrib_val("a_dict", { "a": 1, "b": "two", "c": [3]})
        # import the other model into this model
        self.model.import_sim_data( m2.export_sim_data() )
        # check
        self.assertEqual( self.model.get_model_attrib_val("a_sting"), "hello")
        self.assertEqual( self.model.get_model_attrib_val("a_number"), 123)
        self.assertEqual( self.model.get_model_attrib_val("a_list"), [1, "two", [3]])
        self.assertEqual( self.model.get_model_attrib_val("a_dict"), { "a": 1, "b": "two", "c": [3]})
        
if __name__ == '__main__':
    unittest.main()