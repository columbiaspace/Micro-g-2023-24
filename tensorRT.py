import torch
import torchvision.models as models
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import cv2
from  hubconf import custom

#step 1
best_pt_path = "best.pt"
model = custom(path_or_model=best_pt_path)

dummy_input = torch.randn(1, 3, 416, 416)  # Assuming input size is 416x416
torch.onnx.export(model, dummy_input, 'model.onnx', verbose=True)


# Step 2: Optimize ONNX Model for TensorRT
TRT_LOGGER = trt.Logger(trt.Logger.INFO)
with trt.Builder(TRT_LOGGER) as builder, builder.create_network() as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
    builder.max_workspace_size = 1 << 30  # Set maximum workspace size
    builder.max_batch_size = 1  # Set maximum batch size
    with open('model.onnx', 'rb') as f:
        parser.parse(f.read())
        engine = builder.build_cuda_engine(network)
# Step 3: Serialize the TensorRT Engine to a file
with open('your_tensorrt_model.engine', 'wb') as f:
    f.write(engine.serialize())
# Step 4: Load the TensorRT Engine
with open('your_tensorrt_model.engine', 'rb') as f, trt.Runtime(TRT_LOGGER) as runtime:
    engine_data = f.read()
    engine = runtime.deserialize_cuda_engine(engine_data)
# Function to perform object detection and save frames
def detect_and_save(engine, frame):
    global life_raft_count, orion_count, life_ring_count, lpu_count
    # Allocate buffers for input and output
    bindings = []
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        host_mem = cuda.pagelocked_empty(size, dtype)
        cuda_mem = cuda.mem_alloc(host_mem.nbytes)
        bindings.append(int(cuda_mem))
    # Preprocess input frame and copy to GPU
    # (Assuming frame is in BGR format)
    frame = cv2.resize(frame, (416, 416))
    frame = frame.transpose(2, 0, 1).astype(np.float32)  # Change HWC to CHW
    frame /= 255.0  # Normalize to [0, 1]
    np.copyto(host_mem, frame.ravel())
    cuda.memcpy_htod_async(cuda_mem, host_mem, stream)
    # Run inference
    context = engine.create_execution_context()
    stream = cuda.Stream()
    context.execute_async(bindings=bindings, stream_handle=stream.handle)
    # Get output predictions
    output = np.empty((1, 2535, 85), dtype=np.float32)
    cuda.memcpy_dtoh_async(output, bindings[1], stream)
    stream.synchronize()
    # Process results and save frames
    for det in output[0]:
        class_id = int(det[5])
        if(class_id == 0):
            lpu_count += 1
        elif(class_id == 1):
            life_raft_count += 1
        elif(class_id == 2):
            life_ring_count += 1
        elif(class_id == 3):
            orion_count += 1
        confidence = det[4]
        # Check if confidence is above threshold
        if confidence >= 0.5:
            # Extract bounding box coordinates
            bbox = det[:4]
            # Create a copy of the original frame
            frame_copy = frame.copy()
            # Draw bounding box on frame
            x, y, w, h = bbox
            cv2.rectangle(frame_copy, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
            # Get class name from class ID
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
                cv2.imwrite(f"runs/{class_name}_{orion_count-1}.jpg", frame_copy)
    # Display the frame with bounding boxes
    cv2_imshow(frame)
running the detect_and_save() function:
detect_and_save(engine, frame)
