from math import log
from typing import Iterable, List


class CountVectorizer:
    def __init__(self):
        self._feature_names = []  # List[str]
        self._token2index = {}  # Dict[str, int]

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


def tf_transform(count_matrix: List[List[int]]) -> List[List[float]]:
    return [_tf_transform_row(row) for row in count_matrix]


def _tf_transform_row(row: List[int]) -> List[float]:
    count_sum = sum(row)
    return [count / count_sum for count in row]


def idf_transform(count_matrix: List[List[int]]) -> List[float]:
    num_documents = len(count_matrix)
    document_counts = [0 for _ in range(len(count_matrix[0]))]
    for row in count_matrix:
        for i, count in enumerate(row):
            if count > 0:
                document_counts[i] += 1

    idf_vector = [log((num_documents + 1) / (feature_count + 1)) + 1 for feature_count in
                  document_counts]
    return idf_vector


class TfidfTransformer:
    @staticmethod
    def fit_transform(count_matrix: List[List[int]]) -> List[List[float]]:
        tf_matrix = tf_transform(count_matrix)
        idf_vector = idf_transform(count_matrix)
        tfidf_matrix = [TfidfTransformer._multiply_by_elements(row, idf_vector) for row in
                        tf_matrix]
        return tfidf_matrix

    @staticmethod
    def _multiply_by_elements(left: List[float], right: List[float]) -> List[float]:
        return [left_item * right_item for left_item, right_item in zip(left, right)]


class TfidfVectorizer(CountVectorizer):
    def __init__(self):
        super(TfidfVectorizer, self).__init__()
        self._tfidf_transformer = TfidfTransformer()

    def fit_transform(self, corpus: List[str]) -> List[List[float]]:
        count_matrix = super().fit_transform(corpus)
        return self._tfidf_transformer.fit_transform(count_matrix)
