# !/usr/bin/env python3
import os
import argparse
from tabulate import tabulate

from data_comparator import DataComparator
from csv_handler import CSVHandler


def print_table(data, columns=None):
    """
    Print details of a DataFrame in a tabular format.

    Args:
        data (pd.DataFrame): DataFrame to be printed.
        columns (list): List of columns to include in the printed output.

    Returns:
        None
    """
    if not data.empty:
        print(tabulate(data[columns] if columns else data,
                       headers='keys', tablefmt='psql'))


def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
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


def process_single_file(csv_handler, data_comparator, arguments, base_path):
    df = csv_handler.read_csv(base_path, arguments.file1, arguments.delimiter)
    duplicates_file = f"duplicates_{arguments.file1}"
    csv_handler.write_csv(data_comparator.duplicates_dt(df, arguments.file1), base_path, duplicates_file)
    print_table(csv_handler.read_csv(base_path, duplicates_file, arguments.delimiter, arguments.columns, "output_files"))


def process_two_files(csv_handler, data_comparator, arguments, base_path):
    df1 = csv_handler.read_csv(base_path, arguments.file1, arguments.delimiter, arguments.columns)
    df2 = csv_handler.read_csv(base_path, arguments.file2, arguments.delimiter, arguments.columns)

    print("Duplicates:")
    csv_handler.write_csv(data_comparator.duplicates_dt(df1, arguments.file1), base_path, f"duplicates_{arguments.file1}")
    csv_handler.write_csv(data_comparator.duplicates_dt(df2, arguments.file2), base_path, f"duplicates_{arguments.file2}")

    output_file = arguments.output or f'output_file_{arguments.merge_option}.csv'
    result = data_comparator.compare_dt(df1.drop_duplicates(), df2.drop_duplicates(), arguments.identifier, arguments.merge_option)
    csv_handler.write_csv(result, base_path, output_file)

    print("\nSchemas:\n File1: {file1} {shape1} \n File2: {file2} {shape2} \n".format(
        file1=arguments.file1, shape1=df1.shape, file2=arguments.file2, shape2=df2.shape))

    result = result[result.duplicated(arguments.identifier, keep=False)]

    print(f'The output with \'{arguments.merge_option.upper()}\' generates the following differences:\n')
    print_table(result[[arguments.identifier, '_merge']])

    df_no_join_col = result.drop('_merge', axis=1)
    differences = df_no_join_col.groupby(arguments.identifier).apply(data_comparator.find_differences,
                                                                    identifier=arguments.identifier).dropna()

    print_table(differences, [arguments.identifier, 'Column_Name', 'Left_Value', 'Right_Value'])


def main(arguments, base_path):
    csv_handler = CSVHandler()
    data_comparator = DataComparator()

    if not arguments.file2:
        process_single_file(csv_handler, data_comparator, arguments, base_path)
    else:
        process_two_files(csv_handler, data_comparator, arguments, base_path)


if __name__ == '__main__':
    command_line_args = parse_args()
    script_path = os.path.dirname(os.path.realpath(__file__))
    main(command_line_args, script_path)
