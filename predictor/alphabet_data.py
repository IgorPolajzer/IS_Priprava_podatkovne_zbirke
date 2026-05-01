import glob
import os
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split

class AlphabetData:

    def __init__(self, file_name):
        self.folder_name = file_name
        self.X = None  # Features
        self.y = None  # Labels

    def load_and_parse(self) -> tuple[Any, Any]:
        # Get all csv files from folder.
        path = os.path.join(self.folder_name, "*.csv")
        all_files = glob.glob(path)

        if not all_files:
            raise FileNotFoundError(f"V mapi {self.folder_name} ni bilo najdenih CSV datotek.")

        df_list = [pd.read_csv(f, header=None) for f in all_files]
        df = pd.concat(df_list, ignore_index=True)

        self.X = df.iloc[:, :-1] # All rows and ONLY the last column (Labels)
        self.y = df.iloc[:, -1] # All columns EXCEPT the last one (Features)

        return self.X, self.y

    def get_train_test(self, test_size=0.3):
        self.load_and_parse()
        return train_test_split(self.X, self.y, test_size=test_size, random_state=42)
