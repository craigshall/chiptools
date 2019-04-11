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


def _open_test_dfs(test_fname, expected_fname):
    """creates a test_df and an expected_df for use by test functions
       :param test_fname: the file name to open to create the test_df
       :param expected_fname: the file name to open to create the expected_df"""

    test_df = pd.read_csv(test_fname)

    # wanted to use read_hdf, but that required installing additional packages...keeping things simpler for now
    #expected_df = pd.read_hdf(expected_fname, 'DataFrame')
    #expected_dict = pd.read_hdf(expected_fname, 'dict')
    expected_df = pd.read_csv(expected_fname)
    expected_dict = {'STATION': 72495723213, 'REPORT_TYPE': 'FM-15'}
    return test_df, expected_df, expected_dict


def test_docstring_example():
    """tests drop_emptier_dups with the same df that is in the docstring of the function"""
    df = _create_docstring_df()
    expected = _create_expected_doc()
    exp_dict = {'col1': 1.0, 'col3': 3.0}
    returned, ret_dict = single_val_cols_to_dict(df)
    assert (ret_dict == exp_dict)
    assert (assert_frame_equal(returned, expected) is None)


def test_example_file():
    file_prefix = 'weather'
    test_fname = file_prefix + '_test.csv'
    expected_fname = file_prefix + '_expected.csv'
    test_df, expected_df, expected_dict = _open_test_dfs(test_fname, expected_fname)
    returned_df, returned_dict = single_val_cols_to_dict(test_df)
    assert (expected_dict == returned_dict)
    assert (assert_frame_equal(returned_df, expected_df) is None)
