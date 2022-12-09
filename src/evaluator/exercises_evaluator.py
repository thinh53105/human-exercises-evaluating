import cv2
import numpy as np
import matplotlib.pyplot as plt


class Evaluator:
    
    def __init__(self, signal_filter) -> None:
        self.eval = False
        self.signal_filter = signal_filter
        self.up_list, self.down_list = [], []
        self.color = {"RIGHT": (0, 255, 0), "WRONG": (0, 0, 255)}
        self.fps_list = []
    
    def evaluate(self):
        self.evaluate_counting()
        self.signal_filter.reset()
        self.eval = False

        if self.down_list and self.up_list:
            self.evaluate_right_wrong((525, 350))
            self.up_list, self.down_list = [], []
        
        # self.evaluate_fps()
        self.fps_list = []
    
    def evaluate_counting(self):
        plt.figure(figsize=(10, 10))
        plt.plot(self.signal_filter.angle_list)
        # plt.plot(self.signal_filter.filter_list)
        plt.legend(['raw signal'])
        # plt.legend(['raw signal', 'low-pass-filter'])
        plt.xlabel('frame count')
        plt.ylabel('angle')
        plt.show()

    def evaluate_right_wrong(self, img_size):
        l = len(self.down_list)

        for i in range(l):
            up_img, up_right, up_conf = self.up_list[i]
            down_img, down_right, down_conf = self.down_list[i]

            up_img = cv2.resize(up_img, dsize=img_size)
            down_img = cv2.resize(down_img, dsize=img_size)
            up_str = "RIGHT" if up_right else "WRONG"
            down_str = "RIGHT" if down_right else "WRONG"

            ver = np.concatenate((up_img, down_img), axis=0)
            ver = cv2.putText(ver, up_str, (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, self.color[up_str], 3)
            ver = cv2.putText(ver, str(round(up_conf, 4)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, self.color[up_str], 3)
            ver = cv2.putText(ver, down_str, (50, 450), cv2.FONT_HERSHEY_PLAIN, 3, self.color[down_str], 3)
            ver = cv2.putText(ver, str(round(down_conf, 4)), (50, 500), cv2.FONT_HERSHEY_PLAIN, 3, self.color[down_str], 3)

            lastname = f'{i}/{l}'
            if i != 0:
                cv2.destroyWindow(lastname)

            cur_name = f'{i + 1}/{l}'
            cv2.namedWindow(cur_name)
            cv2.moveWindow(cur_name, 300, 0)
            cv2.imshow(cur_name, ver)
            cv2.waitKey(0)
        if l != 0:
            cv2.destroyWindow(f'{l}/{l}')
    
    def evaluate_fps(self):
        plt.figure(figsize=(10, 10))
        plt.plot(self.fps_list)
        plt.axhline(y=np.average(self.fps_list), color='r', linestyle='-')
        plt.legend(['raw fps', 'average'])
        plt.xlabel('frame count')
        plt.ylabel('fps')
        plt.show()
    
    def evaluate_next(self):
        self.eval = True
    
    def is_eval(self):
        return self.eval