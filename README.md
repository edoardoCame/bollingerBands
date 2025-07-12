# Repository Structure

```
bollingerBands/
├── DATA/
│   ├── audjpy_1440_01.csv
## Bollinger Bands Backtesting & Analysis Suite

This repository provides a modular Python framework for backtesting trading strategies, with a focus on Bollinger Bands and advanced financial data analysis. It includes:

- A robust backtesting engine
- Technical indicator calculations
- Data loaders for tick, minute, and balance data
- Visualization tools (matplotlib, plotly)
- Jupyter notebooks for research, optimization, and reporting

## Project Structure

```
bollingerBands/
├── DATA/                # Raw and processed market data (CSV)
├── notebooks/           # Jupyter notebooks for analysis, optimization, and reporting
│   ├── backtester/      # Backtesting library and usage examples
│   ├── MT5 REPORTS/     # MetaTrader 5 analysis notebooks
│   ├── risk management/ # Risk management and filter notebooks
│   └── temp tools/      # Temporary tools and scripts
├── README.md            # Project overview (this file)
```

## Key Features
- Modular backtesting engine for mean-reversion strategies
- Bollinger Bands and other technical indicators
- Performance metrics: Sharpe ratio, drawdown, win/loss, etc.
- Parameter optimization and walk-forward analysis
- Interactive and static visualizations
- Comparison with real trading results

## Installation & Dependencies

Install required Python packages:

```bash
pip install pandas numpy matplotlib plotly numba
```

## Usage

See the Jupyter notebooks in `notebooks/backtester/` for end-to-end examples:

1. Load and preprocess data (tick, minute, or balance)
2. Calculate technical indicators (e.g., Bollinger Bands)
3. Run backtests and analyze results
4. Visualize performance and compare with real data

Example usage:

```python
from backtester import data_loader, indicators, backtest_engine, visualization
data = data_loader.load_parquet_data('path/to/data.parquet')
minute_data = data_loader.prepare_minute_data(data)
data_with_bands = indicators.bollinger_bands(minute_data, window=1440, num_std_dev=1.0)
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()
trades_df = backtester.get_trades_dataframe()
visualization.plot_cumulative_pnl(trades_df)
```

## Contributing

Contributions are welcome! Please:
- Follow PEP 8 and the project’s Python coding conventions
- Add docstrings and comments to all new functions
- Include tests for new features
- Document changes in the relevant README

## License

MIT License
