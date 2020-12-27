from unittest import mock

from click.testing import CliRunner

from interface import menu, order
from kitchen import deliver, pickup, bake
from recipes import Pepperoni, Hawaiian, Margherita


def randint_1(minimum, maximum):
    return 1


def test_dict():
    hawaiian = Hawaiian()
    assert dict(hawaiian) == {
        "chicken": 90,
        "mozzarella": 125,
        "pineapples": 80,
        "tomato_sauce": 200,
    }


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


def test_menu():
    expected_output = (
        "🧀 Margherita: mozzarella, tomato sauce, tomatoes\n"
        "🍕 Pepperoni: mozzarella, pepperoni, tomato sauce\n"
        "🍍 Hawaiian: chicken, mozzarella, pineapples, tomato sauce\n"
    )
    runner = CliRunner()
    result = runner.invoke(menu)
    assert result.exit_code == 0
    assert result.output == expected_output


def test_order_with_delivery():
    expected_output = "Приготовили за 1с!\n" "Доставили за 1с!\n"
    with mock.patch("random.randint", randint_1):
        runner = CliRunner()
        result = runner.invoke(order, ["pepperoni", "--delivery"])
        assert result.exit_code == 0
        assert result.output == expected_output


def test_order_without_delivery():
    expected_output = "Приготовили за 1с!\n" "Забрали за 1с!\n"
    with mock.patch("random.randint", randint_1):
        runner = CliRunner()
        result = runner.invoke(order, ["hawaiian"])
        assert result.exit_code == 0
        assert result.output == expected_output


def test_incorrect_order():
    with mock.patch("random.randint", randint_1):
        expected_output = "No pizza called meowgarita🐱, use menu command to see available pizzas\n"
        runner = CliRunner()
        result = runner.invoke(order, ["meowgarita🐱"])
        assert result.exit_code == 0
        assert result.output == expected_output
