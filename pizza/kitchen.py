import random
import time

from recipes import PizzaBase


def log(message_format):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            print(message_format.format(end - start))
            return result

        return wrapper

    return decorator


@log
def bake(pizza: PizzaBase):
    """Готовит пиццу"""
    time.sleep(random.randint(3, 6))
    return pizza


@log('Доставили за {}с!')
def delivery(pizza: PizzaBase):
    """Доставляет пиццу"""
    time.sleep(random.randint(1, 3))
    return pizza


@log('Забрали за {}с!')
def pickup(pizza: PizzaBase):
    """Самовывоз"""
    time.sleep(random.randint(2, 5))
    return pizza
