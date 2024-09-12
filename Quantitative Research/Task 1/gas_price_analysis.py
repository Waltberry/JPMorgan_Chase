import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def load_data(file_path):
    """
    Load the natural gas price data from a CSV file.
    Args:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: Dataframe containing the data.
    """
    data = pd.read_csv(file_path)
    data['Dates'] = pd.to_datetime(data['Dates'])
    data = data.sort_values(by='Dates')
    return data

def plot_prices(data):
    """Plot the natural gas prices over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(data['Dates'], data['Prices'], marker='o')
    plt.title('Natural Gas Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()

def analyze_seasonality(data):
    """Analyze and plot the seasonality in the price data."""
    data['Month'] = data['Dates'].dt.month
    monthly_avg = data.groupby('Month')['Prices'].mean()

    plt.figure(figsize=(8, 5))
    monthly_avg.plot(kind='bar')
    plt.title('Average Natural Gas Prices by Month')
    plt.xlabel('Month')
    plt.ylabel('Average Price')
    plt.show()

def extrapolate_future_prices(data, months=12):
    """
    Extrapolate future prices using linear regression.
    Args:
        data (pd.DataFrame): DataFrame containing the historical price data.
        months (int): Number of months to extrapolate into the future.
    Returns:
        pd.DataFrame: DataFrame containing future dates and predicted prices.
    """
    data['Time'] = np.arange(len(data))
    X = data['Time'].values.reshape(-1, 1)
    y = data['Prices'].values

    model = LinearRegression()
    model.fit(X, y)

    future_time = np.arange(len(data), len(data) + months).reshape(-1, 1)
    future_prices = model.predict(future_time)

    future_dates = pd.date_range(data['Dates'].max() + pd.DateOffset(months=1), periods=months, freq='M')

    # Plot the historical and extrapolated prices
    plt.figure(figsize=(10, 6))
    plt.plot(data['Dates'], data['Prices'], label='Historical Prices', marker='o')
    plt.plot(future_dates, future_prices, label='Extrapolated Prices', marker='x')
    plt.title('Natural Gas Price Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

    return pd.DataFrame({'Dates': future_dates, 'Prices': future_prices})

def estimate_price(data, input_date):
    """
    Estimate the price of natural gas on a specific date.
    Args:
        data (pd.DataFrame): DataFrame containing the historical price data.
        input_date (str): The date to estimate the price for.
    Returns:
        float: The estimated price.
    """
    # Convert input_date to a datetime object
    input_date = pd.to_datetime(input_date)

    # Add a column with ordinal date format (numerical representation of date)
    data['Date_ordinal'] = data['Dates'].apply(lambda x: x.toordinal())
    input_date_ordinal = input_date.toordinal()
    
    if data['Dates'].min() <= input_date <= data['Dates'].max():
        # Interpolate the price using ordinal dates
        return np.interp(input_date_ordinal, data['Date_ordinal'], data['Prices'])
    else:
        # Extrapolate using linear regression if date is out of bounds
        model = LinearRegression()
        X = data['Date_ordinal'].values.reshape(-1, 1)
        y = data['Prices'].values
        model.fit(X, y)

        # Predict the price for the input date
        return model.predict([[input_date_ordinal]])[0]