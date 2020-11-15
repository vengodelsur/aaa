from typing import Dict, Any


def create_class(name: str) -> type:
    """
    >>> location_class = create_class("Location")
    >>> location = location_class(**{"address": "город Москва, Лесная, 7",
    ...                              "metro_stations": ["Белорусская"]})
    >>> location.address
    'город Москва, Лесная, 7'
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    class_ = type(name, (object,), {"__init__": __init__})
    return class_


class Deserializer:
    # TODO: refactor json to class instance transformation
    def flat_dict_to_class_instance(self, flat_dict, class_):
        return class_(**flat_dict)

    @staticmethod
    def nested_dict_to_class_instance(nested_dict, class_, is_top_level_call=True):
        # TODO: check keywords
        if not isinstance(nested_dict, dict):
            return nested_dict
        arguments = {
            key: Deserializer.nested_dict_to_class_instance(
                value, create_class(key), is_top_level_call=False
            )
            for key, value in nested_dict.items()
        }
        if is_top_level_call:
            return arguments
        return class_(**arguments)


class ColorizeMixin:
    def colorize(self, string):
        return f"\033[{self.repr_color_code}m{string}\033[m"


class Advert(ColorizeMixin):
    ANSI_yellow = 33
    repr_color_code = ANSI_yellow
    JSONType = Dict[str, Any]

    def __init__(self, json_info: JSONType):
        """
        >>> import json
        >>> lesson_str = '''{
        ...    "title": "python",
        ...    "price": 0,
        ...    "location": {
        ...        "address": "город Москва, Лесная, 7",
        ...        "metro_stations": ["Белорусская"]
        ...    }
        ... }'''
        >>> lesson = json.loads(lesson_str)
        >>> lesson_ad = Advert(lesson)
        >>> lesson_ad.location.address
        'город Москва, Лесная, 7'
        """
        arguments = Deserializer.nested_dict_to_class_instance(
            json_info,
            type(self).__name__,
        )
        for key, value in arguments.items():
            setattr(self, key, value)
            if key == "price":
                self._price = value

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
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be >=0")

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
