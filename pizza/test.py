from unittest import mock

from kitchen import deliver, pickup, bake
from recipes import Pepperoni, Hawaiian, Margherita


def test_dict():
    pass


def test_equality():
    pepperoni_left = Pepperoni()
    pepperoni_right = Pepperoni()
    hawaiian = Hawaiian()
    some_dict = dict(pepperoni_left)
    assert pepperoni_left == pepperoni_right
    assert pepperoni_left != hawaiian
    assert pepperoni_left != some_dict


def test_description():
    description = Margherita.description()
    assert description == "🧀 Margherita: mozzarella, tomato sauce, tomatoes"


def randint_1(minimum, maximum):
    return 1


def test_log_kitchen(capsys):
    with mock.patch("random.randint", randint_1):
        pepperoni = Pepperoni()
        bake(pepperoni)
        captured = capsys.readouterr()
        assert captured.out == "Приготовили за 1с!\n"
        deliver(pepperoni)
        captured = capsys.readouterr()
        assert captured.out == "Доставили за 1с!\n"
        pickup(pepperoni)
        captured = capsys.readouterr()
        assert captured.out == "Забрали за 1с!\n"
