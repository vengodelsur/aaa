from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict


class PizzaSize(Enum):
    L = "L"
    XL = "L"


@dataclass
class PizzaInfo:
    size: PizzaSize


class PizzaBase:
    tomato_sauce = 200
    mozzarella = 125

    def __init__(self, pizza_info: PizzaInfo):
        self.pizza_info = pizza_info

    def __dict__(self, additional_attributes: Tuple[str] = ("pizza_info",)) -> Dict[str, int]:
        ingredients = {attribute: value for attribute, value in object.__dict__(self).items() if
                       attribute not in additional_attributes}
        return ingredients


class Margherita(PizzaBase):
    tomatoes = 100


class Pepperoni(PizzaBase):
    pepperoni = 90


class Hawaiian(PizzaBase):
    chicken = 90
    pineapples = 80
