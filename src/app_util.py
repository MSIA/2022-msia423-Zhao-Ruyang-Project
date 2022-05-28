import numpy as np
# from sklearn.compose import ColumnTransformer
import logging
logger = logging.getLogger(__name__)


def count_down(X: list, days_index: int = 7) -> np.array:
    days = int(X[days_index])
    X = np.array(X).reshape(1, -1)
    full_matrix = None
    for day in range(days):
        record = X.copy()
        record[0, days_index] = day
        if full_matrix is not None:
            full_matrix = np.vstack((full_matrix, record))
        else:
            full_matrix = record

    return np.array(full_matrix)


if __name__ == '__main__':
    a = count_down([1, 1, 2, 1, 1, 1, 1, 15])
    print(a)
    # print(np.array([['1', 1, 2, 1, 1, 1, 1, 15]]).astype('float'))
    # print(['a', 1, 2, 1, 1, 1, 1, 15])