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

    def test_repeated(self):
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        exp_transformed_cities = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        transformed_cities = fit_transform(cities)
        self.assertEqual(transformed_cities, exp_transformed_cities)

