import pandas as pd
from numpy import NaN


# note: there is a far easier way to remove duplicated indices in a single line using duplicated:
# df = df[~df.index.duplicated(keep='first')]

# this function instead of keeping the first or last duplicated row,
# removes duplicates and keeps the row with the most non null columns


def drop_emptier_dups(df):
    """Remove any rows with duplicate indices, keeping the first row with most non null columns.
       Takes a pandas DataFrame and returns the sorted DataFrame

       :param df: the pandas DataFrame to remove duplicated rows from
       :return: df; the sorted DataFrame with duplicated rows removed

        >>> df = pd.DataFrame(index=([pd.to_datetime('2019-04-02 11:00:00')]*3), columns=['A','B','C'], data=[[1, 2, NaN], [3, NaN, 4], [NaN, 5, NaN]])
        >>> print(df)
                               A    B    C
        2019-04-02 11:00:00  1.0  2.0  NaN
        2019-04-02 11:00:00  3.0  NaN  4.0
        2019-04-02 11:00:00  NaN  5.0  NaN
        >>> drop_emptier_dups(df)
                               A    B   C
        2019-04-02 11:00:00  1.0  2.0 NaN
    """

    # ensure that df is sorted so that duplicated indices are contiguous
    df.sort_index(inplace=True)

    # indexing on DatetimeIndexes that are repeated has unpredictable behavior, so slices and bulk dropping are used
    # you can not reliably drop all rows of a dataframe that share a DatetimeIndex by referring to them by index

    keep_df = pd.DataFrame()

    for idx in set(df[df.index.duplicated(keep=False)].index):
        # get the slice that contains the duplicated rows
        dup_slice = df.index.get_loc(idx)
        # create DataFrame with the rows which share the index
        shared_index_df = df[dup_slice].copy()  # could not index with just index had to use slice

        # add a column that contains the number of non null columns to shared_index_df to sort against
        shared_index_df['len'] = shared_index_df.apply(lambda row: len(row.dropna()), axis=1)

        # add back the row from shared_index_df with the most non null columns while dropping the len column
        best_row = (shared_index_df.sort_values('len', ascending=False).drop(columns=['len']).iloc[0])
        best_row.name = idx
        keep_df = keep_df.append(best_row)

    # drop all of the duplicated rows from orbit, it's the only way to be sure.
    df = df[~df.index.duplicated(keep=False)]

    # add back in the best_rows from among those with duplicates indices
    df = pd.concat([df, keep_df], sort=False)  # suppress warnings on future behavior with sort=False

    # Sort the df to put appended rows back in sort order
    df.sort_index(inplace=True)

    return df


def single_val_cols_to_dict(df):
    meta_dict = {}

    # if index.name has a value, store it in the meta_dict under 'index.name'
    if df.index.name is not None:
        if df.index.name != df.name + '_meta':
            meta_dict['index.name'] = df.index.name
        else:
            # if the single value columns have already been written
            raise UserWarning('Single value columns dict being overwritten by single_val_cols_to_dict')

    df.index.name = df.name + '_meta'

    # Made decision not to preserve the original columns list as meta_data
    # meta_dict['column_list'] = list(df.columns)
    # What about storing del_list in meta_data??s

    # go through columns, if only 1 unique value, store in meta_dict with column_name:single_value pair and remove column
    del_list = []
    for col in df.columns:
        if df[col].nunique(dropna=False) == 1:
            meta_dict[col] = df.loc[df.index[0], col]
            del_list.append(col)
    if len(del_list) > 0:
        df.drop(del_list, axis='columns', inplace=True)
    return (df, meta_dict)
