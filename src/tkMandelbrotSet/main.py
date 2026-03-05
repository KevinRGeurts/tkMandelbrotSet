"""
This module's __main__ first asks the user how they want to generate a Mandelbrot set, then
collects input interactively from the user, generates a Mandelbrot set, and outputs results.

Exported classes:
    None

Exported functions:
    __main__: Requests how user wishes to generate a Mandelbrot set
    generate_mandelbrot_set: Gather input, generate a Mandelbrot set, create and display a matplotlip pcolormap of the set
    launch_app: Launch MandelbrotSetApp instance, a tkinter app for displaying and interacting with the Mandelbrot set
    time_set_generation: Gather input, and time how long it takes to generate a Mandelbrot set
    debug: Run a debugging scenario (currently does nothing).

Exported exceptions:
    None
"""


# standard imports
import timeit
import tkinter as tk

# local imports
from UserResponseCollector.UserQueryCommand import askForInt, askForFloat, askForMenuSelection
from tkMandelbrotSet.mandelbrot import MandelbrotSet, plot_mandelbrot_set
from tkMandelbrotSet.mandelbrot_set_app import MandelbrotSetApp
from tkMandelbrotSet.bigraph import BigraphNode, Bigraph, Branch


def debug():
    """
    Run a debugging scenario.
    :return: None
    """
    graph = Bigraph()
    branch1 = Branch(name='branch1')
    tip1 = branch1.tip_node
    node1 = BigraphNode(payload=1)
    branch1.add_node(node1)
    node2 = BigraphNode(payload=2)
    branch1.add_node(node2)
    graph.add_branch(new_branch=branch1)
    # branch1: graph.root -> (branch1 original tip node) -> node1 -> node2
    branch2 = Branch(name='branch2')
    graph.add_branch(at_node=node1, new_branch=branch2)
    # branch2: graph.root -> (branch1 original tip node) -> node1 -> branch2.tip_node
    # Prune the tree at (branch1 original tip node)
    graph.prune(tip1)
    assert(len(graph)==1) # Graph has one remaining branch


    return None


def generate_mandelbrot_set():
    """
    Generate a Mandelbrot set and visualize it using matplotlib.
    :return: None
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

    # Visualize the Mandelbrot set
    plot_mandelbrot_set(_x, _y, _z)

    return None


def launch_app():
    """
    Launch the Mandelbrot Set App.
    :return: None
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
    :return: None
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
    query_dic = {'q':'Quit', '1':'Time the generation of Mandelbrot set', '2':'Generate a Mandelbrot set', '3':'Launch Mandelbrot Set app', 'd':'Debug Scenario'}
    response = askForMenuSelection(query_preface, query_dic)
    
    while response != 'q':
        
        match response:
            
            case '1':
                time_set_generation()

            case '2':
                generate_mandelbrot_set()

            case '3':
                launch_app()
                                
            case 'd':
                debug()
        
        print('--------------------')
        response = askForMenuSelection(query_preface, query_dic)
