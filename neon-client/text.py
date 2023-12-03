from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class DynamicButtonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QHBoxLayout(self)

        # 创建左侧按钮列表布局
        left_layout = QVBoxLayout()
        left_button1 = QPushButton('Button 1', self)
        left_button2 = QPushButton('Button 2', self)
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
        new_button = QPushButton(f'New Button for {button_text}', self)
        self.right_layout.addWidget(new_button)

if __name__ == '__main__':
    app = QApplication([])
    window = DynamicButtonWindow()
    window.show()
    app.exec_()