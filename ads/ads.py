from keyword import iskeyword
from typing import Dict, Any, Union


class Deserializer:
    @staticmethod
    def fix_non_identifier_name(name: str) -> str:
        if iskeyword(name):
            return f"{name}_"
        return name

    @staticmethod
    def default_init(obj, **kwargs):
        for key, value in kwargs.items():
            fixed_key = Deserializer.fix_non_identifier_name(key)
            setattr(obj, fixed_key, value)

    @staticmethod
    def nested_dict_to_class_arguments(nested_dict: Union[dict, Any], class_: type, is_top_level_call=True) -> \
            Union[dict, object]:
        # TODO: check keywords
        if not isinstance(nested_dict, dict):
            return nested_dict
        arguments = {
            key: Deserializer.nested_dict_to_class_arguments(
                value, Deserializer.create_class(key), is_top_level_call=False
            )
            for key, value in nested_dict.items()
        }
        if is_top_level_call:
            return arguments
        return class_(**arguments)

    @staticmethod
    def create_class(name: str) -> type:
        """
        >>> location_class = Deserializer.create_class("Location")
        >>> location = location_class(**{"address": "город Москва, Лесная, 7",
        ...                              "metro_stations": ["Белорусская"]})
        >>> location.address
        'город Москва, Лесная, 7'
        """
        fixed_name = Deserializer.fix_non_identifier_name(name)
        class_ = type(fixed_name, (object,), {"__init__": Deserializer.default_init})
        return class_


class ColorizeMixin:
    def colorize(self, string: str) -> str:
        return f"\033[{self.repr_color_code}m{string}\033[m"




class Advert(ColorizeMixin):
    ANSI_yellow = 33
    repr_color_code = ANSI_yellow
    JSONType = Dict[str, Any]

    def __init__(self, json_info: JSONType):
        """
        >>> import json
        >>> corgi_str = '''{
        ...     "title": "Вельш-корги",
        ...     "price": 1000,
        ...     "class": "dogs",
        ...     "location": {
        ...     "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        ...     }
        ... }'''
        >>> corgi = json.loads(corgi_str)
        >>> corgi_ad = Advert(corgi)
        >>> corgi_ad.location.address
        'сельское поселение Ельдигинское, поселок санатория Тишково, 25'
        >>> corgi_ad.class_
        'dogs'
        """
        arguments = Deserializer.nested_dict_to_class_arguments(
            json_info,
            type(self).__name__,
        )
        Deserializer.default_init(self, **arguments)

    @property
    def price(self, default_value=0):
        """
        >>> import json
        >>> lesson_str = '{"title": "python", "price": -1}'
        >>> lesson = json.loads(lesson_str)
        >>> lesson_ad = Advert(lesson)
        Traceback (most recent call last):
            ...
        ValueError: Price must be >=0

        >>> lesson_str = '{"title": "python"}'
        >>> lesson = json.loads(lesson_str)
        >>> lesson_ad = Advert(lesson)
        >>> lesson_ad.price
        0
        """
        # Warning: this realisation is questionable.
        # It would be more explicit to set the price to default value in init, but then we'd have to
        # store additional info  to tell the ads with price 0 from ads without info on price.
        # Also this way seems to be more convenient if we may need to change the default value.
        return getattr(self, "_price", default_value)

    @price.setter
    def price(self, value: int):
        if value < 0:
            raise ValueError("Price must be >=0")
        self._price = value

    def __repr__(self):
        """
        >>> import json
        >>> iphone_str = '{"title": "iPhone X", "price": 100}'
        >>> iphone = json.loads(iphone_str)
        >>> iphone_ad = Advert(iphone)
        >>> print(iphone_ad)
        \033[33miPhone X | 100 ₽\033[m
        >>> print("next line in default color")
        next line in default color
        """
        return self.colorize(f"{self.title} | {self.price} ₽")  # TODO: handle title not set
