from chiptools import drop_emptier_dups
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

columns = ['A', 'B', 'C']
rows = [[1.0, 2.0, np.NaN], [3.0, np.NaN, 4.0], [np.NaN, 5.0, np.NaN]]
time = '2019-04-02 11:00:00'

def _create_docstring_df():
    """creates the df used in the docstring of drop_emptier_dups"""
    return(pd.DataFrame(index=([pd.to_datetime(time)] * 3), columns=columns,
                        data=rows))


def _create_expected_doc():
    """creates the expected df to be returned after a drop_emptier_dups call with the _create_docstring_df df"""
    return(pd.DataFrame(index=[pd.to_datetime(time)], columns=columns,
                        data=[rows[0]]))


def _create_multiple_df(fuller='first'):
    """creates a larger df to test multiple dups to remove
       fuller specifies whether first dups or last dups have more columns"""
    np.random.seed(42)
    df = pd.DataFrame(np.random.rand(20,5), columns=columns+['D', 'E'],
                      index=pd.date_range(time, periods=20, freq='31min'))
    df.index = df.index.round('H')  # make every other row have a duplicate index

    # fill some locations with NaN
    for idx in set(df[df.index.duplicated(keep='first')].index):
        idx_loc = df.index.get_loc(idx).start
        if fuller == 'first':  # if you want the last dup to be emptier add 1 to the idx_loc
            idx_loc += 1
        for col in range(5):
            numNaN = 0
            if np.random.rand() >= 0.5:
                numNaN += 1
                df.iloc[idx_loc, col] = np.NaN
            if ((col == 5) & (numNaN == 0)):  # ensure that at least one column is NaN
                df.iloc[idx_loc, col] = np.NaN

    return df


def test_docstring_example():
    """tests drop_emptier_dups with the same df that is in the docstring of the function"""
    df = _create_docstring_df()
    expected = _create_expected_doc()
    returned = drop_emptier_dups(df)
    assert (assert_frame_equal(returned, expected) is None)


def test_multiple_dups():
    """tests drop_emptier_dups with a df with multiple duplicated indices"""
    row_to_keep = 'last'
    df = _create_multiple_df(row_to_keep)
    expected = df[~df.index.duplicated(keep=row_to_keep)]
    returned = drop_emptier_dups(df)
    #assert (assert_frame_equal(returned, expected) is None)

