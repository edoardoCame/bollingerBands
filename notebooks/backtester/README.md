# Backtester Library

Una libreria Python modulare per il backtesting di strategie di trading, con particolare focus sulle Bollinger Bands e altri indicatori tecnici.

## Struttura della libreria

```
backtester/
├── __init__.py              # Modulo principale con importazioni
├── data_loader.py           # Funzioni per caricare e preprocessare i dati
├── indicators.py            # Calcolo degli indicatori tecnici
├── backtest_engine.py       # Engine principale per il backtesting
├── visualization.py         # Funzioni per grafici e visualizzazioni
├── utils.py                 # Funzioni di utilità e analisi avanzate
├── example_usage.ipynb      # Notebook di esempio
└── README.md               # Questa documentazione
```

## Installazione delle dipendenze

Prima di utilizzare la libreria, assicurati di avere installate le seguenti dipendenze:

```bash
pip install pandas numpy matplotlib plotly numba
```

## Utilizzo rapido

### Esempio base

```python
# Importa la libreria
from backtester import data_loader, indicators, backtest_engine, visualization

# 1. Carica i dati
data = data_loader.load_parquet_data('path/to/your/data.parquet')
minute_data = data_loader.prepare_minute_data(data)

# 2. Calcola gli indicatori
data_with_bands = indicators.bollinger_bands(minute_data, window=1440, num_std_dev=1.0)

# 3. Esegui il backtest
backtester = backtest_engine.Backtest(data_with_bands.dropna())
results = backtester.run()

# 4. Visualizza i risultati
backtester.print_performance_summary()
trades_df = backtester.get_trades_dataframe()
visualization.plot_cumulative_pnl(trades_df)
```

## Moduli principali

### 1. data_loader.py

Fornisce funzioni per caricare e preprocessare i dati finanziari:

- `load_tick_data(file_path)`: Carica dati tick da file CSV
- `load_parquet_data(file_path)`: Carica dati da file Parquet
- `prepare_minute_data(tick_data)`: Converte dati tick in dati a minuto
- `load_balance_data(file_path)`: Carica dati di balance per confronti

### 2. indicators.py

Calcola indicatori tecnici comuni:

- `bollinger_bands(data, window, num_std_dev)`: Calcola le Bollinger Bands
- `simple_moving_average(data, window)`: Media mobile semplice
- `exponential_moving_average(data, window)`: Media mobile esponenziale
- `relative_strength_index(data, window)`: RSI
- `calculate_volatility(data, window)`: Volatilità rolling

### 3. backtest_engine.py

Engine principale per il backtesting:

- `Backtest`: Classe principale per eseguire backtest
- `backtest_core()`: Funzione ottimizzata con Numba per performance
- Logica di trading per strategia Bollinger Bands mean-reversion

### 4. visualization.py

Funzioni per visualizzare risultati:

- `plot_price_with_bollinger_bands()`: Grafico prezzi con bande
- `plot_cumulative_pnl()`: Grafico PnL cumulativo
- `plot_interactive_price_bands()`: Grafici interattivi con Plotly
- `compare_backtest_vs_real_balance()`: Confronto con dati reali
- `create_performance_dashboard()`: Dashboard completo

### 5. utils.py

Funzioni di utilità avanzate:

- `calculate_sharpe_ratio()`: Calcola Sharpe ratio
- `calculate_maximum_drawdown()`: Calcola maximum drawdown
- `calculate_win_loss_ratio()`: Statistiche win/loss
- `optimize_parameters()`: Ottimizzazione parametri
- `export_results_to_csv()`: Esportazione risultati
- `create_performance_report()`: Report testuale completo

## Strategia implementata

La libreria implementa una strategia di **mean reversion** basata sulle Bollinger Bands:

### Logica di trading:
1. **Entrata Long**: Quando il prezzo attraversa al di sotto della banda inferiore
2. **Uscita Long**: Quando il prezzo attraversa al di sopra della banda centrale (media mobile)
3. **Entrata Short**: Quando il prezzo attraversa al di sopra della banda superiore
4. **Uscita Short**: Quando il prezzo attraversa al di sotto della banda centrale

### Gestione delle posizioni:
- I trade vengono eseguiti al prezzo ask/bid del minuto successivo al segnale
- Il PnL è calcolato in pips (moltiplicazione per 10000)
- Le posizioni aperte alla fine del periodo vengono chiuse automaticamente

## Metriche di performance

La libreria calcola automaticamente diverse metriche:

- **Total Trades**: Numero totale di operazioni
- **Total PnL**: Profitto/perdita totale in pips
- **Average Trade**: PnL medio per operazione
- **Win Rate**: Percentuale di operazioni vincenti
- **Max Drawdown**: Massimo drawdown
- **Best/Worst Trade**: Migliore e peggiore operazione
- **Sharpe Ratio**: Rapporto risk-adjusted return
- **Profit Factor**: Rapporto tra profitti e perdite

## Esempi di utilizzo

### Test con parametri diversi

```python
# Test con diversi parametri delle Bollinger Bands
parameters = [
    {'window': 720, 'num_std_dev': 1.0},   # 12 ore
    {'window': 1440, 'num_std_dev': 1.5},  # 24 ore
    {'window': 2880, 'num_std_dev': 2.0},  # 48 ore
]

for params in parameters:
    data_with_bands = indicators.bollinger_bands(minute_data, **params)
    backtester = backtest_engine.Backtest(data_with_bands.dropna())
    backtester.run()
    backtester.print_performance_summary()
```

### Confronto con dati reali

```python
# Confronta risultati backtest con balance reale
balance_data = data_loader.load_balance_data('balance_file.csv')
trades_df = backtester.get_trades_dataframe()

visualization.compare_backtest_vs_real_balance(
    trades_df, 
    balance_data, 
    title="Backtest vs Real Performance"
)
```

### Analisi avanzate

```python
from backtester import utils

# Calcola metriche di rischio avanzate
pnl_series = trades_df['PnL']
sharpe = utils.calculate_sharpe_ratio(pnl_series)
win_loss_stats = utils.calculate_win_loss_ratio(pnl_series)

# Crea report completo
report = utils.create_performance_report(
    trades_df, 
    backtester.performance_metrics
)
print(report)
```

## Ottimizzazione performance

- **Numba**: Le funzioni critiche utilizzano Numba per ottimizzazione JIT
- **Vectorizzazione**: Uso di operazioni pandas vettorizzate
- **Memory efficiency**: Gestione ottimizzata della memoria per grandi dataset

## Estensibilità

La libreria è progettata per essere facilmente estensibile:

1. **Nuovi indicatori**: Aggiungi funzioni in `indicators.py`
2. **Nuove strategie**: Modifica `backtest_core()` in `backtest_engine.py`
3. **Nuove visualizzazioni**: Aggiungi funzioni in `visualization.py`
4. **Nuove metriche**: Espandi `utils.py` con nuove analisi

## File di esempio

Il file `example_usage.ipynb` fornisce un esempio completo di utilizzo della libreria, incluso:

- Caricamento dati
- Calcolo indicatori
- Esecuzione backtest
- Visualizzazione risultati
- Analisi performance
- Confronto con dati reali
- Test di parametri diversi

## Note sui dati

La libreria supporta:

- **Dati tick**: CSV con colonne date, time, bid, ask
- **Dati Parquet**: File Parquet con bid/ask
- **Dati balance**: CSV con colonne date e balance per confronti
- **Resampling**: Conversione automatica da tick a minuto

## Limitazioni attuali

- Strategia implementata solo per Bollinger Bands mean-reversion
- Supporto limitato per commissioni e slippage
- Logica di position sizing fissa (1 unità per trade)

## Sviluppi futuri

- Supporto per multiple strategie
- Gestione commissioni e slippage
- Position sizing dinamico
- Integrazione con broker API
- Backtesting multi-asset
- Ottimizzazione parametri automatica avanzata

## Contributi

Per contribuire alla libreria:

1. Segui le convenzioni Python PEP 8
2. Includi docstring per tutte le funzioni
3. Aggiungi test per nuove funzionalità
4. Documenta le modifiche nel README

## Licenza

Questa libreria è distribuita sotto licenza MIT.
