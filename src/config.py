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
    WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 750
    BACKGROUND_COLOR = (200, 111, 111)
    

class LPFConfig():
    def __init__(self, exercise_type):
        if exercise_type == 'pushups':
            self.FRAME_SKIP_RATE = 5
            self.T = 50
            self.BETA = 1 - self.FRAME_SKIP_RATE / self.T
        elif exercise_type == 'squats':
            self.FRAME_SKIP_RATE = 5
            self.T = 50
            self.BETA = 1 - self.FRAME_SKIP_RATE / self.T
        else:
            print('NO EXERCISE FOUNDED')

class ExcerciseConfig:
    def __init__(self, exercise_type):
        if exercise_type=='pushups':
            print("="*100)
            print("INITIALIZING PUSHUPS CONFIG")
            print("="*100)

            self.DOWN_WEIGHT = 'src/predictor/models/pushups/pushups_MobileNetV2_down.tflite'
            self.UP_WEIGHT = 'src/predictor/models/pushups/pushups_MobileNetV2_up.tflite'
            self.INDEX_LEFT = (11, 13, 15) 
            self.INDEX_RIGHT = (12, 14, 16)
        elif exercise_type=='squats':
            print("="*100)
            print("INITIALIZING SQUATS CONFIG")
            print("="*100)
            self.DOWN_WEIGHT = 'src/predictor/models/squats/squats_MobileNetV2_down.tflite'
            self.UP_WEIGHT = 'src/predictor/models/squats/squats_MobileNetV2_up.tflite'
            self.INDEX_LEFT = (23, 25, 27) 
            self.INDEX_RIGHT = (24, 26, 28)
        else:
            print('NO EXCERCISE FOUND')

