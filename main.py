#!/usr/bin/env python3

import pandas as pd
import argparse
from tabulate import tabulate


def create_dataframe(csv, delimiter, cols=None):
    """
    Create a DataFrame from a CSV file.

    Parameters:
    - csv (str): Path to the CSV file.
    - delimiter (str): Delimiter used in the CSV file.
    - cols (str): Columns to exclude (indices separated by space).

    Returns:
    - pd.DataFrame: DataFrame from the CSV file.
    """
    df = pd.read_csv(csv, sep=delimiter, engine='python')
    if cols:
        df.drop(df.columns[list(map(int, cols.split()))], axis=1, inplace=True)
    return df


def write_duplicates_output_file(df, source_file, output_file):
    """
    Writes a CSV file with the duplicates found to a DataFrame. The result includes the total number of duplicates in the file.

    Parameters:
    - df (pd.DataFrame): DataFrame to analyze.
    - source_file (str): Name of the source file.
    - output_file (str): Name of the output file.

    Returns:
    - None
    """
    duplicates = df[df.duplicated()]
    num_duplicates = len(duplicates)
    print(f"{source_file} contains: {num_duplicates} duplicates")
    duplicates.to_csv(output_file, index=False)


def remove_duplicates(df):
    """
    Removes duplicates from a DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame to analyze.

    Returns:
    - pd.DataFrame: DataFrame without duplicates.
    """
    return df.drop_duplicates()


def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame, output_file, identifier, merge_option):
    """
    Compares two datasets and finds the differences.

    Parameters:
    - df_1 (pd.DataFrame): First DataFrame.
    - df_2 (pd.DataFrame): Second DataFrame.
    - output_file (str): Name of the output file.
    - identifier (str): Column(s) to order the results by.
    - merge_option (str): Comparison merge_option: left_only, right_only, both, default.

    Returns:
    - pd.DataFrame: DataFrame with the differences found.
    """
    comparison_df = df1.merge(df2, indicator=True, how='outer')
    if merge_option == "default":
        diff_df = comparison_df[comparison_df['_merge'] != 'both'].copy()
    else:
        diff_df = comparison_df[comparison_df['_merge'] == merge_option].copy()
    diff_df.sort_values(identifier, inplace=True)
    diff_df.to_csv(output_file, index=False)
    return diff_df


def handle_type(value):
    """
    Handles the data type for printing.

    Parameters:
    - value: Value to handle.

    Returns:
    - str: Value converted to a string.
    """
    return str(value) if pd.notna(value) and not isinstance(value, list) else value


def find_differences(group, identifier):
    """
    Finds differences in a group of data.

    Parameters:
    - group (pd.DataFrame): Data group.
    - identifier (str): Column to order the results by.

    Returns:
    - pd.DataFrame: DataFrame with the differences found.
    """
    diff_mask = (group.iloc[0] != group.iloc[1]).to_numpy()
    if diff_mask.any():
        different_columns = group.columns[diff_mask].tolist()
        original_values = group.iloc[0, diff_mask].apply(handle_type).tolist()
        different_values = group.iloc[1, diff_mask].apply(handle_type).tolist()

        diff_data = {
            identifier: [group.iloc[0][identifier]] * len(different_columns),
            'Column_Name': different_columns,
            'Left_Value': original_values,
            'Right_Value': different_values
        }

        return pd.DataFrame(diff_data)
    return pd.DataFrame()


def main():
    """
    Main function that handles command line input and runs the comparison.
    """
    parser = argparse.ArgumentParser(description="Compare two CSV files and find differences.")
    parser.add_argument("file1", help="Path to the first CSV file")
    parser.add_argument("--file2", help="Path to the second CSV file")
    parser.add_argument("delimiter", help="Delimiter used in CSV files")
    parser.add_argument("--identifier", help="Column(s) to order the results by")
    parser.add_argument("--merge_option", help="Comparison merge_option: left_only, right_only, both, default")
    parser.add_argument("--columns", help="Columns to exclude (space-separated indices)")
    parser.add_argument("--output", help="Output file name")

    args = parser.parse_args()

    if not args.file2:
        df = create_dataframe(args.file1, args.delimiter)
        write_duplicates_output_file(df, args.file1, "duplicates_" + args.file1)
        remove_duplicates(df)
    else:
        df1 = create_dataframe(args.file1, args.delimiter, args.columns)
        df2 = create_dataframe(args.file2, args.delimiter, args.columns)

        print("Duplicates:")
        write_duplicates_output_file(df1, args.file1, "duplicates_" + args.file1)
        write_duplicates_output_file(df2, args.file2, "duplicates_" + args.file2)

        output_file = args.output or f'output_file_{args.merge_option}.csv'
        result = compare_datasets(remove_duplicates(df1), remove_duplicates(df2), output_file, args.identifier, args.merge_option)

        print("\nSchemas:\n File1: {f1} {s1} \n File2: {f2} {s2} \n".format(
            f1=args.file1, s1=df1.shape, f2=args.file2, s2=df2.shape))

        result.groupby(['_merge'], observed=True).size()

        result = result[result.duplicated(args.identifier, keep=False)]

        print(f'The output with \'{args.merge_option.upper()}\' generates the following differences:\n')
        print(result[[args.identifier, '_merge']])

        df_no_join_col = result.drop('_merge', axis=1)
        differences = df_no_join_col.groupby(args.identifier).apply(find_differences, identifier=args.identifier).dropna()

        if not differences.empty:
            print("\nDetails on differences:")
            print(tabulate(differences[[args.identifier, 'Column_Name', 'Left_Value', 'Right_Value']],
                           headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    main()
