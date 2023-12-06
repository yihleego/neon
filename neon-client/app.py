# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QListWidgetItem, QWidget, QVBoxLayout
from qfluentwidgets import FluentIcon as FIF, PushButton, ListWidget, LineEdit
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentWindow,
                            SubtitleLabel, setFont)

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# pipeline
# handler

# workflow
# node

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
]

workflows = []

recording = False
browser_info = None
client_info = None


class MainWidget(QFrame):
    """
    该窗口左侧为一个列表，右边为一个列表，中间是分隔符
    """

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        # 设置窗口标题和大小
        self.setWindowTitle("PySide Splitter Example")
        self.setGeometry(100, 100, 600, 400)
        self.setObjectName(text.replace(' ', '-'))

        main_layout = QHBoxLayout(self)
        self.componentsWidget = ListWidget()
        self.componentsWidget.setMaximumWidth(200)
        for component in components:
            item = QListWidgetItem(component["name"])
            item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
            item.setData(1, {"idx": len(workflows)})
            self.componentsWidget.addItem(item)
            workflows.append({})

        self.componentsWidget.itemClicked.connect(self.on_left_button_clicked2)  # connect itemClicked to Clicked method

        self.nodesWidget = QWidget()
        self.nodesWidgetLayout = QVBoxLayout(self.nodesWidget)
        self.nodesWidgetLayout.setAlignment(Qt.AlignTop)
        # 将左右两个布局添加到主布局
        main_layout.addWidget(self.componentsWidget)
        main_layout.addWidget(self.nodesWidget)

        self.setLayout(main_layout)

    def on_left_button_clicked2(self, item: QListWidgetItem):
        print(item.text())
        print(item.data(1))
        name = item.text()
        data = item.data(1)
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
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            self.nodesWidgetLayout.addWidget(view)

            def _changed(v):
                print("url", v)
                workflows[data["idx"]] = {"type": name, "value": v}

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
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            self.nodesWidgetLayout.addWidget(view)

            def _clicked(v):
                recording = True
                print("btn", v)
                workflows[data["idx"]] = {"type": name, "value": v}

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
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            self.nodesWidgetLayout.addWidget(view)
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
            hBoxLayout.addWidget(titleLabel)
            hBoxLayout.addWidget(lineEdit)
            self.nodesWidgetLayout.addWidget(view)

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


def run():
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
