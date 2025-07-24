# Friday Market Closing Feature

## Overview

The Friday market closing feature automatically closes all open positions during the last 15 minutes of available data on Fridays and prevents new positions from opening during this time window. Since forex markets operate 24 hours, this feature uses the last 15 minutes of available price data for each Friday. This feature helps traders:

1. Avoid weekend gap risk
2. Ensure all positions are closed before the weekend
3. Prevent new positions from being opened just before the weekend

## Implementation Details

The feature is implemented in the core backtesting engine (`backtest_engine.py`):

- Each minute bar is analyzed to determine if it falls within the last 15 minutes of trading on a Friday
- If a position is open during this time, it is automatically closed
- No new positions are allowed to open during this time window

## Usage

The feature is automatically enabled in the backtesting engine. No additional configuration is required.

```python
from modules.backtester import data_loader, indicators, backtest_engine

# Load and prepare data
data = data_loader.load_parquet_data('your_data.parquet')
minute_data = data_loader.prepare_minute_data(data)

# Calculate Bollinger Bands
data_with_bands = indicators.bollinger_bands(
    minute_data, 
    window=1440,
    num_std_dev=1.0
)

# Run backtest - Friday closing logic is automatically applied
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()
```

## Verification

To verify the Friday closing feature is working as expected:

1. Run the `test_friday_closing.py` script
2. Check the backtest results to confirm:
   - No trades are opened during the last 15 minutes of Fridays
   - Any open positions are closed before the market closes on Fridays

```bash
python test_friday_closing.py
```

## Technical Implementation

The feature works by:

1. Identifying all Fridays in the dataset
2. For each Friday, finding the last 15 minutes of available price data
3. Creating a marker array for these periods
4. Using this marker to:
   - Force close any open positions when entering this time window
   - Prevent new positions from opening during this time

The implementation is optimized with Numba to maintain high performance and works with any forex dataset, regardless of the specific market hours in the data.
