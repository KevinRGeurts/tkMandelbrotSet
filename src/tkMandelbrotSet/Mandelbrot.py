"""
This module defines the MandelbrotSet class, which generates a Mandelbrot set and saves it an an array object.
"""
# standard library imports
from array import array

class MandelbrotSet:
    """
    
    """
    def __init__(self, ul_corner=complex(real=-2.0, imag=-2.0), lr_corner=complex(real=2.0, imag=2.0),
                 pts_real=500, pts_imag=500, z_max=2.0, max_iters=50):
        """
        Initializes the MandelbrotSet object with the specified parameters.
        :parameter ul_corner: The upper left corner of the complex plane to be visualized, complex
        :parameter lr_corner: The lower right corner of the complex plane to be visualized, complex
        :parameter pts_real: The number of points to be calculated along the real axis, integer
        :parameter pts_imag: The number of points to be calculated along the imaginary axis, integer
        :parameter z_max: The maximum value of z to be considered for divergence, float
        :parameter max_iters: The maximum number of iterations to be performed for each point in the complex plane, integer
        """
        self._ul_corner = ul_corner
        self._lr_corner = lr_corner
        self._pts_real = pts_real
        self._pts_imag = pts_imag
        self._z_max = z_max
        self._max_iters = max_iters
        # The Mandelbrot set will be stored as a list of  arraya of integers, where each integer represents the
        # number of iterations it took for the corresponding point in the complex plane to diverge.
        # To access the value at point (real_index=i, imaginary_index=j): self._mandelbrot_set[i][j]
        self._mandelbrot_set = []
        for i in range(pts_real):
            self._mandelbrot_set.append(array('i'))

    @property
    def ul_corner(self):
        """
        Returns the upper left corner of the complex plane to be visualized.
        """
        return self._ul_corner

    @property
    def lr_corner(self):
        """
        Returns the lower right corner of the complex plane to be visualized.
        """
        return self._lr_corner

    @property
    def pts_real(self):
        """
        Returns the number of points to be calculated along the real axis.
        """
        return self._pts_real

    @property
    def pts_imag(self):
        """
        Returns the number of points to be calculated along the imaginary axis.
        """
        return self._pts_imag

    @property
    def z_max(self):
        """
        Returns the maximum value of z to be considered for divergence.
        """
        return self._z_max

    @property
    def max_iters(self):
        """
        Returns the maximum number of iterations to be performed for each point in the complex plane.
        """
        return self._max_iters

    def get_iter_value(self, real_index, imag_index):
        """
        Returns the number of iterations it took for the point at (real_index, img_index) to diverge.
        :parameter real_index: The index of the point along the real axis, integer
        :parameter imag_index: The index of the point along the imaginary axis, integer
        """
        assert(real_index >= 0)
        assert(real_index < self.pts_real)
        assert(imag_index >= 0)
        assert(imag_index < self.pts_imag)
        return self._mandelbrot_set[real_index][imag_index]

    def generate_mandelbrot_set(self):
        """
        Generates the Mandelbrot set and stores it in the _mandelbrot_set attribute.
        """
        for i in range(self._pts_real):
            for j in range(self._pts_imag):
                c = complex(real=self._ul_corner.real + i * (self._lr_corner.real - self._ul_corner.real) / (self._pts_real-1),
                            imag=self._ul_corner.imag + j * (self._lr_corner.imag - self._ul_corner.imag) / (self._pts_imag-1))
                self._mandelbrot_set[i].append(self._point_iterator(c))
                # print(f"i={i}, j={j}, c={str(c)}, iters={self._mandelbrot_set[i][j]}")

    def _point_iterator(self, c):
        """
        Returns the number of iterations it takes for the (complex plane) point c to diverge.
        :parameter c: The point in the complex plane to be evaluated, complex
        """
        z = complex(real=0.0, imag=0.0)
        for i in range(self._max_iters):
            z = z**2 + c
            # print(f"iter = {i}, z = {str(z)}, abs(z) = {abs(z)}")
            if abs(z) > self._z_max:
                return i
        return self._max_iters
