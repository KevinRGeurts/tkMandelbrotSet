# standard library imports
import unittest
import tkinter as tk

# local imports
from tkMandelbrotSet.mandelbrot_set_app import MandelbrotSetApp


class TKinterTestCase(unittest.TestCase):
    """
    Reference: https://stackoverflow.com/questions/4083796/how-do-i-run-unittest-on-a-tkinter-app
    These methods are going to be the same for every GUI test, so put them into a separate class
    """
    def setUp(self):
        self.root=tk.Tk()

    def tearDown(self):
        if self.root:
            self.root.destroy()


class Test_MandelbrotSetApp(TKinterTestCase):
    def test_view_manager(self):
        app = MandelbrotSetApp(self.root)
        vm = app._view_manager
        # Call some of view manager's available methods, simply testing that we don't get an exception or assertion
        vm._get_backward_forward_ids()
        vm._enable_disable_zoom_nav_controls()
        # If we haven't asserted or hit an exception, pass the test.
        self.assertTrue(True)

    def test_plot_widget(self):
        app = MandelbrotSetApp(self.root)
        vm = app._view_manager
        pw = vm._plot_widget
        # Call some of plot widget's available methods, simply testing that we don't get an exception or assertion
        pw.set_state(lrc=complex(1.0,-1.0))
        pw.get_state()
        # If we haven't asserted or hit an exception, pass the test.
        self.assertTrue(True)

    def test_zoom_nav_widget(self):
        app = MandelbrotSetApp(self.root)
        vm = app._view_manager
        zn = vm._zoom_nav_widget
        # Call some of plot widget's available methods, simply testing that we don't get an exception or assertion
        zn._set_state(None)
        zn.get_state()
        # If we haven't asserted or hit an exception, pass the test.
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
