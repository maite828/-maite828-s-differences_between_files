from csv_handler import CSVHandler
from directory_manager import DirectoryManager


class DataComparator:
    def __init__(self, base_path):
        self.base_path = base_path
        self.output_manager = DirectoryManager()
        self.csv_handler = CSVHandler()

    def print_duplicates(self, df, source_file):
        duplicates = df[df.duplicated()]
        num_duplicates = len(duplicates)
        print(f"{source_file} contains: {num_duplicates} duplicates")
        self.csv_handler.write_csv(duplicates, self.output_manager.create_directory(self.base_path, "output_files"),
                                   f"duplicates_{source_file}")

    def compare_datasets(self, df1, df2, output_file, identifier, merge_option):
        comparison_df = df1.merge(df2, indicator=True, how='outer')
        if merge_option == "default":
            diff_df = comparison_df[comparison_df['_merge'] != 'both'].copy()
        else:
            diff_df = comparison_df[comparison_df['_merge'] == merge_option].copy()
        diff_df.sort_values(identifier, inplace=True)
        self.csv_handler.write_csv(diff_df, self.output_manager.create_directory(self.base_path, "output_files"),
                                   output_file)
        return diff_df
