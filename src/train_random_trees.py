from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from math import floor
import numpy as np
import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn import metrics
from sklearn.model_selection import cross_val_score


traindata_path = os.getcwd() + "/data/normalized.csv"


def train_and_test():
    df = pd.read_csv(traindata_path)
    df_failures = df[df.days_to_failure != -1]
    df_working = df[df.days_to_failure == -1]
    df_working = df_working.sample(n=floor((df_failures.shape[0])/5))
    df_failures['bin'] = pd.qcut(df_failures['days_to_failure'], q=5, labels=False)
    print(df_failures)
    df = pd.concat([df_working, df_failures])
    dataset = df.values

    # Create the feature dataset X (date / serial number not yet included, needs to be embedded first)
    X = dataset[:, 2:6]
    X = np.asarray(X).astype('float32')

    # Create the label dataset
    Y = dataset[:,9]
    Y = np.asarray(Y).astype('float32')

    # Split into training, validation and test dataset
    X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X, Y, test_size=0.3)
    X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)

    #  X_train / Y_train (70% of full dataset)     Training Set
    #  X_val / Y_val (15% of full dataset)         Validation Set
    #  X_test / Y_test (15% of full dataset)       Test Set

    print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, Y_test.shape)

    regressor = RandomForestRegressor(n_estimators=100, random_state=0)
    regressor.fit(X_train, Y_train)
    Y_pred = regressor.predict(X_test)

    Y_pred = np.round(Y_pred, 0)

    print('Accuracy:', metrics.accuracy_score(Y_test, Y_pred))
    print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, Y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(Y_test, Y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))


if __name__ == "__main__":
    train_and_test()
