import os

import pandas as pd


class CSVHandler:
    @staticmethod
    def read_csv(path, delimiter, cols=None):
        df = pd.read_csv(path, sep=delimiter, engine='python')
        if cols:
            df.drop(df.columns[list(map(int, cols.split()))], axis=1, inplace=True)
        return df

    @staticmethod
    def write_csv(df, full_path, file_name):
        output_path = os.path.join(full_path, file_name)
        df.to_csv(output_path, index=False)
