from config import UIAppConfig

import cv2
import numpy as np
from .utils import Window, Div, Label, Button

app_config = UIAppConfig()

class UIDrawer:

    def __init__(self):
        self.btn_list = []
        self.window = Window(
            (app_config.WINDOW_WIDTH, app_config.WINDOW_HEIGHT),
            app_config.BACKGROUND_COLOR,
            []
        )
        self.div_title = Div(
            (0, 0), (700, 60), (111, 111, 111),
            []
        )
        self.div_navigator = Div(
            (0, 200), (1000, 200), (55, 55, 55),
            []
        )
        self.lbl_title = Label(
            (45, 0), (700, 60), None,
            'HUMAN EXERCISES EVALUATING', 700, 
            (255, 255, 255), 1.2, 5
        )
        self.btn_pushups = Button(
            (50, 50), (300, 100), (195, 195, 75),
            "Push-ups", 100, 
            (255, 255, 255), 1, 4,
            None
        )
        self.btn_squats = Button(
            (450, 50), (300, 100), (195, 195, 75),
            "Squats", 100, 
            (255, 255, 255), 1, 4,
            None
        )

        self.div_title.add_util(self.lbl_title)
        self.div_navigator.add_util(self.btn_pushups)
        self.div_navigator.add_util(self.btn_squats)
        self.window.add_util(self.div_title)
        self.window.add_util(self.div_navigator)
        self.btn_list.append(self.btn_pushups)
        self.btn_list.append(self.btn_squats)

    def get_ui(self):
        return self.window.get_cur_frame()
    
    def update_ui(self):
        self.window.update()
    
    def get_btn_list(self):
        return self.btn_list
    
    def reset_btn(self):
        for btn in self.btn_list:
            btn.set_state('normal')
