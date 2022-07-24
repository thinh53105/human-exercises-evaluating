from .pose_module import PoseDetector


class PushupsKeypointsDetector(PoseDetector):

    def __init__(self, detection_conf=0.5, tracking_conf=0.5):
        super().__init__(detection_conf, tracking_conf)
    
    def process(self, image, draw=True):
        landmarks = self.find_position(image)
        if not landmarks:
            return image, None
        
        if self.left(landmarks):
            p_indexes = (11, 13, 15)
        else:
            p_indexes = (12, 14, 16)
        
        cur_angle = self.find_angle(landmarks, *p_indexes)

        if draw:
            image = self.draw_angle(image, landmarks, *p_indexes, cur_angle)
        
        return image, cur_angle
