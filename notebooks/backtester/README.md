
# Backtester Library

Libreria Python modulare per il backtesting di strategie di trading, con focus su Bollinger Bands e indicatori tecnici.

## Struttura

```
backtester/
├── __init__.py              # Modulo principale
├── data_loader.py           # Caricamento e preprocessing dati
├── indicators.py            # Indicatori tecnici
├── backtest_engine.py       # Motore di backtest
├── visualization.py         # Grafici e visualizzazioni
├── utils.py                 # Utility e analisi avanzate
├── example_usage.ipynb      # Esempio d'uso
└── README.md                # Questo file
```

## Installazione dipendenze

```bash
pip install pandas numpy matplotlib plotly numba
```

## Utilizzo rapido

```python
from backtester import data_loader, indicators, backtest_engine, visualization
data = data_loader.load_parquet_data('path/to/data.parquet')
minute_data = data_loader.prepare_minute_data(data)
data_with_bands = indicators.bollinger_bands(minute_data, window=1440, num_std_dev=1.0)
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()
backtester.print_performance_summary()
trades_df = backtester.get_trades_dataframe()
visualization.plot_cumulative_pnl(trades_df)
```

## Moduli principali

- **data_loader.py**: Caricamento dati tick, parquet, balance
- **indicators.py**: Bollinger Bands, SMA, EMA, RSI, volatilità
- **backtest_engine.py**: Motore di backtest, logica mean-reversion
- **visualization.py**: Grafici prezzi, PnL, dashboard
- **utils.py**: Sharpe, drawdown, win/loss, ottimizzazione parametri

## Strategia implementata

Mean reversion su Bollinger Bands:
- Entrata Long: prezzo sotto banda inferiore
- Uscita Long: prezzo sopra media mobile
- Entrata Short: prezzo sopra banda superiore
- Uscita Short: prezzo sotto media mobile

## Metriche di performance

- Numero trade, PnL totale, PnL medio, win rate
- Max drawdown, Sharpe, profit factor, best/worst trade

## Esempi avanzati

Test parametri:
```python
for params in [
    {'window': 720, 'num_std_dev': 1.0},
    {'window': 1440, 'num_std_dev': 1.5},
    {'window': 2880, 'num_std_dev': 2.0},
]:
    data_with_bands = indicators.bollinger_bands(minute_data, **params)
    backtester = backtest_engine.Backtest(data_with_bands.dropna())
    backtester.run()
    backtester.print_performance_summary()
```

Confronto con dati reali:
```python
balance_data = data_loader.load_balance_data('balance_file.csv')
trades_df = backtester.get_trades_dataframe()
visualization.compare_backtest_vs_real_balance(trades_df, balance_data, title="Backtest vs Real Performance")
```

## Estendibilità

- Aggiungi indicatori in `indicators.py`
- Nuove strategie in `backtest_engine.py`
- Nuove visualizzazioni in `visualization.py`
- Nuove metriche in `utils.py`

## Contributi

1. Segui PEP 8 e le convenzioni del progetto
2. Includi docstring e commenti
3. Aggiungi test per nuove funzionalità
4. Documenta le modifiche nel README

## Licenza

MIT License
