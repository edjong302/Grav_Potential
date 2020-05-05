import body as bod
import matplotlib.pyplot as plt 
import numpy as np
import os
import sympy as sp

from scipy.integrate import solve_ivp
from time import localtime

# Planets' masses, positions, velocities. The array is [mass, initial x position, initial y position, initial x velocity, initial y velocity].
# If you want to add a planet, simply add an element to the array below. The script will understand.
# For two planets you could use these:
planet_initial_conditions = [[.02, -2, 0, .001, -.005], [.01, 3, 0, 0, 0.01]]

# For three planets you could use these:
#planet_initial_conditions = [[.035, 0, 0, .0025, 0], [.01, -3, 0, 0, -.01], [.01, 3, 0, 0, .02]]

max_time = 2000
adaptive_step_size = 0 # 1 to let the scipy solver adapt the time step size
step_size = 1.e-3
figure_folder = "plots/"
position_files_folder = "output_files/"
figure_name = "two_masses.png"
position_files_prefix = "positions_planet_"

#######################################################

for dirName in [figure_folder, position_files_folder]:
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName,  " Created ")
    else:    
        print("Directory ", dirName,  " already exists")

def distance_function(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Initialize planets of type body
planets = [bod.Body(planet_initial_conditions[i]) for i in range(len(planet_initial_conditions))]

# Format list with initial positions and velocities
U0 = []
for i in planets:
    U0.append(i.positions)
for i in planets:
    U0.append(i.velocities)
U0 = sum(U0, [])

def timestep(t, U):
    # Set up array with first derivatives to return
    return_array = list(U[int(len(U)/2) : len(U)])

    # Loop over planets
    for planet in planets:
        planet_index = planets.index(planet)
        acc_x = 0
        acc_y = 0
        # Loop over all other planets: for all other planets, one should add terms to the x and y acceleration
        for other_planet in planets:
            if planet == other_planet:
                continue # Planets don't self-interact
            else:
                other_planet_index = planets.index(other_planet)
                distance = distance_function(U[2 * planet_index], U[2 * planet_index + 1], U[2 * other_planet_index], U[2 * other_planet_index + 1])
                acc_x += planet.mass * other_planet.mass *(U[2 * other_planet_index] - U[2 * planet_index]) / distance ** (3/2.)
                acc_y += planet.mass * other_planet.mass *(U[2 * other_planet_index + 1] - U[2 * planet_index + 1]) / distance ** (3/2.)
        return_array.append(acc_x)
        return_array.append(acc_y)
    
    return return_array

iatol = 1.e-7 # Defaults for tolerance levels
irtol = 1.e-4

if adaptive_step_size == 0: # Fix the step size if desired
    iatol = 1.
    irtol = 1.

start = localtime()

sol = solve_ivp(timestep, (0, max_time), U0, max_step = step_size, atol = iatol, rtol = irtol) #Engage

end = localtime()

#Timekeeping
sec_passed = end.tm_sec - start.tm_sec
min_passed = end.tm_min - start.tm_min - 1 if sec_passed < 0 else end.tm_min - start.tm_min
sec_passed = sec_passed + 60 if sec_passed < 0 else sec_passed + 0
print("Integrating took {} minutes and {} seconds.".format(min_passed, sec_passed))

# Plots!
fig = plt.figure(figsize = (12,12))
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# Plot and subplot titles
fig.suptitle('Masses moving around one another in Newtonian gravity.')
ax.set_title('Observer reference frame')
ax2.set_title('Reference frame of one of the masses.')
# Plotting trajectories and initial positions
for planet in planets:
    planet_index = planets.index(planet)
    ax.scatter(sol.y[2 * planet_index, :], sol.y[2 * planet_index + 1, :], marker = '.', s = .5, color = '.3')
    ax.plot(sol.y[2 * planet_index, -1], sol.y[2 * planet_index + 1, -1], marker = '.', markersize = 10, color = 'k')
    if planet_index == 0:
        continue
    else:
        ax2.plot(sol.y[2 * planet_index, -1] - sol.y[0, -1], sol.y[2 * planet_index + 1, -1] - sol.y[1, -1], marker = '.', markersize = 10, color = 'k')
        ax2.scatter(sol.y[2 * planet_index, :] - sol.y[0, :], sol.y[2 * planet_index + 1, :] - sol.y[1, :], marker = '.', s = .5, color = '.6')
ax2.plot(0, 0, marker = '.', markersize = 20, color = 'k')

# Save the file to png, and position and time data to txt
fig.savefig(figure_folder + figure_name)
plt.close(fig)

for planet in planets:
    planet_index = planets.index(planet)
    np.savetxt(position_files_folder + position_files_prefix + '{}.txt'.format(planet_index), np.c_[sol.y[2 * planet_index, :], sol.y[2 * planet_index + 1, :]])
np.savetxt(position_files_folder + position_files_prefix + "time.txt", sol.t)
print("Done!")