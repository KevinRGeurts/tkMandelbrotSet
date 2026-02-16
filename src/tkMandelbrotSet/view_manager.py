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
from functools import partial

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
        self._model_mementos = []

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
        self._plot_widget.grid(column=0, row=0, sticky='NWES') # Grid-2
        self.columnconfigure(0, weight=4) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        model = self.getModel()
        self._plot_widget.set_state(model.ul_corner, model.lr_corner, '')

        self._memento_widget = MandelbrotSetMementoWidget(self)
        self.register_subject(self._memento_widget, self.handle_memento_widget_update)
        self._memento_widget.attach(self)
        self._memento_widget.grid(column=1, row=0, sticky='NWES') # Grid-2
        self.columnconfigure(1, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2

        return None

    def handle_model_update(self):
        """
        Handle updates from the model.
        :return None:
        """
        model = self.getModel()
        model_zoom = (model.ul_corner, model.lr_corner)
        pw_state = self._plot_widget.get_state()
        widget_zoom = (pw_state[0], pw_state[1])
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
        pw_state = self._plot_widget.get_state()
        widget_zoom = (pw_state[0], pw_state[1])
        model_zoom = (self.getModel().ul_corner, self.getModel().lr_corner)
        # For efficiency, only update the model corner values if they are different
        if model_zoom != widget_zoom:
            # Note: set_corners() will result in the Model calling notify(), resulting in handel_model_update() getting
            # called, and in the plot being redrawn.
            self.getModel().set_corners(widget_zoom[0], widget_zoom[1])
        else:
            # We'll assume, since the corner values didn't change, that the colormap selection changed.
            # And we need the plot to be redrawn.
            x, y, z = self.getModel().get_plot_data()
            self._plot_widget.make_plot(x, y, z)
        return None

    def handle_memento_widget_update(self):
        """
        Handle updates from MandelbrotSetMementoWidget widget.
        :return: None
        """
        # TODO: Pass the selected memento back to the Model
        return None


class MandelbrotSetPlotWidget(ttk.Labelframe, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which display a matplotlib visualization of the Mandelbrot set.
    Class is also a Subject in Observer design pattern.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget, in this case the tkMandelbrotsetViewManager
        """
        ttk.Labelframe.__init__(self, parent, text="Mandelbrot Set Visualization")
        Subject.__init__(self)
        self._CreateWidgets()

    def _CreateWidgets(self):
        """
        This method is called by __init__() to create the child widgets of the MandelbrotSetPlotWidget.
        :return None:
        """
        # Make a matplotlib Figure that will be added to the matplotlib FigureCanvasTkAgg below,
        # and give it an axes.
        self._figure = Figure(figsize=(5,4), dpi=100)
        self._ax = self._figure.add_subplot()
        
        self._mpl_figure_canvas = FigureCanvasTkAgg(self._figure, self)
        # master is root (seems weird, so is this really necessary)
        # self._mpl_figure_canvas = FigureCanvasTkAgg(self._figure, self.master.master.master)
        self._mpl_figure_canvas.get_tk_widget().grid(column=0, row=0, sticky='NWES') # Grid-3
        self.columnconfigure(0, weight=1) # Grid-3
        self.rowconfigure(0, weight=1) # Grid-3

        # The corners of a zoom rectangle
        self._zoom_ulc = complex(0,0)
        self._zoom_lrc = complex(0,0)

        # Colormap menu button
        self._mbtn_colormap = ttk.Menubutton(self, text='Colormap', takefocus=1)
        self._mbtn_colormap.grid(column=0, row=1) # Grid-3
        self.columnconfigure(0, weight=1) # Grid-3
        self.rowconfigure(1, weight=0) #
        # Colormap menu button menu
        self._menu_colormap = tk.Menu(self._mbtn_colormap)
        self._mbtn_colormap['menu'] = self._menu_colormap

        # Load the Colormap menu with choices
        # Here, for now, we will just add a pair of colormaps. Later, may want to get the full list from matplotlib.
        self._colormaps = {'nipy_spectral':'nipy_spectral', 'Set1':'Set1'}
        for key in self._colormaps:
            self._menu_colormap.add_command(label = str(self._colormaps[key]), command = partial(self.onSelectColormap, key))
        self._selected_colormap = 'nipy_spectral'

        return None

    def onSelectColormap(self, key):
        """
        Handle selection of a colormap from the menu.
        :parameter key: Key of the colormap selected from the menu, string
        :return: None
        """
        assert(isinstance(key, str) and key in self._colormaps)
        self._selected_colormap = key
        self.notify()
        return None

    def get_state(self):
        """
        Returns the zoom corners of the widget, and the selected colormap.
        :return: Tuple (upper-left corner, lower-right-corner, selected colormap), as tuple (complex, complex, string)
        """
        return (self._zoom_ulc, self._zoom_lrc, self._selected_colormap)

    def set_state(self, ulc=complex(0,0), lrc=complex(0,0), cm=''):
        """
        Sets the zoom corners of the widget, and the selected colormap.
        :parameter ulc: Upper-left corner of the zoom rectangle in the complex plane, complex
        :parameter lrc: Lower-right corner of the zoom rectangle in the complex plane, complex
        :return: None
        """
        assert(type(ulc)==complex)
        assert(type(lrc)==complex)
        assert(lrc.real>ulc.real)
        assert(lrc.imag<ulc.imag)
        assert(type(cm)==str)
        self._zoom_ulc = ulc
        self._zoom_lrc = lrc
        if len(cm) != 0:
            self._selected_colormap = cm
        self.notify()
        return None

    def make_plot(self, x, y, z):
        """
        Make the Mandelbrot set plot with calls to matplotlib.
        :parameter x: real-axis (x) values as list of floats
        :parameter y: imaginary-axis (y) values as list of floats
        :parameter z: iterations for divergence at each point, as a list of lists of ints, in column major order, such that,
                      z[j][i] = the zth value at the jth value of the imaginary axis and the ith value of the real axis
        :return: None
        """
        self._ax.set_aspect("equal")
        self._ax.set_xlabel("Real-Axis")
        self._ax.set_ylabel("Imaginary-Axis")
        graph = self._ax.pcolormesh(x, y, z, cmap=self._selected_colormap)
        self._ax.use_sticky_edges = True
        self._mpl_figure_canvas.draw()

        return None


class MandelbrotSetMementoWidget(ttk.Labelframe, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which display the set of "mementos" from the Model
    which represent the "zoom rectangle" history of visualizations of the Mandelbrot set.
    Class is also a Subject in Observer design pattern.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget, in this case the tkMandelbrotsetViewManager
        """
        ttk.Labelframe.__init__(self, parent, text="Mandelbrot Set Zoom Stack")
        Subject.__init__(self)
        self._CreateWidgets()

    def _CreateWidgets(self):
        """
        This method is called by __init__() to create the child widgets of the MandelbrotSetMementoWidget.
        :return None:
        """
        self._lb_mementos = tk.Listbox(self)
        self._lb_mementos.grid(column=0, row=0, sticky='NWES') # Grid-3
        self.columnconfigure(0, weight=1) # Grid-3
        self.rowconfigure(0, weight=1) # Grid-3

        return None

    # def onSelectMemento(self, key):
    #     """
    #     Handle selection of a colormap from the menu.
    #     :parameter key: Key of the colormap selected from the menu, string
    #     :return: None
    #     """
    #     assert(isinstance(key, str) and key in self._colormaps)
    #     self._selected_colormap = key
    #     self.notify()
    #     return None

    # def get_state(self):
    #     """
    #     Returns the zoom corners of the widget, and the selected colormap
    #     :return: Tuple (upper-left corner, lower-right-corner, selected colormap), as tuple (complex, complex, string)
    #     """
    #     return (self._zoom_ulc, self._zoom_lrc, self._selected_colormap)
