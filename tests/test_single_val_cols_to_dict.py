from chiptools import single_val_cols_to_dict
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

columns = ['A', 'B', 'C']
rows = [[1.0, 2.0, np.NaN], [3.0, np.NaN, 4.0], [np.NaN, 5.0, np.NaN]]
time = '2019-04-02 11:00:00'

def _create_docstring_df():
    """creates the df used in the docstring of single_val_cols_to_dict"""
    return pd.DataFrame(index=pd.date_range(time, periods=3, freq='1H'),
                        columns=['col1', 'col2', 'col3'], data=[[1.0, 2.0, 3.0], [1.0, 4.0, 3.0], [1.0, 6.0, 3.0]])


def _create_expected_doc():
    """creates the expected df to be returned after a single_val_cols_to_dict call with the _create_docstring_df df"""
    return pd.DataFrame(index=pd.date_range(time, periods=3, freq='1H'), columns=['col2'],
                        data=[[2.0], [4.0], [6.0]])


def _create_test_dfs(num_rows=3, single_cols=(0, 2, 4), random_cols=(1, 3), nan_cols=None,
                     single_nans=False, rand_nans=True, nans_count=True):
    """creates a test_df and an expected_df for use by test functions
       :param num_rows: the number of rows the dfs should have
       :param single_cols: list-like, the column numbers where cols with only a single value should occur
       :param random_cols: list-like, the column numbers where cols with random values should occur
       :param nan_cols: list-like, the column numbers where all null cols should occur
       :param single_nans: False, do not intersperse NaN values into single_cols
       :param rand_nans: True, do intersperse NaN values into the random_cols
       :param nans_count: True, nans count as a distinct value for determining expected_df"""

    np.random.seed(42)

    idx = pd.date_range(time, periods=num_rows, freq='1H')
    expected_cols = []
    test_cols = []

    #####################
    # Rewrite this next whole section with subroutines that create DataFrames for each type of column

    # test if cols exist and if they should be in expected, if they exist but are not expected add to test_cols
    if single_cols and single_nans and nans_count: expected_cols.extend(single_cols)
    elif single_cols:
        test_cols.extend(single_cols)
    if random_cols: expected_cols.extend(random_cols)
    if nan_cols: test_cols.extend(nan_cols)

    # create dictionary entries for single_val columns first and use those to fill df


    # add all of the expected cols to test_cols
    test_cols.extend(expected_cols)

    expected_cols = ['col' + str(x) for x in sorted(expected_cols)]
    test_cols = ['col' + str(x) for x in sorted(test_cols)]

    expected_df = pd.DataFrame(index=idx, columns=expected_cols)
    test_df = pd.DataFrame(index=idx, columns=test_cols)


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

    return test_df, expected_df


def test_docstring_example():
    """tests drop_emptier_dups with the same df that is in the docstring of the function"""
    df = _create_docstring_df()
    expected = _create_expected_doc()
    exp_dict = {'col1': 1.0, 'col3': 3.0}
    returned, ret_dict = single_val_cols_to_dict(df)
    assert (ret_dict == exp_dict)
    assert (assert_frame_equal(returned, expected) is None)
