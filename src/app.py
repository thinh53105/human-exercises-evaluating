import cv2

from ui.drawer.ui_drawer import UIDrawer

ui = UIDrawer()


def mouse_click(event, x, y, flags, param):
    global ui
    btns_pool = ui.get_btns_pool()

    # mouse hover
    btns_pool.handle_mouse_hover(x, y)

    # mouse clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        btns_pool.handle_mouse_clicked(x, y)


cv2.namedWindow("Human Exercises Evaluating")
cv2.setMouseCallback("Human Exercises Evaluating", mouse_click)

while True:
    ui.update_ui()
    bg = ui.get_ui()

    cv2.imshow("Human Exercises Evaluating", bg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ui.btn_stop_action()
        break

cv2.destroyAllWindows()