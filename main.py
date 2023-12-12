#!/usr/bin/env python3
import os
import pandas as pd
import argparse
from tabulate import tabulate

from data_comparator import DataComparator
from csv_handler import CSVHandler
from directory_manager import DirectoryManager


def print_differences_details(differences, arguments):
    if not differences.empty:
        print("\nDetails on differences:")
        print(tabulate(differences[[arguments.identifier, 'Column_Name', 'Left_Value', 'Right_Value']],
                       headers='keys', tablefmt='psql'))


def handle_type(value):
    return str(value) if pd.notna(value) and not isinstance(value, list) else value


def find_differences(group, identifier):
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


def parse_args():
    parser = argparse.ArgumentParser(description="Compare two CSV files and find differences.")
    parser.add_argument("file1", help="Path to the first CSV file")
    parser.add_argument("--file2", help="Path to the second CSV file")
    parser.add_argument("delimiter", help="Delimiter used in CSV files")
    parser.add_argument("--identifier", help="Column(s) to order the results by")
    parser.add_argument("--merge_option", help="Comparison merge_option: left_only, right_only, both, default")
    parser.add_argument("--columns", help="Columns to exclude (space-separated indices)")
    parser.add_argument("--output", help="Output file name")

    return parser.parse_args()


def main(arguments, obj_handler, obj_comparator, obj_output_manager):
    input_manager = obj_output_manager.create_directory(base_path, "input_files")
    if not arguments.file2:
        df = obj_handler.read_csv(os.path.join(input_manager, arguments.file1), arguments.delimiter)
        obj_comparator.print_duplicates(df, arguments.file1)
        df.drop_duplicates()
    else:
        df1 = obj_handler.read_csv(os.path.join(input_manager, arguments.file1), arguments.delimiter, arguments.columns)
        df2 = obj_handler.read_csv(os.path.join(input_manager, arguments.file2), arguments.delimiter, arguments.columns)

        print("Duplicates:")
        obj_comparator.print_duplicates(df1, arguments.file1)
        obj_comparator.print_duplicates(df2, arguments.file2)

        output_file = arguments.output or f'output_file_{arguments.merge_option}.csv'
        result = obj_comparator.compare_datasets(df1.drop_duplicates(), df2.drop_duplicates(),
                                                 output_file, arguments.identifier, arguments.merge_option)

        print("\nSchemas:\n File1: {f1} {s1} \n File2: {f2} {s2} \n".format(
            f1=arguments.file1, s1=df1.shape, f2=arguments.file2, s2=df2.shape))

        result.groupby(['_merge'], observed=True).size()

        result = result[result.duplicated(arguments.identifier, keep=False)]

        print(f'The output with \'{arguments.merge_option.upper()}\' generates the following differences:\n')
        print(result[[arguments.identifier, '_merge']])

        df_no_join_col = result.drop('_merge', axis=1)
        differences = df_no_join_col.groupby(arguments.identifier).apply(find_differences,
                                                                         identifier=arguments.identifier).dropna()

        print_differences_details(differences, arguments)


if __name__ == '__main__':
    args = parse_args()
    base_path = os.path.dirname(os.path.realpath(__file__))
    output_manager = DirectoryManager()
    csv_handler = CSVHandler()
    comparator = DataComparator(base_path, output_manager, csv_handler)
    main(args, csv_handler, comparator, output_manager)
