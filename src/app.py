import cv2
import numpy as np

from ui.ui_drawer import UIDrawer

ui = UIDrawer()

while True:
    ui.update_ui()
    bg = ui.get_ui()

    cv2.imshow("Push-up Recognition", bg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()