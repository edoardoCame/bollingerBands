# API Reference Documentation

This document provides detailed API documentation for all modules in the Bollinger Bands Trading Suite.

## Table of Contents

- [Backtester Module](#backtester-module)
- [Dynamic Portfolio Modules](#dynamic-portfolio-modules)
- [Data Formats](#data-formats)
- [Performance Metrics](#performance-metrics)
- [Examples](#examples)

## Backtester Module

### `data_loader.py`

#### `load_parquet_data(file_path: str) -> pd.DataFrame`

Loads financial data from a Parquet file.

**Parameters:**
- `file_path` (str): Path to the Parquet file

**Returns:**
- `pd.DataFrame`: DataFrame with financial data

**Example:**
```python
data = load_parquet_data('data/eurusd_1440.parquet')
```

#### `prepare_minute_data(data: pd.DataFrame) -> pd.DataFrame`

Prepares minute-level data for backtesting by adding necessary columns and resampling.

**Parameters:**
- `data` (pd.DataFrame): Raw financial data

**Returns:**
- `pd.DataFrame`: Prepared minute data with bid, ask, and midprice columns

### `indicators.py`

#### `bollinger_bands(data: pd.DataFrame, price_column: str = 'midprice', window: int = 20, num_std_dev: float = 2.0) -> pd.DataFrame`

Calculates Bollinger Bands for the given data.

**Parameters:**
- `data` (pd.DataFrame): Financial data with price information
- `price_column` (str, optional): Column name for price data. Default: 'midprice'
- `window` (int, optional): Period for moving average and standard deviation. Default: 20
- `num_std_dev` (float, optional): Number of standard deviations for bands. Default: 2.0

**Returns:**
- `pd.DataFrame`: Original data with added Bollinger Bands columns:
  - `upper_band`: Upper Bollinger Band
  - `lower_band`: Lower Bollinger Band
  - `middle_band`: Middle Bollinger Band (moving average)
  - `bb_width`: Band width (upper - lower)
  - `bb_position`: Price position within bands (0-1)

**Example:**
```python
data_with_bands = bollinger_bands(
    data, 
    window=1440,  # 24-hour window
    num_std_dev=1.5
)
```

#### `sma(data: pd.DataFrame, column: str, window: int) -> pd.Series`

Calculates Simple Moving Average.

**Parameters:**
- `data` (pd.DataFrame): Input data
- `column` (str): Column name to calculate SMA for
- `window` (int): Period for moving average

**Returns:**
- `pd.Series`: Simple moving average values

#### `ema(data: pd.DataFrame, column: str, window: int) -> pd.Series`

Calculates Exponential Moving Average.

#### `rsi(data: pd.DataFrame, column: str, window: int = 14) -> pd.Series`

Calculates Relative Strength Index.

### `backtest_engine.py`

#### `class Backtest`

Main backtesting class for running Bollinger Bands strategies.

##### `__init__(self, data: pd.DataFrame, initial_balance: float = 10000.0)`

Initialize the backtesting engine.

**Parameters:**
- `data` (pd.DataFrame): Data with Bollinger Bands calculated
- `initial_balance` (float, optional): Starting balance. Default: 10000.0

##### `run(self) -> Dict[str, Any]`

Executes the backtest and returns results.

**Returns:**
- `Dict[str, Any]`: Dictionary containing:
  - `trades`: List of individual trades
  - `equity_curve`: Portfolio value over time
  - `final_balance`: Final portfolio value
  - `total_return`: Total return percentage
  - `num_trades`: Number of trades executed

##### `print_performance_summary(self) -> None`

Prints a comprehensive performance summary including:
- Total return and annualized return
- Sharpe ratio and Sortino ratio
- Maximum drawdown
- Win rate and profit factor
- Number of trades

**Example:**
```python
backtester = Backtest(data_with_bands)
results = backtester.run()
backtester.print_performance_summary()
```

## Dynamic Portfolio Modules

### `portfolio_rebalancer.py`

#### `class DynamicPortfolioRebalancer`

Main class for dynamic portfolio rebalancing with multiple allocation strategies.

##### `__init__(self, returns_data: pd.DataFrame)`

Initialize the portfolio rebalancer.

**Parameters:**
- `returns_data` (pd.DataFrame): DataFrame with returns for multiple strategies

##### `backtest(self, method: str = 'equal', rebalance_frequency: int = 7, **kwargs) -> pd.Series`

Run portfolio backtest with specified rebalancing method.

**Parameters:**
- `method` (str): Rebalancing method. Options:
  - `'equal'`: Equal weight allocation
  - `'momentum'`: Momentum-based allocation
  - `'sharpe_momentum'`: Sharpe-adjusted momentum
  - `'top_n_ranking'`: Top-N strategy selection
  - `'risk_parity'`: Risk parity allocation
- `rebalance_frequency` (int): Days between rebalancing. Default: 7
- `**kwargs`: Method-specific parameters

**Returns:**
- `pd.Series`: Portfolio equity curve

**Method-specific parameters:**

**Momentum:**
- `lookback_days` (int): Days to look back for momentum calculation. Default: 30

**Sharpe Momentum:**
- `lookback_days` (int): Days for calculation. Default: 30
- `min_periods` (int): Minimum periods for calculation. Default: 10

**Top-N Ranking:**
- `top_n` (int): Number of top strategies to select. Default: 3
- `ranking_metric` (str): Metric for ranking ('return', 'sharpe'). Default: 'return'

### `filters.py`

#### `apply_rolling_drawdown_filter(equity_data: pd.DataFrame, threshold: float = 0.15, window: int = 90, restart_threshold: float = 0.10) -> pd.DataFrame`

Applies rolling drawdown filter to protect against excessive losses.

**Parameters:**
- `equity_data` (pd.DataFrame): Equity curves for strategies
- `threshold` (float): Drawdown threshold to trigger stop. Default: 0.15 (15%)
- `window` (int): Rolling window in days. Default: 90
- `restart_threshold` (float): Drawdown level to restart strategy. Default: 0.10 (10%)

**Returns:**
- `pd.DataFrame`: Filtered equity curves

**Key Features:**
- No lookahead bias: Current loss always included
- Maintains constant balance during stop periods
- Automatic restart when conditions improve

### `optimization.py`

#### `grid_search_optimization(rebalancer: DynamicPortfolioRebalancer, methods: List[str] = None, rebalance_frequencies: List[int] = None, **kwargs) -> pd.DataFrame`

Performs comprehensive grid search optimization across parameters.

**Parameters:**
- `rebalancer` (DynamicPortfolioRebalancer): Portfolio rebalancer instance
- `methods` (List[str], optional): List of methods to test
- `rebalance_frequencies` (List[int], optional): List of frequencies to test
- `**kwargs`: Additional method-specific parameters

**Returns:**
- `pd.DataFrame`: Results sorted by performance metric

#### `optimize_single_config(rebalancer: DynamicPortfolioRebalancer, config: Dict[str, Any]) -> Dict[str, Any]`

Optimizes a single configuration.

### `performance_metrics.py`

#### `calculate_performance_metrics(equity_curve: pd.Series, benchmark: pd.Series = None, risk_free_rate: float = 0.02, include_rolling: bool = False, **kwargs) -> Dict[str, float]`

Calculates comprehensive performance and risk metrics.

**Parameters:**
- `equity_curve` (pd.Series): Portfolio equity curve
- `benchmark` (pd.Series, optional): Benchmark for comparison
- `risk_free_rate` (float): Annual risk-free rate. Default: 0.02
- `include_rolling` (bool): Include rolling metrics. Default: False

**Returns:**
- `Dict[str, float]`: Dictionary with metrics:
  - `total_return`: Total return percentage
  - `annual_return`: Annualized return
  - `volatility`: Annual volatility
  - `sharpe_ratio`: Sharpe ratio
  - `sortino_ratio`: Sortino ratio
  - `calmar_ratio`: Calmar ratio
  - `max_drawdown`: Maximum drawdown
  - `var_5`: Value at Risk (5%)
  - `expected_shortfall_5`: Expected Shortfall (5%)
  - `skewness`: Return distribution skewness
  - `kurtosis`: Return distribution kurtosis

### `linearity_analysis.py`

#### `calculate_linearity_metrics(equity_curve: pd.Series) -> Dict[str, float]`

Calculates linearity metrics for equity curve smoothness analysis.

**Parameters:**
- `equity_curve` (pd.Series): Portfolio equity curve

**Returns:**
- `Dict[str, float]`: Dictionary with linearity metrics:
  - `r_squared`: R-squared of linear fit
  - `correlation`: Correlation with linear trend
  - `linearity_score`: Combined linearity score (0-1)
  - `volatility_penalty`: Penalty for high volatility

#### `grid_search_optimization_linearity(rebalancer: DynamicPortfolioRebalancer, optimize_for: str = 'linearity_score', **kwargs) -> pd.DataFrame`

Optimization targeting equity curve linearity rather than just returns.

## Data Formats

### Required CSV Format

CSV files in the `DATA/` folder should have the following columns:

```
datetime,bid,ask,volume
2023-01-01 00:00:00,1.0500,1.0502,1000
2023-01-01 00:01:00,1.0501,1.0503,1200
...
```

### DataFrame Structures

#### Financial Data DataFrame
```python
# Columns: datetime (index), bid, ask, volume
# Optional: midprice (calculated as (bid + ask) / 2)
```

#### Bollinger Bands DataFrame
```python
# Additional columns added by bollinger_bands():
# upper_band, lower_band, middle_band, bb_width, bb_position
```

#### Returns DataFrame
```python
# Index: datetime
# Columns: strategy names (e.g., 'EURUSD_1440', 'GBPUSD_1440')
# Values: daily returns for each strategy
```

## Performance Metrics Reference

### Risk Metrics

- **Value at Risk (VaR)**: Maximum expected loss at given confidence level
- **Expected Shortfall (ES)**: Average loss beyond VaR threshold
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Calmar Ratio**: Annual return / Maximum drawdown

### Return Metrics

- **Sharpe Ratio**: (Return - Risk-free rate) / Volatility
- **Sortino Ratio**: Similar to Sharpe but using downside deviation
- **Information Ratio**: Excess return vs benchmark / Tracking error

### Linearity Metrics

- **R-squared**: Coefficient of determination for linear fit
- **Linearity Score**: Combined metric favoring smooth equity curves
- **Volatility Penalty**: Adjustment for excessive volatility

## Examples

### Complete Workflow Example

```python
from modules.backtester import data_loader, indicators, backtest_engine
from modules.dynamic_portfolio_modules import *

# 1. Load and prepare single strategy data
data = data_loader.load_csv_data('DATA/eurusd_1440_01.csv')
minute_data = data_loader.prepare_minute_data(data)
data_with_bands = indicators.bollinger_bands(minute_data, window=1440)

# 2. Run single strategy backtest
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()

# 3. Portfolio optimization
strategies, combined_df, returns_df = load_trading_data('DATA/')
rebalancer = DynamicPortfolioRebalancer(returns_df)

# 4. Grid search optimization
optimization_results = grid_search_optimization(
    rebalancer,
    methods=['momentum', 'sharpe_momentum', 'equal'],
    rebalance_frequencies=[7, 14, 30],
    lookback_days=[30, 60, 90]
)

# 5. Apply risk management
filtered_strategies = apply_rolling_drawdown_filter(
    strategies,
    threshold=0.15,
    window=90
)

# 6. Linearity optimization
linearity_results = grid_search_optimization_linearity(
    DynamicPortfolioRebalancer(filtered_strategies),
    optimize_for='linearity_score'
)
```

### Custom Strategy Development

```python
# 1. Add new indicator
def custom_indicator(data, param1, param2):
    # Your indicator logic
    return data.copy()

# 2. Modify backtest logic
class CustomBacktest(Backtest):
    def __init__(self, data, custom_params):
        super().__init__(data)
        self.custom_params = custom_params
    
    # Override run method for custom logic
    def run(self):
        # Custom backtesting logic
        return results
```

This API reference provides comprehensive documentation for all major functions and classes in the Bollinger Bands Trading Suite. For additional examples and advanced usage, refer to the Jupyter notebooks in the `notebooks/` directory.