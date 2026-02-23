"""
This module implements the SetMemento class, for storing the "state" of the MandelbrotSet class.

Exported classes:
    SetMemento: Follows the Memento design pattern (as well as can be done in Python) and provides a "state"
                snapshot of the MandelbrotSet class.

Exported functions:
    None

Exported exceptions:
    None
"""


# standard imports


# local imports


class SetMemento(object):
    """
    The SetMemento class follows the Memento design pattern (as well as can be done in Python) and provides a "state"
    snapshot of the MandelbrotSet class.
    """
    def __init__(self, ul_corner=complex(real=-2.0, imag=2.0), lr_corner=complex(real=1.0, imag=-2.0),
                 pts_real=500, pts_imag=500, z_max=2.0, max_iters=50):
        """
        Initializes the SetMemento object with the specified parameters.
        Should only be called by the Originator (MandelbrotSet object), and never by the Caretaker (?).
        :parameter ul_corner: The upper left corner of the complex plane to be visualized, complex
        :parameter lr_corner: The lower right corner of the complex plane to be visualized, complex
        :parameter pts_real: The number of points to be calculated along the real axis, integer
        :parameter pts_imag: The number of points to be calculated along the imaginary axis, integer
        :parameter z_max: The maximum value of z to be considered for divergence, float
        :parameter max_iters: The maximum number of iterations to be performed for each point in the complex plane, integer
        """
        self.set_state(ul_corner, lr_corner, pts_real, pts_imag, z_max, max_iters)

    def get_state(self):
        """
        Should only be called by the Originator (MandelbrotSet object), and never by the Caretaker (?).
        :return: Tuple (ul_corner, lr_corner, pts_real, pts_imag, z_max, max_iters), as tuple (complex, copmlex, integer, integer, float, integer)
            ul_corner: The upper left corner of the complex plane to be visualized, complex
            lr_corner: The lower right corner of the complex plane to be visualized, complex
            pts_real: The number of points to be calculated along the real axis, integer
            pts_imag: The number of points to be calculated along the imaginary axis, integer
            z_max: The maximum value of z to be considered for divergence, float
            max_iters: The maximum number of iterations to be performed for each point in the complex plane, integer
        """
        result = (self._ul_corner, self._lr_corner, self._pts_real, self._pts_imag, self._z_max, self._max_iters)
        return result

    def set_state(self, ul_corner=complex(real=-2.0, imag=2.0), lr_corner=complex(real=1.0, imag=-2.0),
                 pts_real=500, pts_imag=500, z_max=2.0, max_iters=50):
        """
        Set the state of the SetMemento object with the specified parameters.
        Should only be called by the Originator (MandelbrotSet object), and never by the Caretaker (?).
        :parameter ul_corner: The upper left corner of the complex plane to be visualized, complex
        :parameter lr_corner: The lower right corner of the complex plane to be visualized, complex
        :parameter pts_real: The number of points to be calculated along the real axis, integer
        :parameter pts_imag: The number of points to be calculated along the imaginary axis, integer
        :parameter z_max: The maximum value of z to be considered for divergence, float
        :parameter max_iters: The maximum number of iterations to be performed for each point in the complex plane, integer
        :return: None
        """
        assert(max_iters>1)
        assert(z_max>0)
        assert(pts_real>0)
        assert(pts_imag>0)
        assert(lr_corner.real>ul_corner.real)
        assert(lr_corner.imag<ul_corner.imag)
        self._ul_corner = ul_corner
        self._lr_corner = lr_corner
        self._pts_real = pts_real
        self._pts_imag = pts_imag
        self._z_max = z_max
        self._max_iters = max_iters
        return None
