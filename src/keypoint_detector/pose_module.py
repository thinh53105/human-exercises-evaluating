import math

import cv2
import mediapipe as mp


class PoseDetector:

    def __init__(self, detection_conf=0.5, tracking_conf=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
    
    def find_position(self, image):
        landmarks = []
        results = self.pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))
        return landmarks
    
    def find_angle(self, landmarks, p_index_1, p_index_2, p_index_3):
        x1, y1 = landmarks[p_index_1]
        x2, y2 = landmarks[p_index_2]
        x3, y3 = landmarks[p_index_3]

        a = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        b = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
        c = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)

        try:
            angle = math.degrees(math.acos((a**2 + b**2 - c**2) / (2*a*b)))
        except:
            angle = 180

        return angle
    
    def draw_angle(self, image, landmarks, p_index_1, p_index_2, p_index_3, angle):
        x1, y1 = landmarks[p_index_1]
        x2, y2 = landmarks[p_index_2]
        x3, y3 = landmarks[p_index_3]

        image = cv2.circle(image, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
        image = cv2.circle(image, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        image = cv2.circle(image, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
        image = cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 3)
        image = cv2.line(image, (x2, y2), (x3, y3), (255, 255, 255), 3)
        image = cv2.putText(image, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return image

    def left(self, landmarks):
        return landmarks[2] < landmarks[28]
    
    def process(self, image, draw=True):
        return None, None
