import pytest
from PyQt5 import QtCore
from lib.window import ShopWindow
from copy import deepcopy

@pytest.fixture
def data():
    return {'Леденцы со вкусом мяты': [[20, 150, 210, 80], 10],
            'Леденцы со вкусом арбуза': [[220, 150, 210, 80], 200],
            'Леденцы со вкусом дыни': [[420, 150, 210, 80], 45],
            'Леденцы со вкусом огурца': [[620, 150, 210, 80], 9],
            'Леденцы со вкусом лакрицы': [[820, 150, 210, 80], 1]}


def gen_label_text(data_dict):
    label_text = "В магазине осталось:\n"
    for key, value in data_dict.items():
        label_text += "{} : {} штук\n".format(key, data_dict[key][1])
    return label_text


def test_buttons_cnt_text(qtbot, data):
    window = ShopWindow(data_path='..', buttons_data=data)
    assert len(window.buttons) == len(data)  #проверяем количество кнопок
    assert sorted(window.buttons.values()) == sorted(data.keys()) #проверяем тексты кнопок
    label_text = "В магазине осталось:\n"
    for key, value in data.items():
        label_text += "{} : {} штук\n".format(key, value[1])
    assert label_text == window.label.text() #проверяем изначальное количество товара


def test_geometry(qtbot, data):
    window = ShopWindow(data_path='..', buttons_data=data)
    for key in window.buttons:
        assert key.geometry() == QtCore.QRect(*data[window.buttons[key]][0])


def test_buttons_behavior(qtbot, data):
    window = ShopWindow(data_path='..', buttons_data=data)
    k = 0
    clicks = [3, 0, 0, 8, 0]
    for key in window.buttons.keys():
        for i in range(clicks[k]):
            qtbot.mouseClick(key, QtCore.Qt.LeftButton)
        k += 1
    new_data = deepcopy(data)
    new_data['Леденцы со вкусом мяты'][1] -= 3
    new_data['Леденцы со вкусом огурца'][1] -= 8
    assert gen_label_text(new_data) == window.label.text()
    for key in window.buttons:
        assert key.isEnabled()
    new_data['Леденцы со вкусом огурца'][1] -= 1
    new_data['Леденцы со вкусом лакрицы'][1] -= 1
    array_buttons = list(window.buttons.keys())
    qtbot.mouseClick(array_buttons[-2], QtCore.Qt.LeftButton)
    qtbot.mouseClick(array_buttons[-1], QtCore.Qt.LeftButton)
    assert gen_label_text(new_data) == window.label.text()
    for i in range(len(array_buttons)):
        if i < len(array_buttons) - 2:
            assert array_buttons[i].isEnabled()
        else:
            assert not array_buttons[i].isEnabled()
    for i in range(1337):
        qtbot.mouseClick(array_buttons[-1], QtCore.Qt.LeftButton)
    assert gen_label_text(new_data) == window.label.text()


def test_full(qtbot, data):
    window = ShopWindow(data_path='..', buttons_data=data)
    for key in window.buttons.keys():
        for i in range(228):
            qtbot.mouseClick(key, QtCore.Qt.LeftButton)
        assert not key.isEnabled()
