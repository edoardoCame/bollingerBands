"""
Batch backtest for all *_MINUTEDATA.parquet forex files.
Loads each file, runs backtest with window=7200 and num_std_dev=0.5,
exports trades_df to BACKTESTED_STRATEGIES_RAW as CSV.
"""
import os
import sys
sys.path.append('/home/edocame/Desktop/bollingerBands')
from modules.backtester import data_loader, indicators, backtest_engine
import pandas as pd

# Directory containing minute data parquet files
DATA_DIR = '/media/edocame/HDD_2/data_python/03_BID_ASK_DATA'
# Output directory for backtested trades
OUTPUT_DIR = '/media/edocame/HDD_2/data_python/BACKTESTED_STRATEGIES_RAW'

# Backtest parameters
WINDOW = 20160
NUM_STD_DEV = 1
PRICE_COLUMN = 'midprice'

# Find all main *_MINUTEDATA.parquet files
parquet_files = [
    os.path.join(DATA_DIR, f)
    for f in os.listdir(DATA_DIR)
    if f.endswith('_MINUTEDATA.parquet') and not f.startswith('part')
]

for file_path in parquet_files:
    try:
        print(f"Processing {file_path}")
        # Load minute-level data
        minute_df = pd.read_parquet(file_path)
        # Ensure columns are lowercase
        minute_df.columns = [col.lower() for col in minute_df.columns]
        # Calculate Bollinger Bands
        data_with_bands = indicators.bollinger_bands(
            minute_df,
            price_column=PRICE_COLUMN,
            window=WINDOW,
            num_std_dev=NUM_STD_DEV
        )
        complete_data = data_with_bands.dropna()
        # Run backtest
        backtester = backtest_engine.Backtest(complete_data)
        backtester.run()
        trades_df = backtester.get_trades_dataframe()
        # Export trades_df to CSV
        base_name = os.path.basename(file_path).replace('_MINUTEDATA.parquet', '_trades.csv')
        output_path = os.path.join(OUTPUT_DIR, base_name)
        trades_df.to_csv(output_path, index=False)
        print(f"Exported trades to {output_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
