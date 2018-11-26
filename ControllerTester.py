
# http://zetcode.com/gui/pyqt5/
# http://zetcode.com/gui/pyqt5/layout/

# Requires: pygame, pyserial, pyqt5

import sys
import pygame
from pygame.locals import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from AxesWidget import AxesWidget
from ButtonWidget import ButtonWidget
# import serial
# from serial.tools.list_ports import comports


class ControllerTester(QWidget):
    def __init__(self):
        super().__init__()
        pygame.init()

        # Set up the joystick
        pygame.joystick.init()

        self.my_joystick = None
        self.joystick_list = []
        self.num_axes = 0
        self.num_buttons = 0
        self.num_hats = 0

        self.g_keys = None

        # self.ser = serial.Serial()
        # self.ser.baudrate = 9600
        # self.ser.port = 'COM3'
        # # Get list of available ports
        # ports = comports()
        # for p in ports:
        #     print(p)

        self.update_numbered_list_of_controllers()
        # By default, load the first available joystick.
        if len(self.joystick_list) > 0:
            self.connect_to_controller(0)

        self.__timer_init = QTimer()
        self.__timer_init.timeout.connect(self.poll_controller)
        self.__timer_init.setSingleShot(False)
        self.__timer_init.start(10)

        self.button_array = []
        self.axes_sliders_array = []
        self.axes_widget_array = []
        self.hat_array = []
        self.control_layout = None
        self.main_layout = QVBoxLayout()
        self.initUI()

    def update_numbered_list_of_controllers(self):
        # Enumerate joysticks
        self.joystick_list.clear()
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_list.append((i, pygame.joystick.Joystick(i).get_name()))
        print(self.joystick_list)

    def initUI(self):
        hbox_cont_select = QHBoxLayout()
        cb_controllers = QComboBox()
        for item in self.joystick_list:
            cb_controllers.addItem(item[1])
            hbox_cont_select.addWidget(cb_controllers)
        cb_controllers.currentIndexChanged.connect(self.selection_change)

        # Add main layout
        # Add Controller ComboBox
        self.main_layout.addLayout(hbox_cont_select)
        # self.setGeometry(300, 300, 300, 150)
        self.setLayout(self.main_layout)
        # Qt show window
        self.show()

        self.control_layout = self.create_controller_layout()
        self.main_layout.addLayout(self.control_layout)
        # self.main_layout.addStretch(1)

    def create_controller_layout(self):
        # Add controller specific widgets
        controller_vbox_layout = QVBoxLayout()
        if self.my_joystick:
            # Test if any axes exist
            if self.num_axes >= 1:
                # Layout for axes display
                vbox_axes_sliders = QVBoxLayout()
                vbox_axes_sliders.addStretch(1)
                label_axes = QLabel(self)
                label_axes.setText('Axes')
                vbox_axes_sliders.addWidget(label_axes)
                hbox_axes_plot = QHBoxLayout()

                num_axes_is_odd = (self.num_axes % 2) == 1
                axis_num = 1
                for i in range(0, int(self.num_axes/2)):
                    name = 'Axis' + str(axis_num)
                    slider = QSlider(Qt.Horizontal, self)
                    slider.setRange(-100.0, 100.0)
                    self.axes_sliders_array.append(slider)
                    label = QLabel(self)
                    label.setText(name + '-X')
                    vbox_axes_sliders.addWidget(label)
                    vbox_axes_sliders.addWidget(slider)

                    slider = QSlider(Qt.Horizontal, self)
                    slider.setRange(-100.0, 100.0)
                    self.axes_sliders_array.append(slider)
                    label = QLabel(self)
                    label.setText(name + '-Y')
                    vbox_axes_sliders.addWidget(label)
                    vbox_axes_sliders.addWidget(slider)

                    self.axes_widget_array.append(AxesWidget())

                    vbox = QVBoxLayout()
                    axes_label = QLabel(self)
                    axes_label.setText(name)
                    axes_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    axes_label.setAlignment(Qt.AlignCenter)
                    vbox.addWidget(axes_label)
                    self.axes_sliders_array[-2].valueChanged[int].connect(self.axes_widget_array[-1].set_x_value)
                    self.axes_sliders_array[-1].valueChanged[int].connect(self.axes_widget_array[-1].set_y_value)
                    vbox.addWidget(self.axes_widget_array[-1])
                    hbox_axes_plot.addLayout(vbox)

                    axis_num += 1

                if num_axes_is_odd:
                    name = 'Axis' + str(axis_num)
                    slider = QSlider(Qt.Horizontal, self)
                    slider.setRange(-100.0, 100.0)
                    self.axes_sliders_array.append(slider)
                    label = QLabel(self)
                    label.setText(name)
                    vbox_axes_sliders.addWidget(label)
                    vbox_axes_sliders.addWidget(slider)

                    self.axes_widget_array.append(AxesWidget())

                    vbox = QVBoxLayout()
                    axes_label = QLabel(self)
                    axes_label.setText(name)
                    axes_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    axes_label.setAlignment(Qt.AlignCenter)
                    vbox.addWidget(axes_label)
                    self.axes_sliders_array[-1].valueChanged[int].connect(self.axes_widget_array[-1].set_x_value)
                    vbox.addWidget(self.axes_widget_array[-1])
                    hbox_axes_plot.addLayout(vbox)

                # Add axes plot widgets after all sliders
                vbox_axes_sliders.addLayout(hbox_axes_plot)
                controller_vbox_layout.addLayout(vbox_axes_sliders)

            if self.num_buttons > 0:
                # Layout for button checkboxes
                label_buttons = QLabel(self)
                label_buttons.setText('Buttons')
                hbox_label = QHBoxLayout()
                hbox_label.addWidget(label_buttons)
                hbox_buttons = QHBoxLayout()
                hbox_buttons.addStretch(1)
                for i in range(0, self.num_buttons):
                    cb = ButtonWidget(str(i))
                    self.button_array.append(cb)
                    # cb.setEnabled(False)
                    cb.setState(False)
                    hbox_buttons.addWidget(cb)

                controller_vbox_layout.addLayout(hbox_label)
                controller_vbox_layout.addLayout(hbox_buttons)

            if self.num_hats > 0:
                # Layout for D-pad
                label_dpad = QLabel(self)
                label_dpad.setText('D-Pad')
                hbox_label = QHBoxLayout()
                hbox_label.addWidget(label_dpad)
                hbox_dpad = QHBoxLayout()
                for i in range(0, self.num_hats):
                    lbl_2 = QLabel(self)
                    self.hat_array.append(lbl_2)
                    lbl_2.setText(str(self.my_joystick.get_hat(i)))
                    hbox_dpad.addWidget(lbl_2)

                controller_vbox_layout.addLayout(hbox_label)
                controller_vbox_layout.addLayout(hbox_dpad)

        controller_vbox_layout.addStretch(1)
        # self.main_layout.addLayout(self.controller_vbox_layout)
        return controller_vbox_layout

    def remove_control_layout(self):
        def delete_items(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        delete_items(item.layout())

        delete_items(self.control_layout)
        self.button_array = []
        self.axes_sliders_array = []
        self.axes_widget_array = []
        self.hat_array = []
        self.control_layout = None

    def poll_controller(self):
        g_keys = pygame.event.get()
        for event in g_keys:
            if event.type == JOYAXISMOTION or JOYBALLMOTION or JOYBUTTONDOWN or JOYBUTTONUP or JOYHATMOTION:
                values = []
                if self.my_joystick:
                    for i in range(0, self.num_axes):
                        ax_value = self.my_joystick.get_axis(i)
                        values.append(ax_value)
                        self.axes_sliders_array[i].setValue(ax_value * 100)

                    for i in range(0, self.num_buttons):
                        state = self.my_joystick.get_button(i) == 1
                        values.append(state)
                        self.button_array[i].setState(state)

                    for i in range(0, self.num_hats):
                        state = self.my_joystick.get_hat(i)
                        values.append(state)
                        self.hat_array[i].setText(str(state))

                    for w in self.axes_widget_array:
                        w.repaint()

                    print(values)

    def quit(self):
        if self.my_joystick.get_init():
            self.my_joystick.quit()
        self.__timer_init.stop()
        pygame.quit()

    # Overrides
    def closeEvent(self, event):
        # do stuff
        self.quit()
        event.accept()  # let the window close

    def selection_change(self, index):
        """

        :param index: selection index, 0 based
        :return:
        """
        print("Items selection changed to:", self.joystick_list[index])
        # Remove controller widgets
        self.remove_control_layout()
        # Connect to selected controller - disconnect from previous
        self.connect_to_controller(index)
        # Create widgets for new controller
        self.control_layout = self.create_controller_layout()
        self.main_layout.addLayout(self.control_layout)

    def connect_to_controller(self, index: int):
        """

        :param index: 0-based combo box selection index
        :return:
        """
        # Disconnect from controller
        if self.my_joystick:
            self.my_joystick.quit()
        try:
            if len(self.joystick_list) > index:
                self.my_joystick = pygame.joystick.Joystick(index)
                self.my_joystick.init()
                self.num_axes = self.my_joystick.get_numaxes()
                self.num_buttons = self.my_joystick.get_numbuttons()
                self.num_hats = self.my_joystick.get_numhats()
                print('Found', self.num_axes, 'axes')
                print('Found', self.num_buttons, 'buttons')
                print('Found', self.num_hats, 'pov controllers')

                if self.num_axes % 2 != 0:
                    # raise ValueError('Expected pairs of axes, got ' + str(num_axes))
                    self.num_axes = self.num_axes
            else:
                print("Invalid index specified:", index)
        except Exception:
            print("Exception while connecting to controller", index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Controller Tester")
    window = ControllerTester()
    app.exec_()
