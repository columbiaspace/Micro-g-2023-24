
#!git clone https://github.com/WongKinYiu/yolov7

#this should be inside yolov7 dir
# %cd yolov7

from  hubconf import custom

model = custom(path_or_model='best.pt')

model.eval()

import subprocess

# Command to run detect.py script with specified arguments
command = [
    "python",
    "detect.py",
    "--weights", "best.pt",
    "--conf", "0.5",
    "--source", "/content/yolov7/test-img"
]

# Execute the command
subprocess.run(command)
