import platform
import sys
import threading
from ctypes.wintypes import tagPOINT
from http import HTTPStatus

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget
from flask import Flask, request
from pynput import mouse, keyboard

_system = platform.system().lower()
is_linux = _system.find("linux") >= 0
is_windows = _system.find("windows") >= 0
is_mac = _system.find("darwin") >= 0 or _system.find("mac") >= 0


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x, self.y, self.width, self.height = 0, 0, 0, 0
        self.message = ""

    def initUI(self):
        screen = QApplication.primaryScreen()
        width, height = screen.size().toTuple()
        self.resize(width, height)
        self.move(screen.availableGeometry().topLeft())
        self.setWindowTitle('RPA')
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def setData(self, x, y, width, height, message):
        if self.x == x and self.y == y and self.width == width and self.height == height and self.message == message:
            return
        self.x, self.y, self.width, self.height = x, y, width, height
        self.message = message
        self.update()

    def clearData(self):
        self.x, self.y, self.width, self.height = 0, 0, 0, 0
        self.update()

    def paintEvent(self, event):
        if not self.x and not self.y and not self.width and not self.height:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置画笔
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        painter.setPen(pen)

        # 设置画刷
        # brush = QBrush(Qt.green, Qt.SolidPattern)
        # painter.setBrush(brush)

        # 绘制方框
        painter.drawRect(self.x, self.y, self.width, self.height)
        # painter.drawLine(self.x, self.y, self.width, self.height)

        if self.message:
            painter.setBackground(Qt.yellow)
            painter.drawText(self.x, self.y - 5, self.message)


app = Flask(__name__)

qapp = QApplication(sys.argv)
window = MyWidget()

ctrl_pressed = False


def get_process_name_by_pid(pid):
    import psutil
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess as e:
        return f"Process with PID {pid} not found"
    except psutil.AccessDenied as e:
        return f"Access denied to process with PID {pid}"


def on_press(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True


def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
    if key == keyboard.Key.esc:
        window.clearData()


def on_click(x, y, button, pressed):
    import pywinauto
    global ctrl_pressed
    if pressed:
        return
    # released only
    if (button == mouse.Button.left and ctrl_pressed) or button == mouse.Button.middle:
        elem = pywinauto.uia_defines.IUIA().iuia.ElementFromPoint(tagPOINT(x, y))
        element = pywinauto.uia_element_info.UIAElementInfo(elem)
        target = element
        automation_id = target.automation_id
        class_name = target.class_name
        control_id = target.control_id
        control_type = target.control_type
        rectangle = target.rectangle

        while not target.handle or not target.process_id:
            target = target.parent
        handle = target.handle
        process_id = target.process_id
        process_name = ""
        if process_id:
            process_name = get_process_name_by_pid(process_id)

        msg = f"handle: {handle}, process_id: {process_id}, process_name: {process_name}, automation_id: {automation_id}, class_name: {class_name}, control_id: {control_id}, control_type: {control_type}, rectangle: {rectangle}"
        print(msg)

        skips = ["chrome", "msedge"]
        for s in skips:
            if process_name.find(s) >= 0:
                return

        window.setData(int(rectangle.left), int(rectangle.top), int(rectangle.right - rectangle.left), int(rectangle.bottom - rectangle.top), msg)


def listen():
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
            mouse.Listener(on_click=on_click) as m_listener:
        k_listener.join()
        m_listener.join()


@app.get("/")
def index():
    return ""


@app.get("/ping")
def ping():
    return "ok"


@app.post("/messages")
def messages():
    body = request.json
    message = body["message"]
    position = body["position"]
    size = body["size"]
    print('message', message[:message.index(">") + 1])
    print('position', position)
    print('size', size)
    print()
    window.setData(
        int(body["position"]["x"]),
        int(body["position"]["y"]),
        int(body["size"]["width"]),
        int(body["size"]["height"]),
        message[:message.index(">") + 1])
    return {}, HTTPStatus.OK


@app.after_request
def after_request(res):
    # CORS
    h = res.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "*"
    h["Access-Control-Allow-Methods"] = "*"
    return res


def start_api():
    threading.Thread(
        target=app.run,
        kwargs=dict(host="0.0.0.0", port=18000),
        daemon=True,
    ).start()


def start_listen():
    if not is_windows:
        return
    threading.Thread(
        target=listen,
        daemon=True,
    ).start()


if __name__ == '__main__':
    window.show()
    start_api()
    start_listen()
    sys.exit(qapp.exec_())
