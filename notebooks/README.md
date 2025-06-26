

# Notebooks

This folder contains all Jupyter notebooks for the analysis, experimentation, and optimization of Bollinger Bands trading strategies. Each notebook addresses a specific aspect of the project, from parameter optimization to execution analysis, order handling, and practical usage. The project emphasizes GPU-accelerated processing using cuDF and cuML libraries.

## Notebook Descriptions

- **Asset_Explore.ipynb**: Explores and visualizes asset data, providing insights into price behavior and volatility before strategy development. Analyzes the currency pairs available in the data folder.

- **bollinger_backtester.ipynb**: Implements and validates the Bollinger Bands strategy using the Backtrader library. Provides comparison and validation against custom implementations with comprehensive performance metrics.

- **execution_delay_test.ipynb**: Evaluates the effect of order execution delays on strategy performance, simulating realistic market conditions to assess robustness and slippage impact.

- **grid_search_optimization.ipynb**: Performs a comprehensive grid search to optimize Bollinger Bands parameters, identifying the best-performing parameter sets for the strategy using GPU-accelerated processing.

- **manual.ipynb**: User guide for the project, with detailed instructions, practical examples, and explanations of main functions and workflows.

- **mkt orders.ipynb**: Investigates the handling and execution of market orders, comparing them to other order types with hands-on examples and performance analysis.

- **mt5_analysis.ipynb**: Analyzes real trading data exported from MetaTrader 5 (MT5) for the EUR/GBP currency pair. Includes outlier detection, trade duration analysis, and performance visualization of actual trading results.

- **tick_backtest.ipynb**: Runs tick-level backtests of the Bollinger Bands strategy, enabling high-resolution performance evaluation and slippage analysis with realistic market microstructure simulation.

## Asset Search Subfolder

- **asset_search/NZDJPY.csv**: Contains search results and analysis data for the NZD/JPY currency pair.

## Usage Notes

- All notebooks are designed to work with GPU-accelerated libraries (cuDF, cuML) when available
- Data files are automatically loaded from the `../data/` directory
- Notebooks include comprehensive error handling and performance optimization
- Results and visualizations are generated with high-resolution plotting capabilities
