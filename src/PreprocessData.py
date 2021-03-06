import os
from typing import Union, Iterable

import sys
sys.path.append('FinalProject')

import numpy as np
import pandas as pd

from FinalProject.src.Log.Logger import Logger, Severity


class PreprocessData:
    TEST_COLUMN = "marked_as_test"

    class PreprocessDataSettings:
        math_function = {'mean': np.nanmean, 'median': np.nanmedian, 'common': None}

        def __init__(self, nan_math_function=None):
            self.nan_math_function = nan_math_function

        @classmethod
        def calculate(cls, function: str, series: pd.Series):
            return cls.math_function[function](series)

    def __init__(self, title, path=None, label="label"):
        self.path = path
        self.df = None
        self.label = label
        self.title = title
        self.path_to_export = f"static/export/{self.title.lower()}.html"

    def get_y(self) -> pd.Series:
        return self.df[~self.df[self.TEST_COLUMN]][self.label]

    def get_X(self) -> pd.DataFrame:
        return self.df[~self.df[self.TEST_COLUMN]].drop(self.label, axis=1)

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
            X, y = sm.fit_sample(self.get_X(), self.get_y())
            self.replace_x_y(X, y)
        except ValueError:
            Logger.print("Too many differences between the classes.", severity=Severity.WARNING)

    def replace_x_y(self, X_train, y_train):
        X = X_train.append(self.df[self.df[self.TEST_COLUMN]].drop(self.label, axis=1))
        y = y_train.append(self.df[self.df[self.TEST_COLUMN]][self.label])
        X[self.label] = y
        self.df = X

    def filter_features(self, method: str):
        """
        function to drop unnecessary columns by median, mean or half
        """
        if method == 'None':
            return
        df = self.df.copy()
        df = self.delete_column(df, [self.TEST_COLUMN])
        cor = df.corr()
        cor_target = abs(cor[self.label]).drop(self.label)
        if method == "mean":
            irrelevant_features = cor_target[cor_target < cor_target.mean()]
        elif method == "median":
            irrelevant_features = cor_target[cor_target < cor_target.median()]
        else:
            irrelevant_features = cor_target[cor_target < 0.5]
        self.df = self.delete_column(self.df, irrelevant_features.index)

    @staticmethod
    def delete_column(df: pd.DataFrame, columns: Union[str, Iterable]) -> pd.DataFrame:
        """
        :param df: Data frame
        :param columns: a column or columns to drop
        :return: a new Data frame
        """
        return df.drop(columns, axis=1)

    def one_hot_encode(self, sparse_matrix: bool = False):
        """
        :param sparse_matrix: to sparse the matrix
        :return: a new Data frame
        """
        columns = [column for column, dtype in self.df.dtypes.to_dict().items() if dtype == 'object' if
                   column not in {self.TEST_COLUMN, self.label}]
        for column in columns:
            temp_df = pd.get_dummies(self.df[column], sparse=sparse_matrix, prefix=column)
            self.df = pd.concat([self.df, temp_df], axis=1)
            self.df = self.delete_column(self.df, column)

    def is_data_splitted(self):
        return len(self.path) > 1

    def set_data(self):
        if self.is_data_splitted():
            train = self.load_data_from_file(self.train_path)
            train[self.TEST_COLUMN] = False
            test = self.load_data_from_file(self.test_path)
            test[self.TEST_COLUMN] = True
            self.df = train.append(test)
            self.df.reset_index(drop=True, inplace=True)
        else:
            self.df = self.load_data_from_file(self.train_path)

    @property
    def train_path(self):
        return self.path[0]

    @property
    def test_path(self):
        if self.is_data_splitted():
            return self.path[1]
        return None

    @staticmethod
    def load_data_from_file(path):
        """
        :param: path - file location in project
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found! - {path}")
        if path.endswith("xls") or path.endswith("xlsx"):
            return pd.read_excel(path, index_col=False)
        elif path.endswith("csv"):
            return pd.read_csv(path, index_col=False)
        elif path.endswith("pkl"):
            return pd.read_pickle(path)
        raise TypeError("File not supported! Only Excel, CSV and PKL!")

    def impute(self, settings: PreprocessDataSettings) -> pd.DataFrame:
        """
        :param settings: set of nan's handle functions (math)
        :return: dataframe after manipulation
        """
        df = self.df
        train, test = df[~df[self.TEST_COLUMN]].copy(), df[df[self.TEST_COLUMN]].copy()
        if settings.nan_math_function == 'common':
            columns_to_fill_common = [column for column in df if column not in {self.TEST_COLUMN, self.label}]
            for column in columns_to_fill_common:
                most_common = train[column].value_counts(ascending=False).idxmax()
                train[column] = train[column].fillna(most_common)
        elif settings.nan_math_function in settings.math_function:
            for column in train:
                new_value = settings.calculate(settings.nan_math_function, train[column])
                train[column] = train[column].fillna(new_value)
        df = train.append(test)
        df = df.dropna(how='any')
        return df

    def analyze_profile(self):
        """
        This function export an HTML file of data's report
        """
        from pandas_profiling import ProfileReport
        df_profiler = ProfileReport(self.df, title=self.title)
        df_profiler.to_file(self.path_to_export)

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
