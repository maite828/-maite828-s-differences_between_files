#!/usr/bin/env python3
import os
import argparse
from tabulate import tabulate

from data_comparator import DataComparator
from csv_handler import CSVHandler


def print_differences_details(differences, argument):
    if not differences.empty:
        print("\nDetails on differences:")
        print(tabulate(differences[[argument.identifier, 'Column_Name', 'Left_Value', 'Right_Value']],
                       headers='keys', tablefmt='psql'))


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


def main(args, base_path):
    if not args.file2:
        df = CSVHandler.read_csv(base_path, args.file1, args.delimiter)
        comparator = DataComparator()
        CSVHandler.write_csv(comparator.duplicates_dt(df, args.file1), base_path, f"duplicates_{args.file1}")
        # df.drop_duplicates()
        duplicates = CSVHandler.read_csv(base_path, f"duplicates_{args.file1}", args.delimiter, args.columns, "output_files")
        print(tabulate(duplicates, headers='keys', tablefmt='psql'))
    else:
        df1 = CSVHandler.read_csv(base_path, args.file1, args.delimiter, args.columns)
        df2 = CSVHandler.read_csv(base_path, args.file2, args.delimiter, args.columns)

        print("Duplicates:")
        comparator = DataComparator()
        CSVHandler.write_csv(comparator.duplicates_dt(df1, args.file1), base_path, f"duplicates_{args.file1}")
        CSVHandler.write_csv(comparator.duplicates_dt(df2, args.file2), base_path, f"duplicates_{args.file2}")

        output_file = args.output or f'output_file_{args.merge_option}.csv'
        result = comparator.compare_dt(df1.drop_duplicates(), df2.drop_duplicates(), args.identifier, args.merge_option)
        CSVHandler.write_csv(result, base_path, output_file)

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
