import os

import pandas as pd

from directory_manager import DirectoryManager


class CSVHandler:

    @staticmethod
    def read_csv(base_path, file_name, delimiter, cols=None, directory="input_files"):
        full_path = DirectoryManager.create_directory(base_path, directory)
        df = pd.read_csv(os.path.join(full_path, file_name), sep=delimiter, engine='python')
        if cols:
            df.drop(df.columns[list(map(int, cols.split()))], axis=1, inplace=True)
        return df

    @staticmethod
    def write_csv(df, base_path, file_name, directory="output_files"):
        full_path = DirectoryManager.create_directory(base_path, directory)
        df.to_csv(os.path.join(full_path, file_name), index=False)

    @staticmethod
    def handle_type(self):
        return str(self) if pd.notna(self) and not isinstance(self, list) else self
