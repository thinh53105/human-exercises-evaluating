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
        
        self.lb_up, self.lb_down = None, None
        self.lb_configs = config.LabelsCongfig.LB
    
    def open_stream(self, video_path):
        self.start()
        self.stream = cv2.VideoCapture(video_path)
    
    def open_file(self):
        if self.stream:
            return
        filename = askopenfilename()
        if filename:
            self.open_stream(filename)
            video_name = filename.split('/')[-1]
            if video_name in self.lb_configs:
                self.lb_up = self.lb_configs[video_name][0]
                self.lb_down = self.lb_configs[video_name][1]
                

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
        target_up_frame, target_process_up_frame, target_up_angle = None, None, 0
        target_down_frame, target_process_down_frame, target_down_angle = None, None, 200
        p_time = time.time()
        while not self.is_stopped:
            if not self.stream:
                continue
            ret, frame = self.stream.read()
            if not ret:
                self.frame = self.default_frame
                self.stop()
                continue
            process_frame, cur_angle = self.keypoint_detector.process(frame.copy())
            if not cur_angle:
                # self.frame = self.default_frame
                # self.stop()
                continue
            if (frame_count + 1) % self.lpf_config.FRAME_SKIP_RATE == 0:
                cur_angle = max(60, cur_angle)
                Fn, state = self.lpf.cal_next(cur_angle)

                if self.lpf.high and cur_angle > target_up_angle:
                    target_up_frame, target_process_up_frame, target_up_angle = frame, process_frame, cur_angle
                if not self.lpf.high and cur_angle < target_down_angle:
                    target_down_frame, target_process_down_frame, target_down_angle = frame, process_frame, cur_angle
                
                if state == 1:
                    # cv2.imwrite(f'results_images/up_{int(self.lpf.count)}.jpg', target_up_frame)
                    up_cls, conf = self.predictor.predict(target_up_frame, 1)
                    up_right = up_cls == 0
                    if self.lb_up:
                        up_right = self.lb_up[self.no_wrong + self.no_right]
                    self.evaluator.up_list.append((target_process_up_frame, up_right, conf))

                    target_up_frame, target_process_up_frame, target_up_angle = None, None, 0
                
                if state == 0:
                    # cv2.imwrite(f'results_images/down_{int(self.lpf.count)}.jpg', target_down_frame)
                    down_cls, conf = self.predictor.predict(target_down_frame, 0)
                    down_right = down_cls == 0
                    if self.lb_down:
                        down_right = self.lb_down[self.no_wrong + self.no_right]
                    self.evaluator.down_list.append((target_process_down_frame, down_right, conf))

                    if up_right and down_right:
                        self.no_right += 1
                    else:
                        self.no_wrong += 1
                    
                    target_down_frame, target_process_down_frame, target_down_angle = None, None, 200

            self.frame = process_frame
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
        self.lb_up, self.lb_down = None, None
    
    def stop(self):
        if self.is_stopped:
            return
        self.stream = None
        self.is_stopped = True
        self.evaluator.evaluate_next()
        self.frame = self.default_frame.copy()
        self.reset_analysis_value()
