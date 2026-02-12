"""
This module defines the MandelbrotSet class, which generates a Mandelbrot set and stores it for later retrieval.

Exported classes:
    Mandelbrot Set: Class the can generate a Mandelbrot Set.

Exported functions:
    None

Exported exceptions:
    None
"""


# standard library imports
from array import array
from math import floor


class MandelbrotSet:
    """
    
    """
    def __init__(self, ul_corner=complex(real=-2.0, imag=2.0), lr_corner=complex(real=1.0, imag=-2.0),
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
        # The Mandelbrot set will be stored as a list of  arraya of integers, where each integer represents the
        # number of iterations it took for the corresponding point in the complex plane to diverge.
        # To access the value at point (real_index=i, imaginary_index=j): self._mandelbrot_set[i][j]
        self._mandelbrot_set = []
        for i in range(pts_real):
            self._mandelbrot_set.append(array('i'))
        # Flag indicating if generate_mandelbrot_set() method has been called, and thus if results are available.
        self._set_generated = False

    @property
    def ul_corner(self):
        """
        Returns the upper left corner of the complex plane to be visualized, as complex.
        """
        return self._ul_corner

    @property
    def lr_corner(self):
        """
        Returns the lower right corner of the complex plane to be visualized, as complex.
        """
        return self._lr_corner

    @property
    def pts_real(self):
        """
        Returns the number of points to be calculated along the real axis, as integer.
        """
        return self._pts_real

    @property
    def pts_imag(self):
        """
        Returns the number of points to be calculated along the imaginary axis, as integer.
        """
        return self._pts_imag

    @property
    def z_max(self):
        """
        Returns the maximum value of z to be considered for divergence, as integer.
        """
        return self._z_max

    @property
    def max_iters(self):
        """
        Returns the maximum number of iterations to be performed for each point in the complex plane, as integer.
        """
        return self._max_iters

    # TODO: Would a better behavior if the set has not been generated to just go ahead and generate the whole set?
    def get_iter_value(self, real_index, imag_index):
        """
        Returns the number of iterations it took for the point at (real_index, img_index) to diverge.
        :parameter real_index: The index of the point along the real axis, integer
        :parameter imag_index: The index of the point along the imaginary axis, integer
        :return: Iterations it took for the point to diverge, integer
        """
        assert(real_index >= 0)
        assert(real_index < self.pts_real)
        assert(imag_index >= 0)
        assert(imag_index < self.pts_imag)
        result = 0
        if self._set_generated:
            result = self._mandelbrot_set[real_index][imag_index]
        else:
            result = self._point_iterator(complex())
        return result
            

    def get_iter_value_with_ri(self, real_index, imag_index):
        """
        Returns the number of iterations it took for the point at (real_index, img_index) to diverge,
        and the real and imaginary axis coordinates of the point.
        :parameter real_index: The index of the point along the real axis, integer
        :parameter imag_index: The index of the point along the imaginary axis, integer
        :return: Tuple (iterarions to diverge, real-axis coordinate, imaginary-axis coordinate), as (integer, float, float)
        """
        assert(real_index >= 0)
        assert(real_index < self.pts_real)
        assert(imag_index >= 0)
        assert(imag_index < self.pts_imag)
        c = self._indices_to_point(real_index, imag_index)
        return (self.get_iter_value(real_index, imag_index), c.real, c.imag)

    def generate_mandelbrot_set(self):
        """
        Generates the Mandelbrot set and stores it in the _mandelbrot_set attribute.
        :return: None
        """
        for i in range(self._pts_real):
            # print(f"generating set for real index {i}")
            for j in range(self._pts_imag):
                c = self._indices_to_point(i,j)
                self._mandelbrot_set[i].append(self._point_iterator(c))
                # print(f"i={i}, j={j}, c={str(c)}, iters={self._mandelbrot_set[i][j]}")
        self._set_generated = True
        return None

    def _indices_to_point(self, real_index, imag_index):
        """
        Given a real index value and an imaginary index value, return the complex number that corresponds to that
        set of indices.
        :parameter real_index: The index of the point along the real axis, integer
        :parameter imag_index: The index of the point along the imaginary axis, integer
        :return: Complex number corresponding to the indices, as complex
        """
        assert(real_index >= 0)
        assert(real_index < self.pts_real)
        assert(imag_index >= 0)
        assert(imag_index < self.pts_imag)
        c = complex(real=self._ul_corner.real + real_index * (self._lr_corner.real - self._ul_corner.real) / (self._pts_real-1),
                    imag=self._ul_corner.imag + imag_index * (self._lr_corner.imag - self._ul_corner.imag) / (self._pts_imag-1))
        return c
    
    def _point_iterator(self, c):
        """
        Returns the number of iterations it takes for the (complex plane) point c to diverge.
        :parameter c: The point in the complex plane to be evaluated, complex
        :return: Number of iterations it took for point c to diverge, integer
        """
        z = complex(real=0.0, imag=0.0)
        for i in range(self._max_iters):
            z = z**2 + c
            # print(f"iter = {i}, z = {str(z)}, abs(z) = {abs(z)}")
            if abs(z) > self._z_max:
                return i
        return self._max_iters

    # Required so that for loops work
    def __len__(self):
        """
        Return the total number of points in the Mandelbrot set, as integer.
        """
        return self.pts_real*self.pts_imag

    # Required so that for loops work, and so that subscripting works
    def __getitem__(self, subscript):
        """
        Enable iteration through the Mandelbrot set using a single subscript. This will extract items in real-major-order,
        such that the real value varies most slowly. Or said another way, all imaginary values with be extracted for the
        first real value, and then the real value will be incremented to the next value.
        :return: Tuple (iterarions to diverge, real-axis coordinate, imaginary-axis coordinate), as (integer, float, float)
        """
        if type(subscript)!=int: raise TypeError
        if subscript > (len(self)-1): raise IndexError
        real_index = floor(subscript/self.pts_real)
        imag_index = subscript - (real_index * self.pts_real)
        # print(f"subscript: {subscript}, real index: {real_index}, imag index: {imag_index}")
        return self.get_iter_value_with_ri(real_index, imag_index)
