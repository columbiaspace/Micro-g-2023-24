# -*- coding: utf-8 -*-
"""working_Microg_YoloV7_model (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yfRCw30QdM100DUiPlR_A3FFNCEyIzqX
"""

!nvidia-smi

!py3 -v

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/WongKinYiu/yolov7
# %cd yolov7
!pip install -r requirements.txt

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="j19bmHHOB6TxRaOzR8X9")
project = rf.workspace("csi-microg").project("microg-2")
version = project.version(1)
dataset = version.download("yolov7")

!ls

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov7
!wget "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt"

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov7/
!python train.py --batch 16 --cfg cfg/training/yolov7.yaml --epochs 55 --data microg-2-1/data.yaml --weights 'yolov7.pt' --device 0

!python detect.py --weights runs/train/exp/weights/best.pt --conf 0.5 --source microg-2-1/test/images

from PIL import Image
import time
import os

# Directory containing the images with detected objects.
#images not displaying -> export folder and open in IDE
output_dir = "/content/yolov7/runs/detect/exp"

# List all image files in the output directory
image_files = [file for file in os.listdir(output_dir)]
print(image_files)
# Display each image
for image_file in image_files:
    path = output_dir + "/" + image_file
    print(path)
    image = Image.open(path)
    image.show()
    time.sleep(2)