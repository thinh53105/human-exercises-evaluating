from .main import MainDrawer
from .pushups import PushupsDrawer

import matplotlib.pyplot as plt


class UIDrawer:

    def __init__(self, video_streamer):
        self.video_streamer = video_streamer
        self.type = 'pushups'
        self.ui_drawer = MainDrawer(
            self.btn_pushups_action,
            self.btn_squats_action
        )
        self.pushups_drawer = PushupsDrawer(
            self.btn_file_action,
            self.btn_camera_action,
            self.btn_stop_action,
            self.btn_back_action
        )
        self.current_ui = self.pushups_drawer

    def get_ui(self):
        return self.current_ui.window.get_cur_frame()
    
    def update_ui(self):
        if self.type:
            if self.video_streamer.evaluator.is_eval():
                self.video_streamer.evaluator.evaluate()

            frame, analysis_count = self.video_streamer.get_frame()
            stream_frame = self.current_ui.get_stream_frame()
            stream_frame.update_frame(image=frame)
            self.update_analysis_label(*analysis_count)
            
        self.current_ui.window.update()
    
    def update_analysis_label(self, total, no_right, no_wrong):
        self.current_ui.lbl_total.set_text(f"Total : {int(total)}")
        self.current_ui.lbl_right.set_text(f"Right : {no_right}")
        self.current_ui.lbl_wrong.set_text(f"Wrong : {no_wrong}")
        self.current_ui.div_analysis.update(reset=True)
    
    def get_btns_pool(self):
        return self.current_ui.btns_pool
    
    def btn_pushups_action(self):
        self.current_ui = self.pushups_drawer
        self.type = 'pushups'
    
    def btn_squats_action(self):
        print('BUTTON SQUATS CALLED')

    def btn_file_action(self):
        self.video_streamer.open_file()
    
    def btn_camera_action(self):
        self.video_streamer.open_camera()
    
    def btn_stop_action(self):
        self.video_streamer.stop()
    
    def btn_back_action(self):
        self.current_ui = self.ui_drawer
        self.type = None
