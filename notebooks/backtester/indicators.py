"""
Technical indicators for backtesting.

This module provides functions to calculate various technical indicators
used in trading strategies.
"""

import pandas as pd
import numpy as np
from typing import Union


def bollinger_bands(
    data: pd.DataFrame, 
    price_column: str = 'midprice',
    window: int = 20, 
    num_std_dev: float = 2.0
) -> pd.DataFrame:
    """
    Calculate Bollinger Bands for a given DataFrame.
    
    The Bollinger Bands consist of:
    - Upper band: Moving average + (standard deviation * num_std_dev)
    - Lower band: Moving average - (standard deviation * num_std_dev)
    - Middle band: Moving average
    
    Parameters:
    data (pd.DataFrame): DataFrame containing financial data.
    price_column (str): Name of the column containing price data (default: 'midprice').
    window (int): The number of periods for the moving average and standard deviation (default: 20).
    num_std_dev (float): Number of standard deviations for the bands (default: 2.0).
    
    Returns:
    pd.DataFrame: DataFrame with Bollinger Bands columns added.
    
    Raises:
    ValueError: If the specified price column is not found in the DataFrame.
    """
    # Check if the price column exists
    if price_column not in data.columns:
        raise ValueError(f"Price column '{price_column}' not found in DataFrame")
    
    # Create a copy to avoid modifying the original data
    result_df = data.copy()
    
    # Calculate the rolling mean and standard deviation
    rolling_mean = result_df[price_column].rolling(window=window).mean()
    rolling_std = result_df[price_column].rolling(window=window).std()
    
    # Calculate the upper and lower Bollinger Bands
    result_df['upper_band'] = rolling_mean + (rolling_std * num_std_dev)
    result_df['lower_band'] = rolling_mean - (rolling_std * num_std_dev)
    
    # Calculate the middle band (moving average)
    result_df['middle_band'] = rolling_mean
    
    return result_df


def simple_moving_average(
    data: pd.Series, 
    window: int
) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA).
    
    Parameters:
    data (pd.Series): Price data series.
    window (int): Number of periods for the moving average.
    
    Returns:
    pd.Series: Simple moving average series.
    """
    return data.rolling(window=window).mean()


def exponential_moving_average(
    data: pd.Series, 
    window: int
) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA).
    
    Parameters:
    data (pd.Series): Price data series.
    window (int): Number of periods for the moving average.
    
    Returns:
    pd.Series: Exponential moving average series.
    """
    return data.ewm(span=window).mean()


def relative_strength_index(
    data: pd.Series, 
    window: int = 14
) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    Parameters:
    data (pd.Series): Price data series.
    window (int): Number of periods for RSI calculation (default: 14).
    
    Returns:
    pd.Series: RSI values.
    """
    # Calculate price changes
    delta = data.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=window).mean()
    avg_losses = losses.rolling(window=window).mean()
    
    # Calculate RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_volatility(
    data: pd.Series, 
    window: int = 20
) -> pd.Series:
    """
    Calculate rolling volatility (standard deviation).
    
    Parameters:
    data (pd.Series): Price data series.
    window (int): Number of periods for volatility calculation (default: 20).
    
    Returns:
    pd.Series: Rolling volatility values.
    """
    return data.rolling(window=window).std()


def price_change_percentage(
    data: pd.Series, 
    periods: int = 1
) -> pd.Series:
    """
    Calculate percentage price change.
    
    Parameters:
    data (pd.Series): Price data series.
    periods (int): Number of periods for the change calculation (default: 1).
    
    Returns:
    pd.Series: Percentage change values.
    """
    return data.pct_change(periods=periods) * 100
