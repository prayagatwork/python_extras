# preprocessing.py
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def create_dataset(data, time_step=1):
    dataX, dataY = [], []
    for i in range(len(data) - time_step - 1):
        a = data[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(data[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

def preprocess_data(stock_data, time_step=100):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data)

    X, y = create_dataset(scaled_data, time_step)

    training_size = int(len(X) * 0.75)
    X_train, X_test = X[0:training_size], X[training_size:len(X)]
    y_train, y_test = y[0:training_size], y[training_size:len(y)]

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    return X_train, X_test, y_train, y_test, scaler

if __name__ == "__main__":
    from data_collection import get_historical_data
    data = get_historical_data("RELIANCE.BO", "2010-01-01", "2023-01-01")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(data)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
