from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
from enum import Enum


# Assumes range on axes is -100 to 100
class ButtonWidget(QWidget):
    def __init__(self, text: str=''):
        super().__init__()
        self.pixmap_on = QPixmap(os.path.join('images', 'on-16.png'))
        self.pixmap_off = QPixmap(os.path.join('images', 'off-16.png'))
        self.state = False
        self.name_label = QLabel(self)
        self.indicator_label = QLabel(self)
        # Set label text
        self.setLabel(text)
        # set default state to off
        self.setState(False)

        self.init_ui()

    def init_ui(self):
        vbox_layout = QVBoxLayout()

        self.name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.name_label.setAlignment(Qt.AlignCenter)

        vbox_layout.addWidget(self.name_label)
        vbox_layout.addWidget(self.indicator_label)
        self.setLayout(vbox_layout)

    def setState(self, state: bool):
        if state:
            self.indicator_label.setPixmap(self.pixmap_on)
        else:
            self.indicator_label.setPixmap(self.pixmap_off)

    def setLabel(self, text: str):
        self.name_label.setText(text)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setApplicationName("ButtonWidget")
#     window = ButtonWidget()
#     app.exec_()
