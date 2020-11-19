import os
from typing import Union, Iterable

import numpy as np
import pandas as pd

from FinalProject.Log.Logger import Logger


class PreprocessData:
    TEST_COLUMN = "marked_as_test"

    class PreprocessDataSettings:
        math_function = {'mean': np.nanmean, 'median': np.nanmedian, 'drop': None}

        def __init__(self):
            self.nan_math_function = None  # {column: function}
            self.drop_columns = False

        @staticmethod
        def manipulate(series: pd.Series, function):
            return function(series)

    def __init__(self, path: str, label="label", title="test"):
        self.path = path
        self.df = None
        self.label = label
        self.title = title
        self.X = None
        self.y = None
        self.smote = False
        self.filter_features = False

    def get_y(self) -> pd.Series:
        if self.y is None:
            return self.df[self.label]
        return self.y

    def get_X(self) -> pd.DataFrame:
        if self.X is None:
            return self.delete_column(self.df, self.label)
        return self.X

    @property
    def num_of_classes(self):
        return len(set(self.get_y()))

    def apply_smote(self):
        """
        if there is imbalance between classes, SMOTE is an intelligence way to avoid overfitting for one class only
        """
        from imblearn.over_sampling import SMOTE
        sm = SMOTE(random_state=42, k_neighbors=self.num_of_classes)
        try:
            self.X, self.y = sm.fit_sample(self.get_X(), self.get_y())
        except ValueError:
            Logger.print("Too many differences between the classes.")

    def filter_features(self, method):
        """
        function to drop unnecessary columns by median, mean or half
        """
        cor = self.df.corr()
        cor_target = abs(cor[self.label])
        if method == "mean":
            irrelevant_features = cor_target[cor_target < cor_target.mean()]
        elif method == "median":
            irrelevant_features = cor_target[cor_target < cor_target.median()]
        else:
            irrelevant_features = cor_target[cor_target < 0.5]
        self.df = self.delete_column(self.df, irrelevant_features)

    @staticmethod
    def delete_column(df: pd.DataFrame, columns: Union[str, Iterable]) -> pd.DataFrame:
        """
        :param df: Data frame
        :param columns: a column or columns to drop
        :return: a new Data frame
        """
        return df.drop(columns, axis=1)

    def one_hot_encode(self, columns: list = None, sparse_matrix: bool = False):
        """
        :param columns: columns to one hot (0/1)
        :param sparse_matrix: to sparse the matrix
        :return: a new Data frame
        """
        for column in columns:
            temp_df = pd.get_dummies(self.df[column], sparse=sparse_matrix, prefix=column)
            self.df = pd.concat([self.df, temp_df], axis=1)
            self.df = self.delete_column(self.df, column)

    def load_data_from_file(self):
        """
        this function reads file path to a dataframe data structure
        """
        if not os.path.isfile(self.path):
            raise FileNotFoundError("File not found!")
        if self.path.endswith("xls") or self.path.endswith("xlsx"):
            self.df = pd.read_excel(self.path, index_col=False)
        elif self.path.endswith("csv"):
            self.df = pd.read_csv(self.path, index_col=False)
        elif self.path.endswith("pkl"):
            self.df = pd.read_pickle(self.path)
        else:
            raise TypeError("File not supported! Only Excel, CSV and PKL!")

    def nan_handle(self, settings: PreprocessDataSettings) -> pd.DataFrame:
        """
        :param settings: set of nan's handle functions (math)
        :return: dataframe after manipulation
        """
        df = self.df.copy()
        if not settings.nan_math_function:
            return df
        for column, function in settings.nan_math_function:
            new_value = settings.manipulate(df[column], function)
            df[column] = df[column].fillna(new_value)
        if settings.drop_columns:
            df = df.dropna(how='any')
        return df

    def analyze_profile(self):
        """
        This function export an HTML file of data's report
        """
        from pandas_profiling import ProfileReport
        import webbrowser
        path_to_export = f"export/{self.title.lower()}.html"
        df_profiler = ProfileReport(self.df, title=self.title)
        df_profiler.to_file(path_to_export)
        webbrowser.open('file://' + os.path.realpath(path_to_export))

    def split_train_test(self):
        """
        A clever way to split train test by appearances
        """
        from random import choices
        percentage = 0.2
        long_tail = None
        temp_df = self.df.groupby([self.label])
        lst_to_test = []
        self.df[self.TEST_COLUMN] = False
        for pair, indexes in temp_df.groups.items():
            if len(indexes) >= (long_tail or 1 / percentage):
                item = choices(indexes, k=int(len(indexes) * percentage))
                lst_to_test.extend(item)
        for index in lst_to_test:
            self.df.at[index, self.TEST_COLUMN] = True
