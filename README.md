# Grav_Potential

This code simulates the behaviour of any number of massive pointlike bodies orbiting one another in Newtonian gravity, in two dimensions. One needs to have installed the Python packages Numpy, Matplotlib, OS, Pillow and Sympy to run this code.

The code uses an RK4 solver provided by the Python library Scipy to evolve the system. Extra massive bodies can easily be added by adding subarrays to the initial condition array. The solver automatically takes into account all other bodies when it computes the gravitational potential at a given timestep.

A visualisation script is provided to process raw data into a GIF that shows the evolution of the system. By default, the script allows for the plotting of absolute positions of the bodies, or for plotting their positions with respect to the center of mass of the system.


An example GIF for four bodies in Newtonian elliptical orbit is given below.

<p float="left">
  <img src="/gifs/four_masses.gif" width="350" />
</p>
