from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Generator


class PizzaSize(Enum):
    L = "L"
    XL = "L"


@dataclass
class PizzaInfo:
    size: PizzaSize


class PizzaBase:
    NON_INGREDIENTS_ATTRIBUTES: Tuple[str] = ("pizza_info",)

    tomato_sauce = 200
    mozzarella = 125

    def __init__(self, pizza_info: PizzaInfo = PizzaInfo(PizzaSize.L)):
        self.pizza_info = pizza_info

    def __iter__(self) -> Generator[Tuple[str, int], None, None]:
        for key in self.__dict__:
            if key not in self.NON_INGREDIENTS_ATTRIBUTES:
                yield key, getattr(self, key)


class Margherita(PizzaBase):
    tomatoes = 100


class Pepperoni(PizzaBase):
    pepperoni = 90


class Hawaiian(PizzaBase):
    chicken = 90
    pineapples = 80
