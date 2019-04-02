import pandas as pd
from numpy import NaN


# note: there is a far easier way to remove duplicated indices in a single line using duplicated:
# df = df[~df.index.duplicated(keep='first')]

# this function instead of keeping the first or last duplicated row,
# removes duplicates and keeps the row with the most non null columns


def keep_row_most_columns(df):
    """Remove any rows with duplicate indices, keeping the first row with most non null columns.
       Takes a pandas DataFrame and returns the sorted DataFrame

       :param df: the pandas DataFrame to remove duplicated rows from
       :return: df; the sorted DataFrame with duplicated rows removed

       >>> df = pd.DataFrame(index=([pd.to_datetime('2019-04-02 11:00:00')]*3), \
                             columns=['A','B','C'], \
                             data=[[1, 2, NaN], [3, NaN, 4], [NaN, 5, NaN]])
       >>> keep_row_most_columns(df)
    """

    # ensure that df is sorted so that duplicated indices are contiguous
    df.sort_index(inplace=True)

    # indexing on datetimeIndexes that are repeated has unpredictable behavior, so slices and bulk dropping are used
    # you can not reliably drop all rows of a dataframe that share a datetimeIndex by referring to them by index

    keep_df = pd.DataFrame()

    for index, _ in df[df.index.duplicated(keep=False)].iterrows():
        # get the slice that contains the duplicated rows
        dup_slice = df.index.get_loc(index)
        # create DataFrame with the rows which share the index
        shared_index_df = df[dup_slice].copy()  # could not index with just index had to use slice

        # this was not working with a small df with only duplicated indices,
        # so new strategy of dropping all dups at once after the for loop:
        # remove the rows from the df which share the index
        #df.drop(dup_slice.start, inplace=True)

        # add a column that contains the number of non null columns to shared_index_df to sort against
        shared_index_df['len'] = shared_index_df.apply(lambda row: len(row.dropna()), axis=1)

        # add back the row from shared_index_df with the most non null columns while dropping the len column
        best_row = (shared_index_df.sort_values('len', ascending=False).drop(columns=['len']).iloc[0])
        best_row.name = index
        keep_df = keep_df.append(best_row)

    print(keep_df.shape)
    # drop all of the duplicated rows from orbit, it's the only way to be sure.
    # dropping all duplicated rows here because trying to drop duplicates by repeated datetimeIndexes is unpredictable
    df.drop_duplicates(keep=False)
    print(df.shape)

    # add back in the best_rows from among those with duplicates indices
    df = pd.concat([df, keep_df])  # not doing any concat sort as the behavior of that seems unresolved

    # Sort the df to put appended rows back in sort order
    df.sort_index(inplace=True)

    return df

df = pd.DataFrame(index=([pd.to_datetime('2019-04-02 11:00:00')]*3), \
                  columns=['A','B','C'], \
                  data=[[1, 2, NaN], [3, NaN, 4], [NaN, 5, NaN]])
print(df)
dup_slice = df.index.get_loc(pd.to_datetime('2019-04-02 11:00:00'))
print(dup_slice)
# help(keep_row_most_columns)
