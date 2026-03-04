"""
This module defines the tkMandelbrotSetViewManager class, which is a concrete implementation of tkViewManager for a Mandelbrot set visualization application.
Acts as Observer, and handles the interactions between the Mandelbrot set app's widgets, which are also defined in this module.

Exported Classes:
    tkMandelbrotSetViewManager -- Concrete implementation of tkViewManager for a Mandelbrot set visualization application.
    MandelbrotSetPlotWidget -- Tkinter widget that provides a matplotlib visualization of a Mandelbrot set
    MandelbrotSetZoomNavigationWidget -- Tkinter widget that provides widget's for navigating a tree of Mandelbrot set zoom locations

Exported Exceptions:
    None    
 
Exported Functions:
    None
"""


# Standard imports
import tkinter as tk
from tkinter import ttk
from functools import partial
from turtle import color

# 3rd party package imports (e.g., from PyPi)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from matplotlib.patches import Rectangle

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
        Implementation of tkViewManager._CreateWidgets().
        Sets up and registers the child widgets of the tkMandelbrotSetViewManager widget.
        :return None:
        """
        self._zoom_nav_widget = MandelbrotSetZoomNavigationWidget(self)
        self.register_subject(self._zoom_nav_widget, self.handle_zoom_nav_widget_update)
        self._zoom_nav_widget.attach(self)
        self._zoom_nav_widget.grid(column=0, row=0, sticky='NWES') # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=0) # Grid-2
        # Disable/enable appropriate zoom navigation controls based on available zoom directions.
        self._enable_disable_zoom_nav_controls()

        self._plot_widget = MandelbrotSetPlotWidget(self)
        self.register_subject(self._plot_widget, self.handle_plot_widget_update)
        self._plot_widget.attach(self)
        self._plot_widget.grid(column=0, row=1, sticky='NWES') # Grid-2
        self.columnconfigure(0, weight=4) # Grid-2
        self.rowconfigure(1, weight=1) # Grid-2
        model = self.getModel()
        self._plot_widget.set_state(model.ul_corner, model.lr_corner, '', True)

        return None

    def handle_model_update(self):
        """
        Handle updates from the model.
        :return None:
        """
        # Show a wait cursor, since this is a long-ish operation.
        self.master.master.config(cursor='watch')
        self.master.master.update()

        model = self.getModel()
        x, y, z = model.get_current_node_plot_data()

        # Get available zoom locations from Model
        avail_zooms = self.getModel().get_current_node_available_zoom_locations()

        # Ask the plot widget to make the plot
        self._plot_widget.make_plot(x, y, z, avail_zooms)

        # Put the cursor back to normal.
        self.master.master.config(cursor='')

        return None
        
    def handle_plot_widget_update(self):
        """
        Handle updates from MandelbrotSetPlotWidget widget.
        :return None:
        """
        # Show a wait cursor, since this is a long-ish operation.
        self.master.master.config(cursor='watch')
        self.master.master.update()

        pw_state = self._plot_widget.get_state()
        widget_zoom = (pw_state[0], pw_state[1])
        model_zoom = (self.getModel().ul_corner, self.getModel().lr_corner)
        # For efficiency, only update the model corner values if they are different
        if model_zoom != widget_zoom:
            # Note: set_corners() will result in the Model calling notify(), resulting in handel_model_update() getting
            # called, and in the plot being redrawn.
            self.getModel().set_corners(widget_zoom[0], widget_zoom[1])
        else:
            # We'll assume, since the corner values didn't change, that the colormap selection or show zoom checkbutton changed,
            # and we need the plot to be redrawn.
            x, y, z = self.getModel().get_current_node_plot_data()
            # Get available zoom locations from Model
            avail_zooms = self.getModel().get_current_node_available_zoom_locations()
            self._plot_widget.make_plot(x, y, z, avail_zooms)
        # Disable/enable appropriate zoom navigation controls based on available zoom directions.
        self._enable_disable_zoom_nav_controls()

        # Put the cursor back to normal.
        self.master.master.config(cursor='')

        return None

    def handle_zoom_nav_widget_update(self):
        """
        Handle updates from MandelbrotSetZoomNavigationWidget widget.
        :return: None
        """
        (nav_req, nav_index) = self._zoom_nav_widget.get_state()
        match nav_req:
            case 'None':
                pass
            case 'Home':
                self.getModel().home()
            case 'Back':
                self.getModel().rewind()
            case 'Forward':
                self.getModel().forward(nav_index)

        # Disable/enable appropriate zoom navigation controls based on available zoom directions.
        self._enable_disable_zoom_nav_controls()
        # Populate the Forward zoom navigation menu based on available zoom locations
        avail_zooms = self.getModel().get_current_node_available_zoom_locations()
        self._zoom_nav_widget._populateForwardMenu(avail_zooms)

        # Since the model's corner values may have changed based on the model operation performed in the above match statement,
        # it is required to update the zoom widget's corners as well, otherwise the next call to handle_plot_widget_update() method
        # may mistakenly set the model corners.
        pw_state = self._plot_widget.get_state()
        model = self.getModel()
        ulc = model.ul_corner
        lrc = model.lr_corner
        self._plot_widget.set_state(ulc, lrc, pw_state[2], pw_state[3])

        return None

    def _enable_disable_zoom_nav_controls(self):
        """
        This is a utility function called to appropriately enable or disable zoom navigation controls based on available
        zoom directions.
        :return: None
        """
        zoomIDs=self._get_backward_forward_ids()
        back_disabled = False
        if zoomIDs[0].int==0x0: back_disabled=True
        forward_disabled = False
        if len(zoomIDs[1])<1: forward_disabled=True
        self._zoom_nav_widget.disable(back_disabled, forward_disabled)
        return None
    
    def _get_backward_forward_ids(self):
        """
        This is a utility function used to retrieve unique id codes from the Model for the backward and forward possible zoom navigations.
        :return: Tuple as follows:
                 [0] ID of available backward zoom, with UUID(int=0x0x) value indicating no possible backward zoom, as UUID or UUID(int=0x0) 
                 [1] List of IDs of available forwards zoom, with empty indicating no possible backward zoom, as [UUID] 
        """
        back_ID = self.getModel().get_current_node_predecessor_ID()
        forward_IDs = self.getModel().get_current_node_successor_IDs()
        return (back_ID, forward_IDs)


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
        self._figure = Figure(figsize=(5,4), dpi=100) # figsize=(width in inches, height in inches)
        self._ax = self._figure.add_subplot()
        
        self._mpl_figure_canvas = FigureCanvasTkAgg(self._figure, self)
        self._mpl_figure_canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky='NWES') # Grid-3
        self.columnconfigure(0, weight=1) # Grid-3
        self.rowconfigure(0, weight=1) # Grid-3

        # The corners of a zoom rectangle, should be set to complex()
        self._zoom_ulc = None
        self._zoom_lrc = None

        # Colormap menu button
        self._mbtn_colormap = ttk.Menubutton(self, text='Colormap', takefocus=1)
        self._mbtn_colormap.grid(column=0, row=1) # Grid-3
        self.columnconfigure(0, weight=1) # Grid-3
        self.rowconfigure(1, weight=0) # Grid-3
        # Colormap menu button menu
        self._menu_colormap = tk.Menu(self._mbtn_colormap)
        self._mbtn_colormap['menu'] = self._menu_colormap

        # Load the Colormap menu with choices
        # Here, for now, we will just add a pair of colormaps. Later, may want to get the full list from matplotlib.
        self._colormaps = {'nipy_spectral':'nipy_spectral', 'Set1':'Set1'}
        for key in self._colormaps:
            self._menu_colormap.add_command(label = str(self._colormaps[key]), command = partial(self.onSelectColormap, key))
        self._selected_colormap = 'nipy_spectral'

        # matplotlib RectangleSelector (for interactive zooming)
        self._zoom_rectangle = RectangleSelector(self._ax,
                                                 self.zoom_rectangle_callback,
                                                 useblit=True,
                                                 button=[1, 3],  # disable middle button
                                                 minspanx=5,
                                                 minspany=5,
                                                 spancoords='pixels',
                                                 interactive=True)

        self._ckbt_show_zooms = ttk.Checkbutton(self, text='Show Zoom Rectangles', command=self.onShowZoomCheckButtonClick)
        self._ckbt_show_zooms.grid(column=1, row=1) # Grid-3
        self.columnconfigure(1, weight=1) # Grid-3
        self.rowconfigure(1, weight=0) # Grid-3
        self._ivar_show_zooms = tk.IntVar()
        self._ivar_show_zooms.set(1) # Starting state is checked or show
        self._ckbt_show_zooms['variable']=self._ivar_show_zooms

        return None

    def onShowZoomCheckButtonClick(self):
        """
        Handle checking or unchecking the "Show Zoom Rectangles" check button.
        :return: None
        """
        self.notify()
        return None

    def zoom_rectangle_callback(self, eclick, erelease):
        """
        Callback for zoom rectangle.
        :parameter eclick: The matplotlib mouse button click event
        :parameter erelease: The matplotlib mouse button release event
        :return: None
        """
        # Need to see the zoom rectangle, so make visible, so it shows up on the plot.
        for artist in self._zoom_rectangle.artists :
            artist.set_visible(False)
        self._zoom_rectangle.update()

        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        # Handle the possibility that the user dragged in different directions from the initial click 
        if x1 < x2:
            ulcr = x1
            lrcr = x2
        else:
            ulcr = x2
            lrcr = x1
        if y1 > y2:
            ulci = y1
            lrci = y2
        else:
            ulci = y2
            lrci = y1
        self._zoom_ulc = complex(ulcr, ulci)
        self._zoom_lrc = complex(lrcr, lrci)
        # print(f"Zooming to upper-left-corner {self._zoom_ulc} and lower-right-corner {self._zoom_lrc}.")
        self.notify()
        
        # Done with the zoom rectangle, so make it invisible, so it doesn't continue to show up on the plot.
        for artist in self._zoom_rectangle.artists :
            artist.set_visible(False)
        self._zoom_rectangle.update()
        
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
        Returns the zoom corners of the widget, the selected colormap, and if zoom locations should be visually indicated.
        :return: Tuple (upper-left corner, lower-right-corner, selected colormap, show zoom locations), as tuple (complex, complex, string boolean)
        """
        show_zooms = False
        if self._ivar_show_zooms.get() == 1: show_zooms = True
        return (self._zoom_ulc, self._zoom_lrc, self._selected_colormap, show_zooms)

    def set_state(self, ulc=complex(0,0), lrc=complex(0,0), color_map='', show_zooms=True):
        """
        Sets the zoom corners of the widget, the selected colormap, and the state of the show zoom rectangles checkbutton.
        :parameter ulc: Upper-left corner of the zoom rectangle in the complex plane, complex
        :parameter lrc: Lower-right corner of the zoom rectangle in the complex plane, complex
        :parameter color_map: Name of matplotlib colormap
        :parameter show_zooms: True if zoom rectangles should be drawn on the plot, as bool
        :return: None
        """
        assert(type(ulc)==complex)
        assert(type(lrc)==complex)
        assert(lrc.real>ulc.real)
        assert(lrc.imag<ulc.imag)
        assert(type(color_map)==str)
        assert(type(show_zooms)==bool)
        self._zoom_ulc = ulc
        self._zoom_lrc = lrc
        if len(color_map) != 0:
            self._selected_colormap = color_map
        if show_zooms:
            self._ivar_show_zooms.set(1)
        else:
            self._ivar_show_zooms.set(0)
        self.notify()
        return None

    def make_plot(self, x, y, z, avail_zooms=[]):
        """
        Make the Mandelbrot set plot with calls to matplotlib.
        :parameter x: real-axis (x) values as list of floats
        :parameter y: imaginary-axis (y) values as list of floats
        :parameter z: iterations for divergence at each point, as a list of lists of ints, in column major order, such that,
                      z[j][i] = the zth value at the jth value of the imaginary axis and the ith value of the real axis
        :parameter avail_zooms: List of available zooms, to be indicated visually on the plot, as list of tuples:
                                (ulx,uly,lrx,lry), where: ulx = upper-left-corner x-value of zoom location
                                                          uly = upper-left-corner y-value of zoom location
                                                          lrx = lower-right-corner x-value of zoom location
                                                          lry = lower-right-corner y-value of zoom location
        :return: None
        """
        self._ax.cla() # Clear the axes for the next time through...
        
        # Provide axis labels
        self._ax.set_aspect("equal")
        self._ax.set_xlabel("Real-Axis")
        self._ax.set_ylabel("Imaginary-Axis")
        self._ax.use_sticky_edges = True
        
        # Create the Mandelbrot set plot
        graph = self._ax.pcolormesh(x, y, z, cmap=self._selected_colormap)

        # Use rectangle "patches" to visually indicate available zoom locations.
        # And annotate each rectangle with an index number.
        if self._ivar_show_zooms.get() == 1:
            zi = 0
            for zoom in avail_zooms:
                ulx = zoom[0]
                uly = zoom[1]
                lrx = zoom[2]
                lry = zoom[3]
                width = lrx-ulx
                height = uly-lry 
                self._ax.add_patch(Rectangle((ulx, lry), width, height, facecolor="none", ec='r', lw=2))
                self._ax.annotate(f"{zi}", xy=(ulx, uly), xytext=(ulx, lry), color='r', fontsize='large', fontweight='bold')
                zi += 1

        # Actually draw the figure
        self._mpl_figure_canvas.draw()

        return None


class MandelbrotSetZoomNavigationWidget(ttk.Labelframe, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which enables navigation within the set of zoom location
    histories (zoom rectangles) stored by the Model.
    Class is also a Subject in Observer design pattern.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget, in this case the tkMandelbrotsetViewManager
        """
        ttk.Labelframe.__init__(self, parent, text="Mandelbrot Set Zoom History Navigation")
        Subject.__init__(self)
        self._CreateWidgets()

    def _CreateWidgets(self):
        """
        This method is called by __init__() to create the child widgets of the MandelbrotSetZoomNavigationWidget.
        :return None:
        """
        self._possible_moves = ['None', 'Home', 'Back', 'Forward']
        self._requested_move = self._possible_moves[0] # So 'None'
        self._forward_index = 0

        self._btn_home= ttk.Button(self, text='Home', command=self.OnHomeButtonClicked)
        self._btn_home.grid(column=0, row=0) # Grid-3
        self.columnconfigure(0, weight=1) # Grid-3
        self.rowconfigure(0, weight=1) # Grid-3

        self._btn_back = ttk.Button(self, text='<< Back', command=self.OnBackButtonClicked)
        self._btn_back.grid(column=1, row=0) # Grid-3
        self.columnconfigure(1, weight=1) # Grid-3
        self.rowconfigure(0, weight=1) # Grid-3

        # Forward menu button
        self._mbtn_forward = ttk.Menubutton(self, text='Forward', takefocus=1)
        self._mbtn_forward.grid(column=2, row=0) # Grid-3
        self.columnconfigure(2, weight=1) # Grid-3
        self.rowconfigure(0, weight=0) # Grid-3
        # Forward menu button menu
        self._menu_forward = tk.Menu(self._mbtn_forward)
        self._mbtn_forward['menu'] = self._menu_forward

        return None

    def _populateForwardMenu(self, avail_zooms=[]):
        """
        Utility function for populating Forward menu with commands.
        :parameter avail_zooms: List of available zoom locations.
                                Note: It actually makes no difference what objects are in the list to represent available zooms.
                                      The only thing that matters is the numnber of objects in the list.
        :return: None
        """
        # Remove any current commands from the menu
        self._menu_forward.delete(0, self._menu_forward.index(tk.END))
        # Add new commands to the menu
        index = 0
        for zoom in avail_zooms:
            self._menu_forward.add_command(label = f"Zoom Location {index}", command = partial(self.onSelectForwardZoom, index))
            index += 1
        return None

    def onSelectForwardZoom(self, index):
        """
        Handle selection of zoom location from Forward menu.
        :parameter Index: Index (0, 1, 2, ...) of the zoom location selected from the menu, integer
        :return: None
        """
        self._set_state('Forward', index)
        return None
    
    def OnHomeButtonClicked(self):
        """
        Handle click of the Home button
        :return: None
        """
        self._set_state('Home')
        return None

    def OnBackButtonClicked(self):
        """
        Handle click of the Back button
        :return: None
        """
        self._set_state('Back')
        return None

    def _set_state(self, state_string, state_index=-1):
        """
        Set the "move" that the user requests.
        :parameter state_string: One string from list ['None', 'Home', 'Back', 'Forward'], as string
        :parameter state_index: Integer indicating which forward zoom path was requested, as integer
        :return: None
        """
        if state_string in self._possible_moves:
            self._requested_move = state_string
            self._forward_index = state_index
            self.notify()
            self._requested_move = self._possible_moves[0] # So, 'None'
            self._forward_index = -1
        return None

    def get_state(self):
        """
        Returns the "move" that the user requested.
        :return: Tuple (One string from list ['None', 'Home', 'Back', 'Forward'], index of requested forward zoom), as (string, integer)
        """
        return (self._requested_move, self._forward_index)

    def disable(self, back_disabled=True, forward_disabled=True):
        """
        Used to set if widget's 'back' and 'forward' buttons are enabled or disabled.
        :parameter back_disabled: True if the widget's 'back' button should be disabled, False if it should be enabled, boolean
        :parameter forward_disabled: True if the widget's 'forward' button should be disabled, False if it should be enabled, boolean
        :return None:
        """
        # Handle back button
        if back_disabled:
            self._btn_back.state(['disabled'])
        else:
            self._btn_back.state(['!disabled'])
        # Handle forward menu button
        if forward_disabled:
            self._mbtn_forward.state(['disabled'])
        else:
            self._mbtn_forward.state(['!disabled'])
        return None
