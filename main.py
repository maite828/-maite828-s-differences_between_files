#!/usr/bin/env python3
"""
Script to compare two CSV files and find differences.

Usage:
    python script_name.py <file1> [--file2 <file2>] <delimiter> [--identifier <identifier>]
                                [--merge_option <merge_option>] [--columns <columns>] [--output <output>]

Parameters:
    <file1>: Path to the first CSV file.
    --file2: Path to the second CSV file (optional).
    <delimiter>: Delimiter used in CSV files.
    --identifier: Column(s) to order the results by.
    --merge_option: Comparison merge_option: left_only, right_only, both, default.
    --columns: Columns to exclude (space-separated indices).
    --output: Output file name.

Example:
    python script_name.py file1.csv --file2 file2.csv ',' --identifier LEGALENTITYID
"""

import os
import argparse
from tabulate import tabulate

from data_comparator import DataComparator
from csv_handler import CSVHandler


def print_differences_details(differences, args):
    """
    Print details of the differences between two CSV files.

    Parameters:
        differences (pd.DataFrame): DataFrame containing differences.
        args (argparse.Namespace): Parsed command line arguments.
    """
    if not differences.empty:
        print("\nDetails on differences:")
        print(tabulate(differences[[args.identifier, 'Column_Name', 'Left_Value', 'Right_Value']],
                       headers='keys', tablefmt='psql'))


def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Compare two CSV files and find differences.")
    parser.add_argument("file1", help="Path to the first CSV file")
    parser.add_argument("--file2", help="Path to the second CSV file")
    parser.add_argument("delimiter", help="Delimiter used in CSV files")
    parser.add_argument("--identifier", help="Column(s) to order the results by")
    parser.add_argument("--merge_option", help="Comparison merge_option: left_only, right_only, both, default")
    parser.add_argument("--columns", help="Columns to exclude (space-separated indices)")
    parser.add_argument("--output", help="Output file name")

    return parser.parse_args()


def main(args, base_path):
    """
    Main function to compare two CSV files and find differences.

    Parameters:
        args (argparse.Namespace): Parsed command line arguments.
        base_path (str): Base path of the script.
    """
    comparator = DataComparator()  # Create an instance of the class

    if not args.file2:
        df = CSVHandler.read_csv(base_path, args.file1, args.delimiter)
        comparator.duplicates_dt(df, args.file1)
        df = df.drop_duplicates()
    else:
        df1 = CSVHandler.read_csv(base_path, args.file1, args.delimiter, args.columns)
        df2 = CSVHandler.read_csv(base_path, args.file2, args.delimiter, args.columns)

        print("Duplicates:")
        comparator.duplicates_dt(df1, args.file1)
        comparator.duplicates_dt(df2, args.file2)

        output_file = args.output or f'output_file_{args.merge_option}.csv'
        result = comparator.compare_dt(df1.drop_duplicates(), df2.drop_duplicates(),
                                       args.identifier, args.merge_option)

        print("\nSchemas:\n File1: {f1} {s1} \n File2: {f2} {s2} \n".format(
            f1=args.file1, s1=df1.shape, f2=args.file2, s2=df2.shape))

        result.groupby(['_merge'], observed=True).size()

        result = result[result.duplicated(args.identifier, keep=False)]

        print(f'The output with \'{args.merge_option.upper()}\' generates the following differences:\n')
        print(result[[args.identifier, '_merge']])

        df_no_join_col = result.drop('_merge', axis=1)
        differences = df_no_join_col.groupby(args.identifier).apply(comparator.find_differences,
                                                                    identifier=args.identifier).dropna()

        print_differences_details(differences, args)


if __name__ == '__main__':
    arguments = parse_args()
    path = os.path.dirname(os.path.realpath(__file__))
    main(arguments, path)
