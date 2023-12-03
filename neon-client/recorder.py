from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget

_NO_RECT = (0, 0, 0, 0)  # left, top, width, height


class Recorder(QWidget):
    def __init__(self):
        super().__init__()
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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

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
