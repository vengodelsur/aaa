from typing import Optional

import click

from kitchen import bake, pickup, deliver
from recipes import Margherita, Hawaiian, Pepperoni, PizzaBase

PIZZAS = (Margherita, Pepperoni, Hawaiian)
PIZZAS_BY_NAMES = {pizza.__name__.lower(): pizza for pizza in PIZZAS}
MENU = "\n".join(pizza.description() for pizza in PIZZAS)


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza_name", nargs=1)
def order(pizza_name: str, delivery: bool) -> Optional[PizzaBase]:
    """Готовит и доставляет пиццу"""
    try:
        pizza = PIZZAS_BY_NAMES[pizza_name]()
    except KeyError:
        print(f"No pizza called {pizza_name}, use menu command to see available pizzas")
        return None
    pizza = bake(pizza)
    if delivery:
        pizza = deliver(pizza)
    else:
        pizza = pickup(pizza)
    return pizza


@cli.command()
def menu() -> None:
    """Выводит меню"""
    print(MENU)


if __name__ == "__main__":
    cli()
