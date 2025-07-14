"""
Backtesting Library for Trading Strategies.

This package provides a comprehensive set of tools for backtesting trading strategies,
particularly focused on Bollinger Bands and other technical indicators.

Main modules:
- data_loader: Functions for loading and preprocessing financial data
- indicators: Technical indicators calculation functions
- backtest_engine: Core backtesting engine with optimized performance
- visualization: Plotting and visualization utilities

Example usage:
    from backtester import data_loader, indicators, backtest_engine, visualization
    
    # Load data
    data = data_loader.load_parquet_data('path/to/data.parquet')
    minute_data = data_loader.prepare_minute_data(data)
    
    # Add indicators
    data_with_bands = indicators.bollinger_bands(minute_data)
    
    # Run backtest
    bt = backtest_engine.Backtest(data_with_bands)
    results = bt.run()
    
    # Visualize results
    visualization.plot_cumulative_pnl(bt.get_trades_dataframe())
"""

# Version information
__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main classes and functions for easy access
from .data_loader import (
    load_tick_data,
    load_parquet_data,
    prepare_minute_data,
    load_balance_data
)

from .indicators import (
    bollinger_bands,
    simple_moving_average,
    exponential_moving_average,
    relative_strength_index,
    calculate_volatility,
    price_change_percentage
)

from .backtest_engine import (
    Backtest,
    backtest_core
)

from .visualization import (
    plot_price_with_bollinger_bands,
    plot_cumulative_pnl,
    plot_interactive_price_bands,
    plot_interactive_cumulative_pnl,
    compare_backtest_vs_real_balance,
    plot_trade_distribution,
    create_performance_dashboard
)

from .walk_forward import (
    walk_forward_optimization,
    plot_wfo_results
)

# Define what gets imported with "from backtester import *"
__all__ = [
    # Data loading
    'load_tick_data',
    'load_parquet_data',
    'prepare_minute_data',
    'load_balance_data',
    
    # Indicators
    'bollinger_bands',
    'simple_moving_average',
    'exponential_moving_average',
    'relative_strength_index',
    'calculate_volatility',
    'price_change_percentage',
    
    # Backtesting
    'Backtest',
    'backtest_core',
    
    # Visualization
    'plot_price_with_bollinger_bands',
    'plot_cumulative_pnl',
    'plot_interactive_price_bands',
    'plot_interactive_cumulative_pnl',
    'compare_backtest_vs_real_balance',
    'plot_trade_distribution',
    'create_performance_dashboard',
    
    # Walk Forward Optimization
    'walk_forward_optimization',
    'plot_wfo_results'
]
