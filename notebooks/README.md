# Jupyter Notebooks Documentation

This directory contains comprehensive Jupyter notebooks for advanced trading strategy analysis, portfolio optimization, volatility studies, and MetaTrader 5 integration. The notebooks demonstrate practical applications of the Bollinger Bands Trading Suite with real-world examples and advanced analytics.

## 📋 Table of Contents

- [Notebook Categories](#notebook-categories)
- [Getting Started](#getting-started)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 📁 Notebook Categories

### 🚀 Backtester Examples (`backtester/`)

**Purpose**: Learn the core backtesting functionality with practical examples

- **`example_usage.ipynb`**: **Basic Backtesting Tutorial**
  - Step-by-step guide to running your first backtest
  - Data loading and preparation
  - Bollinger Bands calculation and visualization
  - Performance analysis and interpretation
  - **Skill Level**: Beginner
  - **Estimated Time**: 30 minutes

**Key Learning Outcomes**:
- Understand basic backtesting workflow
- Learn to interpret performance metrics
- Master data preparation techniques
- Create professional visualizations

### 📊 Portfolio Optimization

**Purpose**: Advanced portfolio management and optimization techniques

- **`portfolioopt.ipynb`**: **Multi-Strategy Portfolio Construction**
  - Equal-weight portfolio optimization
  - Dynamic rebalancing strategies
  - Risk-adjusted performance metrics
  - Correlation analysis and diversification benefits
  - **Skill Level**: Intermediate
  - **Estimated Time**: 45 minutes

**Key Features**:
- Multi-currency pair analysis
- Weekly rebalancing implementation
- Sharpe ratio optimization
- Maximum drawdown analysis
- Calmar ratio calculations

### 📈 Risk Management (`risk management/`)

**Purpose**: Advanced risk control and portfolio protection techniques

#### Core Risk Management
- **`dynamic opt.ipynb`**: **Dynamic Portfolio Optimization**
  - Real-time portfolio rebalancing
  - Multiple allocation strategies comparison
  - Grid search parameter optimization
  - Walk-forward analysis validation
  - **Skill Level**: Advanced
  - **Estimated Time**: 60 minutes

- **`collinearita_strategie.ipynb`**: **Strategy Correlation Analysis**
  - Inter-strategy correlation measurement
  - Diversification effectiveness analysis
  - Portfolio construction based on correlation
  - **Skill Level**: Intermediate
  - **Estimated Time**: 30 minutes

#### Drawdown Filter Analysis (`drawdown filter/`)

- **`rolling dd.ipynb`**: **Rolling Drawdown Protection** ⭐
  - Implementation of rolling drawdown filters
  - No-lookahead-bias methodology
  - Automatic strategy stopping and restarting
  - Performance impact analysis
  - **Skill Level**: Advanced
  - **Estimated Time**: 45 minutes

- **`regimes.ipynb`**: **Market Regime Classification**
  - Trend vs mean-reversion regime identification
  - Machine learning classification with Random Forest
  - Autocorrelation and variance ratio analysis
  - Interactive regime visualization
  - **Skill Level**: Advanced
  - **Estimated Time**: 60 minutes

- **`autocorrelation.ipynb`**: **Return Autocorrelation Analysis**
  - Rolling autocorrelation computation
  - Market microstructure insights
  - Predictability assessment
  - **Skill Level**: Intermediate
  - **Estimated Time**: 30 minutes

- **`consecutive wins.ipynb`**: **Streak Analysis**
  - Winning and losing streak analysis
  - Statistical significance testing
  - Risk of ruin calculations
  - **Skill Level**: Intermediate
  - **Estimated Time**: 30 minutes

### 🔧 MetaTrader 5 Integration (`MT5 REPORTS/`)

**Purpose**: Bridge between Python analysis and MetaTrader 5 results

- **`mt5_analysis_clean.ipynb`**: **Universal MT5 Analyzer** ⭐
  - Automatic XML optimization report analysis
  - Strategy ranking and selection
  - Parameter optimization visualization
  - Risk-adjusted performance metrics
  - **Skill Level**: Intermediate
  - **Estimated Time**: 30 minutes

- **`deals.ipynb`**: **Individual Trade Analysis**
  - Detailed trade-by-trade breakdown
  - Entry/exit timing analysis
  - Profit/loss distribution studies
  - **Skill Level**: Beginner
  - **Estimated Time**: 25 minutes

- **`live_vs_backtest.ipynb`**: **Reality Check Analysis**
  - Live trading vs backtest comparison
  - Slippage and execution cost analysis
  - Performance degradation identification
  - **Skill Level**: Advanced
  - **Estimated Time**: 45 minutes

### 📊 Volatility Studies (`volatility impact/`)

**Purpose**: Market volatility analysis and regime detection

- **`volatility_check.ipynb`**: **Basic Volatility Tools**
  - Volatility measurement techniques
  - Rolling volatility analysis
  - Volatility impact on strategy performance
  - **Skill Level**: Beginner
  - **Estimated Time**: 20 minutes

- **`visualizzazioni balance.ipynb`**: **Advanced Balance Visualization**
  - Professional equity curve plotting
  - Drawdown period identification
  - Performance comparison tools
  - **Skill Level**: Intermediate
  - **Estimated Time**: 25 minutes

### 🛠️ Utility Tools (`temp tools/`)

**Purpose**: Data conversion and utility functions

- **`convert to parquet.ipynb`**: **Data Format Conversion**
  - CSV to Parquet conversion for better performance
  - Data validation and cleaning
  - **Skill Level**: Beginner
  - **Estimated Time**: 15 minutes

- **`equity comparison.ipynb`**: **Strategy Comparison Tools**
  - Side-by-side strategy performance comparison
  - Statistical significance testing
  - **Skill Level**: Intermediate
  - **Estimated Time**: 30 minutes

## 🚀 Getting Started

### Prerequisites

1. **Install Dependencies**:
   ```bash
   pip install jupyter pandas numpy matplotlib plotly numba scikit-learn
   ```

2. **Setup Data**: Ensure your `DATA/` folder contains properly formatted CSV files

3. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

### Recommended Learning Path

#### Beginner Path (2-3 hours)
1. `backtester/example_usage.ipynb` - Learn basics
2. `volatility impact/volatility_check.ipynb` - Understand market dynamics
3. `MT5 REPORTS/deals.ipynb` - Analyze individual trades

#### Intermediate Path (4-5 hours)
1. Complete Beginner Path
2. `portfolioopt.ipynb` - Portfolio construction
3. `risk management/collinearita_strategie.ipynb` - Correlation analysis
4. `MT5 REPORTS/mt5_analysis_clean.ipynb` - MT5 integration

#### Advanced Path (6-8 hours)
1. Complete Intermediate Path
2. `risk management/dynamic opt.ipynb` - Advanced optimization
3. `risk management/drawdown filter/rolling dd.ipynb` - Risk management
4. `risk management/drawdown filter/regimes.ipynb` - Machine learning

## 🔧 Advanced Features

### Module Integration

All notebooks demonstrate how to use the Python modules effectively:

```python
# Standard imports used across notebooks
from modules.backtester import data_loader, indicators, backtest_engine
from modules.dynamic_portfolio_modules import (
    DynamicPortfolioRebalancer,
    apply_rolling_drawdown_filter,
    grid_search_optimization
)
```

### Interactive Visualizations

Many notebooks include interactive Plotly visualizations:
- Hover data inspection
- Zoom and pan capabilities
- Real-time parameter adjustment
- Multi-dimensional plotting

### Performance Optimization

Notebooks demonstrate performance best practices:
- Numba-accelerated computations
- Vectorized operations
- Memory-efficient data handling
- Parallel processing examples

## 📚 Best Practices

### 1. Data Management

```python
# Always validate data before analysis
def validate_data(df):
    assert 'datetime' in df.columns
    assert 'bid' in df.columns
    assert 'ask' in df.columns
    assert not df.empty
    return True

# Use consistent data loading
data = data_loader.load_csv_data('DATA/eurusd_1440_01.csv')
validate_data(data)
```

### 2. Reproducible Results

```python
# Set random seeds for reproducibility
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# Save important results
results.to_csv('analysis_results.csv')
```

### 3. Memory Management

```python
# Clear variables when working with large datasets
del large_dataframe
import gc
gc.collect()

# Use data types optimization
data = data.astype({'volume': 'float32'})
```

### 4. Error Handling

```python
# Robust data loading
try:
    strategies, combined_df, returns_df = load_trading_data('DATA/')
    print(f"Successfully loaded {len(strategies)} strategies")
except Exception as e:
    print(f"Data loading failed: {e}")
    # Fallback or alternative approach
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Kernel Dies During Execution

**Cause**: Usually memory issues or Numba compilation problems

**Solutions**:
```python
# Reduce data size for testing
test_data = data.tail(1000)

# Clear Numba cache
import numba
# Delete numba cache directory if compilation fails
```

#### 2. Plots Not Displaying

**Cause**: Jupyter or Plotly configuration issues

**Solutions**:
```python
# Enable inline plotting
%matplotlib inline

# For Plotly
import plotly.io as pio
pio.renderers.default = 'notebook'

# Install widget extensions
!jupyter nbextension enable --py widgetsnbextension
```

#### 3. Module Import Errors

**Cause**: Python path or working directory issues

**Solutions**:
```python
# Check current directory
import os
print(f"Current directory: {os.getcwd()}")

# Add project root to path
import sys
sys.path.append('/path/to/bollingerBands')
```

#### 4. Slow Performance

**Cause**: Large datasets or inefficient operations

**Solutions**:
```python
# Profile code performance
%timeit expensive_operation()

# Use smaller datasets for development
sample_data = data.sample(frac=0.1)

# Enable parallel processing where available
results = grid_search_optimization(rebalancer, parallel=True)
```

### Getting Help

1. **Check Error Messages**: Read error messages carefully - they often indicate the exact issue
2. **Review Dependencies**: Ensure all required packages are installed with `pip list`
3. **Restart Kernel**: Many issues resolve with a fresh kernel restart
4. **Check Data Format**: Verify your data matches the expected format
5. **Review Documentation**: Check the main README.md and API documentation

## 🎯 Next Steps

After working through these notebooks:

1. **Customize Strategies**: Modify the backtesting logic for your specific needs
2. **Add New Indicators**: Extend the indicators module with custom technical indicators
3. **Develop New Filters**: Create additional risk management filters
4. **Optimize Parameters**: Use the optimization tools to find optimal settings for your data
5. **Live Trading**: Implement your strategies with proper risk management

Each notebook contains detailed comments and explanations to guide you through the analysis. Start with the basics and gradually work your way up to more advanced topics.
## Notebooks

Structure:
```
notebooks/
├── backtester/
├── MT5 REPORTS/
├── risk management/
├── temp tools/
├── portfolioopt.ipynb
├── volatility_check.ipynb
└── README.md
```

Categories:
- Portfolio Management: portfolio optimization/rebalancing
- Volatility & Regime Analysis: volatility, autocorrelation, regimes
- Risk Management: drawdown filters, risk metrics
- MT5 Reports: MetaTrader 5 results analysis
- Temp Tools: temporary tools

**How to use the modules in notebooks (extensive explanation):**
Import functions from Python modules to:
- Apply rolling drawdown filters
- Calculate dynamic weights
- Optimize parameters and analyze performance

Example:
```python
from modules.dynamic_portfolio_modules.filters import apply_rolling_drawdown_filter
from modules.dynamic_portfolio_modules.utils import calculate_momentum_weights
# ...
```

For technical details on the modules, see `modules/dynamic_portfolio_modules/README_REFACTORING.md`.

