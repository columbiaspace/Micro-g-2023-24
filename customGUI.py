import tkinter as tk
import time
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import cv2

# Set up the main window
root = tk.Tk()
root.geometry("1024x768")  # Increased width to accommodate sidebar
# Set up the sub window

# Refreences this:
#  https://stackoverflow.com/questions/31764908/window-inside-window
sub=tk.Toplevel(root)
sub.transient(root)
sub.title('Sub Window')
label = tk.Label(sub, text="This is a subwindow")
label.pack(padx=20, pady=20)

pos = []

def main_move(event):
    #When the main window moves, adjust the sub window to move with it
    if pos:
        sub.geometry("+{0}+{1}".format(pos[0], pos[1]))
        # Change pos[0] and pos[1] to defined values (eg 50) for fixed position from main

def sub_move(event):
    # Set the min values
    min_w = root.winfo_rootx()
    min_h = root.winfo_rooty()
    # Set the max values minus the buffer for window border
    max_w = root.winfo_rootx() + root.winfo_width() - 15
    max_h = root.winfo_rooty() + root.winfo_height() - 35

    # Conditional statements to keep sub window inside main
    if event.x < min_w:
        sub.geometry("+{0}+{1}".format(min_w, event.y))

    elif event.y < min_h:
        sub.geometry("+{0}+{1}".format(event.x, min_h))

    elif event.x + event.width > max_w:
        sub.geometry("+{0}+{1}".format(max_w - event.width, event.y))

    elif event.y + event.height > max_h:
        sub.geometry("+{0}+{1}".format(event.x, max_h - event.height))

    global pos
    # Set the current sub window position
    pos = [event.x, event.y]  

root.bind('<Configure>', main_move)
sub.bind('<Configure>', sub_move)


# Left Sidebar for Object Class Toggles
left_sidebar = tk.Frame(root)

left_sidebar.pack(side="left", fill="y", padx=10)

# Add toggles for object classes to the sidebar
object_classes = ["Class 1", "Class 2", "Class 3", "Class 4"]
toggle_switches = []
for obj_class in object_classes:
    toggle_label = tk.Label(left_sidebar, text=obj_class)
    toggle_label.pack(pady=2, padx=10)

    toggle = tk.Checkbutton(left_sidebar)
    toggle.pack(pady=2, padx=10)
    toggle_switches.append(toggle)

# Right Sidebar for Saving Objects of Interest
right_sidebar = tk.Frame(root)
right_sidebar.pack(side="right", fill="y", padx=10)

# Timer
timer_label = tk.Label(right_sidebar, text="00:00:00.00")
timer_label.pack(pady=2, padx=10)

timer_running = False
start_time = 0

def update_timer():
    if not timer_running:
        return
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 100)
    seconds = int(seconds)
    timer_label.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}")
    root.after(50, update_timer)

def start_timer():
    global timer_running, start_time
    if not timer_running:
        timer_running = True
        start_time = time.time()
        update_timer()

def stop_timer():
    global timer_running
    timer_running = False

# Define a video capture object
vid = cv2.VideoCapture(0)

def open_camera():
    _, frame = vid.read()
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image)
    photo_image = ImageTk.PhotoImage(image=captured_image)
    video_label.photo_image = photo_image
    video_label.configure(image=photo_image)
    video_label.after(10, open_camera)

def save_results():
    ret, frame = vid.read()
    if ret:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = f"saved_frame_{current_time}.png".replace(':', '-')
        cv2.imwrite(filename, frame)

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image.resize((100, 75)))

        label = tk.Label(right_sidebar, text=current_time)
        label.pack()
        image_label = tk.Label(right_sidebar, image=photo_image)
        image_label.image = photo_image
        image_label.pack()

# Main Frame for the rest of the UI
main_frame = tk.Frame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Title
title_label = tk.Label(main_frame, text="Columbia University MicroG NeXT YOLO Model", font=("Roboto Medium", 16))
title_label.pack(pady=12, padx=10)

# Upper Frame for Input and Controls
upper_frame = tk.Frame(main_frame)
upper_frame.pack(side="top", fill="x", padx=20, pady=10)

# Input Controls in the Upper Frame
input_label = tk.Label(upper_frame, text="Input")
input_label.grid(row=0, column=0, pady=10, padx=10)
input_entry = tk.Entry(upper_frame)
input_entry.grid(row=0, column=1, pady=10, padx=10)

checkbox = tk.Checkbutton(upper_frame, text="Checkbox")
checkbox.grid(row=1, column=0, pady=10, padx=10)

toggle_label = tk.Label(upper_frame, text="Toggle")
toggle_label.grid(row=2, column=0, pady=10, padx=10)
toggle_switch = tk.Checkbutton(upper_frame)
toggle_switch.grid(row=2, column=1, pady=10, padx=10)

dropdown_label = tk.Label(upper_frame, text="Dropdown Box")
dropdown_label.grid(row=1, column=1, pady=10, padx=10)
dropdown = ttk.Combobox(upper_frame, values=["Option 1", "Option 2", "Option 3"])
dropdown.grid(row=1, column=2, pady=10, padx=10)

# Video Feed Frame
video_frame = tk.Frame(main_frame, height=300)
video_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

# Label as a placeholder for video feed
video_label = tk.Label(video_frame, text="Live Video Feed")
video_label.pack(side="top", fill="both", expand=True)

# Bottom Frame for Buttons
bottom_frame = tk.Frame(main_frame)
bottom_frame.pack(side="top", fill="x", padx=20, pady=10)

start_button = tk.Button(bottom_frame, text="Start Analysis", command=start_timer)
start_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

stop_button = tk.Button(bottom_frame, text="Stop Analysis", command=stop_timer)
stop_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

save_button = tk.Button(bottom_frame, text="Save Results", command=save_results)
save_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

open_camera_button = tk.Button(bottom_frame, text="Open Camera", command=open_camera)
open_camera_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

root.mainloop()