from vectorizers import CountVectorizer, tf_transform, idf_transform, TfidfTransformer, \
    TfidfVectorizer


def test_count_vectorizer():
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['crock', 'pot', 'pasta', 'never', 'boil', 'again',
                                              'pomodoro', 'fresh', 'ingredients', 'parmesan', 'to',
                                              'taste']
    assert count_matrix == [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]


def test_tf_transform():
    count_matrix = [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    ]
    tf_matrix = tf_transform(count_matrix)
    assert tf_matrix == [[0.166, 0.166, 0.333, 0.166, 0.166, 0.166, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0.143, 0, 0, 0, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143]]


def test_idf_transform():
    count_matrix = [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    ]
    idf_matrix = idf_transform(count_matrix)
    assert idf_matrix == [1.4, 1.4, 1.0, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4]


def test_tfidf_transformer():
    count_matrix = [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    ]
    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(count_matrix)
    assert tfidf_matrix == [[0.233, 0.233, 0.333, 0.233, 0.233, 0.233, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0.143, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]


def test_tfidf_vectorizer():
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['crock', 'pot', 'pasta', 'never', 'boil', 'again',
                                              'pomodoro', 'fresh', 'ingredients', 'parmesan',
                                              'to', 'taste']
    assert tfidf_matrix == [[0.233, 0.233, 0.333, 0.233, 0.233, 0.233, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0.143, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
