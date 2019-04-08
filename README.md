# chiptools
utility functions for pandas DataFrames

Tool List:
Source code found in chiptools/tools.py
* drop_emptier_dups -- removes rows with duplicated indices which have the most non-null columns
* single_val_cols_to_dict -- removes columns which only contain one value across all rows, storing column_name:value in a dict

Documentation generated with sphinx hosted on readthedocs:
https://df-chiptools.readthedocs.io/en/latest/
