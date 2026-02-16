# tkMandelbrotSet

Source code: [GitHub](https://github.com/KevinRGeurts/tkMandelbrotSet)
---
The tkMandelbrotSet package provides a python class MandelbrotSet for generating Mandelbrot sets. It also provides a
tkinter application for visualizing and interacting with (e.g., zooming into) the Mandelbrot set. The application works,
but continues to be enhanced.

## References:
1. https://en.wikipedia.org/wiki/Mandelbrot_set

## Requirements
- UserResponseCollector>=1.1.0: [GitHub](https://github.com/KevinRGeurts/UserResponseCollector), [PyPi](https://pypi.org/project/UserResponseCollector/)
- matplotlib>=3.10.8: [GitHub](https://github.com/matplotlib/matplotlib), [PyPi](https://pypi.org/project/matplotlib/)

## Basic Usage
To generate and visualize the Mandelbrot set:
```
python -m tkMandelbrotSet.main
```
First, options for generating and visualizing the Mandelbrot set will be requested from the console, then required input will be requested from the console,
and finally, results will be printed to the console or displayed in a plot window.

## Advanced Usage
You can use the MandelbrotSet class to generate your own Mandelbrot set results.
```
# TODO: Add python code here to illustrate use of MandelbrotSet class.
```

## Unittests
Unit tests for RheologyNetworkModelSimulator have filenames starting with test__. To run the unit tests,
type ```python -m unittest discover -s .\..\tests -v``` in a terminal window in the project directory.

## License
MIT License. See the LICENSE file for details