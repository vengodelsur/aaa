from typing import Optional

import click

from kitchen import bake, pickup, deliver
from recipes import Margherita, Hawaiian, Pepperoni, PizzaBase

PIZZAS = (Margherita, Pepperoni, Hawaiian)
PIZZAS_BY_NAMES = {pizza.__name__.lower(): pizza for pizza in PIZZAS}
PIZZA_NAMES = tuple(sorted(PIZZAS_BY_NAMES.keys()))
MENU = "\n".join(PIZZA_NAMES)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza_name', nargs=1)
def order(pizza_name: str, delivery: bool) -> Optional[PizzaBase]:
    """Готовит и доставляет пиццу"""
    try:
        pizza = PIZZAS_BY_NAMES[pizza_name]
    except KeyError:
        print(f"No pizza called {pizza_name}, use menu command to see available pizzas")
        return
    pizza = bake(pizza)
    if delivery:
        pizza = deliver(pizza)
    else:
        pizza = pickup(pizza)
    return pizza


@cli.command()
def menu():
    """Выводит меню"""
    print(MENU)


if __name__ == "__main__":
    cli()
