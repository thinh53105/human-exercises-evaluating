from .pose_module import PoseDetector

class KeypointsDetector(PoseDetector):

    def __init__(self, detection_conf=0.5, tracking_conf=0.5, config=None):
        super().__init__(detection_conf, tracking_conf)
        self.config = config
    
    def process(self, image, draw=True):
        landmarks = self.find_position(image)
        if not landmarks:
            return image, None
        
        if self.left(landmarks):
            p_indexes = self.config.INDEX_LEFT
        else:
            p_indexes = self.config.INDEX_RIGHT
        
        cur_angle = self.find_angle(landmarks, *p_indexes)

        if draw:
            image = self.draw_angle(image, landmarks, *p_indexes, cur_angle)
        
        return image, cur_angle

