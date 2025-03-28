import pytest
import numpy as np

def test_recommendations():
    user_vector = np.array([0.1, 0.2, 0.3])
    movie_factors = np.array([[0.4, 0.5, 0.6], [0.7, 0.8, 0.9]])
    scores = np.dot(movie_factors, user_vector)
    assert len(scores) == 2