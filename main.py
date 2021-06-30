import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def score(y_true, y_pred):
    print("MSE:", mean_squared_error(y_true, y_pred))
    print("RMSE:", mean_squared_error(y_true, y_pred, squared=False))
    print("R2:", r2_score(y_true, y_pred))


data = pd.read_csv("data/laptops_clean.csv").drop("link", axis=1)

# Not Implemented
data = data[~data['gpu'].str.contains("\+")]


data['name'] = data['name'].str.split(expand=True)[0]
data['gpu company'] = data['gpu'].str.split(expand=True)[0]
data['cpu company'] = data['cpu'].str.split(expand=True)[0]
data['price'] = data['price'].astype(float)


label_columns = ['screen diagonal', 'screen resolution', 'cpu', 'ram', 'storage size', 'gpu']
data[label_columns] = data[label_columns].apply(LabelEncoder().fit_transform)

ohe_columns = ['storage type', 'gpu company', 'cpu company', 'name']
ohe_df = pd.get_dummies(data[ohe_columns])
data = pd.concat([data.drop(ohe_columns, axis=1), ohe_df], axis=1)


train_x, test_x, train_y, test_y = train_test_split(data.drop('price', axis=1),
                                                    data['price'],
                                                    test_size=0.25,
                                                    random_state=0)

model = RandomForestRegressor(n_jobs=4, random_state=0)
model.fit(train_x, train_y)
score(test_y, model.predict(test_x))