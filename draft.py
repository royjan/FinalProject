from DataManager import DataManagement
from PreprocessData import PreprocessData

if __name__ == '__main__':
    pp = PreprocessData("data/username.csv", "Username")
    pp.load_data_from_file()
    pp.analyze_profile()
    dm = DataManagement(pp)
    dm.upload_to_db()

