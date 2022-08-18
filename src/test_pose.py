from keypoint_detector.exercises_module import PushupsKeypointsDetector

import time
import cv2
import numpy as np

cap = cv2.VideoCapture('src/sample_videos/test1.mp4')
p_time = 0

detector = PushupsKeypointsDetector()

pred_times = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    t1 = time.time()
    frame, _ = detector.process(frame)
    c_time = time.time()
    pred_times.append(c_time-t1)
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print(np.average(pred_times))
print('Test')