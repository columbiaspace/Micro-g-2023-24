import tkinter as tk
import customtkinter as ctk
# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "light" (default), "dark", "system"
ctk.set_default_color_theme("blue")  # "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.geometry("1024x768")  # Increased width to accommodate sidebar

# Left Sidebar for Object Class Toggles
sidebar = ctk.CTkFrame(root)
sidebar.pack(side="left", fill="y", padx=10)

# Add toggles for object classes to the sidebar
object_classes = ["Class 1", "Class 2", "Class 3", "Class 4"]  # Example object classes
toggle_switches = []
for obj_class in object_classes:
    toggle_label = ctk.CTkLabel(sidebar, text=obj_class)
    toggle_label.pack(pady=2, padx=10)

    toggle = ctk.CTkSwitch(sidebar)
    toggle.pack(pady=2, padx=10)
    toggle_switches.append(toggle)

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

start_button = ctk.CTkButton(bottom_frame, text="Start Analysis")
start_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

stop_button = ctk.CTkButton(bottom_frame, text="Stop Analysis")
stop_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

save_button = ctk.CTkButton(bottom_frame, text="Save Results")
save_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

root.mainloop()