from typing import Iterable, List


class CountVectorizer:
    def __init__(self):
        pass

    def fit_transform(self, corpus: List[str]):
        self._fit(corpus)
        return self._transform(corpus)

    def _fit(self, corpus: Iterable[str]):
        vocabulary = set()
        feature_names = []
        for text in corpus:
            for word in self._tokenize(text):
                if word not in vocabulary:
                    vocabulary.add(word)
                    feature_names.append(word)
        self._feature_names = feature_names
        self._token2index = {token: i for i, token in enumerate(self._feature_names)}

    def _tokenize(self, text: str):
        return text.lower().split()

    def _transform(self, corpus: Iterable[str]):
        return [self._transform_text(text) for text in corpus]

    def _transform_text(self, text: str):
        row = [0 for _ in range(len(self._feature_names))]
        for token in self._tokenize(text):
            row[self._token2index[token]] += 1
        return row

    def get_feature_names(self):
        return self._feature_names
