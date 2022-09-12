from cv2 import FONT_HERSHEY_SIMPLEX

class UIUtilsConfig:

    MOUSE_STATE_DICT = {
        # 'normal' : {'color': (195, 195, 75), 'foreground': (255, 255, 255)},
        'hover' : {'color': (22, 210, 64), 'foreground': (255, 255, 255)},
        'clicked' : {'color': (48, 153, 70), 'foreground': (255, 255, 255)}
    }

    FONT_NAME = FONT_HERSHEY_SIMPLEX
    FONT_HEIGHT = 22


class UIAppConfig:
    WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900
    BACKGROUND_COLOR = (200, 111, 111)
    

class LPFConfig:
    FRAME_SKIP_RATE = 1
    T = 50
    BETA = 1 - FRAME_SKIP_RATE / T

class PushupsConfig:
    PUSHUPS_DOWN_WEIGHT = 'src/predictor/pushups/models/mobinet-20220724_up.tflite'
    PUSHUPS_UP_WEIGHT = 'src/predictor/pushups/models/mobinet-20220724_down.tflite'

class SquatsConfig:
    SQUATS_DOWN_WEIGHT = 'src/predictor/squats/models/mobinet-20220724_up.tflite'
    SQUATS_UP_WEIGHT = 'src/predictor/squats/models/mobinet-20220724_down.tflite'