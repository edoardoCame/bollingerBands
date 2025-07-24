"""
Test script for the Friday closing logic in the backtesting engine.

This script verifies that the backtest engine correctly:
1. Closes all positions in the last 15 minutes of trading on Fridays
2. Prevents new positions from opening during this time
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append('/home/edocame/Desktop/bollingerBands')

# Import the required modules
from modules.backtester.backtest_engine import Backtest
from modules.backtester import indicators

def generate_test_data():
    """
    Generate synthetic data to test the Friday closing logic.
    """
    # Create a date range spanning two weeks
    start_date = pd.Timestamp('2025-07-14')  # Monday
    end_date = pd.Timestamp('2025-07-25')  # Friday, next week
    
    # Create a minute-by-minute date range for forex (24 hours a day)
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        # Include all weekdays
        if current_date.weekday() < 5:  # 0-4 are Monday to Friday
            # Add entries for each minute throughout the day (24 hours)
            for hour in range(0, 24):
                for minute in range(0, 60):
                    dates.append(pd.Timestamp(
                        current_date.year, current_date.month, current_date.day,
                        hour, minute
                    ))
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    # Create a DataFrame with the date range as the index
    df = pd.DataFrame(index=dates)
    
    # Add fake market data
    n = len(df)
    
    # Generate a simulated price series that follows a random walk
    np.random.seed(42)  # For reproducibility
    price_changes = np.random.normal(0, 0.0005, n)
    price = 1.0 + np.cumsum(price_changes)
    
    # Create bid and ask prices with a small spread
    spread = 0.0002
    df['bid'] = price - spread/2
    df['ask'] = price + spread/2
    df['midprice'] = (df['bid'] + df['ask']) / 2
    
    # Calculate Bollinger Bands
    window = 20
    num_std_dev = 2.0
    df_with_bands = indicators.bollinger_bands(
        df, price_column='midprice', window=window, num_std_dev=num_std_dev
    )
    
    # Return the DataFrame with Bollinger Bands, dropping NaN values
    return df_with_bands.dropna()

def run_test():
    """
    Run the backtest with the synthetic data to test the Friday closing logic.
    """
    print("Generating test data...")
    data = generate_test_data()
    
    print(f"Data spans from {data.index.min()} to {data.index.max()}")
    print(f"Total rows: {len(data)}")
    
    # Find the Fridays in the data
    fridays = data[data.index.weekday == 4].index.normalize().unique()
    print(f"Fridays in the dataset: {fridays}")
    
    # Execute the backtest
    print("\nRunning backtest with Friday closing logic...")
    backtester = Backtest(data)
    backtester.run()
    
    # Get the trades DataFrame
    trades_df = backtester.get_trades_dataframe()
    
    print(f"\nTotal trades executed: {len(trades_df)}")
    
    # Check if there are any trades that were opened or remained open during the last 15 minutes of a Friday
    for friday in fridays:
        # Get data for this specific Friday
        friday_data = data[data.index.date == friday.date()]
        
        if len(friday_data) >= 15:
            # Get the last 15 minutes available for this Friday
            friday_close = friday_data.index[-15:]
            
            # Check if any trade was opened during this time
            if not trades_df.empty:
                opened_during_closing = any(
                    entry_idx for entry_idx in trades_df['Entry_idx'] 
                    if entry_idx < len(data) and data.index[entry_idx] in friday_close
                )
                
                print(f"\nFriday {friday.date()}")
                print(f"  Any trades opened during last 15 minutes: {'YES' if opened_during_closing else 'NO'}")
                
                # Check if any trade remained open past the cutoff time
                for i, trade in trades_df.iterrows():
                    entry_time = data.index[trade['Entry_idx']] if trade['Entry_idx'] < len(data) else None
                    exit_time = data.index[trade['Exit_idx']] if trade['Exit_idx'] < len(data) else None
                    
                    # If a trade was opened before the cutoff but closed after, check if it was closed exactly at the cutoff
                    if (entry_time is not None and entry_time.date() == friday.date() and
                            entry_time < friday_close[0] and exit_time in friday_close):
                        print(f"  Found trade closed at cutoff time: Entry={entry_time}, Exit={exit_time}")
                
                # Print the actual time of the last 15 minutes
                print(f"  Last 15 minutes period: {friday_close[0]} to {friday_close[-1]}")
    
    # Print backtest performance summary
    print("\nBacktest performance summary:")
    backtester.print_performance_summary()
    
    return trades_df, data

if __name__ == "__main__":
    trades, data = run_test()
    print("\nTest completed.")
