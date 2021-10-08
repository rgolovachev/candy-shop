import pytest

@pytest.fixture
def data():
    return {1: 2, 3: 4}


def test_data_values(qtbot, data):
    # data[1] = 4
    assert data[1] != data[3]
    data[5] = 6


def test_len_data(data):
    print(data)
    assert 2 == len(data)