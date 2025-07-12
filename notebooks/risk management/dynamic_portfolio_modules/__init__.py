"""
Dynamic Portfolio Optimization Modules
======================================

This package contains modular components for dynamic portfolio optimization
with advanced features like drawdown filtering and linearity-based optimization.

Modules:
--------
- utils: Utility functions for scoring and weight calculation
- data_loader: Functions for loading and preprocessing trading data
- portfolio_rebalancer: Main portfolio rebalancing class
- performance_metrics: Performance calculation and evaluation functions
- optimization: Grid search and optimization routines
- filters: Drawdown and other filtering mechanisms
- linearity_analysis: Linearity-based portfolio optimization
- visualization: Plotting and visualization utilities

Usage:
------
from dynamic_portfolio_modules import data_loader, portfolio_rebalancer
from dynamic_portfolio_modules import optimization, visualization

# Load data
strategies, combined_df, returns_df = data_loader.load_trading_data()

# Create rebalancer
rebalancer = portfolio_rebalancer.DynamicPortfolioRebalancer(returns_df)

# Run optimization
results = optimization.grid_search_optimization(rebalancer)
"""

__version__ = "1.0.0"
__author__ = "Portfolio Optimization Team"

# Import main classes and functions for easy access
try:
    from .data_loader import load_trading_data
    from .portfolio_rebalancer import DynamicPortfolioRebalancer
    from .performance_metrics import calculate_performance_metrics
    from .optimization import grid_search_optimization, optimize_single_config
    from .filters import apply_rolling_drawdown_filter, create_filtered_rebalancer
    from .linearity_analysis import calculate_linearity_metrics, grid_search_optimization_linearity
    from .visualization import plot_equity_curves, plot_weight_allocation, plot_performance_comparison
    from . import utils
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")
    print("This is normal during initial setup. Individual modules can still be imported directly.")
