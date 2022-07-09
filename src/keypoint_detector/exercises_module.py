from .pose_module import PoseDetector


class PushupsKeypointsDetector(PoseDetector):

    def __init__(self, detection_conf=0.5, tracking_conf=0.5):
        super().__init__(detection_conf, tracking_conf)
    
    def process(self, image, draw=True):
        landmarks = self.find_position(image)
        if not landmarks:
            return image, None
        
        if self.left(landmarks):
            p_indexes = (12, 14, 16)
        else:
            p_indexes = (11, 13, 15)
        
        cur_angle = self.find_angle(landmarks, *p_indexes)

        if draw:
            image = self.draw_angle(image, landmarks, *p_indexes, cur_angle)
        
        return image, cur_angle


def main():
    import time
    import cv2

    cap = cv2.VideoCapture(0)
    p_time = 0

    detector = PushupsKeypointsDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, _ = detector.process(frame)
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()