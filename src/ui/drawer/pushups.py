from config import UIAppConfig

from ..utils import Window, Div, Label, Button, ButtonsPool, ImageFrame


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
            (1000, 50), (400, 600), (55, 55, 55),
            []
        )
        self.div_exercise = Div(
            (100, 100), (800, 450), (155, 155, 155),
            []
        )
        self.div_analysis = Div(
            (150, 550), (800, 200), app_config.BACKGROUND_COLOR,
            []
        )
        self.lbl_title = Label(
            (45, 0), (700, 60), None,
            'PUSH-UPS EVALUATING', 700, 
            (255, 255, 255), 1, 5
        )
        self.frame_pushups = ImageFrame(
            (0, 0), (800, 450),
            color=None,
            image=None,
            image_path='src/sample_images/pushups.png'
        )
        self.lbl_total = Label(
            (0, 75), (200, 60), None,
            'Total: 0', 200, 
            (255, 255, 255), 1, 5
        )
        self.lbl_right = Label(
            (200, 75), (200, 60), None,
            'Right: 0', 200, 
            (255, 255, 255), 1, 5
        )
        self.lbl_wrong = Label(
            (400, 75), (200, 60), None,
            'Wrong: 0', 200, 
            (255, 255, 255), 1, 5
        )
        self.lbl_fps = Label(
            (600, 75), (200, 60), None,
            'FPS: 0', 200, 
            (255, 255, 255), 1, 5
        )
        self.btn_file = Button(
            (50, 25), (300, 100), (195, 195, 75),
            "Open File", 150, 
            (255, 255, 255), 1, 4,
            btn_file_func
        )
        self.btn_camera = Button(
            (50, 175), (300, 100), (195, 195, 75),
            "Open Camera", 200, 
            (255, 255, 255), 1, 4,
            btn_camera_func
        )
        self.btn_stop = Button(
            (50, 325), (300, 100), (195, 195, 75),
            "Stop", 100, 
            (255, 255, 255), 1, 4,
            btn_stop_func
        )
        self.btn_back = Button(
            (50, 475), (300, 100), (195, 195, 75),
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
        self.div_exercise.add_util(self.frame_pushups)
        self.div_analysis.add_utils([
            self.lbl_total,
            self.lbl_right,
            self.lbl_wrong,
            self.lbl_fps
        ])
        self.div_navigator.add_utils(self.btns_pool)
        self.window.add_utils([
            self.div_title,
            self.div_exercise,
            self.div_analysis,
            self.div_navigator
        ])
    def get_stream_frame(self):
        return self.frame_pushups