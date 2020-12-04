import unittest

import pytest

from morse import decode
from one_hot_encoder import fit_transform

inputs = ((".... . .-.. .-.. ---   .-- --- .-. .-.. -..", "HELLOWORLD"),
          ("... --- ...", "SOS"),
          (".- ...- .. - ---   .- -. .- .-.. -.-- - .. -.-. ...   .- -.-. .- -.. . -- -.--   .---- ..--- ...--",
           "AVITOANALYTICSACADEMY123"))


@pytest.mark.parametrize("input, output", inputs)
def test_decode(input, output):
    assert decode(input) == output


class TestOneHotEncoder(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(TypeError):
            encoded = fit_transform()

    def test_list(self):
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        exp_transformed_cities = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        transformed_cities = fit_transform(cities)
        self.assertEqual(transformed_cities, exp_transformed_cities)

    def test_strings(self):
        exp_transformed_cities = [('Moscow', [0, 0, 1]), ('Москва', [0, 1, 0]), ('Moscou', [1, 0, 0])]
        transformed_cities = fit_transform("Moscow", "Москва", "Moscou")
        self.assertEqual(transformed_cities, exp_transformed_cities)

    def test_repetitions(self):
        repetitions = ["some_string_1"] * 10 + ["some_string_2"] * 20
        transformed = fit_transform(repetitions)
        self.assertTrue(all(len(encoded) == 2 for string, encoded in transformed))


def test_onehot_empty():
    with pytest.raises(TypeError):
        encoded = fit_transform()


def test_onehot_list():
    cities = ['Moscow', 'New York', 'Moscow', 'London']
    exp_transformed_cities = [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]
    transformed_cities = fit_transform(cities)
    assert (transformed_cities == exp_transformed_cities)


def test_onehot_strings():
    exp_transformed_cities = [('Moscow', [0, 0, 1]), ('Москва', [0, 1, 0]), ('Moscou', [1, 0, 0])]
    transformed_cities = fit_transform("Moscow", "Москва", "Moscou")
    assert (transformed_cities == exp_transformed_cities)


def test_onehot_repetitions():
    repetitions = ["some_string_1"] * 10 + ["some_string_2"] * 20
    transformed = fit_transform(repetitions)
    assert (all(len(encoded) == 2 for string, encoded in transformed))
