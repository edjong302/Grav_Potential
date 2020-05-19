# Grav_Potential

This code simulates the behaviour of any number of massive pointlike bodies orbiting one another in Newtonian gravity, in two dimensions.

The code uses an RK4 solver provided by the Python library Scipy to evolve the system. Extra massive bodies can easily be added by adding subarrays to the initial condition array. The solver automatically takes into account all other bodies when it computes the gravitational potential at a given timestep.

A visualisation script is provided to process raw data into a GIF that shows the evolution of the system. An example GIF for two bodies is given below.

<p float="left">
  <img src="/gifs/four_masses.gif" width="350" />
</p>
