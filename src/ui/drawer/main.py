from config import UIAppConfig

from ..utils import Window, Div, Label, Button, ButtonsPool


app_config = UIAppConfig()


class MainDrawer:

    def __init__(self, btn_pushups_func, btn_squat_func):
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
            (200, 200), (1000, 200), (55, 55, 55),
            []
        )
        self.lbl_title = Label(
            (45, 0), (700, 60), None,
            'HUMAN EXERCISES EVALUATING', 700, 
            (255, 255, 255), 1.2, 5
        )
        self.btn_pushups = Button(
            (150, 50), (300, 100), (195, 195, 75),
            "Push-ups", 150, 
            (255, 255, 255), 1, 4,
            btn_pushups_func
        )
        self.btn_squats = Button(
            (550, 50), (300, 100), (195, 195, 75),
            "Squats", 100, 
            (255, 255, 255), 1, 4,
            btn_squat_func
        )
        self.btns_pool = ButtonsPool([
            self.btn_pushups,
            self.btn_squats
        ])

        self.div_title.add_util(self.lbl_title)
        self.div_navigator.add_utils(self.btns_pool)
        self.window.add_util(self.div_title)
        self.window.add_util(self.div_navigator)
