# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QListWidget, QVBoxLayout, QListWidgetItem, QGridLayout
from qfluentwidgets import FluentIcon as FIF, VerticalSeparator, ListWidget, PushButton, PrimaryPushButton
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentWindow,
                            SubtitleLabel, setFont)

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)


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

        # 创建左侧按钮列表布局
        left_layout = QVBoxLayout()
        left_button1 = PushButton('Button 1', self)
        left_button2 = PushButton('Button 2', self)
        left_button1.clicked.connect(self.on_left_button_clicked)
        left_button2.clicked.connect(self.on_left_button_clicked)
        left_layout.addWidget(left_button1)
        left_layout.addWidget(left_button2)

        # 创建右侧按钮列表布局
        self.right_layout = QVBoxLayout()

        # 将左右两个布局添加到主布局
        main_layout.addLayout(left_layout)
        main_layout.addLayout(self.right_layout)

        self.setLayout(main_layout)

    def on_left_button_clicked(self):
        # 获取点击的按钮文本
        sender_button = self.sender()
        button_text = sender_button.text()

        # 在右侧布局中动态创建新按钮
        new_button = PushButton(f'New Button for {button_text}', self)
        self.right_layout.addWidget(new_button)


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
