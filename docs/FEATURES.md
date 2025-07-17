# Features and Examples Guide

Comprehensive guide showcasing the advanced features and capabilities of the Bollinger Bands Trading Suite with practical examples.

## Table of Contents

- [Core Features Overview](#core-features-overview)
- [Trading Strategy Features](#trading-strategy-features)
- [Portfolio Management Features](#portfolio-management-features)
- [Risk Management Features](#risk-management-features)
- [Advanced Analytics Features](#advanced-analytics-features)
- [Integration Features](#integration-features)
- [Performance Features](#performance-features)

## Core Features Overview

### 🎯 Strategy Engine
- **Numba-accelerated backtesting** for high-performance execution
- **Multiple timeframe support** (minute, hourly, daily data)
- **Comprehensive technical indicators** (Bollinger Bands, SMA, EMA, RSI)
- **Flexible data formats** (CSV, Parquet support)

### 📊 Portfolio Management
- **5 allocation strategies** (Equal, Momentum, Sharpe-Momentum, Top-N, Risk Parity)
- **Dynamic rebalancing** with configurable frequencies
- **Multi-currency portfolio** construction
- **Correlation-based diversification**

### 🛡️ Risk Control
- **Rolling drawdown filters** with no lookahead bias
- **Advanced risk metrics** (VaR, Expected Shortfall, Calmar Ratio)
- **Regime-aware risk management**
- **Automatic strategy stopping/restarting**

## Trading Strategy Features

### Bollinger Bands Strategy Implementation

#### Basic Setup
```python
from modules.backtester import data_loader, indicators, backtest_engine

# Load and prepare data
data = data_loader.load_csv_data('DATA/eurusd_1440_01.csv')
minute_data = data_loader.prepare_minute_data(data)

# Calculate Bollinger Bands with custom parameters
data_with_bands = indicators.bollinger_bands(
    minute_data, 
    window=1440,      # 24-hour window for daily bands
    num_std_dev=1.5   # Tighter bands for more signals
)

# Advanced indicator combinations
data_with_bands['rsi'] = indicators.rsi(data_with_bands, 'midprice', 14)
data_with_bands['sma_200'] = indicators.sma(data_with_bands, 'midprice', 200)
```

#### Advanced Strategy Customization
```python
# Multi-timeframe analysis
def multi_timeframe_bollinger(data):
    """Apply Bollinger Bands on multiple timeframes"""
    timeframes = [1440, 4320, 10080]  # 1d, 3d, 1w
    
    for tf in timeframes:
        bands = indicators.bollinger_bands(data, window=tf, num_std_dev=2.0)
        data[f'upper_band_{tf}'] = bands['upper_band']
        data[f'lower_band_{tf}'] = bands['lower_band']
        data[f'bb_width_{tf}'] = bands['bb_width']
    
    return data

# Apply to your data
enhanced_data = multi_timeframe_bollinger(data_with_bands)
```

#### Strategy Entry/Exit Logic
The core strategy implements sophisticated mean-reversion logic:

**Long Entry Conditions:**
- Price crosses below lower Bollinger Band
- RSI below 30 (oversold confirmation)
- Volume above average (momentum confirmation)

**Long Exit Conditions:**
- Price crosses above middle band (moving average)
- RSI above 70 (profit taking)
- Stop loss at 2x band width

**Short Entry/Exit:** Mirror logic for short positions

### Performance Optimization Features

#### Numba Acceleration
```python
# The core backtesting loop is optimized with Numba
from modules.backtester.backtest_engine import backtest_core
import numpy as np

# This function processes thousands of data points in milliseconds
@njit  # Numba just-in-time compilation
def optimized_strategy_logic(prices, signals):
    # Ultra-fast strategy execution
    return trade_results
```

#### Vectorized Operations
```python
# Efficient pandas operations for large datasets
def calculate_signals_vectorized(data):
    """Vectorized signal calculation for better performance"""
    
    # Bollinger Band signals
    long_signals = (data['midprice'] < data['lower_band']) & \
                   (data['rsi'] < 30)
    
    short_signals = (data['midprice'] > data['upper_band']) & \
                    (data['rsi'] > 70)
    
    # Exit signals
    long_exits = data['midprice'] > data['middle_band']
    short_exits = data['midprice'] < data['middle_band']
    
    return long_signals, short_signals, long_exits, short_exits
```

## Portfolio Management Features

### Dynamic Allocation Strategies

#### 1. Momentum-Based Allocation
```python
from modules.dynamic_portfolio_modules import DynamicPortfolioRebalancer

# Load multiple strategy returns
strategies, combined_df, returns_df = load_trading_data('DATA/')

# Create portfolio with momentum allocation
rebalancer = DynamicPortfolioRebalancer(returns_df)

# Momentum strategy: Allocate more to recent outperformers
momentum_results = rebalancer.backtest(
    method='momentum',
    lookback_days=30,        # Look back 30 days for momentum
    rebalance_frequency=7,   # Rebalance weekly
    volatility_adjustment=True  # Adjust for volatility
)
```

#### 2. Sharpe-Adjusted Momentum
```python
# Risk-adjusted momentum allocation
sharpe_momentum_results = rebalancer.backtest(
    method='sharpe_momentum',
    lookback_days=60,        # Longer lookback for stability
    min_periods=20,          # Minimum data points required
    rebalance_frequency=14   # Bi-weekly rebalancing
)
```

#### 3. Top-N Strategy Selection
```python
# Focus on best-performing strategies only
top_n_results = rebalancer.backtest(
    method='top_n_ranking',
    top_n=3,                 # Select top 3 strategies
    ranking_metric='sharpe', # Rank by Sharpe ratio
    rebalance_frequency=30   # Monthly rebalancing
)
```

#### 4. Risk Parity Allocation
```python
# Equal risk contribution from each strategy
risk_parity_results = rebalancer.backtest(
    method='risk_parity',
    lookback_days=90,        # Longer period for risk estimation
    rebalance_frequency=7,
    min_weight=0.05,         # Minimum 5% allocation
    max_weight=0.40          # Maximum 40% allocation
)
```

### Advanced Portfolio Analytics

#### Correlation Analysis
```python
from modules.dynamic_portfolio_modules.utils import calculate_correlation_matrix

# Analyze strategy correlations
correlation_matrix = calculate_correlation_matrix(returns_df)

# Identify highly correlated strategies
high_corr_pairs = []
for i in range(len(correlation_matrix)):
    for j in range(i+1, len(correlation_matrix)):
        if abs(correlation_matrix.iloc[i, j]) > 0.7:
            high_corr_pairs.append((
                correlation_matrix.index[i], 
                correlation_matrix.columns[j],
                correlation_matrix.iloc[i, j]
            ))

print("Highly correlated strategy pairs:")
for pair in high_corr_pairs:
    print(f"{pair[0]} - {pair[1]}: {pair[2]:.3f}")
```

#### Portfolio Optimization
```python
from modules.dynamic_portfolio_modules.optimization import grid_search_optimization

# Comprehensive parameter optimization
optimization_results = grid_search_optimization(
    rebalancer,
    methods=['momentum', 'sharpe_momentum', 'equal', 'risk_parity'],
    rebalance_frequencies=[7, 14, 30],
    lookback_days=[30, 60, 90],
    parallel=True,           # Use multiprocessing
    n_jobs=-1               # Use all CPU cores
)

# Best configuration
best_config = optimization_results.iloc[0]
print(f"Best method: {best_config['method']}")
print(f"Best frequency: {best_config['rebalance_frequency']} days")
print(f"Best lookback: {best_config['lookback_days']} days")
print(f"Sharpe ratio: {best_config['sharpe_ratio']:.3f}")
```

## Risk Management Features

### Rolling Drawdown Filter

#### Basic Implementation
```python
from modules.dynamic_portfolio_modules.filters import apply_rolling_drawdown_filter

# Apply rolling drawdown protection
filtered_strategies = apply_rolling_drawdown_filter(
    strategies,
    threshold=0.15,          # Stop at 15% drawdown
    window=90,               # 90-day rolling window
    restart_threshold=0.10   # Restart at 10% drawdown
)

# Compare performance before and after filtering
original_performance = strategies.sum(axis=1).cumsum()
filtered_performance = filtered_strategies.sum(axis=1).cumsum()
```

#### Advanced Filter Configuration
```python
# Multi-level risk management
def advanced_risk_management(strategies):
    # Level 1: Individual strategy protection
    level1_filtered = apply_rolling_drawdown_filter(
        strategies,
        threshold=0.20,      # Individual strategy threshold
        window=60
    )
    
    # Level 2: Portfolio-level protection  
    portfolio_equity = level1_filtered.sum(axis=1).cumsum()
    portfolio_dd = calculate_drawdown(portfolio_equity)
    
    # Stop entire portfolio if drawdown > 25%
    stop_mask = portfolio_dd > 0.25
    
    # Apply portfolio-level stops
    final_filtered = level1_filtered.copy()
    final_filtered.loc[stop_mask] = 0
    
    return final_filtered
```

### Advanced Risk Metrics

#### Value at Risk (VaR) and Expected Shortfall
```python
from modules.dynamic_portfolio_modules.performance_metrics import calculate_performance_metrics

# Calculate comprehensive risk metrics
portfolio_returns = filtered_performance.pct_change().dropna()

risk_metrics = calculate_performance_metrics(
    portfolio_returns,
    include_rolling=True,
    var_confidence=0.05,     # 5% VaR
    es_confidence=0.05       # 5% Expected Shortfall
)

print(f"Daily VaR (5%): {risk_metrics['var_5']:.3f}")
print(f"Daily Expected Shortfall (5%): {risk_metrics['expected_shortfall_5']:.3f}")
print(f"Maximum Drawdown: {risk_metrics['max_drawdown']:.3f}")
print(f"Calmar Ratio: {risk_metrics['calmar_ratio']:.3f}")
```

#### Rolling Risk Analysis
```python
# Dynamic risk monitoring
def rolling_risk_analysis(returns, window=90):
    """Calculate rolling risk metrics"""
    rolling_metrics = {}
    
    rolling_metrics['volatility'] = returns.rolling(window).std() * np.sqrt(252)
    rolling_metrics['var_5'] = returns.rolling(window).quantile(0.05)
    rolling_metrics['sharpe'] = (returns.rolling(window).mean() * 252) / \
                                (returns.rolling(window).std() * np.sqrt(252))
    
    return pd.DataFrame(rolling_metrics)

# Apply to portfolio
rolling_risks = rolling_risk_analysis(portfolio_returns)
```

## Advanced Analytics Features

### Market Regime Analysis

#### Regime Classification
```python
from modules.dynamic_portfolio_modules.regime_analysis import classify_market_regimes

# Classify market conditions
regime_data = classify_market_regimes(
    price_data,
    trend_window=100,        # Window for trend detection
    volatility_window=30,    # Window for volatility regime
    autocorr_lags=10        # Lags for autocorrelation analysis
)

# Strategy performance by regime
regime_performance = {}
for regime in ['trending', 'mean_reverting', 'high_vol', 'low_vol']:
    mask = regime_data['regime'] == regime
    regime_performance[regime] = {
        'return': portfolio_returns[mask].mean() * 252,
        'volatility': portfolio_returns[mask].std() * np.sqrt(252),
        'sharpe': (portfolio_returns[mask].mean() * 252) / 
                 (portfolio_returns[mask].std() * np.sqrt(252))
    }
```

#### Autocorrelation Analysis
```python
def autocorrelation_analysis(returns, max_lags=20):
    """Analyze return predictability"""
    from scipy.stats import jarque_bera
    
    # Calculate autocorrelations
    autocorrs = [returns.autocorr(lag=i) for i in range(1, max_lags+1)]
    
    # Test for randomness
    jb_stat, jb_pvalue = jarque_bera(returns.dropna())
    
    # Ljung-Box test for autocorrelation
    from scipy.stats import jarque_bera  # Use appropriate test
    
    return {
        'autocorrelations': autocorrs,
        'jarque_bera_pvalue': jb_pvalue,
        'mean_reversion_strength': sum(autocorrs[:5]) / 5
    }
```

### Linearity Analysis

#### Equity Curve Smoothness Optimization
```python
from modules.dynamic_portfolio_modules.linearity_analysis import grid_search_optimization_linearity

# Optimize for smooth equity curves
linearity_results = grid_search_optimization_linearity(
    rebalancer,
    optimize_for='linearity_score',  # Target smooth growth
    weight_return=0.3,              # 30% weight on returns
    weight_linearity=0.7,           # 70% weight on smoothness
    methods=['momentum', 'equal']
)

# Best linearity configuration
best_linear = linearity_results.iloc[0]
print(f"Best linearity score: {best_linear['linearity_score']:.3f}")
print(f"R-squared: {best_linear['r_squared']:.3f}")
```

## Integration Features

### MetaTrader 5 Integration

#### Automatic XML Analysis
```python
# Analyze MT5 optimization results
from notebooks.MT5_REPORTS.mt5_analysis_clean import MT5Analyzer

analyzer = MT5Analyzer('mt5_optimization_results.xml')

# Extract top configurations
top_configs = analyzer.get_top_configurations(
    metric='profit_factor',
    top_n=10,
    min_trades=100
)

# Compare with Python backtest
python_results = backtester.run()
mt5_results = analyzer.get_configuration_results(top_configs[0])

comparison = {
    'python_return': python_results['total_return'],
    'mt5_return': mt5_results['total_return'],
    'python_sharpe': python_results['sharpe_ratio'],
    'mt5_sharpe': mt5_results['sharpe_ratio']
}
```

#### Live vs Backtest Validation
```python
def validate_live_performance(backtest_results, live_results):
    """Compare live trading with backtest expectations"""
    
    # Calculate performance degradation
    return_degradation = (backtest_results['annual_return'] - 
                         live_results['annual_return']) / \
                        backtest_results['annual_return']
    
    # Estimate transaction costs
    estimated_costs = abs(return_degradation) * 0.5  # Assume 50% due to costs
    
    # Calculate slippage impact
    slippage_impact = abs(return_degradation) - estimated_costs
    
    return {
        'return_degradation': return_degradation,
        'estimated_transaction_costs': estimated_costs,
        'slippage_impact': slippage_impact,
        'validation_score': 1 - abs(return_degradation)  # Higher is better
    }
```

## Performance Features

### Parallel Processing

#### Multi-Core Optimization
```python
from multiprocessing import Pool
import os

def parallel_backtest(strategy_params):
    """Run backtest for single parameter set"""
    # Backtest logic here
    return results

# Parallel grid search
def parallel_grid_search(param_grid):
    n_cores = os.cpu_count() - 1  # Leave one core free
    
    with Pool(n_cores) as pool:
        results = pool.map(parallel_backtest, param_grid)
    
    return results

# Example usage
param_combinations = [
    {'window': 20, 'std_dev': 1.5},
    {'window': 40, 'std_dev': 2.0},
    {'window': 60, 'std_dev': 2.5}
]

parallel_results = parallel_grid_search(param_combinations)
```

### Memory Optimization

#### Efficient Data Handling
```python
# Memory-efficient data processing
def process_large_dataset(file_path, chunk_size=10000):
    """Process large datasets in chunks"""
    results = []
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        chunk_result = process_chunk(chunk)
        results.append(chunk_result)
        
        # Free memory
        del chunk
        gc.collect()
    
    return pd.concat(results)

# Optimize data types
def optimize_dtypes(df):
    """Reduce memory usage by optimizing data types"""
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = df[col].astype('float32')
        elif df[col].dtype == 'int64':
            df[col] = df[col].astype('int32')
    
    return df
```

### Caching and Persistence

#### Results Caching
```python
from functools import lru_cache
import pickle

@lru_cache(maxsize=128)
def cached_backtest(window, std_dev, symbol):
    """Cache backtest results to avoid recomputation"""
    # Expensive backtest calculation
    return results

# Persistent caching
def save_results(results, filename):
    """Save results for later use"""
    with open(f'cache/{filename}.pkl', 'wb') as f:
        pickle.dump(results, f)

def load_results(filename):
    """Load previously saved results"""
    with open(f'cache/{filename}.pkl', 'rb') as f:
        return pickle.load(f)
```

This comprehensive guide demonstrates the full capabilities of the Bollinger Bands Trading Suite. Each feature is designed to work together, providing a complete solution for quantitative trading strategy development and portfolio management.