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
        columns (str, list or slice): Columns to include in the printed output. It can be a single column name,
                                      a list of column names, or a slice (e.g., [0:5]).

    Returns:
        None
    """
    if not data.empty:
        if isinstance(columns, slice):
            # If 'columns' is a slice, use iloc to select the specified range of columns
            data_to_print = data.iloc[:, columns]
        else:
            # Otherwise, use the specified columns or all columns if 'columns' is None
            data_to_print = data[columns] if columns else data

        print(tabulate(data_to_print, headers='keys', tablefmt='psql'))


def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Compare two CSV files and find differences.")
    parser.add_argument('file1', help="Path to the first CSV file")
    parser.add_argument('--file2', help="Path to the second CSV file")
    parser.add_argument('delimiter', help="Delimiter used in CSV files")
    parser.add_argument('--identifier', help="Column(s) to order the results by")
    parser.add_argument('--merge_option', help="Comparison merge_option: left_only, right_only, both, default")
    parser.add_argument('--cols_index', help="Columns to exclude (space-separated indices)")
    parser.add_argument('--output', help="Output file name")

    return parser.parse_args()


def process_single_file(csv_handler, data_comparator, base_path, file_name, delimiter, cols):
    """
    Process a single CSV file: find duplicates and print details.

    Args:
        csv_handler (CSVHandler): Instance of CSVHandler class.
        data_comparator (DataComparator): Instance of DataComparator class.
        base_path (str): Base path of the script.
        file_name (str): Name of the CSV file.
        delimiter (str): Delimiter used in the CSV file.
        cols (str): Columns I want to show when reading the final file of duplicates.

    Returns:
        None
    """
    df = csv_handler.read_csv(base_path, file_name, delimiter)

    duplicates_file = f"duplicates_{file_name}"
    csv_handler.write_csv(data_comparator.duplicates_dt(df, file_name), base_path, duplicates_file, delimiter)

    # Print details of the duplicates
    duplicates = csv_handler.read_csv(base_path, duplicates_file, delimiter, directory="output_files")
    if cols:
        valid_range = CSVHandler.convert_cols_index_list(cols)
        print_table(duplicates, columns=slice(valid_range[0], valid_range[1]))
    else:
        print_table(duplicates)


def process_two_files(csv_handler, data_comparator, base_path, file1_name, file2_name, delimiter, identifier,
                      cols, output_file, merge_option):
    """
    Process two CSV files: compare them for differences and print details.

    Args:
        csv_handler (CSVHandler): Instance of CSVHandler class.
        data_comparator (DataComparator): Instance of DataComparator class.
        base_path (str): Base path of the script.
        file1_name (str): Path to the first CSV file.
        file2_name (str): Path to the second CSV file.
        delimiter (str): Delimiter used in the CSV files.
        identifier (str): Column(s) to identify rows for comparison.
        cols (str): Columns to exclude (space-separated indices).
        output_file (str): Output file name.
        merge_option (str): Comparison merge_option: left_only, right_only, both, default.

    Returns:
        None
    """

    df1 = csv_handler.read_csv(base_path, file1_name, delimiter, cols)
    df2 = csv_handler.read_csv(base_path, file2_name, delimiter, cols)

    print("Duplicates:")
    csv_handler.write_csv(data_comparator.duplicates_dt(df1, file1_name), base_path, f"duplicates_{file1_name}", delimiter)
    csv_handler.write_csv(data_comparator.duplicates_dt(df2, file2_name), base_path, f"duplicates_{file2_name}", delimiter)

    output_file = output_file or f'output_file_{merge_option}.csv'
    result = data_comparator.compare_dt(df1.drop_duplicates(), df2.drop_duplicates(), identifier, merge_option)

    csv_handler.write_csv(result, base_path, output_file, delimiter)

    print("\nSchemas:\n File1: {file1} {shape1} \n File2: {file2} {shape2} \n".format(
        file1=file1_name, shape1=df1.shape, file2=file2_name, shape2=df2.shape))

    result = result[result.duplicated(identifier, keep=False)]

    print(f'The output with \'{merge_option.upper()}\' generates the following differences:\n')
    print_table(result[[identifier, '_merge']])

    # Group by '_merge' column and count occurrences
    df_no_join_col = result.drop('_merge', axis=1)
    differences = df_no_join_col.groupby(identifier).apply(data_comparator.find_differences,
                                                           identifier=identifier).dropna()

    print_table(differences, [identifier, 'Column_Name', 'Left_Value', 'Right_Value'])


def main(arguments, base_path):
    """
    Main function to compare two CSV files and find differences.

    Args:
        arguments (argparse.Namespace): Parsed command line arguments.
        base_path (str): Base path of the script.

    Returns:
        None
    """
    # Create instances of classes
    csv_handler = CSVHandler()
    data_comparator = DataComparator()

    if not arguments.file2:
        process_single_file(csv_handler, data_comparator, base_path, arguments.file1, arguments.delimiter,
                            arguments.cols_index)
    else:
        process_two_files(csv_handler, data_comparator, base_path, arguments.file1, arguments.file2, arguments.delimiter,
                          arguments.identifier, arguments.cols_index, arguments.output, arguments.merge_option)


if __name__ == '__main__':
    command_line_args = parse_args()
    script_path = os.path.dirname(os.path.realpath(__file__))
    main(command_line_args, script_path)
