import matplotlib.pyplot as plt 
import numpy as np
import os


from PIL import Image

number_of_planets = 2
# This is where and how your PNG's will be saved
tmp_figure_folder = "gif_figures/"
tmp_figure_name_prefix = "tmp_two_masses_"
# Where your output files are and what they are called
position_files_folder = "output_files/"
position_files_prefix = "positions_planet_"
time_file_name = position_files_prefix + "time.txt"
# Controls the timestep between two plots, and total time plotted
plot_interval = 6000
portion_of_data_used = 1
# What do you call your GIF
gif_folder = "gifs/"
gif_name = "two_masses.gif"
frames_per_second = 20

#######################################################

times = np.loadtxt(position_files_folder + time_file_name)
data = np.zeros((number_of_planets, 2, len(times))) # Dimensions number of planets, x or y, time

for dirName in [tmp_figure_folder, gif_folder]:
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName,  " Created ")
    else:    
        print("Directory ", dirName,  " already exists")

for i in range(number_of_planets):
    data[i, 0, :] = np.loadtxt(position_files_folder + position_files_prefix + "{}.txt".format(i), usecols=0)
    data[i, 1, :] = np.loadtxt(position_files_folder + position_files_prefix + "{}.txt".format(i), usecols=1)

print("Loaded all data: now plotting images.")

xlim = np.array([np.min(data[:, 0, :]), np.max(data[:, 0, :])])
ylim = np.array([np.min(data[:, 1, :]), np.max(data[:, 1, :])])

for t in range(0, int(portion_of_data_used * len(times)), plot_interval):
    fig = plt.figure(figsize = (12,12))
    fig.suptitle("System at time {}.".format(round(times[t], 1)))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(1.1 * xlim)
    ax.set_ylim(1.1 *ylim)
    for n in range(number_of_planets):
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