# Notebooks Directory

This folder contains Jupyter notebooks for advanced trading strategy analysis, portfolio optimization, volatility studies, and MetaTrader 5 integration. The project focuses on Bollinger Bands strategies with comprehensive market regime analysis and risk management.

## Table of Contents
- [Notebook Categories](#notebook-categories)
- [Key Features by Category](#key-features-by-category)
- [Data Requirements](#data-requirements)
- [Technical Implementation](#technical-implementation)
- [Usage Workflow](#usage-workflow)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Notebook Categories

### 📊 Portfolio Management
- **`portfolioopt.ipynb`**: **Equal-Weight Portfolio Optimization**
  - Multi-strategy portfolio construction with weekly rebalancing
  - Performance comparison between individual strategies and diversified portfolio
  - Risk metrics including Sharpe ratio, maximum drawdown, and Calmar ratio
  - Correlation analysis and rebalancing impact assessment
  - Comprehensive performance visualization and statistics

### 📈 Volatility & Market Regime Analysis
- **`volatility_check.ipynb`**: **Basic Volatility Analysis Tools**
  - Volatility measurement and analysis utilities
  - Basic volatility impact studies

- **`volatility impact/`**: **Advanced Volatility Studies**
  - **`regimes.ipynb`**: **Market Regime Classification** ⭐
    - Trend vs Mean-Reversion regime identification
    - Autocorrelation and variance ratio analysis
    - Random Forest classifier for regime prediction
    - Rigorous methodology without lookahead bias
    - Interactive visualizations with Plotly
  
  - **`autocorrelation.ipynb`**: **Autocorrelation Analysis**
    - Rolling autocorrelation computation
    - Market microstructure analysis
    - Interactive dashboards for correlation studies
  
  - **`visualizzazioni balance.ipynb`**: **Balance Visualization**
    - Advanced balance curve plotting
    - Drawdown visualization and analysis
    - Performance comparison tools

### 🔧 MetaTrader 5 Integration
- **`MT5 REPORTS/`**: **Complete MT5 Analysis Suite**
  - **`mt5_analysis_clean.ipynb`**: **Universal MT5 Analyzer** ⭐
    - Automatic analysis of any MT5 optimization XML export
    - Strategy performance evaluation and ranking
    - Parameter optimization visualization
    - Risk-adjusted performance metrics
  
  - **`deals.ipynb`**: **Trade Deal Analysis**
    - Detailed individual trade analysis
    - Deal performance breakdown
    - Risk assessment per trade
  
  - **`live_vs_backtest.ipynb`**: **Live vs Backtest Comparison**
    - Performance comparison between live and backtest results
    - Slippage and execution analysis
    - Real-world performance validation

## Key Features by Category

### Portfolio Optimization
- **Equal-Weight Strategy**: Diversified portfolio across multiple currency pairs
- **Weekly Rebalancing**: Systematic rebalancing to maintain target allocations
- **Risk Metrics**: Comprehensive risk assessment including drawdown analysis
- **Performance Comparison**: Individual strategies vs diversified portfolio

### Market Regime Analysis
- **Rigorous Methodology**: Prevents lookahead bias with proper temporal splitting
- **Machine Learning**: Random Forest classifier for regime prediction
- **Interactive Dashboards**: Real-time visualization of regime transitions
- **Statistical Foundation**: Based on autocorrelation and variance ratio tests

### Volatility Studies
- **Rolling Analysis**: Time-varying volatility and correlation measures
- **Impact Assessment**: How volatility affects strategy performance
- **Visualization Tools**: Advanced plotting capabilities for volatility analysis

### MetaTrader 5 Integration
- **Universal Compatibility**: Works with any MT5 XML export format
- **Automated Analysis**: Complete analysis pipeline from data import to recommendations
- **Error Handling**: Robust processing of various MT5 export formats
- **Performance Ranking**: Automatic identification of best-performing strategies

## Data Requirements

### Sample Data Included
- **EURCHF BARS 30m.csv**: Historical 30-minute EURCHF price data
- **Balance CSV files**: Strategy performance results from backtesting
- **MT5 XML exports**: Sample MetaTrader 5 optimization results

### Data Format Requirements
- **CSV Files**: Must include datetime and balance columns
- **XML Files**: Standard MT5 optimization export format
- **Price Data**: OHLC format with datetime indexing

## Technical Implementation

### Machine Learning
- **Scikit-learn**: Random Forest classifiers for regime prediction
- **Feature Engineering**: Autocorrelation and variance ratio indicators
- **Model Validation**: Proper train/test splitting with temporal constraints
- **Performance Metrics**: Accuracy, precision, recall, and confusion matrices

### Visualization
- **Plotly**: Interactive dashboards and 3D visualizations
- **Matplotlib/Seaborn**: Statistical plots and correlation matrices
- **Real-time Updates**: Dynamic filtering and zoom capabilities
- **Export Options**: High-resolution image and HTML exports

### Data Processing
- **Pandas**: Efficient data manipulation and analysis
- **NumPy**: Mathematical computations and array operations
- **Memory Optimization**: Efficient handling of large datasets
- **Error Handling**: Comprehensive exception management

## Usage Workflow

### 1. Portfolio Analysis
```bash
# Start with portfolio optimization
jupyter notebook portfolioopt.ipynb
```

### 2. Market Regime Analysis
```bash
# Analyze market regimes
jupyter notebook volatility\ impact/regimes.ipynb
```

### 3. Volatility Studies
```bash
# Study volatility effects
jupyter notebook volatility\ impact/autocorrelation.ipynb
```

### 4. MT5 Integration
```bash
# Analyze MT5 results
jupyter notebook MT5\ REPORTS/mt5_analysis_clean.ipynb
```

### 5. Balance Visualization
```bash
# Visualize performance
jupyter notebook volatility\ impact/visualizzazioni\ balance.ipynb
```

## Best Practices

### Data Handling
- Always check data quality before analysis
- Handle missing values appropriately
- Use proper datetime indexing
- Validate data ranges and formats

### Analysis Methodology
- Prevent lookahead bias in predictive models
- Use proper train/test splitting
- Validate results with multiple metrics
- Document assumptions and limitations

### Visualization
- Use interactive plots for exploratory analysis
- Include proper labels and legends
- Export high-resolution images for reports
- Implement zoom and filtering capabilities

## Troubleshooting

### Common Issues
- **Memory errors**: Reduce data size or use chunking
- **Import errors**: Check package installations
- **File not found**: Verify file paths and extensions
- **Visualization not showing**: Restart kernel and re-run cells

### Performance Optimization
- Use vectorized operations where possible
- Implement data caching for repeated operations
- Consider GPU acceleration for large datasets
- Profile code to identify bottlenecks

---

For detailed documentation on each component, see the README files in the respective subfolders.
