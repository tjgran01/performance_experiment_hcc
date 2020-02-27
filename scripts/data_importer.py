import pandas as pd

class DataImporter(object):
    def __init__(self, data_dir="./data/", data_fname="performance_data.csv",
                 using_sample=False, input_format="csv"):
        if input_format == ".csv":
            self.data = self.read_in_csv_data(data_dir, data_fname)
            



    def read_in_csv_data(self):

        if not self.using_sample:
            data_file = pd.read_csv(f"{data_dir}{data_fname}")
        else:
            data = pd.read_csv(f"{data_dir}sample_data.csv")

        return data


di = DataImporter(using_sample=True)
