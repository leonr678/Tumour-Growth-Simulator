# Tumour-Growth-Simulator
A GUI tumour growth (or shrinking) simulation, using Python, that shows the progression of the tumour over time, given input parameters.

# Required Libraries

All libraries, except NumPy, are included with Python's standard library:

- ***Tkinter (GUI)***
- ***MatPlotLib***
- ***NumPy***  

# How to use

When the application is run, a window will pop up which will contain text and entries which correspond to the parameters for tumour growth. These are: initial volume, growth rate, duration (days) and final volume. When the parameters are confirmed, a graph of tumour volume against time will be plotted, using a logistic model. To reset the application, click the "New parameters" button.

# Programming and Mathematical Methods

This GUI application makes use of classes, functions, error handling, input validation, and conditional logic. Event-driven programming is used. For the simulation, we use a famous numerical method called Euler's method, to solve the Logistic differential equation (for the specified parameters) which is as follows:

dy/dx = ry(1-y/K)

where r and K are interpreted in this case as the growth rate and the maximum size of the tumour.

# Further improvements

- ***Better simulation, perhaps with an animation***
- ***More developed GUI***
- ***More complex mathematical model*** 
