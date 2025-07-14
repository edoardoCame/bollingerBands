
## backtester

Struttura:
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

**Cosa fa (spiegazione estensiva):**
Permette di:
- Caricare dati tick/minuto/balance
- Calcolare indicatori tecnici (Bollinger Bands, SMA, EMA, RSI)
- Eseguire strategie mean-reversion sulle Bollinger Bands
- Analizzare risultati: PnL, drawdown, Sharpe, winrate, equity curve
- Visualizzare performance e confrontare con dati reali

MIT License
