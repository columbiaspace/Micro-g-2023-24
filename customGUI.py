import tkinter as tk
import customtkinter as ctk
import time
from tkinter import *
from PIL import Image, ImageTk 
import cv2
# from models.yolov7 import YOLOv7
import torch

# load model frameworrk
# model = YOLOv7("cfg/training/yolov7.yaml")

# # Load the trained weights from best.pt. only for testing, at the competition, best.pt will be in the same directory
# weights_path = '/content/drive/My Drive/2023/24 Micro-g NExT/Micro-g YOLO Model Workspace/results/best.pt'
# model.load_state_dict(torch.load(weights_path))

# model.eval()


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue") 

root = ctk.CTk()
root.geometry("1024x768")  # Increased width to accommodate sidebar

# Left Sidebar for Object Class Toggles
left_sidebar = ctk.CTkFrame(root)
left_sidebar.pack(side="left", fill="y", padx=10)

# Add toggles for object classes to the sidebar
object_classes = ["Class 1", "Class 2", "Class 3", "Class 4"]  # Example object classes
toggle_switches = []
for obj_class in object_classes:
    toggle_label = ctk.CTkLabel(left_sidebar, text=obj_class)
    toggle_label.pack(pady=2, padx=10)

    toggle = ctk.CTkSwitch(left_sidebar)
    toggle.pack(pady=2, padx=10)
    toggle_switches.append(toggle)

# Right Sidebar for Saving Objects of Interest
right_sidebar = ctk.CTkFrame(root)
right_sidebar.pack(side="right", fill="y", padx=10)

# Timer
timer_label = ctk.CTkLabel(right_sidebar, text="00:00:00.00")
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

# # Declare the width and height in variables 
# width, height = 900, 400

# # Set the width and height 
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

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
        # Get the current time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Save the frame as an image file
        filename = f"saved_frame_{current_time}.png".replace(':', '-')
        cv2.imwrite(filename, frame)

        # Convert the frame for displaying in the GUI
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image.resize((100, 75)))  # Resize for thumbnail

        # Create a label and add it to the right sidebar
        label = ctk.CTkLabel(right_sidebar, text=current_time)
        label.pack()
        image_label = ctk.CTkLabel(right_sidebar, image=photo_image)
        image_label.image = photo_image  # Keep a reference
        image_label.pack()

# Main Frame for the rest of the UI
main_frame = ctk.CTkFrame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Title
title_label = ctk.CTkLabel(main_frame, text="Columbia University MicroG NeXT YOLO Model", font=("Roboto Medium", 16))
title_label.pack(pady=12, padx=10)

# Upper Frame for Input and Controls
upper_frame = ctk.CTkFrame(main_frame)
upper_frame.pack(side="top", fill="x", padx=20, pady=10)

# Input Controls in the Upper Frame
input_label = ctk.CTkLabel(upper_frame, text="Input", width=10)
input_label.grid(row=0, column=0, pady=10, padx=10)
input_entry = ctk.CTkEntry(upper_frame, placeholder_text="Type here...")
input_entry.grid(row=0, column=1, pady=10, padx=10)

checkbox = ctk.CTkCheckBox(upper_frame, text="Checkbox")
checkbox.grid(row=1, column=0, pady=10, padx=10)

toggle_label = ctk.CTkLabel(upper_frame, text="Toggle", width=10)
toggle_label.grid(row=2, column=0, pady=10, padx=10)
toggle_switch = ctk.CTkSwitch(upper_frame)
toggle_switch.grid(row=2, column=1, pady=10, padx=10)

dropdown_label = ctk.CTkLabel(upper_frame, text="Dropdown Box", width=10)
dropdown_label.grid(row=1, column=1, pady=10, padx=10)
dropdown = ctk.CTkComboBox(upper_frame, values=["Option 1", "Option 2", "Option 3"])
dropdown.grid(row=1, column=2, pady=10, padx=10)

# Video Feed Frame
video_frame = ctk.CTkFrame(main_frame, height=300)  # Set a fixed height or adjust as needed
video_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

# Label as a placeholder for video feed
video_label = tk.Label(video_frame, text="Live Video Feed", bg="#333333", fg="white")
video_label.pack(side="top", fill="both", expand=True)

# Bottom Frame for Buttons
bottom_frame = ctk.CTkFrame(main_frame)
bottom_frame.pack(side="top", fill="x", padx=20, pady=10)

start_button = ctk.CTkButton(bottom_frame, text="Start Analysis", command=start_timer)
start_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

stop_button = ctk.CTkButton(bottom_frame, text="Stop Analysis", command=stop_timer)
stop_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

save_button = ctk.CTkButton(bottom_frame, text="Save Results", command=save_results)
save_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

open_camera_button = ctk.CTkButton(bottom_frame, text="Open Camera", command=open_camera)
open_camera_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

root.mainloop()