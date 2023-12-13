import pandas as pd


class DataComparator:
    @staticmethod
    def duplicates_dt(df, file_name):
        """
        Identify and print details on duplicate rows within a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame to check for duplicates.
            file_name (str): Name of the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the duplicate rows.
        """
        # Identify duplicate rows
        duplicates = df[df.duplicated()]

        # Get the number of duplicate rows
        num_duplicates = len(duplicates)

        # Print the information about duplicates
        print(f"{file_name} contains: {num_duplicates} duplicates")

        return duplicates

    @staticmethod
    def compare_dt(df1, df2, identifier, merge_option):
        """
        Compare two DataFrames based on a specified identifier column and merge option.

        Args:
            df1 (pd.DataFrame): First DataFrame.
            df2 (pd.DataFrame): Second DataFrame.
            identifier (str): Column(s) to identify rows for comparison.
            merge_option (str): Comparison merge_option: left_only, right_only, both, default.

        Returns:
            pd.DataFrame: DataFrame containing the differences.
        """
        # Perform an outer merge
        comparison_df = pd.merge(df1, df2, how='outer', indicator=True)

        # Select rows based on the merge option
        if merge_option == "default":
            diff_df = comparison_df[comparison_df['_merge'] != 'both'].copy()
        else:
            diff_df = comparison_df[comparison_df['_merge'] == merge_option].copy()

        # Sort the result by the specified identifier column
        diff_df.sort_values(identifier, inplace=True)

        return diff_df

    @staticmethod
    def find_differences(group, identifier):
        """
        Find and return the differences between two rows in a DataFrame group.

        Args:
            group (pd.DataFrame): DataFrame group.
            identifier (str): Column(s) to identify rows for comparison.

        Returns:
            pd.DataFrame: DataFrame containing the differences.
        """
        # Extract values for the two rows
        values_row1 = group.iloc[0]
        values_row2 = group.iloc[1]

        # Identify columns with differences
        diff_mask = values_row1 != values_row2

        if diff_mask.any():
            # Get identifier value for the group
            identifier_value = values_row1[identifier]

            # Create a DataFrame with differences
            differences_data = {
                identifier: [identifier_value] * diff_mask.sum(),
                'Column_Name': diff_mask.index[diff_mask].tolist(),
                'Left_Value': values_row1[diff_mask].tolist(),
                'Right_Value': values_row2[diff_mask].tolist()
            }

            return pd.DataFrame(differences_data)

        return pd.DataFrame()
