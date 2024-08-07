import numpy as np
import pandas as pd
from bsedata.bse import BSE
from data_collection import get_historical_data
from preprocessing import preprocess_data
from model import create_lstm_model, train_model

def get_bse_companies():
    b = BSE(update_codes=True)
    return list(b.getScripCodes().values())

def calculate_best_trade_period(stock_data, training_size, test_predictions, scaler):
    valid = stock_data[training_size:training_size + len(test_predictions)].copy()
    valid.loc[:, 'Predictions'] = scaler.inverse_transform(test_predictions)

    # Find the best buy and sell points
    min_price = valid['Predictions'].min()
    min_price_time = valid['Predictions'].idxmin()
    
    # After the minimum point, find the maximum price for selling
    post_min = valid.loc[min_price_time:]
    max_price = post_min['Predictions'].max()
    max_price_time = post_min['Predictions'].idxmax()
    
    profit = max_price - min_price

    best_trade = {
        'Best Buy Price': min_price,
        'Best Buy Time': min_price_time,
        'Best Sell Price': max_price,
        'Best Sell Time': max_price_time,
        'Profit': profit
    }

    return best_trade

if __name__ == "__main__":
    start_date = "2010-01-01"
    end_date = "2023-01-01"
    
    # Step 1: Get the list of BSE companies
    bse_companies = get_bse_companies()
    
    most_profitable_stock = {
        'Symbol': None,
        'Best Buy Price': 0,
        'Best Buy Time': None,
        'Best Sell Price': 0,
        'Best Sell Time': None,
        'Profit': -np.inf
    }
    
    for stock_symbol in bse_companies:
        try:
            # Step 2: Get the data
            data = get_historical_data(stock_symbol, start_date, end_date)
            if data is None or data.empty:
                continue

            # Step 3: Preprocess the data
            X_train, X_test, y_train, y_test, scaler = preprocess_data(data)
            
            # Step 4: Create and train the model
            model = create_lstm_model((X_train.shape[1], 1))
            train_model(model, X_train, y_train)
            
            # Step 5: Make predictions
            test_predictions = model.predict(X_test)
            test_predictions = scaler.inverse_transform(test_predictions)
            
            # Step 6: Calculate the best trade period
            training_size = int(len(data) * 0.75)
            best_trade = calculate_best_trade_period(data, training_size, test_predictions, scaler)
            
            # Step 7: Update the most profitable stock if necessary
            if best_trade['Profit'] > most_profitable_stock['Profit']:
                most_profitable_stock = {
                    'Symbol': stock_symbol,
                    'Best Buy Price': best_trade['Best Buy Price'],
                    'Best Buy Time': best_trade['Best Buy Time'],
                    'Best Sell Price': best_trade['Best Sell Price'],
                    'Best Sell Time': best_trade['Best Sell Time'],
                    'Profit': best_trade['Profit']
                }
        except Exception as e:
            print(f"An error occurred with stock {stock_symbol}: {e}")
            continue
    
    # Output the most profitable stock and its details
    print("Most Profitable Stock:", most_profitable_stock['Symbol'])
    print("Best Buy Price:", most_profitable_stock['Best Buy Price'])
    print("Best Buy Time:", most_profitable_stock['Best Buy Time'])
    print("Best Sell Price:", most_profitable_stock['Best Sell Price'])
    print("Best Sell Time:", most_profitable_stock['Best Sell Time'])
    print("Profit:", most_profitable_stock['Profit'])
