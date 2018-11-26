from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QColor, QPainter
import sys


# Assumes range on axes is -100 to 100
class AxesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.value = (0, 0)

    def init_ui(self):
        self.setMinimumSize(120, 120)
        self.setMaximumSize(120, 120)

    def set_x_value(self, x):
        self.value = (x, self.value[1])

    def set_y_value(self, y):
        self.value = (self.value[0], y)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        h = size.height()
        # step = int(round(h / 200))
        qp.setPen(QColor(255, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        x = self.value[0] / 2 + 60
        y = self.value[1] / 2 + 60
        qp.drawEllipse(x, y, 7, 7)
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0, 0))
        qp.drawRect(9, 9, h - 11, h - 11)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setApplicationName("AxesWidget")
#     window = AxesWidget()
#     app.exec_()
