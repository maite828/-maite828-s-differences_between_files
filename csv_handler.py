import os
import pandas as pd
from directory_manager import DirectoryManager


class CSVHandler:
    @staticmethod
    def read_csv(base_path, file_name, delimiter, cols=None, directory="input_files"):
        """
        Read a CSV file and return a DataFrame.

        Args:
            base_path (str): Base path for file operations.
            file_name (str): Name of the CSV file.
            delimiter (str): Delimiter used in the CSV file.
            cols (str): Columns to exclude (space-separated indices).
            directory (str): Directory to read the CSV file from.

        Returns:
            pd.DataFrame: DataFrame containing the CSV data.
        """
        full_path = DirectoryManager.create_directory(base_path, directory)
        file_path = os.path.join(full_path, file_name)
        df = pd.read_csv(file_path, sep=delimiter, engine='python')

        # Exclude specified columns
        if cols:
            df.drop(columns=df.columns[list(map(int, cols.split()))], inplace=True)

        return df

    @staticmethod
    def write_csv(df, base_path, file_name, directory="output_files"):
        """
        Write a DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame to be written.
            base_path (str): Base path for file operations.
            file_name (str): Name of the CSV file.
            directory (str): Directory to write the CSV file to.

        Returns:
            None
        """
        full_path = DirectoryManager.create_directory(base_path, directory)
        file_path = os.path.join(full_path, file_name)
        df.to_csv(file_path, index=False)

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
