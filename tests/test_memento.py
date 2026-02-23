"""
This module contains unit tests for the SetMemento class.
"""


# standard library imports
import unittest


# local imports
from tkMandelbrotSet.memento import SetMemento


class Test_BigraphNode(unittest.TestCase):
    def test_init_set_state_get_state(self):
        memento = SetMemento(ul_corner=complex(-1.0,1.0), lr_corner=complex(0.5,-1.5),
                             pts_real=100, pts_imag=110, z_max=3.0, max_iters=25)
        exp_val = (complex(-1.0,1.0), complex(0.5,-1.5), 100, 110, 3.0, 25)
        act_val = memento.get_state()
        self.assertTupleEqual(exp_val, act_val)


if __name__ == '__main__':
    unittest.main()
