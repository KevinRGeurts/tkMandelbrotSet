"""
This module defines the tkMandelbrotSetViewManager class, which is a concrete implementation of tkViewManager for a Mandelbrot set visualization application.
Acts as Observer, and handles the interactions between the Mandelbrot set app's widgets, which are also defined in this module.

Exported Classes:
    tkMandelbrotSetViewManager -- Concrete implementation of tkViewManager for a Mandelbrot set visualization application.

Exported Exceptions:
    None    
 
Exported Functions:
    None
"""


# Standard imports
import tkinter as tk
from tkinter import ttk

# 3rd party package imports (e.g., from PyPi)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Local imports
from tkAppFramework.tkViewManager import tkViewManager
from tkAppFramework.ObserverPatternBase import Subject


class tkMandelbrotSetViewManager(tkViewManager):
    """
    Concrete implementation of tkViewManager. Acts as Observer, and handles the interactions between Mandelbrot set app's widgets.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: The parent widget of this widget, The MandelbrotSetApp, which hereafter will be
        accessed as self.master.
        """
        tkViewManager.__init__(self, parent)
        # Force a preliminary draw of the plot.
        self.handle_model_update()
        
    def _CreateWidgets(self):
        """
        Implementation of tkViewManager._CreateWidgets.
        Sets up and registers the child widgets of the tkMandelbrotSetViewManager widget.
        :return None:
        """
        self._plot_widget = MandelbrotSetPlotWidget(self)
        self.register_subject(self._plot_widget, self.handle_plot_widget_update)
        self._plot_widget.attach(self)
        self._plot_widget.get_tk_widget().grid(column=0, row=0, sticky='NWES') # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2

        return None

    def handle_model_update(self):
        """
        Handle updates from the model.
        :return None:
        """
        model = self.getModel()
        model_zoom = (model.ul_corner, model.lr_corner)
        widget_zoom = self._plot_widget.get_state()
        # For efficiency, only update the plot widget if it's zoom value doesn't match the model value.
        if widget_zoom != model_zoom:
            model.generate_mandelbrot_set()
            x, y, z = model.get_plot_data()
            self._plot_widget.make_plot(x, y, z)
        return None
        
    def handle_plot_widget_update(self):
        """
        Handle updates from MandelbrotSetPlotWidget widget.
        :return None:
        """
        widget_zoom = self._plot_widget.get_state()
        model_zoom = (self.getModel().ul_corner, self.getModel().lr_corner)
        # For efficiency, only update the model corner values if they are different
        if model_zoom != widget_zoom:
            self.getModel().ul_corner = widget_zoom[0]
            self.getModel().lr_corner = widget_zoom[1]
        return None


class MandelbrotSetPlotWidget(ttk.Labelframe, FigureCanvasTkAgg, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which allow the beats per minute of the metronome to be set.
    Class is also a Subject in Observer design pattern.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget, in this case the tkMetronomeViewManager
        :parameter bpm: An initial beats per minute setting for this widget, int
        """
        ttk.Labelframe.__init__(self, parent, text="Mandelbrot Set Visualization")
        Subject.__init__(self)
        self._figure = Figure(figsize=(5,4), dpi=100)
        self._ax = self._figure.add_subplot()
        self._ax.set_aspect("equal")
        self._ax.set_xlabel("Real-Axis")
        self._ax.set_ylabel("Imaginary-Axis")
        self._ax.pcolormesh([-2.0, 1.0], [2.0, -2.0], [[1.0, 1.0], [1.0, 1.0]]) # dummy plot to draw below
        # master is root
        FigureCanvasTkAgg.__init__(self, self._figure, self.master.master.master)
        FigureCanvasTkAgg.draw(self)

        self._zoom_ulc = complex(0,0)
        self._zoom_lrc = complex(0,0)

    def get_state(self):
        """
        Returns the zoom corners of the widget.
        :return: Tuple (upper-left corner, lower-right-corner), as tuple (complex, complex)
        """
        return (self._zoom_ulc, self._zoom_lrc)

    def make_plot(self, x, y, z):
        """
        Make the Mandelbrot set plot with calls to matplotlib.
        :parameter x: real-axis (x) values as list of floats
        :parameter y: imaginary-axis (y) values as list of floats
        :parameter z: iterations for divergence at each point, as a list of lists of ints, in column major order, such that,
                      z[j][i] = the zth value at the jth value of the imaginary axis and the ith value of the real axis
        :return: None
        """
        graph = self._ax.pcolormesh(x, y, z, cmap="nipy_spectral")
        # plt.colorbar(graph)
        FigureCanvasTkAgg.draw(self)

        return None
