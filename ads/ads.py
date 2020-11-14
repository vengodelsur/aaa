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


class Advert:
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

    @property
    def price(self):
        """
        >>> import json
        >>> lesson_str = '{"title": "python", "price": -1}'
        >>> lesson = json.loads(lesson_str)
        >>> lesson_ad = Advert(lesson)
        Traceback (most recent call last):
            ...
        ValueError: Price must be >=0
        """
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be >=0")
