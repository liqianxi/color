#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
import os

def gst_pipeline_string():
    # Parameters from the camera_node
    # Refer here : https://github.com/duckietown/dt-duckiebot-interface/blob/
    #   daffy/packages/camera_driver/config/jetson_nano_camera_node/duckiebot.yaml
    res_w, res_h, fps = 640, 480, 30
    fov = 'full'
    # find best mode
    camera_mode = 3  #
    # compile gst pipeline
    gst_pipeline = f""" \
        nvarguscamerasrc \
        sensor-mode={camera_mode} exposuretimerange="100000 80000000" ! \
        video/x-raw(memory:NVMM), width={res_w}, height={res_h}, format=NV12,
            framerate={fps}/1 ! \
        nvjpegenc ! \
        appsink \
    """

    # ---
    print(f"Using GST pipeline: `{gst_pipeline}`")
    return gst_pipeline

def most_frequent(List):
    return max(set(List), key = List.count)

def represent_color(split_part):
    new_array = split_part.transpose(2,0,1).reshape(-1,3)
    #temp = [str(i) for i in new_array]
    #for row,col,rgb in split_part:
    #    pass
    unique,counts = np.unique(new_array,axis=0,return_counts=True)


    return unique[np.argmax(counts)]


N_SPLITS = int(os.environ["N_SPLITS"])
cap = cv2.VideoCapture()
cap.open(gst_pipeline_string(), cv2.CAP_GSTREAMER)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    frame = cv2.imdecode(frame, 1)  # BGR colour
    #print(frame.shape)#(480, 640, 3)
    split_height = int(frame.shape[0]/N_SPLITS)
    #color_list = []

    for row_idx in range(N_SPLITS):
        split_part = frame[row_idx*split_height:(row_idx+1)*split_height]
        #print(split_part.shape)(24, 640, 3)
        color= represent_color(split_part)
        #color_list.append(color)
        print(f"Most present RGB color from row {row_idx*split_height} to {(row_idx+1)*split_height} is {color}")

    sleep(1)
