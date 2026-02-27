"""
This module defines the MandelbrotSetModel class, which is the Model object for the MandelbrotSetApp.

Exported classes:
    MandelbrotSetModel: Class that is the Model object for the MandelbrotSetApp.

Exported functions:
    None

Exported exceptions:
    None
"""


# standard library imports
from uuid import UUID

# package imports
from tkMandelbrotSet.mandelbrot import MandelbrotSet
from tkMandelbrotSet.bigraph import Bigraph, BigraphNode, Branch
from tkMandelbrotSet.memento import SetMemento
from tkMandelbrotSet.exceptions import MandelbrotSetNoPreviousZoomLocation, MandelbrotSetNoNextZoomLocation
from tkAppFramework.model import Model


class MandelbrotSetModel(Model):
    """
    Class is the Model object for the MandelbrotSetApp.
    """
    def __init__(self):
        """
        Initialize the MandelbrotSetModel with a MandelbrotSet object for doing the computations, and with a
        Bigraph object for storing the set zoom paths.
        """
        super().__init__()
        self._mandelbrot_set = MandelbrotSet()
        root_memento = self._mandelbrot_set.create_memento()
        root_node = BigraphNode(payload=root_memento)
        branch_first_node = BigraphNode(payload=root_memento) # Same payload as root_node, at least for now
        self._zoom_graph = Bigraph(root_node)
        self._current_branch = Branch(branch_first_node, 'only branch for now')
        self._zoom_graph.add_branch(new_branch=self._current_branch)
        self._current_node = branch_first_node

    @property
    def ul_corner(self):
        return self._mandelbrot_set.ul_corner

    @property
    def lr_corner(self):
        return self._mandelbrot_set.lr_corner

    def get_current_node_predecessor_ID(self):
        """
        Return the GUID of the predecessor of the current zoom location (node).
        :return: UUID if a predecessor exists, or UUID(int=0x0) if it does not
        """
        result = UUID(int=0x0) # This is the "no predecessor" return value
        pre = self._current_node.predecessor
        if pre is not None:
            result = pre.nodeID
        return result

    def get_current_node_successor_IDs(self):
        """
        Return the GUIDs of the successors of the current zoom location (node).
        :return: List of UUID if one or more successors exists, or an empty list if none exist
        """
        result = [] # This is the "no successors" return value, it it stays an empty list
        sucs = self._current_node.get_successors()
        for suc in sucs:
            result.append(suc.nodeID)
        return result
    
    def get_current_node_plot_data(self):
        """
        Return Mandelbrot set data (formatted for plotting) for the current zoom location (node).
        :return: as tuple:
            [0]: real-axis (x) values as list of floats
            [1]: imaginary-axis (y) values as list of floats
            [2]: iterations for divergence at each point, as a list of lists of ints, in column major order, such that,
                 z[j][i] = the zth value at the jth value of the imaginary axis and the ith value of the real axis
        """
        memento = self._current_node.payload
        self._mandelbrot_set.set_memento(memento)
        plot_data = self._mandelbrot_set.get_plot_data()
        return plot_data

    def home(self):
        """
        Move the current zoom location back to the root of zoom tree.
        Note: For now, the move is actually to the root's successor, which has the same payload as the root.
        :return: None
        """
        self._current_node = self._zoom_graph.root.successor
        self.notify()
        return None

    def rewind(self):
        """
        Move the current zoom location back one location (node) in the zoom tree. If there is no previous location,
        then the current zoom location is not changed, and an exception (MandelbrotSetNoPreviousZoomLocation) is raised.
        :return: None
        """
        move_to_node = self._current_node.predecessor
        if move_to_node is not None:
            self._current_node = move_to_node
            self.notify()
        else:
            raise MandelbrotSetNoPreviousZoomLocation
        return None

    def forward(self):
        """
        Move the current zoom location forward one location (node) in the zoom tree. If there is no next location,
        then the current zoom location is not changed, and an exception (MandelbrotSetNoNextZoomLocation) is raised.
        Note that as currently implemented, this method will always move forward to the first successor available, and
        thus it does not (yet) understand tree branching.
        :return: None
        """
        move_to_node = self._current_node.successor
        if move_to_node is not None:
            self._current_node = move_to_node
            self.notify()
        else:
            raise MandelbrotSetNoNextZoomLocation
        return None

    def set_corners(self, ul_corner=complex(real=-2.0, imag=2.0), lr_corner=complex(real=1.0, imag=-2.0)):
        """
        Create a new zoom location, and set both corners of the complex plane to be visualized.
        Note that currently this new zoom location is always added as the new tip of the only branch.
        :parameter ul_corner: The upper left corner of the complex plane to be visualized, complex
        :parameter lr_corner: The lower right corner of the complex plane to be visualized, complex
        :return: None
        """
        self._mandelbrot_set.set_corners(ul_corner, lr_corner)
        memento = self._mandelbrot_set.create_memento()
        new_node = BigraphNode(payload=memento)
        self._zoom_graph.branches[0].add_node(new_node)
        self._current_node = new_node
        self.notify()
        return None
