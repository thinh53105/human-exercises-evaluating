import cv2

import time
from threading import Thread, Lock

import tkinter as tk
from tkinter.filedialog import askopenfilename

from keypoint_detector.exercises_module import PushupsKeypointsDetector

root = tk.Tk()
root.withdraw()

class VideoStreamer:
    
    def __init__(self) -> None:
        self.stream = None
        self.default_frame = cv2.imread('src/sample_images/img001.png')
        self.frame = self.default_frame
        self.keypoint_detector = PushupsKeypointsDetector()
        self.is_stopped = False
        self.thread = None
    
    def open_stream(self, video_path):
        self.start()
        self.stream = cv2.VideoCapture(video_path)
    
    def open_file(self):
        if self.stream:
            return
        filename = askopenfilename()
        if filename:
            self.open_stream(filename)

    def open_camera(self):
        if self.stream:
            return
        self.open_stream(0)
    
    def start(self):
        self.is_stopped = False
        if self.thread:
            self.thread.join()
        self.thread = Thread(target=self.loop, args=())
        self.thread.start()

    def loop(self):
        while not self.is_stopped:
            if not self.stream:
                continue
            ret, frame = self.stream.read()
            if not ret:
                self.frame = self.default_frame
                self.stop()
                continue
            frame, cur_angle = self.keypoint_detector.process(frame)
            if not cur_angle:
                self.frame = self.default_frame
                self.stop()
                continue
            self.frame = frame

    def get_frame(self):
        return self.frame
    
    def stop(self):
        self.stream = None
        self.is_stopped = True
        
    
    
