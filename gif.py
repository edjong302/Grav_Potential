import matplotlib.pyplot as plt 
import numpy as np
import os


from PIL import Image

number_of_planets = 4
# This is where and how your PNG's will be saved
tmp_figure_folder = "gif_figures/"
tmp_figure_name_prefix = "tmp_four_masses_"
# Where your output files are and what they are called
position_files_folder = "output_files/"
position_files_prefix = "positions_four_planets_"
time_file_name = position_files_prefix + "time.txt"
masses_file_name = position_files_prefix + "masses.txt"
# Controls the timestep between two plots, and total time plotted
plot_interval = 12000
portion_of_data_used = 1
plot_wrt_center_of_mass = 1
# What do you call your GIF
gif_folder = "gifs/"
gif_name = "four_masses_long_com.gif"
frames_per_second = 60

#######################################################

times = np.loadtxt(position_files_folder + time_file_name)
masses = np.loadtxt(position_files_folder + masses_file_name)
data = np.zeros((number_of_planets, 2, len(times))) # Dimensions: number of planets, x or y, time

for dirName in [tmp_figure_folder, gif_folder]:
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName,  " Created ")
    else:    
        print("Directory ", dirName,  " already exists")

for i in range(number_of_planets):
    data[i, 0, :] = np.loadtxt(position_files_folder + position_files_prefix + "{}.txt".format(i), usecols=0)
    data[i, 1, :] = np.loadtxt(position_files_folder + position_files_prefix + "{}.txt".format(i), usecols=1)

# Calculate center of mass using a sum of coordinates weighted by planets' masses if needed
if plot_wrt_center_of_mass == 1:
    data_com = np.tensordot(np.array([1 for i in range(number_of_planets)]), np.tensordot(data, masses, ([0], [0])) / np.sum(masses), 0)
    

print("Loaded all data: now plotting images.")
if plot_wrt_center_of_mass == 1:
    xlim = np.array([np.min(data[:, 0, :] - data_com[:, 0, :]), np.max(data[:, 0, :] - data_com[:, 0, :])])
    ylim = np.array([np.min(data[:, 1, :] - data_com[:, 1, :]), np.max(data[:, 1, :] - data_com[:, 1, :])])
else:
    xlim = np.array([np.min(data[:, 0, :]), np.max(data[:, 0, :])])
    ylim = np.array([np.min(data[:, 1, :]), np.max(data[:, 1, :])])

for t in range(0, int(portion_of_data_used * len(times)), plot_interval):
    fig = plt.figure(figsize = (12,12))
    fig.suptitle("System at time {}.".format(round(times[t], 1)))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(1.1 * xlim)
    ax.set_ylim(1.1 *ylim)
    for n in range(number_of_planets):
        if plot_wrt_center_of_mass == 1:
            ax.scatter(data[n, 0, 0:t] - data_com[0, 0, :t], data[n, 1, 0:t] - data_com[0, 1, :t], marker = '.', s = 8, color = '.3')
            ax.plot(data[n, 0, t] - data_com[0, 0, t], data[n, 1, t] - data_com[0, 1, t], marker = '.', markersize = 30, color = 'k')
        else:
            ax.scatter(data[n, 0, 0:t], data[n, 1, 0:t], marker = '.', s = 8, color = '.3')
            ax.plot(data[n, 0, t], data[n, 1, t], marker = '.', markersize = 30, color = 'k')
    fig.savefig(tmp_figure_folder + tmp_figure_name_prefix + "{}.png".format(t))
    plt.close(fig)

print("Made images: now making gif.")

images = []

for t in range(0, int(portion_of_data_used * len(times)), plot_interval):
    frame = Image.open(tmp_figure_folder + tmp_figure_name_prefix + "{}.png".format(t))
    images.append(frame)
images[0].save(gif_folder + gif_name, save_all=True, append_images=images[1:], duration=1000/frames_per_second, loop=0)