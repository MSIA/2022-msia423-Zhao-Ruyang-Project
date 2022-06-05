import numpy as np
# from sklearn.compose import ColumnTransformer
import logging


logger = logging.getLogger(__name__)


def count_down(start_row: list, days_index: int = 7) -> np.array:
    """Expand the list into a matrix by counting down the number of days left"""
    try:
        days = int(start_row[days_index])
    except IndexError as e:
        logger.error('Index of days is out of range of provided list. %s', e)
        raise e
    except ValueError as e:
        logger.error('Unable to convert non-integer string to int. %s', e)
        raise e
    start_row = np.array(start_row).reshape(1, -1)
    full_matrix = None
    for day in range(days):
        record = start_row.copy()
        record[0, days_index] = day
        if full_matrix is not None:
            full_matrix = np.vstack((full_matrix, record))
        else:
            full_matrix = record

    return np.array(full_matrix)


def time_of_day(time: str):
    """Parse hour from input str and output time of day"""
    # Get hour from a time str and convert to int
    try:
        hour, minute = time.split(':')
    except ValueError as e:
        logger.error('Check format of the time. %s', time)
        raise e
    try:
        hour = int(hour)
    except ValueError as e:
        logger.error('Unable to convert non-integer string `%s` to int.', hour)
        raise e
    # Find time of day
    if 0 <= hour < 4:
        segment = 'Late_Night'
    elif 4 <= hour < 8:
        segment = 'Early_Morning'
    elif 9 <= hour < 12:
        segment = 'Morning'
    elif 13 <= hour < 16:
        segment = 'Afternoon'
    elif 17 <= hour < 20:
        segment = 'Evening'
    else:
        segment = 'Night'

    return segment


if __name__ == '__main__':
    list_in = ['a', 'b', 'not_number']
    index_in = 2
    count_down(list_in, index_in)
    import joblib
    # a = count_down([1, 1, 2, 1, 1, 1, 1, 15])
    # print(a)
    # print(np.array([['1', 1, 2, 1, 1, 1, 1, 15]]).astype('float'))
    # print(['a', 1, 2, 1, 1, 1, 1, 15])
 #    encoder = joblib.load('models/encoder.joblib')
 #    input = np.array([['SpiceJet', 'Delhi', 'Afternoon', '2', 'Chennai', 'Economy', '8.5', '0'],
 # ['SpiceJet', 'Delhi', 'Afternoon', '2', 'Chennai', 'Economy', '8.5', '1'],
 # ['SpiceJet', 'Delhi', 'Afternoon', '2', 'Chennai', 'Economy', '8.5', '2']])
 #    print(input)
 #    res = encoder.transform(input)
 #    # print(res)