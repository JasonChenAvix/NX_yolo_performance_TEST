from ultralytics import YOLO  # Import the YOLO module from Ultralytics
import cv2
import numpy as np
import os
import torch
import time

# Setting up the device for GPU if available
torch.cuda.set_device(0)  # Set to your desired GPU, if using CUDA

# Initialize the YOLO model
# model = YOLO('opt.engine',task='detect')
model = YOLO('yolov8s_test.engine',task='detect')
# model = YOLO('yolov8s_half_sim.engine',task='detect')
#model = YOLO('yolov8s_half_sim_ws8.engine',task='detect')
# Video file to be processed and the output video file
input_video_path = 'classroom.mp4'

# Open the input video
cap = cv2.VideoCapture(input_video_path)

# Get video properties
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = 1280
height = 736
#width = 1280
#height = 736
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object to save the output video
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform detection
    #tic = time.time()
    #frame = cv2.resize(frame, (width, height))
    toc = time.time()
    #resize = toc - tic
    results = model.predict(source=frame, conf=0.6, classes=0, imgsz=(height,width), verbose=True, half = True, device="cuda:0")
    # results = model.predict(source=frame, conf=0.6, classes=0, imgsz=(height,width), verbose=True, half = True)
    current = time.time()-toc
    print(f"inference time is {current}")
    boxes = results[0].boxes

    # Annotate the frame with detected objects
    annotated_frame = results[0].plot()

    # Write the annotated frame to the output video
    #out.write(annotated_frame)

    # Optionally display the frame in a window (for testing)
    cv2.imshow('Frame', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
#out.release()
cv2.destroyAllWindows()
