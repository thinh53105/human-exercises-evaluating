from config import UIUtilsConfig

import cv2
import numpy as np

ui_utils_config = UIUtilsConfig()


class Utils:

    def __init__(self, start_pos, w_h, color):
        self.x, self.y = start_pos
        self.abs_x, self.abs_y = start_pos
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
    
    def update_abs_pos_for_sub_util(self, util):
        if isinstance(util, Container):
            for sub_util in util.util_list:
                sub_util.abs_x += self.abs_x
                sub_util.abs_y += self.abs_y
                self.update_abs_pos_for_sub_util(sub_util)
    
    def add_util(self, util):
        self.util_list.append(util)
        util.abs_x = self.abs_x + util.x
        util.abs_y = self.abs_y + util.y
        self.update_abs_pos_for_sub_util(util)
    
    def add_utils(self, util_list):
        for util in util_list:
            self.add_util(util)
    
    def update(self):
        for util in self.util_list:
            if isinstance(util, Container):
                util.update()
            self.cur_frame = util.place(self.cur_frame)


class Window(Container):

    def __init__(self, w_h, color, util_list):
        super().__init__(start_pos=(0, 0), w_h=w_h, color=color, util_list=util_list)


class Div(Container):

    def __init__(self, start_pos, w_h, color, util_list):
        super().__init__(start_pos=start_pos, w_h=w_h, color=color, util_list=util_list)
    
    def place(self, image):
        x, y, w, h = self.x, self.y, self.w, self.h
        image[y:y+h, x:x+w] = self.cur_frame
        return image


class Button(Utils):

    def __init__(self, start_pos, w_h, color_normal, text, text_width, fg_color_normal, fg_scale, fg_strong, func):
        super().__init__(start_pos=start_pos, w_h=w_h, color=color_normal)
        self.text = text
        self.text_width = text_width
        self.color_normal = color_normal
        self.fg_color = self.fg_color_normal = fg_color_normal
        self.fg_scale = fg_scale
        self.fg_strong = fg_strong
        self.func = func
        self.state = 'normal'

    def place(self, image):
        if self.state != 'normal':
            self.color = ui_utils_config.MOUSE_STATE_DICT[self.state]['color']
            self.fg_color = ui_utils_config.MOUSE_STATE_DICT[self.state]['foreground']
        else:
            self.color = self.color_normal
            self.fg_color = self.fg_color_normal

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
        return self.abs_x <= x <= self.abs_x + self.w and self.abs_y <= y <= self.abs_y + self.h

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


class ButtonsPool(list):

    def __init__(self, btn_list):
        self.extend(btn_list)
    
    def hanle_mouse_hover(self, x, y):
        for btn in self:
            if btn.mouse_focus(x, y) and btn.get_state() != 'clicked':
                btn.set_state('hover')
            elif btn.get_state() == 'hover':
                btn.set_state('normal')

    def handle_mouse_clicked(self, x, y):
        for btn in self:
            if btn.mouse_focus(x, y):
                self.reset_btn()
                btn.set_state('clicked')
                btn.call_func()
                btn.set_state('normal')
    
    def reset_btn(self):
        for btn in self:
            btn.set_state('normal')
