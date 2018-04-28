import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import sklearn.metrics as metrics
import json as Jason
from itertools import combinations
import math
import datetime
from pathlib import Path
from ML.preprocessor import PreProcessor


INPUT_CSV = "static/csv/data.csv"
CATEGORICAL_ATTRIBS = ['part_id', 'diameter', 'material']
CONTINUOUS_ATTRIBS = ['part_year', 'failure_year', 'length']
Y_label = 'has_failed'
CURRENT_YEAR = int(datetime.date.isoformat(datetime.datetime.today())[0:4])
MODEL_DATA_SHAPE = dict()
MIN_FAILURE_YEAR = 1950
MAX_PREDICTION_RANGE = 100


def brute_force(attributes):
    """Return all possible combinations of attributes
    that may be considered as an input strategy"""
    bf_combinations = []
    for length_option in range(1, len(attributes)):
        bf_combinations.extend([list(x) for x in combinations(attributes, length_option)])

    return bf_combinations

def split_test_data(X, Y):
    """Select out a third of the events
    randomly so that test data is similar in
    distribution to the training data"""
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.33, random_state=5
    )
    return (X_train, X_test, Y_train, Y_test)

def encode_categorical_attributes(df, categorical_attribs, training_data=False):
    """Translates categorical data columns into
    a binary matrix"""

    cat_dfs = dict()
    for attrib in categorical_attribs:
        categories = df[attrib].unique()
        if training_data:
            MODEL_DATA_SHAPE[attrib] = len(categories)
        category_column = dict()
        for i,category in enumerate(categories):
            category_column[category] = i
        binary_data = np.zeros((len(df[attrib]), MODEL_DATA_SHAPE[attrib]))
        for i, evnt in enumerate(df[attrib]):
            try:
                binary_data[i][category_column[evnt]] = 1
            except Exception:
                pass

        df_attrib = pd.DataFrame(binary_data)
        cat_dfs[attrib] = df_attrib
    return cat_dfs

def get_input_matrix(attribs, categorical_attribs, data, categorical_data):
    dfs = list()
    for attrib in attribs:
        if attrib in categorical_attribs:
            dfs.append(pd.DataFrame(data=categorical_data[attrib]))
        else:
            dfs.append(pd.DataFrame(data[attrib]))
    c_df = pd.concat(dfs, axis=1)
    return c_df

def train_model(train_x, train_y):
    lm = MLPClassifier(solver='adam', random_state=0)
    lm.fit(train_x, train_y)
    return lm

def compare_ML_results(DATA, CATEGORICAL_DATA, CATEGORICAL_ATTRIBS, Y):
    """Returns a dictionary of the attributes used (tuple):
    and the respective mean square error, when predicting
    over the test data"""

    attributes = np.concatenate([DATA.keys(), CATEGORICAL_ATTRIBS], axis=0)
    performances = list()
    for attr_set in brute_force(attributes)[:]:

        X = get_input_matrix(attr_set, CATEGORICAL_ATTRIBS, DATA, CATEGORICAL_DATA)

        train_x, test_x, train_y, test_y = split_test_data(X, Y)

        model = train_model(train_x, train_y)

        predicted = model.predict(test_x)

        performance = metrics.accuracy_score(y_true=test_y, y_pred=predicted)

        attribs_key = PreProcessor.attributes_to_str(attr_set)

        performances.append({
            "combination": attribs_key,
            "accuracy": math.trunc(performance * 100)
        })
    return performances

def results(input_csv=INPUT_CSV):
    df = pd.read_csv(input_csv)
    Y = df[Y_label]
    DATA = df.drop(np.concatenate([[Y_label], CATEGORICAL_ATTRIBS], axis=0), axis=1)
    CATEGORICAL_DATA = encode_categorical_attributes(df, CATEGORICAL_ATTRIBS, training_data=True)
    results = compare_ML_results(DATA, CATEGORICAL_DATA, CATEGORICAL_ATTRIBS, Y)
    # print(results)
    return results

def predictions(attrib_list, input_csv=INPUT_CSV,
                failure_year=MIN_FAILURE_YEAR,
                prediction_range=MAX_PREDICTION_RANGE):
    results_title = "failures_mlp_year%d_range%d_attr_%s"%(failure_year,prediction_range,attrib_list)
    file = "ML/predicted_failures/%s.csv"%results_title

    result_file = Path(file)
    if not result_file.is_file():

        attrib_list = PreProcessor.attributes_from_str(attrib_list)
        if not attrib_list.__contains__('failure_year'):
            attrib_list.append('failure_year')
        df = pd.read_csv(input_csv)
        DATA = df.drop(np.concatenate([[Y_label], CATEGORICAL_ATTRIBS], axis=0), axis=1)
        CATEGORICAL_DATA = encode_categorical_attributes(df, CATEGORICAL_ATTRIBS, training_data=True)
        X = get_input_matrix(attrib_list, CATEGORICAL_ATTRIBS, DATA, CATEGORICAL_DATA)

        Y = df[Y_label]
        model = train_model(X, Y)

        df = pd.read_csv(input_csv)
        yet_to_fail = pd.DataFrame(data=df[df.has_failed == 0]).reset_index(drop=True)
        cat_attribs = []
        for attr in attrib_list:
            if attr in CATEGORICAL_ATTRIBS:
                cat_attribs.append(attr)
        CATEGORICAL_DATA = encode_categorical_attributes(yet_to_fail, CATEGORICAL_ATTRIBS)
        DATA = yet_to_fail.drop(np.concatenate([[Y_label], CATEGORICAL_ATTRIBS], axis=0), axis=1)
        X = get_input_matrix(attrib_list, cat_attribs, DATA, CATEGORICAL_DATA)

        for i,event in enumerate(yet_to_fail.itertuples()):
            part_year = None
            try:
                part_year = int(event.part_year)
            except Exception:
                part_year = failure_year
            for pred_year in range(failure_year,failure_year + prediction_range):
                yet_to_fail.loc[i, 'failure_year'] = pred_year
                X.loc[i, 'failure_year'] = pred_year
                prediction = model.predict(X.iloc[[i]])[0]
                if prediction:
                    yet_to_fail.loc[i, 'has_failed'] = 1
                    break
        will_fail = yet_to_fail[yet_to_fail.has_failed == 1]
        will_fail = will_fail.drop(['has_failed'], axis=1)
        # print(will_fail.head())
        will_fail.to_csv(file, index=False)
        return Jason.dumps(will_fail.to_json(orient='index'))
    return Jason.dumps(pd.read_csv(file).to_json(orient='index'))

