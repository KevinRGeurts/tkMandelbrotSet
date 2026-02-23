# standard library imports
import unittest
from array import array

# local imports
from tkMandelbrotSet.mandelbrot import MandelbrotSet


class Test_MandelbrotSet(unittest.TestCase):
    def test_init_property_getters(self):
        ms = MandelbrotSet()
        self.assertEqual(ms.ul_corner, complex(real=-2.0, imag=2.0))
        self.assertEqual(ms.lr_corner, complex(real=1.0, imag=-2.0))
        self.assertEqual(ms.pts_real, 500)
        self.assertEqual(ms.pts_imag, 500)
        self.assertEqual(ms._z_max, 2.0)
        self.assertEqual(ms._max_iters, 50)
        self.assertEqual(len(ms._mandelbrot_set), 500)
        self.assertTrue(all(type(row)==array for row in ms._mandelbrot_set))

    def test_ul_corner_property_setter(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        # Check that we are starting after __init__ with the expected ulc value
        self.assertEqual(ms.ul_corner, ulc)
        # Check that the set is not generated
        self.assertFalse(ms._set_generated)
        # Generate the set
        ms.generate_mandelbrot_set()
        # Check that the set is generated
        self.assertTrue(ms._set_generated)
        # Change the ulc
        new_ulc=complex(real=-1.7, imag=0.0)
        ms.ul_corner=new_ulc
        # Check that we have the expected new ulc value
        self.assertEqual(ms.ul_corner, new_ulc)
        # Check that the set is again not generated
        self.assertFalse(ms._set_generated)
        
    def test_lr_corner_property_setter(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        # Check that we are starting after __init__ with the expected lrc value
        self.assertEqual(ms.lr_corner, lrc)
        # Check that the set is not generated
        self.assertFalse(ms._set_generated)
        # Generate the set
        ms.generate_mandelbrot_set()
        # Check that the set is generated
        self.assertTrue(ms._set_generated)
        # Change the lrc
        new_lrc=complex(real=-1.5, imag=-0.2)
        ms.lr_corner=new_lrc
        # Check that we have the expected new lrc value
        self.assertEqual(ms.lr_corner, new_lrc)
        # Check that the set is again not generated
        self.assertFalse(ms._set_generated)
    
    def test_set_corners(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        # Check that we are starting after __init__ with the expected ulc and lrc values
        self.assertEqual(ms.ul_corner, ulc)
        self.assertEqual(ms.lr_corner, lrc)
        # Check that the set is not generated
        self.assertFalse(ms._set_generated)
        # Generate the set
        ms.generate_mandelbrot_set()
        # Check that the set is generated
        self.assertTrue(ms._set_generated)
        # Change the ulc and lrc
        new_ulc=complex(real=-1.7, imag=0.0)
        new_lrc=complex(real=-1.5, imag=-0.2)
        ms.set_corners(new_ulc, new_lrc)
        # Check that we have the expected new ulc and lrc value
        self.assertEqual(ms.ul_corner, new_ulc)
        self.assertEqual(ms.lr_corner, new_lrc)
        # Check that the set is again not generated
        self.assertFalse(ms._set_generated)

    def test_get_iter_value_set_generated(self):
        exp_val = 19
        ms = MandelbrotSet()
        ms._mandelbrot_set[0].append(exp_val)
        ms._set_generated = True
        act_val = ms.get_iter_value(0,0)
        self.assertEqual(exp_val, act_val)

    def test_get_iter_value_set_not_generated(self):
        exp_val = 0
        ms = MandelbrotSet()
        ms._mandelbrot_set[0].append(exp_val)
        act_val = ms.get_iter_value(0,0)
        self.assertEqual(exp_val, act_val)

    def test_get_iter_value_with_ri_set_generated(self):
        exp_val = (19,-2.0,2.0)
        ms = MandelbrotSet()
        ms._mandelbrot_set[0].append(exp_val[0])
        ms._set_generated = True
        act_val = ms.get_iter_value_with_ri(0,0)
        self.assertTupleEqual(exp_val, act_val)

    def test_get_iter_value_with_ri_set_not_generated(self):
        exp_val = (0,-2.0,2.0)
        ms = MandelbrotSet()
        ms._mandelbrot_set[0].append(exp_val[0])
        act_val = ms.get_iter_value_with_ri(0,0)
        self.assertTupleEqual(exp_val, act_val)

    def test_point_iterator_max_iters(self):
        pnt = complex(real=0.1, imag=0.1)
        ms = MandelbrotSet()
        exp_val = ms.max_iters
        act_val = ms._point_iterator(pnt)
        self.assertEqual(exp_val, act_val)

    def test_point_iterator_diverge(self):
        pnt = complex(real=-0.8, imag=0.2)
        ms = MandelbrotSet()
        exp_val = 14
        act_val = ms._point_iterator(pnt)
        self.assertEqual(exp_val, act_val)

    def test_generate_mandelbrot_set(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,5,5)
        ms.generate_mandelbrot_set()
        # Test the corners of the box and the center point (ul, ur, ll, lr, cp)
        exp_val = (3, 5, 3, 5, 50)
        act_val = (ms.get_iter_value(0,0), ms.get_iter_value(4,0), ms.get_iter_value(0,4), ms.get_iter_value(4,4), ms.get_iter_value(2,2))
        self.assertTupleEqual(exp_val, act_val)

    def test_len(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,5,5)
        exp_val = 25
        act_val = len(ms)
        self.assertEqual(exp_val, act_val)

    def test_getitem(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        ms.generate_mandelbrot_set()
        # Order in exp_value is [ul, ll, ur, lr]
        exp_val = [(3, -1.8, 0.1), (3, -1.8, -0.1,), (5, -1.6, 0.1), (5, -1.6, -0.1)]
        act_val = [ms[0], ms[1], ms[2], ms[3]]
        self.assertListEqual(exp_val, act_val)

    def test_getitem_bad_subscript_type(self):
        ms = MandelbrotSet()
        self.assertRaises(TypeError, ms.__getitem__, 'not an int but a str')

    def test_iteration(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        # Order in exp_value is [ul, ll, ur, lr]
        #               i=0, j=0       i=0,   j=1         i=1, j=0       i=1,  j=1
        exp_val = [(3, -1.8, 0.1), (3, -1.8, -0.1,), (5, -1.6, 0.1), (5, -1.6, -0.1)]
        ms = MandelbrotSet(ulc,lrc,2,2)
        ms.generate_mandelbrot_set()
        act_val=[]
        for pnt in ms:
            act_val.append(pnt)
        self.assertListEqual(exp_val, act_val)

    def test_indices_to_point(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        exp_val = [complex(-1.8, 0.1), complex(-1.8, -0.1,), complex(-1.6, 0.1), complex(-1.6, -0.1)]
        act_val = [ms._indices_to_point(0,0), ms._indices_to_point(0,1), ms._indices_to_point(1,0), ms._indices_to_point(1,1)]    
        self.assertListEqual(exp_val, act_val)

    def test_get_plot_data(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        (act_x, act_y, act_z) = ms.get_plot_data()
        # Check x
        exp_val = [-1.8, -1.6]
        self.assertListEqual(exp_val, act_x)
        # Check y
        exp_val = [0.1, -0.1]
        self.assertListEqual(exp_val, act_y)
        # Check z: [[(0,0),(1,0)],[(0,1),(1,1)]]
        exp_val = [[3, 5],[3, 5]]
        self.assertListEqual(exp_val, act_z)

    def test_get_plot_data_invert_z_True(self):
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        ms = MandelbrotSet(ulc,lrc,2,2)
        (act_x, act_y, act_z) = ms.get_plot_data(True)
        # Check x
        exp_val = [-1.8, -1.6]
        self.assertListEqual(exp_val, act_x)
        # Check y
        exp_val = [0.1, -0.1]
        self.assertListEqual(exp_val, act_y)
        # Check z: [[(0,0),(1,0)],[(0,1),(1,1)]]
        exp_val = [[50-3, 50-5],[50-3, 50-5]]
        self.assertListEqual(exp_val, act_z)

    def test_create_memento_set_memento(self):
        # First, test MandelbrotSet.create_memento()
        ulc=complex(real=-1.8, imag=0.1)
        lrc=complex(real=-1.6, imag=-0.1)
        pr = 50
        pi = 40
        zmax = 3.0
        maxi = 25
        ms = MandelbrotSet(ulc,lrc,pr,pi,zmax,maxi)
        exp_val = (ulc, lrc, pr, pi, zmax, maxi)
        memento = ms.create_memento()
        act_val = memento.get_state()
        self.assertTupleEqual(exp_val, act_val)
        # Second, test MandelbrotSet.set_memento()
        ms = MandelbrotSet()
        ms.set_memento(memento)
        act_val = (ms.ul_corner, ms.lr_corner, ms.pts_real, ms.pts_imag, ms.z_max, ms.max_iters)
        self.assertTupleEqual(exp_val, act_val)


if __name__ == '__main__':
    unittest.main()
