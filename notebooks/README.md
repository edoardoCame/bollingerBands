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
## Notebooks

Struttura:
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

Categorie:
- Portfolio Management: ottimizzazione/ribilanciamento portafoglio
- Volatility & Regime Analysis: volatilità, autocorrelazione, regimi
- Risk Management: filtri drawdown, metriche rischio
- MT5 Reports: analisi risultati MetaTrader 5
- Temp Tools: strumenti temporanei

**Come usare i moduli nei notebook (spiegazione estensiva):**
Importa funzioni dai moduli Python per:
- Applicare filtri rolling drawdown
- Calcolare pesi dinamici
- Ottimizzare parametri e analizzare performance

Esempio:
```python
from risk_management.dynamic_portfolio_modules.filters import apply_rolling_drawdown_filter
from risk_management.dynamic_portfolio_modules.utils import calculate_momentum_weights
# ...
```

Per dettagli tecnici sui moduli, vedi `risk management/dynamic_portfolio_modules/README_REFACTORING.md`.

