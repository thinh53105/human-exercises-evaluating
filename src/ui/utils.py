from config import UIUtilsConfig

import cv2
import numpy as np

ui_utils_config = UIUtilsConfig()


class Utils:

    def __init__(self, start_pos, w_h, color):
        self.x, self.y = start_pos
        self.w, self.h = w_h
        self.color = color
    
    def place(self, image):
        image = cv2.rectangle(image, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, cv2.FILLED)
        return image


class Container(Utils):

    def __init__(self, start_pos, w_h, color, util_list):
        super().__init__(start_pos=start_pos, w_h=w_h, color=color)
        self.cur_frame = self.get_default_frame()
        self.util_list = util_list

    def get_default_frame(self):
        ones_array = np.ones((self.h, self.w, 3), dtype="uint8")
        bg_color_array = np.array(self.color).reshape(1, 1, 3)
        default_frame = ones_array * bg_color_array
        return default_frame.astype('uint8')
    
    def get_cur_frame(self):
        return self.cur_frame
    
    def add_util(self, util):
        self.util_list.append(util)
    
    def update(self):
        for util in self.util_list:
            if isinstance(util, Container):
                util.update()
            self.cur_frame = util.place(self.cur_frame)


class Window(Container):

    def __init__(self, w_h, color, util_list=[]):
        super().__init__(start_pos=(None, None), w_h=w_h, color=color, util_list=util_list)


class Div(Container):

    def __init__(self, start_pos, w_h, color, util_list=[]):
        super().__init__(start_pos=start_pos, w_h=w_h, color=color, util_list=util_list)
    
    def place(self, image):
        x, y, w, h = self.x, self.y, self.w, self.h
        image[y:y+h, x:x+w] = self.cur_frame
        return image


class Button(Utils):

    def __init__(self, start_pos, w_h, text, text_width, fg_scale, fg_strong, func):
        super().__init__(start_pos=start_pos, w_h=w_h, color=None)
        self.text = text
        self.text_width = text_width
        self.fg_color = None
        self.fg_scale = fg_scale
        self.fg_strong = fg_strong
        self.func = func
        self.state = 'normal'

    def place(self, image):
        self.color = ui_utils_config.MOUSE_STATE_DICT[self.state]['color']
        self.fg_color = ui_utils_config.MOUSE_STATE_DICT[self.state]['foreground']

        image = cv2.rectangle(image, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, cv2.FILLED)
        image = cv2.putText(
            image, 
            self.text, 
            (self.x + (self.w - self.text_width) // 2, self.y + (self.h + ui_utils_config.FONT_HEIGHT * self.fg_scale) // 2),
            ui_utils_config.FONT_NAME,
            self.fg_scale,
            self.fg_color,
            self.fg_strong)
        return image

    def mouse_focus(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

    def get_state(self):
        return self.state

    def set_state(self, state_name):
        self.state = state_name

    def call_func(self):
        self.func()


class Label(Utils):

    def __init__(self, start_pos, w_h, color, text, text_width, fg_color, fg_scale, fg_strong):
        super().__init__(start_pos=start_pos, w_h=w_h, color=color)
        self.text = text
        self.text_width = text_width
        self.fg_color = fg_color
        self.fg_scale = fg_scale
        self.fg_strong = fg_strong

    def place(self, image):
        if self.color:
            image = cv2.rectangle(image, (self.x, self.y), (self.x + self.w, self.y + self.h), self.bg, cv2.FILLED)
        image = cv2.putText(
            image, 
            self.text, 
            (self.x + (self.w - self.text_width) // 2, self.y + int(self.h + ui_utils_config.FONT_HEIGHT * self.fg_scale) // 2),
            ui_utils_config.FONT_NAME, 
            self.fg_scale, 
            self.fg_color, 
            self.fg_strong)
        return image

    def set_text(self, new_text):
        self.text = new_text
