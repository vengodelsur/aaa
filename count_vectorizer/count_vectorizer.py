from typing import Iterable, List


class CountVectorizer:
    def __init__(self):
        pass

    def fit_transform(self, corpus: List[str]) -> List[List[int]]:
        """
        Создает словарь по корпусу и выдает матрицу признаков корпуса,
        основанную на этом словаре
        :param corpus: корпус (список текстов)
        :return: матрица признаков для корпуса
        """
        self._fit(corpus)
        return self._transform(corpus)

    def _fit(self, corpus: Iterable[str]):
        """
        Создает словарь признаков по корпусу
        :param corpus: корпус (набор текстов)
        """
        vocabulary = set()
        feature_names = []
        for text in corpus:
            for word in self._tokenize(text):
                if word not in vocabulary:
                    vocabulary.add(word)
                    feature_names.append(word)
        self._feature_names = feature_names
        self._token2index = {token: i for i, token in enumerate(self._feature_names)}

    def _tokenize(self, text: str) -> List[str]:
        """
        Разбивает текст на токены
        :param text: текст для токенизации
        :return: список токенов текста
        """
        return text.lower().split()

    def _transform(self, corpus: Iterable[str]) -> List[List[int]]:
        """
        Выдаёт матрицу признаков по корпусу
        :param corpus: набор текстов
        :return: матрица признаков
        """
        return [self._transform_text(text) for text in corpus]

    def _transform_text(self, text: str) -> List[int]:
        """
        Выдаёт вектор признаков для одного текста
        :param text: текст
        :return: вектор признаков
        """
        row = [0 for _ in range(len(self._feature_names))]
        for token in self._tokenize(text):
            row[self._token2index[token]] += 1
        return row

    def get_feature_names(self) -> List[str]:
        """
        Выдаёт список признаков словаря
        :return: список признаков
        """
        return self._feature_names
