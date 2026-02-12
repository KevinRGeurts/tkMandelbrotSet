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

    def test_get_iter_value_set_generated(self):
        exp_val = 19
        ms = MandelbrotSet()
        ms._mandelbrot_set[0].append(exp_val)
        ms._set_generated = True
        act_val = ms.get_iter_value(0,0)
        self.assertEqual(exp_val, act_val)

    def test_get_iter_value_set_not_generated(self):
        exp_val = 50
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
        exp_val = (50,-2.0,2.0)
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


if __name__ == '__main__':
    unittest.main()
