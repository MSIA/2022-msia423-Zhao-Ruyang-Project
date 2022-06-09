import numpy as np
import pytest

from src.app_util import count_down, time_of_day


def test_count_down():
    """Test whether the count_down() function outputs as expected."""
    list_in = ['a', 'b', 3]
    index_in = 2
    array_test = count_down(list_in, index_in)
    array_true = np.array([['a', 'b', 0], ['a', 'b', 1], ['a', 'b', 2]])
    np.testing.assert_array_equal(array_test, array_true)


def test_count_down_index():
    """Test whether the count_down() function handles out of index as expected."""
    list_in = ['a', 'b', 3]
    index_in = 3
    with pytest.raises(IndexError):
        count_down(list_in, index_in)


def test_count_down_nonint():
    """Test whether the count_down() function handles non-int string as expected."""
    list_in = ['a', 'b', 'not_number']
    index_in = 2
    with pytest.raises(ValueError):
        count_down(list_in, index_in)


def test_time_of_day():
    """Test whether the time_of_day() function outputs as expected."""
    time_in = '13:15'
    out_test = time_of_day(time_in)
    out_true = 'Afternoon'
    assert out_true == out_test


def test_time_of_day_unpack():
    """Test whether the time_of_day() function handles exception as expected."""
    time_in = '1315'
    with pytest.raises(ValueError):
        time_of_day(time_in)


def test_time_of_day_nonint():
    """Test whether the time_of_day() function handles exception as expected."""
    time_in = 'a:15'
    with pytest.raises(ValueError):
        time_of_day(time_in)
