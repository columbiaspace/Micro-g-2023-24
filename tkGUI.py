import tkinter as tk
import time
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os

# Set up the main window
root = tk.Tk()
root.geometry("1024x768")  # Increased width to accommodate sidebar

# Left Sidebar for Object Class Toggles
left_sidebar = tk.Frame(root)
left_sidebar.pack(side="left", fill="y", padx=10)

# Add toggles for object classes to the sidebar
object_classes = ["orion", "LPU", "life-raft", "life-ring"]
toggle_switches = []

# Dictionary to store the toggle state of each class
class_toggles = {obj_class: tk.BooleanVar() for obj_class in object_classes}

for obj_class in object_classes:
    toggle_label = tk.Label(left_sidebar, text=obj_class)
    toggle_label.pack(pady=2, padx=10)

    toggle = tk.Checkbutton(left_sidebar, text=obj_class, variable=class_toggles[obj_class])
    toggle.pack(pady=2, padx=10)

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

def update_image_gallery():
    image_directory = '/runs'  # Adjust to your directory
    for filename in os.listdir(image_directory):
        # Determine the class of the image from its filename
        image_class = None
        for cls in class_toggles:
            if cls in filename:
                image_class = cls
                break
        
        if image_class and class_toggles[image_class].get():
            full_path = os.path.join(image_directory, filename)
            
            if full_path not in displayed_images:
                img = Image.open(full_path)
                img_thumbnail = img.resize((100, 75))  # Resize the image
                img_thumbnail = ImageTk.PhotoImage(img_thumbnail)
                
                # Get the current time for the label
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                label = tk.Label(right_sidebar, text=current_time)
                label.pack()

                image_label = tk.Label(right_sidebar, image=img_thumbnail)
                image_label.image = img_thumbnail  # Keep a reference
                image_label.pack()

                displayed_images.add(full_path)

    root.after(2000, update_image_gallery)


displayed_images = set()

def open_camera():
    global vid  # Assuming vid is the camera object managed externally
    ret, frame = vid.read()  # Get the current frame from the camera
    if ret:
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image)
        video_label.photo_image = photo_image  # Keep a reference to avoid garbage collection
        video_label.configure(image=photo_image)
    video_label.after(10, open_camera)  # Refresh the image in the label at regular intervals


# Main Frame for the rest of the UI
main_frame = tk.Frame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Title
title_label = tk.Label(main_frame, text="Columbia SEE LION", font=("Roboto Medium", 16))
title_label.pack(pady=12, padx=10)

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

open_camera_button = tk.Button(bottom_frame, text="Open Camera", command=open_camera)
open_camera_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

update_image_gallery()

root.mainloop()
