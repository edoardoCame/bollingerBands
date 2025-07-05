
# Bollinger Bands Trading Strategy Analysis

Comprehensive trading strategy analysis and optimization system based on Bollinger Bands indicators. This project implements high-performance financial data processing using GPU-accelerated libraries (cuDF, cuML) and provides extensive backtesting capabilities from tick-level to minute-level data analysis.

## Repository Structure

```
├── .venv/                      # Python virtual environment
├── notebooks/
│   ├── portfolioopt.ipynb      # Portfolio optimization using modern portfolio theory
│   ├── volatility_check.ipynb # Basic volatility analysis tools
│   ├── MT5 REPORTS/            # MetaTrader 5 analysis tools
│   │   ├── deals.ipynb         # Trade deal analysis
│   │   ├── live_vs_backtest.ipynb  # Live vs backtest comparison
│   │   ├── mt5_analysis_clean.ipynb  # Universal MT5 optimization results analyzer
│   │   └── README.md           # Comprehensive MT5 analysis documentation
│   ├── volatility impact/     # Advanced volatility and market regime analysis
│   │   ├── autocorrelation.ipynb    # Autocorrelation analysis with interactive dashboards
│   │   ├── regimes.ipynb           # Market regime classification (trend vs mean reversion)
│   │   ├── visualizzazioni balance.ipynb  # Advanced balance visualization tools
│   │   ├── EURCHF BARS 30m.csv    # Historical EURCHF 30-minute price data
│   │   ├── balance backtest 5min.csv      # 5-minute backtest results
│   │   ├── balance backtest from 2020 eurchf.csv  # EURCHF historical results
│   │   └── README.md           # Comprehensive volatility analysis guide
│   └── README.md               # Detailed notebook descriptions and usage guide
└── README.md                   # This file - Complete project overview
```

## Project Components

### Core Notebooks
- **Portfolio Optimization**: Modern portfolio theory implementation with equal-weight rebalancing
- **Volatility Analysis**: Market regime classification and autocorrelation studies
- **MetaTrader 5 Integration**: Universal analysis tools for MT5 optimization results

### Strategy Implementation
- **Bollinger Bands Core**: Configurable period and standard deviation parameters
- **Signal Generation**: Buy/sell signals based on price band interactions
- **Risk Management**: Position sizing, stop-loss, and take-profit mechanisms
- **Portfolio Theory**: Equal-weight diversification with weekly rebalancing

### Analysis & Validation
- **Market Regime Analysis**: Trend vs mean-reversion classification using autocorrelation and variance ratio
- **Volatility Impact Studies**: Analysis of volatility effects on strategy performance
- **MT5 Integration**: Analysis of real trading data from MetaTrader 5
- **Performance Metrics**: Comprehensive statistics including Sharpe ratio, maximum drawdown, and profit factor
- **Risk Assessment**: VaR, CVaR, and portfolio risk decomposition

## Technical Features

- **GPU Acceleration**: Utilizes cuDF and cuML for high-performance data processing
- **Machine Learning**: Random Forest classifiers for regime prediction without lookahead bias
- **Interactive Visualization**: Plotly-based dashboards for strategy analysis
- **Scalable Architecture**: Handles large datasets efficiently with optimized memory usage
- **Error Handling**: Robust exception management and data validation
- **Documentation**: Comprehensive guides and examples in notebook format

## Quick Start Guide

### 1. Environment Setup
```bash
# Navigate to project directory
cd /workspaces/bollingerBands

# Activate the virtual environment (if available)
source .venv/bin/activate

# Install required packages
pip install pandas numpy matplotlib plotly seaborn scikit-learn jupyter
```

### 2. Portfolio Optimization
Start with modern portfolio theory analysis:
```bash
jupyter notebook notebooks/portfolioopt.ipynb
```

### 3. Market Regime Analysis
Analyze trend vs mean-reversion regimes:
```bash
jupyter notebook notebooks/volatility\ impact/regimes.ipynb
```

### 4. Volatility Impact Studies
Explore autocorrelation and volatility effects:
```bash
jupyter notebook notebooks/volatility\ impact/autocorrelation.ipynb
```

### 5. MetaTrader 5 Analysis
Analyze MT5 optimization results:
```bash
jupyter notebook notebooks/MT5\ REPORTS/mt5_analysis_clean.ipynb
```

### 6. Balance Visualization
Visualize balance curves and performance:
```bash
jupyter notebook notebooks/volatility\ impact/visualizzazioni\ balance.ipynb
```

## Key Features by Category

### Portfolio Management
- **Equal-Weight Rebalancing**: Weekly portfolio rebalancing across multiple strategies
- **Risk Diversification**: Multi-asset portfolio construction
- **Performance Metrics**: Sharpe ratio, maximum drawdown, Calmar ratio analysis
- **Correlation Analysis**: Rolling correlation studies between strategies

### Market Regime Analysis
- **Trend vs Mean-Reversion**: Classification using autocorrelation and variance ratio
- **Machine Learning**: Random Forest classifier for regime prediction
- **Lookahead Bias Prevention**: Rigorous temporal split methodology
- **Interactive Visualization**: Plotly-based regime analysis dashboards

### Volatility Studies
- **Autocorrelation Analysis**: Rolling autocorrelation computation
- **Variance Ratio Tests**: Lo-MacKinlay variance ratio implementation
- **Regime Persistence**: Analysis of regime duration and transitions
- **Impact Assessment**: Volatility effects on strategy performance

## Requirements

- **Python 3.8+**
- **Jupyter Notebook/Lab**
- **Key Libraries**: pandas, numpy, matplotlib, plotly, seaborn, scikit-learn
- **Optional**: cudf, cuml (for GPU acceleration)

## Data Sources

The project includes sample data:
- **EURCHF 30m bars**: Historical price data for analysis
- **Balance CSV files**: Strategy performance results
- **MT5 XML exports**: MetaTrader 5 optimization results

## Documentation Structure

This repository contains comprehensive documentation at multiple levels:

### 📋 Root Documentation
- **`README.md`** - Complete project overview and quick start guide

### 📁 Notebooks Documentation  
- **`notebooks/README.md`** - Comprehensive guide to all analysis notebooks
- **`notebooks/MT5 REPORTS/README.md`** - Complete MT5 analysis suite documentation
- **`notebooks/volatility impact/README.md`** - Advanced volatility analysis guide

### 🔬 Individual Notebook Documentation
Each notebook contains:
- Detailed markdown explanations
- Code comments and docstrings
- Usage examples and best practices
- Troubleshooting guides

### 📊 Analysis Methodology Documentation
- **Market Regime Classification**: Rigorous temporal methodology preventing lookahead bias
- **Portfolio Optimization**: Equal-weight rebalancing with comprehensive risk metrics
- **Volatility Analysis**: Statistical foundation with autocorrelation and variance ratio tests
- **MT5 Integration**: Universal compatibility with any MT5 export format

All documentation is designed to be self-contained while providing cross-references for deeper understanding of related concepts and methodologies.

## Performance Notes

- **Memory Optimization**: Efficient handling of large financial datasets
- **GPU Acceleration**: Optional cuDF/cuML support for enhanced performance
- **Modular Design**: Easy to extend with additional strategies and analysis tools
- **Robust Error Handling**: Comprehensive exception management and data validation
- **Interactive Dashboards**: Real-time visualization updates and filtering

## Contributing

When adding new notebooks or analysis:
1. Include comprehensive markdown documentation
2. Implement proper error handling
3. Add sample data or clear data source instructions
4. Update relevant README files
5. Test with various data scenarios

---

For detailed workflow instructions and technical documentation, see the README files in each subfolder.
