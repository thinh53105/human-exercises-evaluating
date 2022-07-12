from config import UIAppConfig

from ..utils import Window, Div, Label, Button, ButtonsPool


app_config = UIAppConfig()


class PushupsDrawer:

    def __init__(self, btn_file_func, btn_camera_func, btn_stop_func, btn_back_func):
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
            (0, 200), (1600, 200), (55, 55, 55),
            []
        )
        self.lbl_title = Label(
            (45, 0), (700, 60), None,
            'PUSH-UPS EVALUATING', 700, 
            (255, 255, 255), 1, 5
        )
        self.btn_file = Button(
            (50, 50), (300, 100), (195, 195, 75),
            "Open File", 150, 
            (255, 255, 255), 1, 4,
            btn_file_func
        )
        self.btn_camera = Button(
            (450, 50), (300, 100), (195, 195, 75),
            "Open Camera", 200, 
            (255, 255, 255), 1, 4,
            btn_camera_func
        )
        self.btn_stop = Button(
            (850, 50), (300, 100), (195, 195, 75),
            "Stop", 100, 
            (255, 255, 255), 1, 4,
            btn_stop_func
        )
        self.btn_back = Button(
            (1250, 50), (300, 100), (195, 195, 75),
            "Back", 100, 
            (255, 255, 255), 1, 4,
            btn_back_func
        )
        self.btns_pool = ButtonsPool([
            self.btn_file,
            self.btn_camera,
            self.btn_stop,
            self.btn_back
        ])

        self.div_title.add_util(self.lbl_title)
        self.div_navigator.add_utils(self.btns_pool)
        self.window.add_util(self.div_title)
        self.window.add_util(self.div_navigator)