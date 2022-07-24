import cv2
import matplotlib.pyplot as plt

import config

from threading import Thread, Lock

import tkinter as tk
from tkinter.filedialog import askopenfilename

from keypoint_detector.exercises_module import PushupsKeypointsDetector
from counter.lpf import LowPassFilter
from evaluator.exercises_evaluator import PushupsEvaluator
from predictor.pushups.predictor import PushupsPredictor

root = tk.Tk()
root.withdraw()

class VideoStreamer:
    
    def __init__(self) -> None:
        self.stream = None
        self.default_frame = cv2.imread('src/sample_images/img001.png')
        self.frame = self.default_frame.copy()
        self.keypoint_detector = PushupsKeypointsDetector()
        self.is_stopped = False
        self.thread = None
        self.lpf_config = config.LPFConfig
        self.lpf = LowPassFilter(self.lpf_config.BETA)
        self.evaluator = PushupsEvaluator(signal_filter=self.lpf)
        self.predictor = PushupsPredictor([
            'src/predictor/pushups/models/mobinet-20220724_up.tflite',
            'src/predictor/pushups/models/mobinet-20220724_down.tflite'],
            )
        self.total, self.no_right, self.no_wrong = 0, 0, 0
    
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

    def get_frame(self):
        self.total = int(self.lpf.count)
        return self.frame, (self.total, self.no_right, self.no_wrong)
    
    def reset_analysis_value(self):
        self.total, self.no_right, self.no_wrong = 0, 0, 0
    
    def stop(self):
        if self.is_stopped:
            return
        self.stream = None
        self.is_stopped = True
        self.evaluator.evaluate_next()
        self.frame = self.default_frame.copy()
        self.reset_analysis_value()
