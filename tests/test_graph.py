from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals
import unittest
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from sim_model import graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        g = graph.Graph()
        self.graph = g

    def test_add_node(self):
        self.graph.add_node('aaa')
        self.assertTrue(self.graph.has_node('aaa'))
        self.assertListEqual(self.graph.get_nodes(), ['aaa'])
        self.assertListEqual(self.graph.get_node_prop_names('aaa'), [])
        self.assertFalse(self.graph.has_node('bbb'))

    def test_add_node_prop(self):
        self.graph.add_node('aaa')
        self.graph.set_node_prop('aaa', 'k1', 123)
        self.graph.set_node_prop('aaa', 'k2', [1,2,3])
        self.graph.set_node_prop('aaa', 'k3', {'one': 1, 'tow': 2, 'three': 3})
        self.graph.set_node_prop('aaa', 'k4', 'str123')
        self.graph.set_node_prop('aaa', 'k5', False)
        self.assertListEqual(sorted(self.graph.get_node_prop_names('aaa')), ['k1', 'k2', 'k3', 'k4', 'k5'])
        self.assertEqual(self.graph.get_node_prop('aaa', 'k1'), 123)
        self.assertListEqual(self.graph.get_node_prop('aaa', 'k2'), [1,2,3])
        self.assertDictEqual(self.graph.get_node_prop('aaa', 'k3'), {'one': 1, 'tow': 2, 'three': 3})
        self.assertEqual(self.graph.get_node_prop('aaa', 'k4'), 'str123')
        self.assertEqual(self.graph.get_node_prop('aaa', 'k5'), False)

    def test_add_edge_type(self):
        self.graph.add_edge_type('et1', True)
        self.assertTrue(self.graph.has_edge_type('et1'))
        self.graph.add_edge_type('et2', False)
        self.assertFalse(self.graph.has_edge_type('et3'))

    def test_add_del_edge(self):
        self.graph.add_edge_type('et1', True)
        self.assertTrue(self.graph.has_edge_type('et1'))
        self.assertFalse(self.graph.has_edge_type('et2'))
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge('aaa', 'bbb', 'et1')
        self.assertTrue(self.graph.has_edge('aaa', 'bbb', 'et1'))
        self.assertFalse(self.graph.has_edge('aaa', 'ccc', 'et1'))
        self.graph.del_edge('aaa', 'bbb', 'et1')
        self.assertFalse(self.graph.has_edge('aaa', 'bbb', 'et1'))

    def test_del_multi_edges1(self):
        self.graph.add_edge_type('et1', True)
        self.assertTrue(self.graph.has_edge_type('et1'))
        self.assertFalse(self.graph.has_edge_type('et2'))
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge('aaa', 'bbb', 'et1')
        self.graph.add_edge('aaa', 'ccc', 'et1')
        self.graph.del_edge('aaa', None, 'et1')
        self.assertFalse(self.graph.has_edge('aaa', 'bbb', 'et1'))
        self.assertFalse(self.graph.has_edge('aaa', 'ccc', 'et1'))

    def test_del_multi_edges2(self):
        self.graph.add_edge_type('et1', True)
        self.assertTrue(self.graph.has_edge_type('et1'))
        self.assertFalse(self.graph.has_edge_type('et2'))
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge('aaa', 'ccc', 'et1')
        self.graph.add_edge('bbb', 'ccc', 'et1')
        self.graph.del_edge(None, 'ccc', 'et1')
        self.assertFalse(self.graph.has_edge('aaa', 'bbb', 'et1'))
        self.assertFalse(self.graph.has_edge('aaa', 'ccc', 'et1'))

    def test_add_bad_edge(self):
        self.graph.add_edge_type('et1', True)
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        # self.assertRaises(self.graph.add_edge('aaa', 'ccc', 'et1'))

    def test_get_nodes_with_in_out_edge(self):
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge_type('et1', True)
        self.graph.add_edge('aaa', 'bbb', 'et1')
        self.assertListEqual(self.graph.get_nodes_with_in_edge('et1'), ['bbb'])
        self.assertListEqual(self.graph.get_nodes_with_out_edge('et1'), ['aaa'])

    def test_successors_predecessors(self):
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge_type('et1', True)
        self.graph.add_edge('aaa', 'bbb', 'et1')
        self.graph.add_edge('bbb', 'ccc', 'et1')
        self.graph.add_edge_type('et2', True)
        self.graph.add_edge('aaa', 'ccc', 'et2')
        self.assertListEqual(self.graph.successors('aaa', 'et1'), ['bbb'])
        self.assertListEqual(self.graph.successors('bbb', 'et1'), ['ccc'])
        self.assertListEqual(self.graph.successors('ccc', 'et1'), [])
        self.assertListEqual(self.graph.predecessors('aaa', 'et1'), [])
        self.assertListEqual(self.graph.predecessors('bbb', 'et1'), ['aaa'])
        self.assertListEqual(self.graph.predecessors('ccc', 'et1'), ['bbb'])

    def test_degree(self):
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge_type('et1', True)
        self.graph.add_edge('aaa', 'bbb', 'et1')
        self.graph.add_edge('bbb', 'ccc', 'et1')
        self.graph.add_edge_type('et2', True)
        self.graph.add_edge('aaa', 'ccc', 'et2')
        self.assertEqual(self.graph.degree_out('aaa', 'et1'), 1)
        self.assertEqual(self.graph.degree_out('bbb', 'et1'), 1)
        self.assertEqual(self.graph.degree_out('ccc', 'et1'), 0)
        self.assertEqual(self.graph.degree_in('aaa', 'et1'), 0)
        self.assertEqual(self.graph.degree_in('bbb', 'et1'), 1)
        self.assertEqual(self.graph.degree_in('ccc', 'et1'), 1)
        self.assertEqual(self.graph.degree('aaa', 'et1'), 1)
        self.assertEqual(self.graph.degree('bbb', 'et1'), 2)
        self.assertEqual(self.graph.degree('ccc', 'et1'), 1)

    def test_snapshot(self):
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge_type('et1', True)
        self.graph.add_edge('aaa', 'bbb', 'et1')
        old_ssid = self.graph.get_active_snapshot()
        new_ssid = self.graph.new_snapshot()
        self.graph.add_edge_type('et2', True)
        self.graph.add_edge('bbb', 'ccc', 'et2')
        self.assertFalse(self.graph.has_edge('aaa', 'bbb', 'et1'))
        self.assertTrue(self.graph.has_edge('bbb', 'ccc', 'et2'))
        self.graph.set_active_snapshot(old_ssid)
        self.assertTrue(self.graph.has_edge('aaa', 'bbb', 'et1'))
        self.assertFalse(self.graph.has_edge('bbb', 'ccc', 'et2'))
        self.graph.clear_snapshot(old_ssid)
        self.assertFalse(self.graph.has_edge('aaa', 'bbb', 'et1'))
        self.assertFalse(self.graph.has_edge('bbb', 'ccc', 'et2'))

    def test_set_successors(self):
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge_type('et1', True)
        self.graph.add_edge('aaa', 'bbb', 'et1')
        self.graph.add_edge('aaa', 'ccc', 'et1')
        self.assertListEqual(self.graph.successors('aaa', 'et1'), ['bbb', 'ccc'])
        self.graph.set_successors('aaa', ['ccc', 'bbb'], 'et1')
        self.assertListEqual(self.graph.successors('aaa', 'et1'), ['ccc', 'bbb'])

    def test_set_predecessors(self):
        self.graph.add_node('aaa')
        self.graph.add_node('bbb')
        self.graph.add_node('ccc')
        self.graph.add_edge_type('et1', True)
        self.graph.add_edge('aaa', 'ccc', 'et1')
        self.graph.add_edge('bbb', 'ccc', 'et1')
        self.assertListEqual(self.graph.predecessors('ccc', 'et1'), ['aaa', 'bbb'])
        self.graph.set_predecessors('ccc', ['bbb', 'aaa'], 'et1')
        self.assertListEqual(self.graph.predecessors('ccc', 'et1'), ['bbb', 'aaa'])

if __name__ == '__main__':
    unittest.main()