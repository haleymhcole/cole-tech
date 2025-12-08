import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 1. Generate Plot Frames and Create GIF
def create_animated_plot_gif(gif_filename="animated_plot.gif"):
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, 100)
    line, = ax.plot(x, np.sin(x))

    def update(frame):
        line.set_ydata(np.sin(x + frame / 10.0))
        return line,

    ani = animation.FuncAnimation(fig, update, frames=range(50), blit=True)
    ani.save(gif_filename, writer='pillow', fps=10) # Save as GIF
    plt.close(fig) # Close the plot to prevent it from showing up separately

# 2. Display GIF in Tkinter
def display_gif_in_tkinter(root, gif_filename):
    info = Image.open(gif_filename)
    frames = info.n_frames
    photoimage_objects = []

    for i in range(frames):
        # Seek to the frame and convert to PhotoImage
        info.seek(i)
        frame_image = ImageTk.PhotoImage(info)
        photoimage_objects.append(frame_image)

    gif_label = tk.Label(root)
    gif_label.pack()

    current_frame_index = 0
    def animate_gif():
        nonlocal current_frame_index
        image = photoimage_objects[current_frame_index]
        gif_label.configure(image=image)
        current_frame_index = (current_frame_index + 1) % frames
        root.after(100, animate_gif) # Adjust delay as needed

    animate_gif() # Start the animation

if __name__ == "__main__":
    create_animated_plot_gif()

    root = tk.Tk()
    root.title("Animated Plot GIF")

    display_gif_in_tkinter(root, "animated_plot.gif")

    root.mainloop()