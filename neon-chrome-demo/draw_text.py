from PyQt5.QtGui import (QPainter,
                         QPen,
                         QColor)
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication)
from PyQt5.QtCore import (Qt,
                          QCoreApplication,
                          QTimer)


class TransparentWindow(QMainWindow):

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            pen_color: str,
            pen_size: int):
        super().__init__()
        self.highlight_x = x
        self.highlight_y = y
        self.highlight_width = width
        self.highlight_height = height
        self.pen_color = pen_color
        self.pen_size = pen_size
        self.initUI()

    def initUI(self):
        """Initialize the user interface of the window."""
        self.setGeometry(
            self.highlight_x,
            self.highlight_y,
            self.highlight_width + self.pen_size,
            self.highlight_height + self.pen_size)
        self.setStyleSheet('background: transparent')
        self.setWindowFlag(Qt.FramelessWindowHint)

    def paintEvent(self, event):
        """Paint the user interface."""
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(QColor(self.pen_color), self.pen_size))
        painter.drawRect(
            self.pen_size - 1,
            self.pen_size - 1,
            self.width() - 2 * self.pen_size,
            self. height() - 2 * self.pen_size)
        painter.end()


def highlight_on_screen(
        x: int,
        y: int,
        width: int,
        height: int,
        pen_color: str = '#aaaa00',
        pen_size: int = 2,
        timeout: int = 20):
    """Highlights an area as a rectangle on the main screen.

        `x` x position of the rectangle

        `y` y position of the rectangle

        `width` width of the rectangle

        `height` height of the rectangle

        `pen_color` Optional: color of the rectangle as a hex value;
                              defaults to `#aaaa00`

        `pen_size` Optional: border size of the rectangle; defaults to 2

        `timeout` Optional: time in seconds the rectangle
                            disappears; defaults to 2 seconds
        """
    app = QApplication([])
    window = TransparentWindow(x, y, width, height, pen_color, pen_size)
    window.show()
    QTimer.singleShot(timeout * 1000, QCoreApplication.quit)
    app.exec_()


highlight_on_screen(0, 0, 100, 100)