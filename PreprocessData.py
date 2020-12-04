import os
from typing import Union, Iterable

import numpy as np
import pandas as pd
from FinalProject.Log.Logger import Logger


class PreprocessData:
    TEST_COLUMN = "marked_as_test"

    class PreprocessDataSettings:
        math_function = {'mean': np.nanmean, 'median': np.nanmedian, 'drop': None}

        def __init__(self, drop_columns=False):
            self.nan_math_function = dict()  # {column: function}
            self.drop_columns = drop_columns

        @staticmethod
        def manipulate(series: pd.Series, function):
            return function(series)

    def __init__(self, path: list, label="label", title="test"):
        self.path = path
        self.df = None
        self.label = label
        self.title = title
        self.X = None
        self.y = None
        self.smote = False
        self._filter_features = False

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
            self.replace_x_y()
        except ValueError:
            Logger.print("Too many differences between the classes.")

    def replace_x_y(self):
        self.df = self.X
        self.df[self.label] = self.y

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
            self.split_train_test()

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

    def nan_handle(self, settings: PreprocessDataSettings) -> pd.DataFrame:
        """
        :param settings: set of nan's handle functions (math)
        :return: dataframe after manipulation
        """
        df = self.df.copy()
        if settings.nan_math_function:
            for column, function in settings.nan_math_function.items():
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


if __name__ == '__main__':
    from collections import Counter
    pp = PreprocessData(path=['data/train.csv', 'data/test.csv'], label='Pclass')
    pp.set_data()
    pp.df = pp.delete_column(pp.df, ['PassengerId', 'Name', 'Cabin', 'Ticket'])
    pp.one_hot_encode(['Sex', 'Embarked'])
    pp_settings = PreprocessData.PreprocessDataSettings(drop_columns=True)
    pp.df = pp.nan_handle(pp_settings)
    print(Counter(pp.df[pp.label]))
    pp.apply_smote()
    print(Counter(pp.df[pp.label]))
