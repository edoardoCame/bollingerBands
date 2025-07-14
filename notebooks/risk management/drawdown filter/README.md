
# Drawdown Filter & Regime Analysis

This folder contains notebooks and tools for volatility analysis, market regime classification, and drawdown filtering. All advanced filtering logic is implemented in modular Python code (`risk management/dynamic_portfolio_modules/filters.py`).

## Contents

drawdown filter/
## drawdown filter

Structure:
```
drawdown filter/
├── autocorrelation.ipynb
├── consecutive wins.ipynb
├── regimes.ipynb
├── rolling dd.ipynb
├── README.md
```

**Rolling Drawdown Filter (extensive explanation):**
Monitors drawdown over a rolling window (e.g., 90 days) and stops the strategy if drawdown exceeds a threshold. During the stop, the balance remains constant. The strategy restarts only if drawdown recovers above a restart threshold. No lookahead bias: the loss that triggers the stop is always included in the filtered equity.

For batch/production use, leverage the Python modules in `modules/dynamic_portfolio_modules/filters.py`.
- For production or batch filtering, use the modular code in `dynamic_portfolio_modules/`

## Contributing
- Follow PEP 8 and project conventions
- Add docstrings and comments
- Update this README for new analysis

---
