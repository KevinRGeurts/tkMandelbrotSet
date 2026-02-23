"""
This module's __main__ first asks the user how they want to generate a Mandelbrot set, then
collects input interactively from the user, generates a Mandelbrot set, and prints some results.

Exported classes:
    None

Exported functions:
    __main__: Requests how user wishes to generate a Mandelbrot set
    generate_for_text_plot: Gather input, generate a Mandelbrot set, create and print a TextPlot of the set
    generate_for_heat_map: Gather input, generate a Mandelbrot set, create a display a matplotlip pcolormap of the set
    launch_app: Launch MandelbrotSetApp instance, a tkinter app for displaying and interacting with the Mandelbrot set
    time_set_generation: Gather input, and time how long it takes to generate a Mandelbrot set

    debug: Run a debugging scenario (currently does nothing).

Exported exceptions:
    None
"""


# standard imports
from array import array
import timeit
import tkinter as tk

# PyPi package imports
import matplotlib.pyplot as plt

# local imports
from UserResponseCollector.UserQueryCommand import askForInt, askForFloat, askForPathSave, askForPathSave, askForStr, askForMenuSelection
from RheologyNetworkModelSimulator.qplot import TextPlot
from tkMandelbrotSet.mandelbrot import MandelbrotSet
from tkMandelbrotSet.mandelbrot_set_app import MandelbrotSetApp
from tkMandelbrotSet.bigraph import BigraphNode


def debug():
    """
    Run a debugging scenario.
    """
    suc = BigraphNode(payload=1)
    node = BigraphNode()
    node.successor = suc
    # Now try to add suc again, which should not happen
    node.successor = suc
    # Add a second, unique successor to node
    suc2 = BigraphNode(payload=2)
    node.successor = suc2
    # Getter should still get the first successor added

    return None


def generate_for_text_plot():
    """
    Generate a Mandelbrot set and make a text plot.
    """
    
    # Collect from user required inputs
    ulr = askForFloat('Enter the upper-left corner real value (suggest -2.0)')
    uli = askForFloat('Enter the upper-left corner imaginary value (suggest 2.0)')
    lrr = askForFloat('Enter the lower-right corner real value (suggest 2.0)')
    lri = askForFloat('Enter the lower-right corner imaginary value (suggest -2.0)')
    nr = askForInt('Enter the number of points per real side (suggest 60)', minimum=2)
    ni = askForInt('Enter the number of points per imaginary side (suggest 20)', minimum=2)

    
    # Generate the Mandelbrot set
    ms = MandelbrotSet(complex(ulr,uli),complex(lrr,lri),nr,ni)
    ms.generate_mandelbrot_set()

    # Obtain the mandelbrot set values, and package them for plotting
    _x=array('f')
    _y=array('f')
    _sym=array('u')
    _sym.append('X')
    for i in range(nr):
        for j in range(ni):
            pnt_res = ms.get_iter_value_with_ri(i,j)
            if pnt_res[0] >= ms.max_iters:
                # We will only plot points that did not diverge
                _x.append(pnt_res[1])
                _y.append(pnt_res[2])

    # Create the TextPlot for visualizing the set
    tp = TextPlot(ncur=1, npts=len(_x), x=[_x], y=[_y], symbol=_sym, titl1='Mandelbrot Set')

    # Print the TextPlot of the Mandelbrot Set
    print(str(tp))

    return None

def generate_for_heat_map():
    """
    Generate a Mandelbrot set and make a heat map using Matplotlib.
    """
    
    # Collect from user required inputs
    ulr = askForFloat('Enter the upper-left corner real value (suggest -2.0)')
    uli = askForFloat('Enter the upper-left corner imaginary value (suggest 2.0)')
    lrr = askForFloat('Enter the lower-right corner real value (suggest 1.0)')
    lri = askForFloat('Enter the lower-right corner imaginary value (suggest -2.0)')
    nr = askForInt('Enter the number of points per real side (suggest 500)', minimum=2)
    ni = askForInt('Enter the number of points per imaginary side (suggest 500)', minimum=2)

    
    # Generate the Mandelbrot set
    ms = MandelbrotSet(complex(ulr,uli),complex(lrr,lri),nr,ni)
    ms.generate_mandelbrot_set()

    # Get the plotting data
    (_x, _y, _z) = ms.get_plot_data(True)

    # Create the plot for visualizing the set
    ax=plt.axes()
    ax.set_aspect("equal")
    graph = ax.pcolormesh(_x, _y, _z, cmap="nipy_spectral")
    plt.colorbar(graph)
    plt.xlabel("Real-Axis")
    plt.ylabel("Imaginary-Axis")

    # Show the plot
    plt.show()

    return None


def launch_app():
    """
    Launch the Mandelbrot Set App.
    """
    # Get Tcl interpreter up and running and get the root widget
    root = tk.Tk()
    # Create the metronome app
    app = MandelbrotSetApp(root)
    # Start the metronome app's event loop running
    app.mainloop()
    return None


def time_set_generation():
    """
    Time how long it takes to generate a Mandelbrot set.
    """

    nt = askForInt('Enter the number of times to generate the set (suggest 100)', minimum=1, maximum=100)

    # Generate the Mandelbrot set a specified number of times, and calculate the average time it took to generate the set once.
    took = timeit.timeit("MandelbrotSet().generate_mandelbrot_set()", globals=globals(), number=nt)
    print(f"After {nt} set generations, average time to generate the set was {took/nt} seconds.")
    
    return None


if __name__ == '__main__':
    """
    Query the user for how they wish to generate a Mandelbrot set, and then launch that usage.
    This includes a "debug" usage to set up what ever situation is needed for debugging, since I can't seem to reliably debug unit tests.
    """
    print('---------------------------------------------_')
    print('-----     Mandelbrot Set Generator       -----')
    print('---------------------------------------------_')
    
    # Build a query for the user to obtain their choice of how to user the simulator
    query_preface = 'How do you want to generate a Mandelbrot set?'
    query_dic = {'q':'Quit', '1':'Generate for text plot', '2':'Time set generation', '3':'Generate for heat map', '4':'Launch Mandelbrot Set app', 'd':'Debug Scenario'}
    response = askForMenuSelection(query_preface, query_dic)
    
    while response != 'q':
        
        match response:
            
            case '1':
                generate_for_text_plot()

            case '2':
                time_set_generation()

            case '3':
                generate_for_heat_map()

            case '4':
                launch_app()
                                
            case 'd':
                debug()
        
        print('--------------------')
        response = askForMenuSelection(query_preface, query_dic)

