"""
This module defines the MandelbrotSetModel class, which is the Model object for the MandelbrotSetApp, following the tkAppFramework.

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
from tkMandelbrotSet.mandelbrot import MandelbrotSet, plot_mandelbrot_set
from tkMandelbrotSet.bigraph import Bigraph, BigraphNode, Branch
from tkMandelbrotSet.memento import SetMemento
from tkMandelbrotSet.exceptions import MandelbrotSetNoPreviousZoomLocation, MandelbrotSetNoNextZoomLocation
from tkAppFramework.model import Model


class MandelbrotSetModel(Model):
    """
    Class is the Model object for the MandelbrotSetApp, following the tkAppFramework.
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
        self._current_branch = Branch(branch_first_node, f"branch starting with node {branch_first_node.nodeID}")
        self._zoom_graph.add_branch(new_branch=self._current_branch)
        self._current_node = branch_first_node

    @property
    def ul_corner(self):
        """
        Return the upper left corner of the Mandelbrot set in the complex plane, as complex.
        """
        return self._mandelbrot_set.ul_corner

    @property
    def lr_corner(self):
        """
        Return the lower right corner of the Mandelbrot set in the complex plane, as complex.
        """
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

    def get_current_node_available_zoom_locations(self):
        """
        Get a list of the available zoom locations (that is, payload locations of node successors) for the current zoom
        location (node).
        :return: List of available zooms as list of tuples:
                    (ulx,uly,lrx,lry), where: ulx = upper-left-corner x-value (real-axis) of zoom location
                                              uly = upper-left-corner y-value (imaginary-axis) of zoom location
                                              lrx = lower-right-corner x-value (real-axis) of zoom location
                                              lry = lower-right-corner y-value (imaginary-axis) of zoom location        
        """
        avail_zooms = []
        sucs = self._current_node.get_successors()
        for suc in sucs:
            payload = suc.payload
            state = payload.get_state()
            location = (state[0].real, state[0].imag, state[1].real, state[1].imag)
            avail_zooms.append(location)
        return avail_zooms
    
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

    def prune(self):
        """
        Prune the zoom tree at the current zoom location.
        :return: None
        """
        # Set the current branch to the branch that will be retained after the prune.
        self._current_branch = self._zoom_graph.get_nodes_branch(self._current_node)
        self._zoom_graph.prune(self._current_node)
        return None
    
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

    def forward(self, index=-1):
        """
        Move the current zoom location forward one location (node) in the zoom tree, with index parameter being an index
        into the list of successor nodes of the current node.
        If there is no next location, then the current zoom location is not changed, and an exception (MandelbrotSetNoNextZoomLocation) is raised.
        Note that if index<0 (default value) this method will move forward to the LAST successor available, and
        thus along the most recently created branch.
        :return: None
        """
        sucs = self._current_node.get_successors()
        if len(sucs) == 0 or index > len(sucs)-1:
            move_to_node = None
        elif index < 0:
            move_to_node = sucs[len(sucs)-1]
        else:
            move_to_node = sucs[index]
        if move_to_node is not None:
            self._current_branch = self._zoom_graph.get_nodes_branch(move_to_node)
            self._current_node = move_to_node
            self.notify()
        else:
            raise MandelbrotSetNoNextZoomLocation
        return None

    def set_corners(self, ul_corner=complex(real=-2.0, imag=2.0), lr_corner=complex(real=1.0, imag=-2.0)):
        """
        Create a new zoom location, and set both corners of the complex plane to be visualized.
        Note that this will:
            (1) add the new zoom location as the new tip of a branch, if we are zooming from the current tip of a branch, or
            (2) split a branch, create a new branch, and make the new zoom location the tip of the new brach, if we
                are zooming from a location along a current branch
        :parameter ul_corner: The upper left corner of the complex plane to be visualized, complex
        :parameter lr_corner: The lower right corner of the complex plane to be visualized, complex
        :return: None
        """
        self._mandelbrot_set.set_corners(ul_corner, lr_corner)
        memento = self._mandelbrot_set.create_memento()
        new_node = BigraphNode(payload=memento)
        # If current node is the tip node of the current branch, then add the new node such that it becomes the new tip
        # of the current branch. We will use the node ids to determine node "equality".
        if self._current_node.nodeID == self._current_branch.tip_node.nodeID:
            self._current_branch.add_node(new_node)
        # Otherwise, we are "splitting" the current branch, so we need to create a new branch at the current node.
        else:
            new_branch = Branch(tip=new_node, name=f"branch starting with node {new_node.nodeID}")
            self._zoom_graph.add_branch(at_node=self._current_node, new_branch=new_branch)
            self._current_branch = new_branch
        self._current_node = new_node
        self.notify()
        return None

    def export_plot(self):
        """
        Export the current Mandelbrot Set visualization plot to a graphics file. This will be done by launching
        matplotlib's interactive figure window, which provides a toolbar button for saving to various formats of
        image files.
        :return: None
        """
        (x, y ,z) = self.get_current_node_plot_data()
        plot_mandelbrot_set(x, y, z, bare=True)
        return None
