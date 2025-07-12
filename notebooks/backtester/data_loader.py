"""
Data loading utilities for backtesting.

This module provides functions to load and preprocess tick data for backtesting purposes.
"""

import pandas as pd
from typing import List, Dict, Optional


def load_tick_data(file_path: str) -> pd.DataFrame:
    """
    Load tick data from a CSV file, parse dates and times, and set a datetime index.
    
    Parameters:
    file_path (str): The path to the CSV file containing tick data.
    
    Returns:
    pd.DataFrame: A DataFrame with a datetime index and tick data columns.
    
    Raises:
    FileNotFoundError: If the specified file path does not exist.
    ValueError: If the CSV file has an unexpected format.
    """
    try:
        # Define column names based on the file structure
        column_names: List[str] = ['date', 'time', 'bid', 'ask', 'last', 'volume', 'flags']
        
        # Read the CSV file, specifying the tab separator and skipping the header
        df = pd.read_csv(file_path, sep='\t', header=0, names=column_names, skiprows=1)
        
        # Convert date and time columns to a single datetime column
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        
        # Set the new datetime column as the index
        df.set_index('datetime', inplace=True)
        
        # Drop the original date and time columns
        df.drop(['date', 'time'], axis=1, inplace=True)
        
        return df
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading tick data: {str(e)}")


def load_parquet_data(file_path: str) -> pd.DataFrame:
    """
    Load tick data from a Parquet file.
    
    Parameters:
    file_path (str): The path to the Parquet file containing tick data.
    
    Returns:
    pd.DataFrame: A DataFrame with tick data.
    
    Raises:
    FileNotFoundError: If the specified file path does not exist.
    ValueError: If the Parquet file has an unexpected format.
    """
    try:
        df = pd.read_parquet(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading parquet data: {str(e)}")


def prepare_minute_data(
    tick_data: pd.DataFrame, 
    resample_rule: str = '1T'
) -> pd.DataFrame:
    """
    Resample tick data to minute intervals and calculate midprice.
    
    Parameters:
    tick_data (pd.DataFrame): DataFrame containing tick data with 'bid' and 'ask' columns.
    resample_rule (str): Resampling rule (default: '1T' for 1-minute intervals).
    
    Returns:
    pd.DataFrame: Resampled DataFrame with 'bid', 'ask', and 'midprice' columns.
    
    Raises:
    ValueError: If required columns are missing from the input DataFrame.
    """
    # Check if required columns exist
    required_columns = ['bid', 'ask']
    missing_columns = [col for col in required_columns if col not in tick_data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Resample tick_data to specified intervals, taking the first non-null bid and ask
    minute_sample = tick_data.resample(resample_rule).agg({'bid': 'first', 'ask': 'first'})
    
    # Calculate midprice
    minute_sample['midprice'] = (minute_sample['bid'] + minute_sample['ask']) / 2
    
    # Remove rows with NaN values
    minute_sample_clean = minute_sample.dropna()
    
    return minute_sample_clean


def load_balance_data(file_path: str) -> pd.DataFrame:
    """
    Load balance data from CSV file for comparison with backtest results.
    
    Parameters:
    file_path (str): The path to the CSV file containing balance data.
    
    Returns:
    pd.DataFrame: A DataFrame with datetime index and balance data.
    
    Raises:
    FileNotFoundError: If the specified file path does not exist.
    ValueError: If the CSV file has an unexpected format.
    """
    try:
        # Read the balance file
        dft = pd.read_csv(file_path, sep='\t', encoding='utf-16')
        
        # Convert date column to datetime and set as index
        dft['<DATE>'] = pd.to_datetime(dft['<DATE>'])
        dft.set_index('<DATE>', inplace=True)
        
        return dft
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading balance data: {str(e)}")
