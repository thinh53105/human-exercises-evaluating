from cv2 import FONT_HERSHEY_SIMPLEX

class UIUtilsConfig:

    MOUSE_STATE_DICT = {
        'normal' : {'color': (195, 195, 75), 'foreground': (255, 255, 255)},
        'hover' : {'color': (22, 210, 64), 'foreground': (255, 255, 255)},
        'clicked' : {'color': (48, 153, 70), 'foreground': (255, 255, 255)}
    }

    FONT_NAME = FONT_HERSHEY_SIMPLEX
    FONT_HEIGHT = 22


class UIAppConfig:
    WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 720
    VIDEO_X, VIDEO_Y = 50, 70
    SCALE_RATE = 1.5
    VIDEO_WIDTH, VIDEO_HEIGHT = int(576 * SCALE_RATE), int(320 * SCALE_RATE)
    BACKGROUND_COLOR = (200, 111, 111)
    
