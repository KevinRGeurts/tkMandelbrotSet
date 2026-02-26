"""
This module defines the MandelbrotSet class, which generates a Mandelbrot set and stores it for later retrieval.

Exported classes:
    MandelbrotSet: Class that can generate a Mandelbrot Set.

Exported functions:
    None

Exported exceptions:
    None
"""


# standard library imports
from array import array
from math import floor

# package imports
from tkMandelbrotSet.memento import SetMemento


class MandelbrotSet(object):
    """
    Class that can generate a Mandelbrot Set.
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
        # The Mandelbrot set will be stored as a list of  arrays of integers, where each integer represents the
        # number of iterations it took for the corresponding point in the complex plane to diverge.
        # To access the value at point (real_index=i, imaginary_index=j): self._mandelbrot_set[i][j]
        self._mandelbrot_set = []
        for i in range(self.pts_real):
            self._mandelbrot_set.append(array('i'))
        assert(len(self._mandelbrot_set)==self.pts_real)
        # Flag indicating if generate_mandelbrot_set() method has been called, and thus if results are available.
        self._set_generated = False

    def create_memento(self):
        """
        Create a SetMemento object that is a snapshot of the "state" of this MandelbrotSet object.
        :return: SetMemento object
        """
        memento = SetMemento(self._ul_corner, self._lr_corner, self._pts_real, self._pts_imag, self._z_max, self._max_iters)
        return memento

    def set_memento(self, memento=SetMemento()):
        """
        Use the argument memento to restore the "state" of the MandelbrotSet object to the snapshot stored by the memento.
        :return: None
        """
        state = memento.get_state()
        self.set_corners(state[0], state[1])
        self._pts_real = state[2]
        self._pts_imag = state[3]
        self._z_max = state[4]
        self._max_iters = state[5]
        return None

    def _clear_mandelbrot_set_data(self):
        """
        Utility function called to clear Mandelbrot set data.
        :return: None
        """
        if self._set_generated:
            for i in range(self.pts_real):
                column = self._mandelbrot_set[i]
                for j in range(self.pts_imag):
                    column.pop()
                assert(len(column)==0)
            assert(len(self._mandelbrot_set)==self.pts_real)
            self._set_generated = False
        return None

    @property
    def ul_corner(self):
        """
        Returns the upper left corner of the complex plane to be visualized, as complex.
        """
        return self._ul_corner

    @ul_corner.setter
    def ul_corner(self, value):
        """
        :parameter value: as complex
        """
        assert(type(value)==complex)
        self._ul_corner = value
        self._clear_mandelbrot_set_data()

    @property
    def lr_corner(self):
        """
        Returns the lower right corner of the complex plane to be visualized, as complex.
        """
        return self._lr_corner

    @lr_corner.setter
    def lr_corner(self, value):
        """
        :parameter value: as complex
        """
        assert(type(value)==complex)
        self._lr_corner = value
        self._clear_mandelbrot_set_data()

    def set_corners(self, ul_corner=complex(real=-2.0, imag=2.0), lr_corner=complex(real=1.0, imag=-2.0)):
        """
        Set both corners of the complex plane to be visualized. Call this function instead of the property setters
        for the individual corners when you want to change both corners and only want one notify() to Observers.
        :parameter ul_corner: The upper left corner of the complex plane to be visualized, complex
        :parameter lr_corner: The lower right corner of the complex plane to be visualized, complex
        :return: None
        """
        assert(type(ul_corner)==complex)
        assert(type(lr_corner)==complex)
        assert(lr_corner.real>ul_corner.real)
        assert(lr_corner.imag<ul_corner.imag)
        self._ul_corner = ul_corner
        self._lr_corner = lr_corner
        self._clear_mandelbrot_set_data()
        return None

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
            result = self._point_iterator(complex(self._indices_to_point(real_index, imag_index)))
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
        # This if makes it "safe" (that is, no time wasted) to call the more than once without any changes to the set generating attributes.
        # If the set has already been generated, then it won't be regenerated.
        if not self._set_generated:
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
    
    def get_plot_data(self, invert_z = False):
        """
        Package up and return data required to make a Mandelbot set plot, in a format appropriate for matplotlib.
        If the set has not yet been generated by a call to generate_mandelbrot_set() method, then it will be generated.
        :parameter invert_z: If True, then returned z-values will be (self.max-iters - z), which may match z-values better
                             to certain plotting color maps.
        :return: as tuple:
            [0]: real-axis (x) values as list of floats
            [1]: imaginary-axis (y) values as list of floats
            [2]: iterations for divergence at each point, as a list of lists of ints, in column major order, such that,
                 z[j][i] = the zth value at the jth value of the imaginary axis and the ith value of the real axis
        """
        # If the Mandelbrot set has not been generated, then generate it.
        if not self._set_generated:
            self.generate_mandelbrot_set()
        
        # Get and package up the axes data for plotting
        _x=[]
        for i in range(self.pts_real):
            _x.append(self._indices_to_point(i,0).real)
        _y=[]
        for j in range(self.pts_imag):
            _y.append(self._indices_to_point(0,j).imag)
    
        # Obtain the mandelbrot set values, and package them for plotting
        _z=[]
        for j in range(self.pts_imag):
            _z.append([])
            for i in range(self.pts_real):
                pnt_res = self.get_iter_value_with_ri(i,j)
                if invert_z:
                    _z[j].append(self.max_iters - pnt_res[0])
                else:
                    _z[j].append(pnt_res[0])
        return (_x, _y, _z)

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
