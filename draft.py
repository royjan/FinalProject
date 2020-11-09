# from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
# # from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
#
payload = {
    "class_name": "ScikitSolver",
    "model": "LinearRegression",
}# from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
#
# from DataManager import DataManagement
# from PreprocessData import PreprocessData
#
# if __name__ == '__main__':
#     pp = PreprocessData("data/username.csv", "Username")
#     pp.load_data_from_file()
#     pp.analyze_profile()
#     dm = DataManagement()
#     dm.set_data_from_preprocess_object(pp)
#     dm.df_to_db()
#
#
from FinalProject.CeleryWorkerTask import train
z = train.s(x=[[1, 2, 3], [3, 4, 5], [5, 6, 7]], y=[1, 3, 5], config=payload).apply_async(queue='test')
print(z)

