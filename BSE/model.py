# model.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, X_train, y_train, batch_size=1, epochs=1):
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs)

if __name__ == "__main__":
    from data_collection import get_historical_data
    from preprocessing import preprocess_data

    data = get_historical_data("RELIANCE.BO", "2010-01-01", "2023-01-01")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(data)
    
    model = create_lstm_model((X_train.shape[1], 1))
    train_model(model, X_train, y_train)
    print("Model trained.")
