
# Drawdown Filter & Regime Analysis

This folder contains notebooks and tools for volatility analysis, market regime classification, and drawdown filtering. All advanced filtering logic is implemented in modular Python code (`risk management/dynamic_portfolio_modules/filters.py`).

## Contents

## drawdown filter

Struttura:
```
drawdown filter/
├── autocorrelation.ipynb
├── consecutive wins.ipynb
├── regimes.ipynb
├── rolling dd.ipynb
├── README.md
```

**Rolling Drawdown Filter (spiegazione estensiva):**
Monitora il drawdown su una finestra mobile (es. 90 giorni) e blocca la strategia se il drawdown supera una soglia. Durante lo stop, il bilancio resta costante. La strategia riparte solo se il drawdown rientra sotto una soglia di restart. Nessun lookahead bias: la perdita che fa scattare lo stop viene sempre inclusa nell’equity filtrata.

Per uso batch/produzione, usa i moduli Python in `risk management/dynamic_portfolio_modules/filters.py`.
- For production or batch filtering, use the modular code in `dynamic_portfolio_modules/`

## Contributing
- Follow PEP 8 and project conventions
- Add docstrings and comments
- Update this README for new analysis

---
