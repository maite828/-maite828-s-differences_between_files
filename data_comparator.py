import os
import pandas as pd
from directory_manager import DirectoryManager
from csv_handler import CSVHandler


class DataComparator:

    @staticmethod
    def duplicates_dt(df, file_name):
        duplicates = df[df.duplicated()]
        num_duplicates = len(duplicates)
        print(f"{file_name} contains: {num_duplicates} duplicates")
        return duplicates

    @staticmethod
    def compare_dt(df1, df2, identifier, merge_option):
        comparison_df = df1.merge(df2, indicator=True, how='outer')
        if merge_option == "default":
            diff_df = comparison_df[comparison_df['_merge'] != 'both'].copy()
        else:
            diff_df = comparison_df[comparison_df['_merge'] == merge_option].copy()
        diff_df.sort_values(identifier, inplace=True)
        return diff_df

    @staticmethod
    def find_differences(group, identifier):
        diff_mask = (group.iloc[0] != group.iloc[1]).to_numpy()
        if diff_mask.any():
            different_columns = group.columns[diff_mask].tolist()
            original_values = group.iloc[0, diff_mask].apply(CSVHandler.handle_type).tolist()
            different_values = group.iloc[1, diff_mask].apply(CSVHandler.handle_type).tolist()

            diff_data = {
                identifier: [group.iloc[0][identifier]] * len(different_columns),
                'Column_Name': different_columns,
                'Left_Value': original_values,
                'Right_Value': different_values
            }

            return pd.DataFrame(diff_data)
        return pd.DataFrame()
