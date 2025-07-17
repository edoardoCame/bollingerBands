bollingerBands/

# BollingerBands: Backtesting & Risk Management Suite

## Here you find:
- `fil## Essential Installation
```bash
pip install pandas numpy matplotlib plotly numba
```

## Essential Usage Example
```python
from modules.backtester import data_loader, indicators, backtest_engine
data = data_loader.load_parquet_data('file.parquet')
minute_data = data_loader.prepare_minute_data(data)
data_with_bands = indicators.bollinger_bands(minute_data, window=1440, num_std_dev=1.0)
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()
```

## Further Information
- `notebooks/backtester/` : Complete backtest examples
- `notebooks/risk management/` : Risk management, filters, portfolio notebooks
- `modules/dynamic_portfolio_modules/README_REFACTORING.md` : Technical module detailsawdown filters (automatic strategy stop on drawdown, no lookahead bias)
- `portfolio_rebalancer.py`: Dynamic portfolio rebalancing (momentum, sharpe, top N, equal, risk parity weighting)
- `performance_metrics.py`: Advanced risk/return metrics (VaR, ES, rolling metrics)
- `optimization.py`: Grid search and parameter optimization
- `linearity_analysis.py`: Equity curve linearity analysis (R², linearity score)
- `utils.py`, `data_loader.py`, ...

**Rolling Drawdown Filter (extensive explanation):**
The rolling drawdown filter monitors drawdown over a rolling window (e.g., 90 days) and stops the strategy if drawdown exceeds a threshold. During the stop, the balance remains constant. The strategy restarts only if drawdown recovers above a restart threshold. No lookahead bias: the loss that triggers the stop is always included in the filtered equity.Structure (dettagliata)

```
bollingerBands/
├── DATA/ 
│   ├── audjpy_1440_01.csv
│   ├── audjpy_14d_1.csv
│   ├── ...
├── modules/
│   ├── backtester/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── indicators.py
│   │   ├── backtest_engine.py
│   │   ├── visualization.py
│   │   ├── utils.py
│   │   └── walk_forward.py
│   └── dynamic_portfolio_modules/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── filters.py
│       ├── linearity_analysis.py
│       ├── optimization.py
│       ├── performance_metrics.py
│       ├── portfolio_rebalancer.py
│       ├── utils.py
│       ├── visualization.py
│       └── README_REFACTORING.md
├── notebooks/
│   ├── backtester/
│   │   ├── example_usage.ipynb
│   │   └── README.md
│   ├── MT5 REPORTS/
│   │   ├── deals.ipynb
│   │   ├── live_vs_backtest.ipynb
│   │   ├── mt5_analysis_clean.ipynb
│   │   └── README.md
│   ├── risk management/
│   │   ├── drawdown filter/
│   │   │   ├── autocorrelation.ipynb
│   │   │   ├── consecutive wins.ipynb
│   │   │   ├── regimes.ipynb
│   │   │   ├── rolling dd.ipynb
│   │   │   └── README.md
│   │   ├── collinearita_strategie.ipynb
│   │   ├── dynamic opt.ipynb
│   │   └── ...
│   ├── temp tools/
│   │   ├── convert to parquet.ipynb
│   │   ├── equity comparison.ipynb
│   │   └── ...
│   └── README.md
├── README.md
```

## Core Modules (extensive explanation)

### modules/backtester/
Contains everything needed to:
- Load tick/minute/balance data (`data_loader.py`)
- Calculate technical indicators (Bollinger Bands, SMA, EMA, RSI, etc. in `indicators.py`)
- Run mean-reversion strategies on Bollinger Bands (`backtest_engine.py`)
- Analyze results: PnL, drawdown, Sharpe, winrate, equity curve (`utils.py`)
- Visualize performance and compare with real data (`visualization.py`)

**How it works:**
1. Load historical data (tick/minute/balance)
2. Calculate Bollinger Bands or other indicators
3. Run the strategy backtest
4. Analyze and visualize the results

### modules/dynamic_portfolio_modules/
Qui trovi:
- `filters.py`: Filtri rolling drawdown (stop automatico strategie in drawdown, senza lookahead bias)
- `portfolio_rebalancer.py`: Ribilanciamento dinamico portafoglio (pesatura momentum, sharpe, top N, equal, risk parity)
- `performance_metrics.py`: Metriche rischio/rendimento avanzate (VaR, ES, rolling metrics)
- `optimization.py`: Grid search e ottimizzazione parametri
- `linearity_analysis.py`: Analisi linearità equity curve (R², score linearità)
- `utils.py`, `data_loader.py`, ...

**Rolling Drawdown Filter (spiegazione estensiva):**
Il filtro rolling drawdown monitora il drawdown su una finestra mobile (es. 90 giorni) e blocca la strategia se il drawdown supera una soglia. Durante lo stop, il bilancio resta costante. La strategia riparte solo se il drawdown rientra sotto una soglia di restart. Tutto senza lookahead bias: la perdita che fa scattare lo stop viene sempre inclusa nell’equity filtrata.

## Installazione Essenziale
```bash
pip install pandas numpy matplotlib plotly numba
```

## Esempio d’uso essenziale
```python
from backtester import data_loader, indicators, backtest_engine
data = data_loader.load_parquet_data('file.parquet')
minute_data = data_loader.prepare_minute_data(data)
data_with_bands = indicators.bollinger_bands(minute_data, window=1440, num_std_dev=1.0)
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()
```

## Approfondimenti
- `notebooks/backtester/` : Esempi completi di backtest
- `notebooks/risk management/` : Notebook su filtri, gestione rischio, portfolio
- `notebooks/risk management/dynamic_portfolio_modules/README_REFACTORING.md` : Dettagli tecnici moduli

MIT License
