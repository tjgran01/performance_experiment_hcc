import pandas as pd
import scipy

import seaborn as sns

def parse_ht(ht, as_cm=True):
    ht_ = ht.split("'")
    ft_ = float(ht_[0])
    inches = float(ht_[1].replace("\"",""))
    if as_cm:
        return ((12*ft_) + inches) * 2.54
    return (12*ft_) + inches


def convert_to_float(x):

    return float(x)


class DataImporter(object):
    def __init__(self, data_dir="./data/", data_fname="eraser_test.csv",
                 using_sample=False, input_format="csv", demographics=False):
        self.using_sample = using_sample
        if input_format == "csv":
            self.data = self.read_in_csv_data(data_dir, data_fname)
            self.data = self.clean_data()
        if demographics == True:
            self.demographics = pd.read_csv(f"{data_dir}{data_fname[:-4]}_demographics.csv")
            self.demographics = self.clean_demographics()


    def read_in_csv_data(self, data_dir, data_fname):

        if not self.using_sample:
            data = pd.read_csv(f"{data_dir}{data_fname}")
        else:
            data = pd.read_csv(f"{data_dir}sample_data.csv")

        return data


    def clean_demographics(self):

        self.demographics["height_inches"] = self.demographics["height"].apply(lambda x:parse_ht(x, as_cm=False))
        self.demographics["height_centimeters"] = self.demographics["height"].apply(lambda x:parse_ht(x, as_cm=True))

        return self.demographics


    def clean_data(self):

        self.data["speed"] = self.data["speed"].apply(lambda x:convert_to_float(x))
        return self.data


    def combine_data(self):

        to_drop = ["group_x", "group_y"]

        combined = self.data.merge(self.demographics.set_index('par_id'), on='par_id')
        combined["group"] = combined["group_x"]
        combined = combined.drop(to_drop, axis=1)
        self.combined = combined


    def group_means(self, group_value="group", dep_variable="height_centimeters"):

        for elm in self.combined.groupby([f"{group_value}"]):
            print(elm[1][f"{dep_variable}"].describe())


    def return_plot(self, x="group", y="height_centimeters", plottype="box"):

        if plottype == "box":
            ax = sns.boxplot(x=x, y=y, data=self.combined)
        elif plottype == "reg":
            ax = sns.regplot(x=x, y=y, data=self.combined)
        elif plottype == "dist":
            ax = sns.distplot(self.combined[f"{x}"].tolist())
        return ax


    def run_ttest(self, )


if __name__ == "__main__":
    di = DataImporter(using_sample=True, demographics=True)
