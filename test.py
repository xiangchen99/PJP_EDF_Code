import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

def draw_speedometer(speed):
    ax.clear()  # Clear the axis to redraw the speedometer
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    
    # Draw the speedometer dial as a circle
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none')
    ax.add_artist(circle)
    
    # Add markings and numbers
    for num in range(0, 101, 10):
        angle_rad = np.radians((num / 100) * 180 - 90)
        x = np.cos(angle_rad)
        y = np.sin(angle_rad)
        ax.text(x, y, str(num), horizontalalignment='center', verticalalignment='center')
    
    # Calculate the needle's position
    angle_rad = np.radians((speed / 100) * 180 - 90)
    x = np.cos(angle_rad)
    y = np.sin(angle_rad)
    
    # Draw the needle
    ax.plot([0, x], [0, y], color='red')
    
    # Hide the axis
    ax.axis('off')
    
    # Update the canvas
    canvas.draw()

def update_speed(val):
    draw_speedometer(slider.get())

# Create the Tkinter window
root = tk.Tk()
root.wm_title("Embedding Matplotlib in Tkinter")

# Create a matplotlib figure and axis for the speedometer
fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Adjust subplot edges

# Create a FigureCanvasTkAgg object
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a Tkinter slider to control the speed
slider = tk.Scale(root, from_=0, to=100, orient='horizontal', command=update_speed)
slider.pack(side=tk.BOTTOM, fill=tk.X)

# Initial draw of the speedometer
draw_speedometer(0)

tk.mainloop()
