import cv2
import numpy as np

from ui.ui_drawer import UIDrawer

ui = UIDrawer()


def mouse_click(event, x, y, flags, param):
    global ui
    btn_list = ui.get_btn_list()

    # mouse hover
    for btn in btn_list:
        if btn.mouse_focus(x, y) and btn.get_state() != 'clicked':
            btn.set_state('hover')
        elif btn.get_state() == 'hover':
            btn.set_state('normal')

    # mouse clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        for btn in btn_list:
            if btn.mouse_focus(x, y):
                ui.reset_btn()
                btn.set_state('clicked')
                btn.call_func()
                ui.reset_btn()


cv2.namedWindow("Push-up Recognition")
cv2.setMouseCallback("Push-up Recognition", mouse_click)

while True:
    ui.update_ui()
    bg = ui.get_ui()

    cv2.imshow("Push-up Recognition", bg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()