# standard library imports
import unittest
from uuid import UUID

# local imports
from tkMandelbrotSet.mandelbrot_set_model import MandelbrotSetModel
from tkMandelbrotSet.exceptions import MandelbrotSetNoPreviousZoomLocation, MandelbrotSetNoNextZoomLocation
from tkMandelbrotSet.mandelbrot import MandelbrotSet
from tkMandelbrotSet.bigraph import Bigraph, Branch, BigraphNode


class Test_MandelbrotSetModel(unittest.TestCase):
    def test_init(self):
        msm = MandelbrotSetModel()
        self.assertEqual(type(msm._mandelbrot_set), MandelbrotSet)
        self.assertEqual(type(msm._zoom_graph), Bigraph)
        self.assertEqual(type(msm._current_branch), Branch)
        self.assertEqual(type(msm._current_node), BigraphNode)

    def test_ul_corner_property_getter(self):
        msm = MandelbrotSetModel()
        exp_val = complex(real=-2.0, imag=2.0)
        act_val = msm.ul_corner
        self.assertEqual(exp_val, act_val)

    def test_lr_corner_property_getter(self):
        msm = MandelbrotSetModel()
        exp_val = complex(real=1.0, imag=-2.0)
        act_val = msm.lr_corner
        self.assertEqual(exp_val, act_val)
        
    def test_set_corners(self):
        msm = MandelbrotSetModel()
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        exp_val = complex(real=-1.0, imag=1.0)
        act_val = msm.ul_corner
        self.assertEqual(exp_val, act_val)
        exp_val = complex(real=0.0, imag=-1.0)
        act_val = msm.lr_corner
        self.assertEqual(exp_val, act_val)

    def test_set_corners_to_split_branch(self):
        msm = MandelbrotSetModel()
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        exp_val = []
        exp_val.append(msm._current_node.nodeID)
        msm.rewind()
        msm.set_corners(ul_corner=complex(real=-0.5, imag=0.5), lr_corner=complex(real=-0.1, imag=-0.5))
        exp_val.append(msm._current_node.nodeID)
        msm.rewind()
        act_val = msm.get_current_node_successor_IDs()
        self.assertEqual(exp_val, act_val)

    def test_get_current_node_predecessor_ID(self):
        msm = MandelbrotSetModel()
        exp_val = msm._current_node.nodeID
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        act_val = msm.get_current_node_predecessor_ID()
        self.assertEqual(exp_val, act_val)

    def test_get_current_node_predecessor_ID_no_predecessor(self):
        msm = MandelbrotSetModel()
        exp_val = UUID(int=0x0)
        msm.rewind()
        act_val = msm.get_current_node_predecessor_ID()
        self.assertEqual(exp_val, act_val)

    def test_rewind(self):
        msm = MandelbrotSetModel()
        exp_val = msm._current_node.nodeID
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        msm.rewind()
        act_val = msm._current_node.nodeID
        self.assertEqual(exp_val, act_val)

    def test_rewind_fail(self):
        msm = MandelbrotSetModel()
        msm.rewind()
        self.assertRaises(MandelbrotSetNoPreviousZoomLocation, msm.rewind)
        
    def test_home(self):
        msm = MandelbrotSetModel()
        exp_val = msm._current_node.nodeID
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        msm.home()
        act_val = msm._current_node.nodeID
        self.assertEqual(exp_val, act_val)

    def test_forward(self):
        msm = MandelbrotSetModel()
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        exp_val = msm._current_node.nodeID
        msm.rewind()
        msm.forward()
        act_val = msm._current_node.nodeID
        self.assertEqual(exp_val, act_val)

    def test_forward_fail(self):
        msm = MandelbrotSetModel()
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        exp_val = msm._current_node.nodeID
        msm.rewind()
        msm.forward()
        self.assertRaises(MandelbrotSetNoNextZoomLocation, msm.forward)

    def test_get_current_node_successor_IDs(self):
        msm = MandelbrotSetModel()
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        exp_val = [msm._current_node.nodeID]
        msm.rewind()
        act_val = msm.get_current_node_successor_IDs()
        self.assertListEqual(exp_val, act_val)

    def test_get_current_node_successor_IDs_no_successors(self):
        msm = MandelbrotSetModel()
        exp_val = 0
        act_val = len(msm.get_current_node_successor_IDs())
        self.assertEqual(exp_val, act_val)

    def test_get_current_node_available_zoom_locations(self):
        msm = MandelbrotSetModel()
        msm.set_corners(ul_corner=complex(real=-1.0, imag=1.0), lr_corner=complex(real=0.0, imag=-1.0))
        exp_val = [(-1.0, 1.0, 0.0, -1.0)]
        msm.rewind()
        act_val = msm.get_current_node_available_zoom_locations()
        self.assertListEqual(exp_val, act_val)

    def test_get_current_node_available_zoom_locations_no_locations(self):
        msm = MandelbrotSetModel()
        exp_val = 0
        act_val = len(msm.get_current_node_available_zoom_locations())
        self.assertEqual(exp_val, act_val)

    def test_get_current_node_plot_data(self):
        msm = MandelbrotSetModel()
        msm._mandelbrot_set = MandelbrotSet(complex(real=-1.8, imag=0.1),complex(real=-1.6, imag=-0.1),2,2)
        memento = msm._mandelbrot_set.create_memento()
        msm._current_node.payload = memento
        (act_x, act_y, act_z) = msm.get_current_node_plot_data()
        # Check x
        exp_val = [-1.8, -1.6]
        self.assertListEqual(exp_val, act_x)
        # Check y
        exp_val = [0.1, -0.1]
        self.assertListEqual(exp_val, act_y)
        # Check z: [[(0,0),(1,0)],[(0,1),(1,1)]]
        exp_val = [[3, 5],[3, 5]]
        self.assertListEqual(exp_val, act_z)


if __name__ == '__main__':
    unittest.main()
