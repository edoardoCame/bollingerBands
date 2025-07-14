bollingerBands/

# BollingerBands: Backtesting & Risk Management Suite

## 📦 Project Structure (dettagliata)

```
bollingerBands/
├── DATA/ 
│   ├── audjpy_1440_01.csv
│   ├── audjpy_14d_1.csv
│   ├── ...
├── notebooks/
│   ├── backtester/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── indicators.py
│   │   ├── backtest_engine.py
│   │   ├── visualization.py
│   │   ├── utils.py
│   │   ├── example_usage.ipynb
│   │   └── README.md
│   ├── MT5 REPORTS/
│   │   ├── deals.ipynb
│   │   ├── live_vs_backtest.ipynb
│   │   ├── mt5_analysis_clean.ipynb
│   │   └── README.md
│   ├── risk management/
│   │   ├── dynamic_portfolio_modules/
│   │   │   ├── __init__.py
│   │   │   ├── data_loader.py
│   │   │   ├── filters.py
│   │   │   ├── linearity_analysis.py
│   │   │   ├── optimization.py
│   │   │   ├── performance_metrics.py
│   │   │   ├── portfolio_rebalancer.py
│   │   │   ├── utils.py
│   │   │   └── README_REFACTORING.md
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
│   ├── README.md
├── README.md
```

## Moduli Core (spiegazione estensiva)

### backtester/
Contiene tutto il necessario per:
- Caricare dati tick/minuto/balance (`data_loader.py`)
- Calcolare indicatori tecnici (Bollinger Bands, SMA, EMA, RSI, ecc. in `indicators.py`)
- Eseguire strategie mean-reversion sulle Bollinger Bands (`backtest_engine.py`)
- Analizzare risultati: PnL, drawdown, Sharpe, winrate, equity curve (`utils.py`)
- Visualizzare performance e confrontare con dati reali (`visualization.py`)

**Come funziona:**
1. Carichi i dati storici (tick/minuto/balance)
2. Calcoli le Bollinger Bands o altri indicatori
3. Esegui il backtest della strategia
4. Analizzi e visualizzi i risultati

### risk management/dynamic_portfolio_modules/
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
