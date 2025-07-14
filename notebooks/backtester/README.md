
## backtester

Structure:
```
backtester/
├── data_loader.py
├── indicators.py
├── backtest_engine.py
├── visualization.py
├── utils.py
├── example_usage.ipynb
├── README.md
```

**What it does (extensive explanation):**
Allows you to:
- Load tick/minute/balance data
- Calculate technical indicators (Bollinger Bands, SMA, EMA, RSI)
- Run mean-reversion strategies on Bollinger Bands
- Analyze results: PnL, drawdown, Sharpe, winrate, equity curve
- Visualize performance and compare with real data

MIT License
