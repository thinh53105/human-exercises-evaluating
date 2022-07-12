from .main import MainDrawer
from .pushups import PushupsDrawer


class UIDrawer:

    def __init__(self):
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
        self.current_ui = self.ui_drawer

    def get_ui(self):
        return self.current_ui.window.get_cur_frame()
    
    def update_ui(self):
        self.current_ui.window.update()
    
    def get_btns_pool(self):
        return self.current_ui.btns_pool
    
    def btn_pushups_action(self):
        self.current_ui = self.pushups_drawer
    
    def btn_squats_action(self):
        print('BUTTON SQUATS CALLED')

    def btn_file_action(self):
        print('BUTTON FILE CALLED')
    
    def btn_camera_action(self):
        print('BUTTON CAMERA CALLED')
    
    def btn_stop_action(self):
        print('BUTTON STOP CALLED')
    
    def btn_back_action(self):
        self.current_ui = self.ui_drawer
