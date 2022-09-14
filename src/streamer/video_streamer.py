import cv2
import matplotlib.pyplot as plt

import config

from threading import Thread, Lock
import time

import tkinter as tk
from tkinter.filedialog import askopenfilename

from keypoint_detector.exercises_module import KeypointsDetector
from counter.lpf import LowPassFilter
from evaluator.exercises_evaluator import Evaluator
from predictor.excercise_predictor import Predictor


root = tk.Tk()
root.withdraw()

class VideoStreamer:
    
    def __init__(self, type) -> None:
        self.stream = None
        self.type = type
        self.default_frame = cv2.imread(f'src/sample_images/{type}.png')
        self.frame = self.default_frame.copy()
        self.is_stopped = False
        self.thread = None
        self.lpf_config = config.LPFConfig(exercise_type=self.type)
        self.lpf = LowPassFilter(self.lpf_config.BETA)
        self.exc_config = config.ExcerciseConfig(exercise_type=self.type)
        self.evaluator = Evaluator(signal_filter=self.lpf)
        self.keypoint_detector = KeypointsDetector(config=self.exc_config)
        self.predictor = Predictor([
                self.exc_config.UP_WEIGHT,
                self.exc_config.DOWN_WEIGHT],
                )

        self.total, self.no_right, self.no_wrong = 0, 0, 0
        self.fps = 0
    
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
        frame_count = 0
        target_frame, target_angle = None, 0
        p_time = time.time()
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
                # self.frame = self.default_frame
                # self.stop()
                continue
            if (frame_count + 1) % self.lpf_config.FRAME_SKIP_RATE == 0:
                cur_angle = max(60, cur_angle)
                Fn, state = self.lpf.cal_next(cur_angle)

                if self.lpf.high and cur_angle > target_angle:
                    target_frame, target_angle = frame, cur_angle
                if not self.lpf.high and cur_angle < target_angle:
                    target_frame, target_angle = frame, cur_angle
                
                if state == 1:
                    up_right, conf = self.predictor.predict(target_frame, 1)
                    self.evaluator.up_list.append((target_frame, up_right, conf))

                    target_angle = 200
                
                if state == 0:
                    down_right, conf = self.predictor.predict(target_frame, 0)
                    self.evaluator.down_list.append((target_frame, down_right, conf))

                    if up_right and down_right:
                        self.no_right += 1
                    else:
                        self.no_wrong += 1
                    
                    target_angle = 0

            self.frame = frame
            frame_count += 1
            c_time = time.time()
            self.fps = 1 / (c_time - p_time + 1e-9)
            self.evaluator.fps_list.append(self.fps)
            p_time = c_time

    def get_frame(self):
        self.total = int(self.lpf.count)
        return self.frame, (self.total, self.no_right, self.no_wrong, self.fps)
    
    def reset_analysis_value(self):
        self.total, self.no_right, self.no_wrong, self.fps = 0, 0, 0, 0
    
    def stop(self):
        if self.is_stopped:
            return
        self.stream = None
        self.is_stopped = True
        self.evaluator.evaluate_next()
        self.frame = self.default_frame.copy()
        self.reset_analysis_value()
