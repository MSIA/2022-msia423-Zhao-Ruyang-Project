import pandas as pd
import pytest

from src.preprocess_util import convert_column

df_in = pd.DataFrame(
    [[5000.0, 'one'],
     [11100.0, 'two']],
    index=['cloud_a', 'cloud_b'],
    columns=['miles', 'stops'])
dict_in = {
    'one': 1,
    'two': 2
}


def test_convert_column():
    """Test whether convert_column() outputs as expected"""
    col_in = 'stops'
    df_out = convert_column(df_in, col_in, dict_in)
    df_true = pd.DataFrame(
        [[5000.0, 1],
         [11100.0, 2]],
        index=['cloud_a', 'cloud_b'],
        columns=['miles', 'stops'])
    pd.testing.assert_frame_equal(df_true, df_out)


def test_convert_column_invalidcol():
    """Test whether convert_column() handles non-existent column"""
    col_in = 'not_exist'
    with pytest.raises(KeyError):
        convert_column(df_in, col_in, dict_in)
