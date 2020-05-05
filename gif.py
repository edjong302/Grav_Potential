from PIL import Image

images = []

for i in range(0, 109, 1):
    frame = Image.open("visit%04i.png" %float(i))
    images.append(frame)
images[0].save('chi.gif', save_all=True, append_images=images[1:], duration=50, loop=0)