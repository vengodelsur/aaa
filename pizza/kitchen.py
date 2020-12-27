import random
import time
from typing import Callable, Any

from recipes import PizzaBase


def log(message_format: str) -> Callable:
    def decorator(function: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            print(message_format.format(int(end - start)))
            return result

        return wrapper

    return decorator


@log("Приготовили за {}с!")
def bake(pizza: PizzaBase) -> PizzaBase:
    """Готовит пиццу"""
    time.sleep(random.randint(3, 6))
    return pizza


@log("Доставили за {}с!")
def deliver(pizza: PizzaBase) -> PizzaBase:
    """Доставляет пиццу"""
    time.sleep(random.randint(1, 3))
    return pizza


@log("Забрали за {}с!")
def pickup(pizza: PizzaBase) -> PizzaBase:
    """Самовывоз"""
    time.sleep(random.randint(2, 5))
    return pizza
