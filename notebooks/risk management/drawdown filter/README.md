# Navigation

For related documentation, see:
- **../../README.md** – Notebooks directory overview
- **../../MT5 REPORTS/README.md** – MT5 analysis suite

# drawdown filter

Questa cartella contiene notebook e strumenti per l’analisi della volatilità, dei regimi di mercato e dei drawdown.

Contenuto:
- autocorrelation.ipynb : Analisi autocorrelazione
- consecutive wins.ipynb : Analisi sequenze vincenti
- regimes.ipynb : Classificazione regimi di mercato
- rolling dd.ipynb : Analisi drawdown rolling
- README.md : Questo file

### 📊 Data Files

#### Price Data
- **`EURCHF BARS 30m.csv`**: Historical 30-minute EURCHF price data
  - Format: OHLC with datetime indexing
  - Usage: Primary data source for regime analysis
  - Coverage: Comprehensive historical data for analysis

#### Backtest Results
- **`balance backtest 5min.csv`**: 5-minute strategy backtest results
- **`balance backtest from 2020 eurchf.csv`**: EURCHF strategy results from 2020
- **Additional CSV files**: Various strategy performance datasets

## 🔬 Technical Methodology

### Market Regime Classification

#### Theoretical Foundation
The regime classification is based on two key statistical indicators:

1. **Autocorrelation**: Measures serial correlation in returns
   - Positive autocorrelation → Trend (momentum) regime
   - Negative autocorrelation → Mean-reversion regime

2. **Variance Ratio**: Lo-MacKinlay (1988) test for random walk
   - VR > 1 → Trend regime (positive serial correlation)
   - VR < 1 → Mean-reversion regime (negative serial correlation)

#### Classification Logic
```python
if autocorr > 0 and variance_ratio > 1:
    regime = 1  # Trend
elif autocorr < 0 and variance_ratio < 1:
    regime = 0  # Mean-Reversion
else:
    regime = NaN  # Undefined regime
```

#### Machine Learning Pipeline
1. **Feature Engineering**: Calculate lagged indicators to prevent lookahead bias
2. **Temporal Splitting**: Chronological train/test split (no random shuffling)
3. **Model Training**: Random Forest classifier with balanced class weights
4. **Validation**: Comprehensive metrics including confusion matrices
5. **Prediction**: Out-of-sample regime forecasting

### Lookahead Bias Prevention

#### Critical Methodology
The analysis implements rigorous measures to prevent lookahead bias:

1. **Temporal Awareness**: OHLC bars available at END of time period
2. **Feature Lagging**: All indicators use lag-1 to simulate real-time availability
3. **Prediction Horizon**: Clear separation between observation and prediction periods
4. **Chronological Splitting**: Test set always chronologically after training set

#### Implementation Details
```python
# Correct approach - features with lag
df['autocorr_lag'] = df['autocorr'].shift(1)
df['vr_lag'] = df['vr'].shift(1)

# Predict future regime using only past information
df['target_regime'] = df['current_regime'].shift(-horizon)
```

## 📈 Analysis Capabilities

### 1. Regime Identification
- **Real-time Classification**: Identify current market regime
- **Prediction Models**: Forecast future regime transitions
- **Confidence Intervals**: Assess prediction reliability
- **Regime Persistence**: Analyze regime duration and stability

### 2. Performance Impact
- **Strategy Adaptation**: How strategies perform in different regimes
- **Parameter Optimization**: Regime-specific parameter selection
- **Risk Management**: Regime-aware position sizing
- **Portfolio Allocation**: Regime-based asset allocation

### 3. Visualization Suite
- **Interactive Dashboards**: Real-time regime visualization
- **Historical Analysis**: Regime transitions over time
- **Performance Heatmaps**: Strategy performance by regime
- **Correlation Matrices**: Regime indicator relationships

### 4. Statistical Validation
- **Model Performance**: Accuracy, precision, recall metrics
- **Feature Importance**: Indicator significance analysis
- **Baseline Comparison**: Performance vs naive strategies
- **Robustness Testing**: Stability across different periods

## 🛠️ Technical Requirements

### Essential Dependencies
```python
pandas>=1.3.0          # Data manipulation
numpy>=1.21.0           # Numerical computations
matplotlib>=3.4.0       # Static plotting
seaborn>=0.11.0         # Statistical visualization
scikit-learn>=1.0.0     # Machine learning
```

### Optional Enhancements
```python
plotly>=5.0.0          # Interactive visualizations
scipy>=1.7.0           # Advanced statistical functions
```

## 🚀 Usage Guide

### Quick Start - Regime Analysis

#### Step 1: Data Preparation
```python
# Load EURCHF data
df = pd.read_csv('EURCHF BARS 30m.csv', sep='\t')
df['DATETIME'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'])
```

#### Step 2: Run Analysis
```bash
# Open the regime analysis notebook
jupyter notebook regimes.ipynb

# Execute all cells for complete analysis
```

#### Step 3: Interpret Results
- Review regime classification performance
- Analyze feature importance
- Examine prediction accuracy
- Study regime transition patterns

### Advanced Usage - Custom Analysis

#### Autocorrelation Studies
```bash
# Detailed autocorrelation analysis
jupyter notebook autocorrelation.ipynb
```

#### Balance Visualization
```bash
# Advanced balance curve analysis
jupyter notebook visualizzazioni\ balance.ipynb
```

## 📊 Expected Outputs

### Regime Analysis Results
```
📊 REGIME CLASSIFICATION RESULTS
   Model Accuracy: 0.642
   Baseline Accuracy: 0.567
   Improvement: +13.2%
   
   Feature Importance:
   - Autocorrelation (week): 0.345
   - Variance Ratio (week): 0.289
   - Autocorrelation (month): 0.201
   - Variance Ratio (month): 0.165
   
🎯 REGIME PREDICTIONS (Test Set)
   Trend Regime: 45.2% of periods
   Mean-Reversion: 54.8% of periods
   
📈 PERFORMANCE METRICS
   Precision (Trend): 0.67
   Recall (Trend): 0.58
   F1-Score (Trend): 0.62
```

### Visualization Outputs
- **Regime Timeline**: Price chart with regime overlays
- **Confusion Matrix**: Prediction accuracy visualization
- **Feature Importance**: Bar chart of indicator significance
- **Interactive Dashboards**: Real-time regime monitoring

## 🔍 Analysis Insights

### Key Findings
1. **Regime Persistence**: Market regimes tend to persist for several periods
2. **Predictive Power**: Autocorrelation and variance ratio provide significant predictive value
3. **Strategy Adaptation**: Different strategies perform better in different regimes
4. **Risk Management**: Regime awareness improves risk-adjusted returns

### Practical Applications
- **Strategy Selection**: Choose strategies based on predicted regime
- **Parameter Optimization**: Adjust parameters for current regime
- **Risk Management**: Increase position sizes in favorable regimes
- **Portfolio Allocation**: Rebalance based on regime predictions

## 🎯 Performance Optimization

### Computational Efficiency
- **Vectorized Operations**: Use pandas/numpy operations where possible
- **Memory Management**: Efficient data structures for large datasets
- **Caching**: Store intermediate results to avoid recalculation
- **Parallel Processing**: Utilize multiple cores for computation

### Model Optimization
- **Feature Selection**: Remove redundant indicators
- **Hyperparameter Tuning**: Optimize model parameters
- **Ensemble Methods**: Combine multiple models for better predictions
- **Online Learning**: Update models with new data

## 🆘 Troubleshooting

### Common Issues

#### Data Loading Problems
**Issue**: CSV reading errors
**Solution**: 
- Check file path and separator
- Verify datetime format
- Handle missing values appropriately

#### Model Training Errors
**Issue**: Insufficient data for training
**Solution**:
- Increase data window size
- Check for missing values
- Verify class balance

#### Visualization Issues
**Issue**: Plots not displaying
**Solution**:
- Restart kernel
- Check matplotlib/plotly installation
- Verify data format

### Performance Issues
**Issue**: Slow computation
**Solution**:
- Reduce data size for testing
- Use sampling for exploration
- Optimize rolling window calculations
- Consider GPU acceleration

## 📚 Further Reading

### Academic References
- Lo, A. W., & MacKinlay, A. C. (1988). Stock market prices do not follow random walks
- Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work
- Campbell, J. Y., Lo, A. W., & MacKinlay, A. C. (1997). The econometrics of financial markets

### Implementation Resources
- Pandas documentation for time series analysis
- Scikit-learn documentation for machine learning
- Plotly documentation for interactive visualization

## 🤝 Contributing

### Adding New Analysis
1. Follow existing notebook structure
2. Include comprehensive documentation
3. Implement proper error handling
4. Add visualization components
5. Update this README

### Code Quality
- Use descriptive variable names
- Include docstrings for functions
- Add comments for complex logic
- Follow PEP 8 style guidelines

---

**🎯 Comprehensive volatility analysis with rigorous methodology and actionable insights!**
