# tkMandelbrotSet

Source code: [GitHub](https://github.com/KevinRGeurts/tkMandelbrotSet)
---
The tkMandelbrotSet package provides a python class MandelbrotSet for generating Mandelbrot sets. It also provides a
```tkinter``` application for visualizing and interacting with (e.g., zooming into) the Mandelbrot set.

## Application Features:
- The Mandelbrot set is visualized by a ```matplotlib pcolormesh``` figure.
- The user can zoom into the Mandelbrot set visualization by clicking and dragging a zooming rectangle with the mouse.
- The user can move backward and forward through the history of zooms.
- Red numbered rectangles on the visualization indicate the location of previous zooms.
- The user can "prune" the history of zooms to eliminate unwanted zoom locations.
- The user can visualize the Mandelbrot set using different colormaps.
- The user can export the Mandelbrot set visualization to an image file.

## Application Known Issues and Limitations:
1. File|Open..., File|Save, and File|Save As... menu bar options are not currently implemented. File open and save dialogs will
   be presented, but no action will be taken when they are closed.

## References:
1. https://en.wikipedia.org/wiki/Mandelbrot_set
2. "The Mandelbrot Set," by Branner, Bodil, "Chaos and Fractals: The Mathematics Behind the Computer Graphics,"
   Devaney, Robert L., and Linda Keen, eds., Proceedings of Symposia in Applied Mathematics, Volume 39,
   American Mathematical Society, 1989, pp. 75-106.

## Requirements
- matplotlib>=3.10.8: [GitHub](https://github.com/matplotlib/matplotlib), [PyPi](https://pypi.org/project/matplotlib/)
- tkAppFramework>=0.9.3: [GitHub](https://github.com/KevinRGeurts/tkAppFramework), [PyPi](https://pypi.org/project/tkAppFramework/)
- UserResponseCollector>=1.1.0: [GitHub](https://github.com/KevinRGeurts/UserResponseCollector), [PyPi](https://pypi.org/project/UserResponseCollector/)

## Credit where credit is due
- The Memento design pattern used to snapshot the state of the MandelbrotSet class follow the concepts, UML diagrams, and examples provided in
  "Design Patterns: Elements of Reusable Object-Oriented Software," by Eric Gamma, Richard Helm, Ralph Johnson,
  and John Vlissides, published by Addison-Wesley, 1995.

## Application Usage
To launch the application for interacting with and visualizing the Mandelbrot set:
```
python -m tkMandelbrotSet.mandelbrot_set_app
```
Choose Help | View Help... from the application's menu bar to read instructions for using the application.

## Advanced Usage
You can use the MandelbrotSet class to generate your own Mandelbrot set results.
```
from tkMandelbrotSet.mandelbrot import MandelbrotSet, plot_mandelbrot_set

# Generate the Mandelbrot set
upper_left_corner = complex(real=-2.0, imag=2.0)
lower_rigt_corner = complex(real=1.0, imag=-2.0)
number_real_axis_pts = 500
number_imag_axis_pts = 500
ms = MandelbrotSet(upper_left_corner, lower_right_corner, number_real_axis_pts, number_imag_axis_pts)
ms.generate_mandelbrot_set()

# Get the plotting data
(x, y, z) = ms.get_plot_data(True)

# Visualize the Mandelbrot set
plot_mandelbrot_set(x, y, z)
```

## Unittests
Unit tests for tkMandelbrotSet have filenames starting with test_. To run the unit tests,
type ```python -m unittest discover -s .\..\tests -v``` in a terminal window in the project directory.

While the unit tests are executing, a few ```tkinter``` windows will appear and disappear, as the application
is being tested.

## License
MIT License. See the LICENSE file for details