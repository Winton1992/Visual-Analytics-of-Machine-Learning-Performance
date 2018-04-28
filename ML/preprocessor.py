import pandas as pd
import datetime

class PreProcessor:

    def __init__(self):
        self.CURRENT_YEAR = int(datetime.date.isoformat(datetime.datetime.today())[0:4])
        self.failure_events = "static/csv/upload//pfail.csv"
        self.pipes = "static/csv/upload/pdata.csv"

    def update_data(self):
        data = self.dataframe_of_training_data()
        return data.to_csv("static/csv/data.csv", index=False)

    def dataframe_of_all_installations(self):
        df = pd.read_csv(self.pipes)
        return df

    def dataframe_of_failure_years(self):
        df = pd.read_csv(self.failure_events)
        return df

    def dataframe_of_training_data(self):
        installations = self.dataframe_of_all_installations()
        fails = self.dataframe_of_failure_years()
        part_id = PreProcessor.column_title_for("part_id")
        nd = pd.merge(fails, installations, how='outer', on=[part_id])
        nd = self.add_boolean_failure_to_csv_so_that_we_can_do_binary_classifier_for_fail_notfail_on_x(nd)
        failure_year = PreProcessor.column_title_for("failure_year")
        nd[failure_year] = nd[failure_year].fillna(self.CURRENT_YEAR)
        nd[failure_year] = nd[failure_year].astype(int)
        nd = PreProcessor.clean_header_names(nd)
        return nd

    def add_boolean_failure_to_csv_so_that_we_can_do_binary_classifier_for_fail_notfail_on_x(self, df):
        failure_year = PreProcessor.column_title_for("failure_year")
        has_failed = [1 if failure < self.CURRENT_YEAR else 0 for failure in df[failure_year]]
        has_failed = pd.DataFrame(has_failed, columns=['has_failed'])
        df = pd.concat([df, has_failed], axis=1)
        return df


    @staticmethod
    def attributes_from_str(self, attr_str):
        full_names = {
            "PY": "part_year",
            "FY": "failure_year",
            "DI": "diameter",
            "LN": "length",
            "PI": "part_id",
            "MT": "material"
        }
        attr_set = [full_names[i] for i in attr_str.split(',')]
        return attr_set

    @staticmethod
    def attributes_to_str(attr_set):
        abbreviations = {
            "part_year": "PY",
            "failure_year": "FY",
            "diameter": "DI",
            "length": "LN",
            "part_id": "PI",
            "material": "MT"
        }
        """reduce names to abbreviations"""
        attr_set = [abbreviations[i] for i in attr_set]

        attribs_key = ",".join(attr_set)
        return attribs_key

    @staticmethod
    def clean_header_names(df, reverse=False):
        c_names = PreProcessor.what_columns()
        if reverse:
            pass
        try:
            assert c_names == set([c for c in df.columns])
        except AssertionError as e:
            print("The input data contains attributes not accounted for in this model")
            print(e)
        df.columns = [c_names[col] for col in df.columns]
        return df

    @staticmethod
    def what_columns():
        cols = {
            'Part ID': 'part_id',
            'Failure_Year': 'failure_year',
            'Install Year': 'part_year',
            'Diameter Size': 'diameter',
            'Length': 'length',
            'Material': 'material',
            'has_failed': 'has_failed'
        }
        return cols

    @staticmethod
    def column_title_for(name):
        names = PreProcessor.what_columns()
        for key in names:
            if names[key] == name:
                return key