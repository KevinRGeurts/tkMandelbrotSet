"""
This module defines the MandelbrotSetApp class, which is a concrete implementation of the tkApp framework for a Mandelbrot set visualization application.

Exported Classes:
    MandelbrotSetApp -- Concrete implementation of tkApp for a Mandelbrot set visualization application.

Exported Exceptions:
    None    
 
Exported Functions:
    __main__: Starts Tcl interpreter and launches Mandelbrot set application.

Scripting:
    To run the MandelbrotSetApp, execute this module as the main program. This will create an instance of the MandelbrotSetApp and start its event loop.

Logging:
    The MetronomeApp class sets up a dedicated logger named 'mandelbrot_set_app_logger' to handle logging for the application. 
    The logging level can be configured during initialization. As set up, the logger is configured to output log messages
    to stderr via a StreamHandler.
"""


# standard imports
import tkinter as tk
import logging
import sysconfig

# local imports
from tkAppFramework.tkApp import AppAboutInfo, tkApp
import tkMandelbrotSet.mandelbrot_set_model
import tkMandelbrotSet.view_manager


class MandelbrotSetApp(tkApp):
    """
    Class represents a Mandelbrot set application built using tkinter, leveraging tkApp framework.
    """
    def __init__(self, parent, log_level = logging.INFO) -> None:
        """
        :param log_level: The logging level to set for the logger, e.g., logging.DEBUG, logging.INFO, etc.
        """
        help_file_path = sysconfig.get_path('data') + '\\Help\\tkMandelbrotSet\\MandelbrotSetApp_HelpFile.txt'
        menu_dictionary = {'File':{'Open...':self.onFileOpen, 'Save':self.onFileSave, 'Save As...':self.onFileSaveAs, 'Export Plot...':self.onExportPlot, 'Exit':self.onFileExit}, \
                           'Help':{'View Help...':self.onViewHelp,'About...':self.onHelpAbout}}
        info = AppAboutInfo(name='Mandelbrot Set', version='1.0.0', copyright='2026', author='Kevin R. Geurts',
                            license='MIT License', source='https://github.com/KevinRGeurts/tkMandelbrotSet',
                            help_file=help_file_path)
        super().__init__(parent, title="Mandelbrot Set", menu_dict=menu_dictionary, app_info=info,
                         file_types=[('JSON file', '*.json')], log_level=log_level)

    def _createViewManager(self):
        """
        Factory method to create the view manager for the app.
        :return: The view manager for the app, tkMetronomeViewManager
        """
        return tkMandelbrotSet.view_manager.tkMandelbrotSetViewManager(self)

    def _createModel(self):
        """
        Factory method to create the model for the app.
        :return: The model for the app, MandelbrotSetModel object
        """
        return tkMandelbrotSet.mandelbrot_set_model.MandelbrotSetModel()

    def onExportPlot(self):
        """
        Handle File | Export Plot... menu bar selection.
        :return: None
        """
        # Show a wait cursor, since this is a long-ish operation.
        self.master.config(cursor='watch')
        self.master.update()

        self.getModel().export_plot()

        # Put the cursor back to normal.
        self.master.config(cursor='')

        return None

    def _setup_logging(self, log_level=logging.INFO):
        """
        This method extends tkApp._setup_logging to configure logging specifically for the metronome app.
        :param log_level: The logging level to set for the logger, e.g., logging.DEBUG, logging.INFO, etc.
        :return: None
        """
        super()._setup_logging(log_level)
        
        # Create a logger with name 'metronome_app_logger'. This is NOT the root logger, which is one level up from here, and has no name.
        logger = logging.getLogger('mandelbrot_set_app_logger')
        # This is the threshold level for the logger itself, before it will pass to any handlers, which can have their own threshold.
        # Should be able to control here what the stream handler receives and thus what ends up going to stderr.
        # Use this key for now:
        #   DEBUG = debug messages sent to this logger will end up on stderr
        #   INFO = info messages sent to this logger will end up on stderr
        logger.setLevel(log_level)
        # Set up this highest level below root logger with a stream handler
        sh = logging.StreamHandler()
        # Set the threshold for the stream handler itself, which will come into play only after the logger threshold is met.
        sh.setLevel(log_level)
        # Add the stream handler to the logger
        logger.addHandler(sh)
            
        return None


if __name__ == '__main__':
    # Get Tcl interpreter up and running and get the root widget
    root = tk.Tk()
    # Create the metronome app
    app = MandelbrotSetApp(root)
    # Start the metronome app's event loop running
    app.mainloop()
