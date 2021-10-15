import yaml
from PyQt5.QtWidgets import QLabel,  QMainWindow, QPushButton
import os


class ShopWindow(QMainWindow):

    def __init__(self, data_path='', buttons_data=None):
        super().__init__()

        self.buttons = dict()
        self.counter = dict()
        self.data_geometry = list()

        with open(os.path.join(data_path, 'data/data_name.yml'), 'r') as file:
            self.setWindowTitle(yaml.safe_load(file))

        with open(os.path.join(data_path, 'data/data_geometry.yml'), 'r') as file:
            self.data_geometry = yaml.safe_load(file)

        if buttons_data is not None:
            self.buttons_data = buttons_data
        else:
            with open('data/data.yml', 'r') as file:
                self.buttons_data = yaml.safe_load(file)

        for key in self.buttons_data.keys():
            cur_btn = QPushButton(key, self)
            self.buttons[cur_btn] = key
            cur_btn.setGeometry(*self.buttons_data[key][0])
            cur_btn.clicked.connect(self.on_click)
            self.counter[cur_btn] = self.buttons_data[key][1]

        self.label_update(True)

        # # это константа
        self.label.setGeometry(*self.data_geometry[0])

        # это тоже константа
        self.resize(*self.data_geometry[1])

    def on_click(self):
        self.counter[self.sender()] -= 1
        if self.counter[self.sender()] == 0:
             self.sender().setEnabled(False)
        self.label_update()

    def label_update(self, first_time=False):
        label_text = "В магазине осталось:\n"
        for key, value in self.counter.items():
            label_text += "{} : {} штук\n".format(self.buttons[key], value)
        if first_time:
            self.label = QLabel(label_text, self)
        else:
            self.label.setText(label_text)