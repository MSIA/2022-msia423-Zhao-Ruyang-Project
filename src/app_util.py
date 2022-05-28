import numpy as np
# from sklearn.compose import ColumnTransformer
import logging
logger = logging.getLogger(__name__)

def count_down(X: list, days_index: int = 7) -> np.array:
    days = int(X[days_index])
    X = np.array(X).reshape(1, -1)
    full_matrix = X.copy()
    for day in reversed(range(days)):
        record = X.copy()
        record[0, days_index] = day
        full_matrix = np.vstack((full_matrix, record))
    # full_matrix = full_matrix.astype('float')
    return full_matrix


if __name__ == '__main__':
    a = count_down([1, 1, 2, 1, 1, 1, 1, 15])
    print(a)
    print(np.array([['1', 1, 2, 1, 1, 1, 1, 15]]).astype('float'))
    print(['a', 1, 2, 1, 1, 1, 1, 15])