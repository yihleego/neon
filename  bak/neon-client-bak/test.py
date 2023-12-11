import json
import os.path
import platform
import sys
import threading
import time
import uuid
from ctypes.wintypes import tagPOINT
from functools import partial

from PIL import ImageGrab
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QListWidgetItem, QVBoxLayout
from playwright.sync_api import sync_playwright
from pywinauto import Application
from pywinauto.controls.hwndwrapper import HwndWrapper
from qfluentwidgets import FluentIcon as FIF, PushButton, ListWidget, LineEdit, ImageLabel
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentWindow,
                            SubtitleLabel, setFont)

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

_system = platform.system().lower()
is_linux = _system.find("linux") >= 0
is_windows = _system.find("windows") >= 0
is_mac = _system.find("darwin") >= 0 or _system.find("mac") >= 0

components = [
    {
        "name": "打开网页",
        "group": "WEB",
        "component": "",
    },
    {
        "name": "查找网页元素",
        "group": "WEB",
        "component": "",
    },
    {
        "name": "输入UIA控件",
        "group": "UIA",
        "component": "",
    },
    {
        "name": "点击UIA控件",
        "group": "UIA",
        "component": "",
    },
    {
        "name": "点击CV控件",
        "group": "CV",
        "component": "",
    },
]

workflows = []


class MainWidget(QFrame):
    """
    该窗口左侧为一个列表，右边为一个列表，中间是分隔符
    """

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.recording = False
        self.recording_callback = None

        main_layout = QVBoxLayout(self)

        replay_button = PushButton()
        replay_button.setText("Replay")
        replay_button.clicked.connect(self.on_replay_click)
        main_layout.addWidget(replay_button)

        # 设置窗口标题和大小
        self.setWindowTitle("PySide Splitter Example")
        self.setGeometry(100, 100, 600, 400)
        self.setObjectName(text.replace(' ', '-'))

        body_layout = QHBoxLayout(self)
        self.componentsWidget = ListWidget()
        self.componentsWidget.setMaximumWidth(200)
        for component in components:
            item = QListWidgetItem(component["name"])
            item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
            # item.setData(1, {"idx": len(workflows)})
            self.componentsWidget.addItem(item)

        self.componentsWidget.itemClicked.connect(self.on_left_button_clicked2)  # connect itemClicked to Clicked method

        self.nodesWidget = QWidget()
        self.nodesWidgetLayout = QVBoxLayout(self.nodesWidget)
        self.nodesWidgetLayout.setAlignment(Qt.AlignTop)
        # 将左右两个布局添加到主布局
        body_layout.addWidget(self.componentsWidget)
        body_layout.addWidget(self.nodesWidget)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

    def on_replay_click(self):
        print(workflows)
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        content = None
        for node in workflows:
            ttype = node["type"]
            value = node.get("value")
            if ttype == "打开网页":
                # 创建一个新的浏览器上下文
                context = browser.new_context()
                # 创建一个新的页面
                page = context.new_page()
                # 打开网页
                page.goto(value)
            elif ttype == "查找网页元素":
                content = page.text_content(value["selector"])
            elif ttype == "输入UIA控件":
                handle = int(value["handle"])
                wrapper = HwndWrapper(handle).set_focus()
                wrapper.set_focus()
                wrapper.move_window(0, 0)
                app = Application(backend='uia')
                app.connect(handle=handle)
                main = app.window(class_name="Notepad")
                control = main.child_window(class_name=value["class_name"])
                control.type_keys('^a')
                control.type_keys(content)
            elif ttype == "点击UIA控件":
                name = None
                if "name" in value:
                    name = value["name"]
                control = main.child_window(class_name=value["class_name"], title=name, found_index=0)
                control.click_input()
            elif ttype == "点击CV控件":
                from airtest.core.settings import Settings
                from airtest.core.api import exists, touch, Template, connect_device,click
                Settings.CVSTRATEGY = ['tpl', 'sift', 'brisk']
                Settings.FIND_TIMEOUT = 5
                Settings.FIND_TIMEOUT_TMP = 1
                app = connect_device("Windows:///" + str(handle) + "?foreground=False")
                chats = exists(Template(value["path"]))
                if chats:
                    click(chats)
            time.sleep(0.2)
        p.stop()

    def on_left_button_clicked2(self, item: QListWidgetItem):
        print(item.text())
        print(item.data(1))
        name = item.text()
        idx = len(workflows)
        workflows.append({})

        new_item = QListWidgetItem()
        new_item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        new_item.setData(1, {"key": "test"})

        if item.text() == '打开网页':
            view = QWidget()
            view.setMaximumHeight(50)
            hBoxLayout = QHBoxLayout(view)
            titleLabel = SubtitleLabel(view)
            titleLabel.setText("打开网页")
            # titleLabel.resize(100, 50)
            # titleLabel.setStyleSheet('color:black;')
            lineEdit = LineEdit(view)
            lineEdit.setText('')
            lineEdit.setClearButtonEnabled(True)
            valueLabel = SubtitleLabel(view)
            valueLabel.hide()
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            hBoxLayout.addWidget(valueLabel)
            self.nodesWidgetLayout.addWidget(view)

            def _changed(v):
                print("url", v)
                workflows[idx] = {"type": name, "value": v}

            lineEdit.textChanged.connect(_changed)
        elif item.text() == '查找网页元素':
            view = QWidget()
            view.setMaximumHeight(50)
            hBoxLayout = QHBoxLayout(view)
            titleLabel = SubtitleLabel(view)
            titleLabel.setText("查找网页元素")
            # titleLabel.resize(100, 50)
            # titleLabel.setStyleSheet('color:black;')
            lineEdit = PushButton(view)
            lineEdit.setText('点击这里选择网页元素')
            valueLabel = SubtitleLabel(view)
            valueLabel.hide()
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            hBoxLayout.addWidget(valueLabel)
            self.nodesWidgetLayout.addWidget(view)

            def _clicked(v):
                print("btn", v)
                workflows[idx] = {"type": name, "value": None}
                self.recording = True

                def _callback(v):
                    valueLabel.show()
                    valueLabel.setText(v.get("selector"))
                    workflows[idx]["value"] = v

                self.recording_callback = _callback

            lineEdit.clicked.connect(_clicked)
        elif item.text() == '输入UIA控件':
            view = QWidget()
            view.setMaximumHeight(50)
            hBoxLayout = QHBoxLayout(view)
            titleLabel = SubtitleLabel(view)
            titleLabel.setText("输入UIA控件")
            # titleLabel.resize(100, 50)
            # titleLabel.setStyleSheet('color:black;')
            lineEdit = PushButton(view)
            lineEdit.setText('点击这里选择UIA控件')
            valueLabel = SubtitleLabel(view)
            valueLabel.hide()
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            hBoxLayout.addWidget(valueLabel)
            self.nodesWidgetLayout.addWidget(view)

            def _clicked(v):
                print("btn", v)
                workflows[idx] = {"type": name, "value": None}
                self.recording = True

                def _callback(v):
                    valueLabel.show()
                    valueLabel.setText(v.get("name") + " " + v.get("class_name"))
                    workflows[idx]["value"] = v

                self.recording_callback = _callback

            lineEdit.clicked.connect(_clicked)
        elif item.text() == '点击UIA控件':
            view = QWidget()
            view.setMaximumHeight(50)
            hBoxLayout = QHBoxLayout(view)
            titleLabel = SubtitleLabel(view)
            titleLabel.setText("点击UIA控件")
            # titleLabel.resize(100, 50)
            # titleLabel.setStyleSheet('color:black;')
            lineEdit = PushButton(view)
            lineEdit.setText('点击这里选择UIA控件')
            valueLabel = SubtitleLabel(view)
            valueLabel.hide()
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            hBoxLayout.addWidget(valueLabel)
            self.nodesWidgetLayout.addWidget(view)

            def _clicked(v):
                print("btn", v)
                workflows[idx] = {"type": name, "value": None}
                self.recording = True

                def _callback(v):
                    valueLabel.show()
                    valueLabel.setText(v.get("name") + " " + v.get("class_name"))
                    workflows[idx]["value"] = v

                self.recording_callback = _callback

            lineEdit.clicked.connect(_clicked)
        elif item.text() == '点击CV控件':
            view = QWidget()
            view.setMaximumHeight(50)
            hBoxLayout = QHBoxLayout(view)
            titleLabel = SubtitleLabel(view)
            titleLabel.setText("点击CV控件")
            # titleLabel.resize(100, 50)
            # titleLabel.setStyleSheet('color:black;')
            lineEdit = PushButton(view)
            lineEdit.setText('点击这里进行截图')
            valueLabel = ImageLabel(view)
            valueLabel.hide()
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            hBoxLayout.addWidget(valueLabel)
            self.nodesWidgetLayout.addWidget(view)

            def _clicked(v):
                print("btn", v)
                workflows[idx] = {"type": name, "value": None}
                self.recording = True

                def _callback(v):
                    valueLabel.show()
                    valueLabel.setImage(v.get("path"))
                    # valueLabel.setText(os.path.basename(v.get("path")))
                    workflows[idx]["value"] = v

                self.recording_callback = _callback

            lineEdit.clicked.connect(_clicked)

    def set_browser_info(self, v):
        print("set_browser_info", v)
        if self.recording:
            self.recording = False
            self.recording_callback(v)

    def set_client_info(self, v):
        print("set_client_info", v)
        if self.recording:
            self.recording = False
            self.recording_callback(v)

    def set_screenshot_info(self, v):
        print("set_screenshot_info", v)
        if self.recording:
            self.recording = False
            self.recording_callback(v)

    def on_left_button_clicked(self):
        # 获取点击的按钮文本
        sender_button = self.sender()
        button_text = sender_button.text()

        # 在右侧布局中动态创建新按钮
        new_button = PushButton(button_text, self)
        self.right_layout.addWidget(new_button)

        def _btn():
            if button_text == '打开网页':
                pass

        new_button.clicked.connect(_btn)


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = MainWidget('Home Interface', self)
        self.appInterface = Widget('Application Interface', self)
        # self.videoInterface = Widget('Video Interface', self)
        self.libraryInterface = Widget('library Interface', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        # self.addSubInterface(self.videoInterface, FIF.VIDEO, '视频')

        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', FIF.LIBRARY_FILL, NavigationItemPosition.BOTTOM)
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('RPA IDE')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox('关于', 'RPA开发中', self)
        w.yesButton.setText('确定')
        w.cancelButton.setText('取消')
        if w.exec():
            # QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))
            pass

    def set_browser_info(self, v):
        print("set_browser_info", v)
        self.homeInterface.set_browser_info(v)

    def set_client_info(self, v):
        print("set_client_info", v)
        self.homeInterface.set_client_info(v)

    def set_screenshot_info(self, v):
        print("set_screenshot_info", v)
        self.homeInterface.set_screenshot_info(v)

    def start(self):
        self.show()


from http.server import HTTPServer, SimpleHTTPRequestHandler


class MyRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, win=None, **kwargs):
        self.win = win
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == '/messages':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            parsed_data = json.loads(post_data)

            # 处理你的JSON数据
            print("Received JSON data:", parsed_data)
            self.win.set_browser_info(parsed_data)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write("POST request received".encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")


class API:
    def __init__(self, win):
        self.win = win

    def start(self):
        threading.Thread(
            target=self.run,
            kwargs=dict(host="0.0.0.0", port=18000),
            daemon=True,
        ).start()

    def run(self, host="0.0.0.0", port=18000):
        server_address = (host, port)
        handler = partial(MyRequestHandler, win=self.win)
        httpd = HTTPServer(server_address, handler)
        print(f'Starting server on port {port}')
        httpd.serve_forever()


from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget

_NO_RECT = (0, 0, 0, 0)  # left, top, width, height


class Painter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.rect: tuple[int, int, int, int] = _NO_RECT
        self.message: str = ""
        self.init()

    def init(self):
        screen = QApplication.primaryScreen()
        width, height = screen.size().toTuple()
        self.resize(width, height)
        self.move(screen.availableGeometry().topLeft())
        self.setWindowTitle('RPA Recorder')
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        if is_windows:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Widget | Qt.Tool)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Widget)

    def draw(self, rect: tuple[int, int, int, int], message: str = ""):
        if self.rect == rect and self.message == message:
            return
        self.rect = rect
        self.message = message
        self.update()

    def clear(self):
        self.draw(_NO_RECT)

    def paintEvent(self, event):
        x, y, w, h = self.rect
        if x <= 0 and y <= 0 and w <= 0 and h <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置画笔
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))

        # 绘制方框
        painter.drawRect(x, y, w, h)

        # 绘制文本
        if self.message:
            painter.setBackground(Qt.yellow)
            painter.drawText(x, y - 5, self.message)

    def start(self):
        self.show()


class EventType:
    CLICK = "click"
    DBCLICK = "dbclick"
    MOUSEDOWN = "mousedown"
    MOUSEUP = "mouseup"
    MOUSEMOVE = "mousemove"
    KEYDOWN = "keydown"
    KEYUP = "keyup"


from pynput import mouse, keyboard


class Listener:
    def __init__(self):
        self._keyboard_states: dict[keyboard.Key, bool] = {}  # key -> pressed
        self._mouse_states: dict[mouse.Button, tuple[int, int]] = {}  # key -> position
        self._mouse_position: tuple[int, int] = (0, 0)
        self._listeners: dict[EventType, list] = {
            EventType.CLICK: [],
            EventType.DBCLICK: [],
            EventType.KEYDOWN: [],
            EventType.KEYUP: [],
            EventType.MOUSEDOWN: [],
            EventType.MOUSEUP: [],
            EventType.MOUSEMOVE: [],
        }

    def _on_press(self, key):
        self._keyboard_states[key] = True
        self._trigger(EventType.KEYDOWN, key, self._mouse_position[0], self._mouse_position[1])

    def _on_release(self, key):
        self._trigger(EventType.KEYUP, key, self._mouse_position[0], self._mouse_position[1])
        self._keyboard_states[key] = False

    def _on_click(self, x, y, button, pressed):
        if pressed:
            self._mouse_states[button] = (x, y)
            self._trigger(EventType.MOUSEDOWN, button, x, y)
        else:
            self._trigger(EventType.MOUSEUP, button, x, y)
            self._trigger(EventType.CLICK, button, x, y)
            self._mouse_states[button] = None

            # print(_keyboard_states)
            # print(_mouse_states)

    def _on_move(self, x, y):
        _position = (x, y)
        self._trigger(EventType.MOUSEMOVE, None, x, y)

    def _trigger(self, event, *args):
        listeners = self._listeners[event]
        for keys, func in listeners:
            # print('keys', keys)
            ok = True
            for key in keys:
                if isinstance(key, keyboard.Key):
                    if not self._keyboard_states.get(key):
                        ok = False
                        break
                elif isinstance(key, mouse.Button):
                    if not self._mouse_states.get(key):
                        ok = False
                        break
                else:
                    ok = False
                    break
            if ok:
                func(*args)

    def _run(self):
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as k_listener, \
                mouse.Listener(on_click=self._on_click, on_move=self._on_move) as m_listener:
            k_listener.join()
            m_listener.join()

    def listen(self, event, keys, func):
        self._listeners[event].append((keys, func))

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()


def on_event(l, r, w):
    if not is_windows:
        return

    def get_process_name_by_pid(pid):
        import psutil
        try:
            process = psutil.Process(pid)
            return process.name()
        except psutil.NoSuchProcess as e:
            return f"Process with PID {pid} not found"
        except psutil.AccessDenied as e:
            return f"Access denied to process with PID {pid}"

    def detect(_, x, y):
        import pywinauto
        elem = pywinauto.uia_defines.IUIA().iuia.ElementFromPoint(tagPOINT(x, y))
        element = pywinauto.uia_element_info.UIAElementInfo(elem)
        target = element
        name = target.name
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

        w.set_client_info({
            "name": name,
            "automation_id": automation_id,
            "class_name": class_name,
            "control_id": control_id,
            "control_type": control_type,
            "rectangle": rectangle,
            "handle": handle,
            "process_id": process_id,
            "process_name": process_name,
        })

        skips = ["chrome", "msedge"]
        for s in skips:
            if process_name.find(s) >= 0:
                return

        r.draw((int(rectangle.left), int(rectangle.top), int(rectangle.right - rectangle.left), int(rectangle.bottom - rectangle.top)), msg)

    def screenshot(_, x, y):
        import pywinauto
        elem = pywinauto.uia_defines.IUIA().iuia.ElementFromPoint(tagPOINT(x, y))
        element = pywinauto.uia_element_info.UIAElementInfo(elem)
        target = element
        rectangle = target.rectangle
        region = (rectangle.left, rectangle.top, rectangle.right, rectangle.bottom)
        # 获取屏幕截图
        screenshot_ = ImageGrab.grab(bbox=region)
        # 保存截图
        abspath = os.path.abspath(f"./screenshot/{str(uuid.uuid4())}.png")
        screenshot_.save(abspath)

        w.set_screenshot_info({
            "path": abspath
        })

    # listener.listen(listener.EventType.CLICK, [mouse.Button.left, keyboard.Key.ctrl_l], on_click)
    l.listen(EventType.MOUSEMOVE, [keyboard.Key.ctrl_l], detect)
    l.listen(EventType.MOUSEUP, [keyboard.Key.alt_l], screenshot)


if __name__ == '__main__':
    win = MainWindow()
    api = API(win)
    ptr = Painter(win)
    ltn = Listener()
    on_event(ltn, ptr, win)
    ltn.start()
    api.start()
    ptr.start()
    win.start()
    sys.exit(app.exec())
