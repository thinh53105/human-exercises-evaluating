from .main import MainDrawer
from .pushups import PushupsDrawer


class UIDrawer:

    def __init__(self, video_streamer):
        self.video_streamer = video_streamer.start()
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
            frame = self.video_streamer.get_frame()
            stream_frame = self.current_ui.get_stream_frame()
            stream_frame.update_frame(image=frame)
        self.current_ui.window.update()
    
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
