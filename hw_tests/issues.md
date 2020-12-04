## issue-01
Дана функция, кодирующая строку в соответсвии с таблицей азбуки Морзе

```python
# полный код в файле morse.py
def encode(message: str) -> str:
    """
    Кодирует строку в соответсвии с таблицей азбуки Морзе
    """
    encoded_signs = [
        LETTER_TO_MORSE[letter] for letter in message
    ]

    return ' '.join(encoded_signs)
```

Напишите на неё тесты с использование `doctest`

**DoD (Definition of Done) - критерии, позволяющие понять, что задача сделана, как ожидается**:
* используется директива
* используется флаг
* тест с message = 'SOS'
* тест с исклечением (Exception)
* файл README.md с описанием шагов для запуска
* файл result с командами и результатами запуска
* файл *.py с функцией и доктестами
* нет замечаний от `flake8`

## issue-02
Дана функция, декодирующая строку из азбуки Морзе в английский

```python
# полный код в файле morse.py
def decode(morse_message: str) -> str:
    """
    Декодирует строку из азбуки Морзе в английский
    """
    decoded_letters = [
        MORSE_TO_LETTER[letter] for letter in morse_message.split()
    ]

    return ''.join(decoded_letters)
```

Напишите на неё параметрический тест, используя `pytest.mark.parametrize`

**DoD (Definition of Done) - критерии, позволяющие понять, что задача сделана, как ожидается**:
* минимум 3 тестовых примера
* файл README.md с описанием шагов для запуска
* файл result с командами и результатами запуска
* файл *.py с функцией и тестами
* нет замечаний от `flake8`

## issue-03
Дана функция, кодирующая значение в бинарное представление на основе порядкового номера первого встречаемго элемента\
Подробнее про `One Hot Encoding` можно почтитать тут - [How to One Hot Encode Sequence Data in Python](https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/)

```python
# полный код в файле one_hot_encoder.py
def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows
```

Напишите на неё тесты с использованием `unittest`

**DoD (Definition of Done) - критерии, позволяющие понять, что задача сделана, как ожидается**:
* минимум 4 тестовых примера
* минимум 2 метода проверки (`assertEqual`, `assertNotIn`, ...)
* пример с перехватом исключения
* файл README.md с описанием шагов для запуска
* файл result с командами и результатами запуска
* файл *.py с функцией и тестами
* нет замечаний от `flake8`

## issue-04
Дана функция, кодирующая значение в бинарное представление на основе порядкового номера первого встречаемго элемента\
Подробнее про `One Hot Encoding` можно почтитать тут - [How to One Hot Encode Sequence Data in Python](https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/)

```python
# полный код в файле one_hot_encoder.py
def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows
```

Напишите на неё тесты с использованием `pytest`

**DoD (Definition of Done) - критерии, позволяющие понять, что задача сделана, как ожидается**:
* минимум 4 тестовых примера
* пример с перехватом исключения
* файл README.md с описанием шагов для запуска
* файл result с командами и результатами запуска
* файл *.py с функцией и тестами
* нет замечаний от `flake8`

## issue-05
Дана функция, возвращающая текущий год. Дату и время получаем из API-worldclock

```python
# полный код в файле what_is_year_now.py
def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год

    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)
```

Напишите на неё тесты, проверяющие все сценарии работы

**DoD (Definition of Done) - критерии, позволяющие понять, что задача сделана, как ожидается**и:
* добейтесь 100% покртыия кода тестами
* используйте unittest.mock для замены реального обращения к API
* предоставьте отчет о покрытии в виде директории с html файлами
* файл README.md с описанием шагов для запуска
* файл result с командами и результатами запуска
* файл *.py с функцией и тестами
* нет замечаний от `flake8`
