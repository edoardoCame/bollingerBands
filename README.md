
# Bollinger Bands Trading Strategy Analysis

Comprehensive trading strategy analysis and optimization system based on Bollinger Bands indicators. This project implements high-performance financial data processing using GPU-accelerated libraries (cuDF, cuML) and provides extensive backtesting capabilities from tick-level to minute-level data analysis.

## Repository Structure

```
├── data/
│   ├── AUDJPY_full_1min.txt    # 1-minute OHLC data for AUD/JPY
│   ├── NZDJPY_full_1min.txt    # 1-minute OHLC data for NZD/JPY
│   └── USDJPY_full_1min.txt    # 1-minute OHLC data for USD/JPY
├── logs/
│   └── README.md               # Documentation for log files and outputs
├── notebooks/
│   ├── Asset_Explore.ipynb     # Asset data exploration and visualization
│   ├── bollinger_backtester.ipynb  # Backtrader-based strategy validation
│   ├── execution_delay_test.ipynb  # Order execution delay impact analysis
│   ├── grid_search_optimization.ipynb  # Automated parameter optimization
│   ├── manual.ipynb            # User guide and workflow documentation
│   ├── mkt orders.ipynb        # Market order execution analysis
│   ├── mt5_analysis.ipynb      # MetaTrader 5 real trading data analysis
│   ├── tick_backtest.ipynb     # High-resolution tick-level backtesting
│   ├── asset_search/
│   │   └── NZDJPY.csv         # Asset analysis results for NZD/JPY
│   └── README.md               # Detailed notebook descriptions
└── README.md                   # This file
```

## Project Components

### Data Analysis & Exploration
- **Historical Price Data**: 1-minute OHLC data for major currency pairs (AUD/JPY, NZD/JPY, USD/JPY)
- **Asset Analysis**: Comprehensive exploration of price behavior, volatility patterns, and market microstructure
- **Real Trading Data**: Integration with MetaTrader 5 for actual trading performance analysis

### Strategy Implementation
- **Bollinger Bands Core**: Configurable period and standard deviation parameters
- **Signal Generation**: Buy/sell signals based on price band interactions
- **Risk Management**: Position sizing, stop-loss, and take-profit mechanisms

### Backtesting & Validation
- **Multiple Frameworks**: Custom implementation + Backtrader library validation
- **Tick-Level Testing**: High-resolution backtesting with realistic market simulation
- **Execution Analysis**: Order delay impact assessment and slippage modeling
- **Performance Metrics**: Comprehensive statistics including Sharpe ratio, maximum drawdown, and profit factor

### Optimization & Research
- **Grid Search**: Automated parameter optimization using GPU acceleration
- **Market Order Analysis**: Comparison of different order execution strategies
- **Delay Impact Studies**: Realistic trading condition simulation

## Technical Features

- **GPU Acceleration**: Utilizes cuDF and cuML for high-performance data processing
- **Scalable Architecture**: Handles large datasets efficiently with optimized memory usage
- **Visualization**: Advanced plotting and analysis charts for strategy insights
- **Error Handling**: Robust exception management and data validation
- **Documentation**: Comprehensive guides and examples in notebook format

## Quick Start Guide

### 1. Environment Setup
```bash
# Activate the virtual environment (if available)
source .venv/bin/activate

# Install required packages
pip install cudf cuml jupyter pandas numpy matplotlib backtrader
```

### 2. Data Exploration
Start with asset exploration to understand your data:
```bash
jupyter notebook notebooks/Asset_Explore.ipynb
```

### 3. Strategy Validation
Validate the Bollinger Bands strategy implementation:
```bash
jupyter notebook notebooks/bollinger_backtester.ipynb
```

### 4. Parameter Optimization
Run automated parameter optimization:
```bash
jupyter notebook notebooks/grid_search_optimization.ipynb
```

### 5. Advanced Analysis
- **Real Trading Analysis**: Use `mt5_analysis.ipynb` for MetaTrader 5 data
- **Tick-Level Testing**: Run `tick_backtest.ipynb` for high-resolution analysis
- **Execution Studies**: Analyze order delays with `execution_delay_test.ipynb`

## Requirements

- **Python 3.8+**
- **CUDA-compatible GPU** (recommended for cuDF/cuML acceleration)
- **Jupyter Notebook/Lab**
- **Key Libraries**: cudf, cuml, pandas, numpy, matplotlib, backtrader

## Documentation

- **Notebooks README**: Detailed descriptions in `notebooks/README.md`
- **Logs README**: Output documentation in `logs/README.md`
- **User Manual**: Step-by-step guide in `notebooks/manual.ipynb`

## Performance Notes

- GPU acceleration provides significant speedup for large datasets
- Memory optimization techniques implemented for handling large tick data
- Parallel processing capabilities for parameter optimization
- Efficient data structures for minimal memory footprint
5. **Optimization**: Run `grid_search_optimization.ipynb` for parameter tuning

---

For more details, see the README files in each folder.
