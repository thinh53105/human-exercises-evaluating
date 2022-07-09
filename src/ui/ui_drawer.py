from config import UIAppConfig

import cv2
import numpy as np
from .utils import Window, Div, Label, Button

app_config = UIAppConfig()

class UIDrawer:

    def __init__(self):
        self.window = Window(
            (app_config.WINDOW_WIDTH, app_config.WINDOW_HEIGHT),
            app_config.BACKGROUND_COLOR
        )
        self.div_title = Div(
            (0, 0), (700, 60), (111, 111, 111),
        )
        self.label_title = Label(
            (45, 0), (700, 60), None,
            'HUMAN EXERCISES EVALUATING', 700, 
            (255, 255, 255), 1.2, 5
        )
        self.div_title.add_util(self.label_title)
        self.window.add_util(self.div_title)

    def get_ui(self):
        return self.window.get_cur_frame()
    
    def update_ui(self):
        self.window.update()