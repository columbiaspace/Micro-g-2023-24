
from google.colab import drive
from  hubconf import custom
import subprocess


best_pt_path = "best.pt"
model = custom(path_or_model=best_pt_path)

model.eval()


# !pip3 install -U jetson-stats

import cv2
import torch
from torchvision.transforms import functional as F
from hubconf import custom
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
from datetime import datetime
import json
from hubconf import custom
from google.colab.patches import cv2_imshow


# Load YOLOv7 model
model = custom(path_or_model='best.pt')

def take_photo(filename='photo.jpg', quality=0.8, delay=2):
    js = Javascript('''
      async function takePhoto(quality) {
        const div = document.createElement('div');
        const video = document.createElement('video');
        video.style.display = 'block';
        const stream = await navigator.mediaDevices.getUserMedia({video: true});

        document.body.appendChild(div);
        div.appendChild(video);
        video.srcObject = stream;
        await video.play();

        google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

        await new Promise(resolve => setTimeout(resolve, 500));

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        stream.getVideoTracks()[0].stop();
        div.remove();
        return canvas.toDataURL('image/jpeg', quality);
      }
      ''')
    display(js)
    data = eval_js('takePhoto({})'.format(quality))
    binary = b64decode(data.split(',')[1])
    with open(filename, 'wb') as f:
        f.write(binary)
    return filename

# Usage: take_photo(filename='photo.jpg', quality=0.8, delay=2)
# The 'delay' parameter specifies the delay in seconds before capturing the photo automatically



life_raft_count = 0
orion_count = 0
life_ring_count = 0
lpu_count = 0


def print_results(results, indent=0):
    # Iterate over the attributes of the results object
    for attr_name in dir(results):
        # Skip private and special attributes
        if attr_name.startswith('__'):
            continue

        # Get the value of the attribute
        attr_value = getattr(results, attr_name)

        # Print the attribute name and value
        print(' ' * indent + f'{attr_name}: {attr_value}')

        # If the attribute is an object, recursively print its contents
        if hasattr(attr_value, '__dict__'):
            print_results(attr_value, indent + 4)

# Load YOLOv7 model
model = custom(path_or_model=best_pt_path)

# Function to perform object detection and save frames
def detect_and_save(frame):
    global life_raft_count, orion_count, life_ring_count, lpu_count

    # Perform object detection
    results = model(frame)
    print_results(results)


    # Process results and save frames
    for result in results.pred:
        for det in result:
            class_id = int(det[5])
            print(class_id)
            if(class_id == 0):
                lpu_count+=1
            elif(class_id == 1):
                life_raft_count+=1
            elif(class_id == 2):
                life_ring_count+=1
            elif(class_id == 3):
                orion_count+=1


            confidence = det[4]

            # Check if confidence is above threshold
            if confidence >= 0.5:
                # Extract bounding box coordinates
                bbox = det[:4].tolist()

                # Create a copy of the original frame
                frame_copy = frame.copy()

                # Draw bounding box on frame
                x, y, w, h = bbox
                cv2.rectangle(frame_copy, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)

                # Get class name from class ID
                # class_name = class_mapping.get(class_id)
                class_name = results.names[class_id]

                # Get current time
                current_time = datetime.now().strftime("%H:%M:%S")

                # Add class name and detection time next to the bounding box
                cv2.putText(frame_copy, f'{class_name} {current_time}', (int(x), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Save frame with bounding box
                if(class_id == 0):
                  cv2.imwrite(f"runs/{class_name}_{lpu_count-1}.jpg", frame_copy)
                elif(class_id == 1):
                  cv2.imwrite(f"runs/{class_name}_{life_raft_count-1}.jpg", frame_copy)
                elif(class_id == 2):
                  cv2.imwrite(f"runs/{class_name}_{life_ring_count-1}.jpg", frame_copy)
                elif(class_id == 3):
                  cv2.imwrite(f"runs/{class_name}_{orion_count-1}.jpg",frame_copy)


    # Display the frame with bounding boxes
    cv2_imshow(frame)


# Take photo from live camera feed
filename = take_photo()

# Read the captured image
frame = cv2.imread(filename)

detect_and_save(frame)



