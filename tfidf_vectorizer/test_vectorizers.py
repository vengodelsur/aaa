from typing import List

from vectorizers import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)


def are_almost_equal(left: List[float], right: List[float], eps: float = 0.00001) -> bool:
    return len(left) == len(right) and all(
        abs(left_item - right_item) < eps for left_item, right_item in zip(left, right)
    )


def are_almost_equal_matrices(left: List[List[float]], right: List[List[float]]) -> bool:
    return all(
        len(left) == len(right) and are_almost_equal(left_vector, right_vector)
        for left_vector, right_vector in zip(left, right)
    )


def test_count_vectorizer():
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == [
        "crock",
        "pot",
        "pasta",
        "never",
        "boil",
        "again",
        "pomodoro",
        "fresh",
        "ingredients",
        "parmesan",
        "to",
        "taste",
    ]
    assert count_matrix == [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    ]


def test_tf_transform():
    count_matrix = [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
    tf_matrix = TfidfTransformer.tf_transform(count_matrix)
    expected_tf_matrix = [
        [
            0.14285714285714285,
            0.14285714285714285,
            0.2857142857142857,
            0.14285714285714285,
            0.14285714285714285,
            0.14285714285714285,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.14285714285714285,
            0.0,
            0.0,
            0.0,
            0.14285714285714285,
            0.14285714285714285,
            0.14285714285714285,
            0.14285714285714285,
            0.14285714285714285,
            0.14285714285714285,
        ],
    ]
    assert are_almost_equal_matrices(tf_matrix, expected_tf_matrix)


def test_idf_transform():
    count_matrix = [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
    idf_matrix = TfidfTransformer.idf_transform(count_matrix)
    expected_idf_matrix = [
        1.4054651081081644,
        1.4054651081081644,
        1.0,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
        1.4054651081081644,
    ]
    assert are_almost_equal(idf_matrix, expected_idf_matrix)


def test_tfidf_transformer():
    count_matrix = [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(count_matrix)
    expected_tfidf_matrix = [
        [
            0.20078072972973776,
            0.20078072972973776,
            0.2857142857142857,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.14285714285714285,
            0.0,
            0.0,
            0.0,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
        ],
    ]
    assert are_almost_equal_matrices(tfidf_matrix, expected_tfidf_matrix)


def test_tfidf_vectorizer():
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == [
        "crock",
        "pot",
        "pasta",
        "never",
        "boil",
        "again",
        "pomodoro",
        "fresh",
        "ingredients",
        "parmesan",
        "to",
        "taste",
    ]
    expected_tfidf_matrix = [
        [
            0.20078072972973776,
            0.20078072972973776,
            0.2857142857142857,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.0,
            0.0,
            0.14285714285714285,
            0.0,
            0.0,
            0.0,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
            0.20078072972973776,
        ],
    ]
    assert are_almost_equal_matrices(tfidf_matrix, expected_tfidf_matrix)
