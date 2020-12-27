# coding: utf-8

import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Generator, List

import emoji as emoji


class PizzaSize(Enum):
    L = "L"
    XL = "L"


@dataclass
class PizzaInfo:
    size: PizzaSize


class PizzaBase:
    ICON = ":bread:"

    tomato_sauce = 200
    mozzarella = 125

    def __init__(self, pizza_info: PizzaInfo = PizzaInfo(PizzaSize.L)):
        self.pizza_info = pizza_info

    def __iter__(self) -> Generator[Tuple[str, int], None, None]:
        for key in self.ingredients():
            yield key, getattr(self, key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PizzaBase):
            return False
        return dict(self) == dict(other)

    @classmethod
    def ingredients(cls: type) -> List[str]:
        def filter_attributes(item: object) -> bool:
            return not inspect.ismethod(item)

        def is_ingredient(item: str) -> bool:
            return not item.startswith("__") and item != "ICON"

        members = [item[0] for item in inspect.getmembers(cls, filter_attributes)]
        return list(filter(is_ingredient, members))

    @classmethod
    def description(cls) -> str:
        ingredients = ", ".join(cls.ingredients()).replace("_", " ")
        return emoji.emojize(f"{cls.ICON} {cls.__name__}: {ingredients}")


class Margherita(PizzaBase):
    ICON = ":cheese_wedge:"
    tomatoes = 100


class Pepperoni(PizzaBase):
    ICON = ":pizza:"
    pepperoni = 90


class Hawaiian(PizzaBase):
    ICON = ":pineapple:"
    chicken = 90
    pineapples = 80
