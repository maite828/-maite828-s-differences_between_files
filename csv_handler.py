import os
import pandas as pd
from directory_manager import DirectoryManager


class CSVHandler:
    @staticmethod
    def read_csv(base_path, file_name, delimiter, cols_index=None, directory="input_files"):
        """
        Read a CSV file and return a DataFrame.

        Args:
            base_path (str): Base path for file operations.
            file_name (str): Name of the CSV file.
            delimiter (str): Delimiter used in the CSV file.
            cols_index (str): Indices of columns to exclude (space-separated indices).
            directory (str): Directory to read the CSV file from.

        Returns:
            pd.DataFrame: DataFrame containing the CSV data.
        """

        full_path = DirectoryManager.create_directory(base_path, directory)
        df = pd.read_csv(os.path.join(full_path, file_name), sep=delimiter, engine='python')

        if cols_index:
            df.drop(columns=df.columns[CSVHandler.convert_cols_index_list(cols_index)], inplace=True)

        return df

    @staticmethod
    def write_csv(df, base_path, file_name, delimiter, directory="output_files"):
        """
        Write a DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame to be written.
            base_path (str): Base path for file operations.
            file_name (str): Name of the CSV file.
            delimiter (str): Delimiter used in the CSV file.
            directory (str): Directory to write the CSV file to.

        Returns:
            None
        """
        full_path = DirectoryManager.create_directory(base_path, directory)
        file_path = os.path.join(full_path, file_name)
        df.to_csv(file_path, sep=delimiter, index=False)

    @staticmethod
    def handle_type(value):
        """
        Handle the data type of value.

        Args:
            value: Value to be handled.

        Returns:
            str or value: Handled value, converted to a string if applicable.
        """
        return str(value) if pd.notna(value) and not isinstance(value, list) else value

    @staticmethod
    def convert_cols_index_list(cols_index):
        """
        This method converts a string of columns indices to a list of integers.
        Args:
            cols_index (str): A string of columns indices.
        Returns:
            list: A list of integers.
        """
        # Convert cols_index to a list of integers
        if cols_index:
            cols_index_list = []
            for part in cols_index.split():
                if '-' in part:
                    cols_indices = [int(index) for index in part.split("-")]
                    cols_index_list.extend(cols_indices)
                else:
                    cols_index_list.append(int(part))
            cols_index = cols_index_list

        return cols_index
