# Bollinger Bands Trading Suite

A comprehensive Python framework for backtesting Bollinger Bands trading strategies with advanced portfolio management, risk control, and performance optimization.

## 🌟 Key Features

- **🎯 Bollinger Bands Strategy Engine**: Optimized mean-reversion strategies with Numba acceleration
- **📊 Advanced Portfolio Management**: Dynamic rebalancing with multiple allocation methods
- **🛡️ Risk Management**: Rolling drawdown filters and sophisticated risk metrics
- **⚡ Performance Optimization**: Grid search and linearity-based optimization
- **📈 Comprehensive Analytics**: Advanced visualization and performance reporting
- **🔌 MT5 Integration**: Direct MetaTrader 5 analysis and comparison tools

## 🚀 Quick Start

### Installation

```bash
pip install pandas numpy matplotlib plotly numba scikit-learn tqdm
```

### Basic Usage

```python
from modules.backtester import data_loader, indicators, backtest_engine

# Load and prepare data
data = data_loader.load_parquet_data('your_data.parquet')
minute_data = data_loader.prepare_minute_data(data)

# Calculate Bollinger Bands
data_with_bands = indicators.bollinger_bands(
    minute_data, 
    window=1440,  # 24-hour window for minute data
    num_std_dev=1.0
)

# Run backtest
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()
```

### Portfolio Optimization

```python
from modules.dynamic_portfolio_modules import (
    load_trading_data,
    DynamicPortfolioRebalancer,
    grid_search_optimization
)

# Load multiple strategies
strategies, combined_df, returns_df = load_trading_data('DATA/')

# Create and optimize portfolio
rebalancer = DynamicPortfolioRebalancer(returns_df)
results = grid_search_optimization(
    rebalancer,
    methods=['momentum', 'sharpe_momentum', 'equal'],
    rebalance_frequencies=[7, 14, 30]
)
```

## 📁 Repository Structure

```
bollingerBands/
├── DATA/                           # Historical price data (CSV format)
│   ├── audjpy_1440_01.csv         # AUD/JPY 24h timeframe
│   ├── eurusd_1440_01.csv         # EUR/USD 24h timeframe
│   └── ...                        # Additional currency pairs
│
├── modules/                       # Core Python modules
│   ├── backtester/               # Main backtesting engine
│   │   ├── data_loader.py        # Data loading utilities
│   │   ├── indicators.py         # Technical indicators
│   │   ├── backtest_engine.py    # Core backtesting logic
│   │   ├── visualization.py      # Performance visualization
│   │   ├── utils.py              # Utility functions
│   │   └── walk_forward.py       # Walk-forward analysis
│   │
│   └── dynamic_portfolio_modules/ # Advanced portfolio management
│       ├── portfolio_rebalancer.py  # Dynamic rebalancing
│       ├── filters.py              # Risk management filters
│       ├── optimization.py         # Parameter optimization
│       ├── performance_metrics.py  # Advanced metrics
│       ├── linearity_analysis.py   # Equity curve analysis
│       └── utils.py                # Portfolio utilities
│
├── notebooks/                     # Jupyter notebook examples
│   ├── backtester/               # Basic backtesting examples
│   ├── risk management/          # Risk management studies
│   ├── MT5 REPORTS/             # MetaTrader 5 integration
│   └── volatility impact/       # Market regime analysis
│
└── temp tools/                   # Utility scripts and tools
```

## 🔧 Core Modules

### Backtester Module (`modules/backtester/`)

The core backtesting engine provides:

- **Data Loading**: Support for tick, minute, and balance data formats
- **Technical Indicators**: Bollinger Bands, SMA, EMA, RSI, and more
- **Strategy Engine**: Optimized mean-reversion strategy implementation
- **Performance Analysis**: Comprehensive PnL, drawdown, and risk metrics
- **Visualization**: Professional charts and performance reports

**Key Components:**
- `backtest_engine.py`: Numba-optimized backtesting core
- `indicators.py`: Technical indicator calculations
- `data_loader.py`: Flexible data loading and preprocessing
- `visualization.py`: Advanced plotting and analysis tools

### Dynamic Portfolio Modules (`modules/dynamic_portfolio_modules/`)

Advanced portfolio management system featuring:

- **Dynamic Rebalancing**: Multiple allocation strategies (momentum, Sharpe, equal-weight, risk parity)
- **Risk Management**: Rolling drawdown filters with configurable thresholds
- **Performance Optimization**: Grid search and linearity-based optimization
- **Advanced Metrics**: VaR, Expected Shortfall, rolling performance metrics
- **Linearity Analysis**: Unique equity curve smoothness optimization

**Key Components:**
- `portfolio_rebalancer.py`: Main portfolio management class
- `filters.py`: Risk management and drawdown protection
- `optimization.py`: Parameter optimization and grid search
- `performance_metrics.py`: Advanced risk-return calculations
- `linearity_analysis.py`: Equity curve linearity optimization

## 📊 Features Deep Dive

### Bollinger Bands Strategy

The core strategy implements a mean-reversion approach:
- **Long Entry**: Price crosses below lower Bollinger Band
- **Long Exit**: Price crosses above middle band (moving average)
- **Short Entry**: Price crosses above upper Bollinger Band  
- **Short Exit**: Price crosses below middle band

### Rolling Drawdown Filter

Advanced risk management feature:
- Monitors drawdown over configurable rolling windows (e.g., 90 days)
- Automatically stops strategy when drawdown exceeds threshold
- Restarts only when drawdown recovers above restart threshold
- **No lookahead bias**: Current loss always included in filtered equity
- Maintains constant balance during stop periods

### Portfolio Rebalancing Methods

1. **Momentum**: Allocates based on recent performance trends
2. **Sharpe-Momentum**: Risk-adjusted momentum allocation
3. **Top-N Ranking**: Focuses on best-performing strategies
4. **Equal Weight**: Simple diversification across all strategies
5. **Risk Parity**: Allocation based on risk contribution

### Performance Optimization

- **Grid Search**: Systematic parameter space exploration
- **Linearity Optimization**: Unique approach targeting smooth equity curves
- **Walk-Forward Analysis**: Out-of-sample validation
- **Multi-objective Optimization**: Balance return, risk, and smoothness

## 📚 Usage Examples

### Advanced Portfolio Setup

```python
from modules.dynamic_portfolio_modules import *

# Load and filter strategies
strategies, combined_df, returns_df = load_trading_data('DATA/')
filtered_strategies = apply_rolling_drawdown_filter(
    strategies, 
    threshold=0.15,  # 15% drawdown threshold
    window=90        # 90-day rolling window
)

# Create optimized portfolio
rebalancer = DynamicPortfolioRebalancer(filtered_strategies)
results = grid_search_optimization_linearity(
    rebalancer,
    optimize_for='linearity_score'
)
```

### Risk Analysis

```python
from modules.dynamic_portfolio_modules.performance_metrics import calculate_performance_metrics

# Calculate comprehensive risk metrics
metrics = calculate_performance_metrics(
    equity_curve,
    include_rolling=True,
    var_confidence=0.05,
    es_confidence=0.05
)

print(f"Annual Return: {metrics['annual_return']:.2%}")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
print(f"VaR (5%): {metrics['var_5']:.2%}")
```

### MetaTrader 5 Integration

```python
# Analyze MT5 optimization results
from notebooks.MT5_REPORTS.mt5_analysis_clean import analyze_mt5_results

results = analyze_mt5_results('mt5_optimization.xml')
top_configs = results.get_top_configurations(metric='profit_factor')
```

## 📖 Documentation

### 📚 Complete Documentation Suite

This repository includes comprehensive documentation for all skill levels:

- **[📋 Documentation Index](docs/README.md)** - Navigate all available documentation
- **[🔧 API Reference](docs/API_REFERENCE.md)** - Complete function and class documentation  
- **[⚙️ Installation Guide](docs/INSTALLATION.md)** - Setup instructions and troubleshooting
- **[🌟 Features Guide](docs/FEATURES.md)** - Advanced examples and use cases
- **[📓 Notebooks Guide](notebooks/README.md)** - Interactive tutorials and examples

### 🎯 Quick Links

- **Getting Started**: Follow the [Installation Guide](docs/INSTALLATION.md) and try the [Basic Examples](notebooks/backtester/)
- **Advanced Features**: Explore [Portfolio Management](docs/FEATURES.md#portfolio-management-features) and [Risk Control](docs/FEATURES.md#risk-management-features)
- **Technical Details**: Review [Module Documentation](modules/dynamic_portfolio_modules/README_REFACTORING.md) and [API Reference](docs/API_REFERENCE.md)
- **Live Trading**: Check [MT5 Integration](notebooks/README.md#metatrader-5-integration) for real-world implementation

## 🛠️ Development

### Testing

```bash
# Run basic functionality tests
python -m pytest tests/ -v

# Test backtesting engine
python -c "from modules.backtester import backtest_engine; print('Backtester loaded successfully')"

# Test portfolio modules
python -c "from modules.dynamic_portfolio_modules import DynamicPortfolioRebalancer; print('Portfolio modules loaded successfully')"
```

### Adding New Strategies

1. Extend `indicators.py` with new technical indicators
2. Modify `backtest_engine.py` for new entry/exit logic
3. Add visualization support in `visualization.py`
4. Create example notebook in `notebooks/backtester/`

## 📈 Performance

- **Numba Acceleration**: Core backtesting loops optimized with Numba JIT compilation
- **Vectorized Operations**: Efficient pandas/numpy operations throughout
- **Parallel Processing**: Grid search and optimization support multiprocessing
- **Memory Efficient**: Optimized data structures for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Use Cases

- **Quantitative Trading**: Professional backtesting and strategy development
- **Risk Management**: Advanced portfolio protection and optimization
- **Academic Research**: Market regime analysis and strategy evaluation
- **Portfolio Management**: Multi-strategy allocation and rebalancing
- **Educational**: Learning quantitative finance and trading systems