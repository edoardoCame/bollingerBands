"""
Walk Forward Optimization module for backtesting strategies.

This module provides functions for performing walk forward optimization
to avoid lookhead bias in backtesting strategies.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Optional
from datetime import timedelta

from . import indicators, backtest_engine


def _optimize_parameters_wfo(
    minute_data: pd.DataFrame,
    window_start: int,
    window_stop: int,
    window_step: int,
    std_start: float,
    std_stop: float,
    std_step: float,
    price_column: str = 'midprice'
) -> pd.DataFrame:
    """
    Optimize parameters for walk forward optimization using single-threaded approach.
    This avoids multiprocessing import issues.
    """
    import numpy as np
    from tqdm import tqdm
    
    # Generate parameter ranges to test
    window_range = np.arange(window_start, window_stop + window_step, window_step, dtype=int)
    std_range = np.arange(std_start, std_stop + std_step, std_step)
    
    # Create list of parameters to test
    parameters_to_test = [
        {'window': w, 'num_std_dev': s}
        for w in window_range
        for s in std_range
    ]
    
    print(f"Starting optimization with {len(parameters_to_test)} parameter combinations...")
    print("Using single-threaded approach for reliability.")
    
    # Execute single-threaded optimization
    results_summary = []
    
    for params in tqdm(parameters_to_test, desc='Parameter optimization'):
        w = params['window']
        s = params['num_std_dev']
        
        try:
            # Calculate Bollinger Bands for current parameters
            df = indicators.bollinger_bands(
                minute_data, 
                price_column=price_column, 
                window=w, 
                num_std_dev=s
            ).dropna()
            
            # Check if we have sufficient data
            if len(df) <= 50:
                result = {
                    'window': w,
                    'num_std_dev': s,
                    'total_trades': 0,
                    'total_pnl': 0.0,
                    'win_rate': 0.0,
                    'max_drawdown': 0.0
                }
            else:
                # Execute backtest
                bt = backtest_engine.Backtest(df)
                bt.run()
                m = bt.performance_metrics
                
                result = {
                    'window': w,
                    'num_std_dev': s,
                    'total_trades': m.get('total_trades', 0),
                    'total_pnl': m.get('total_pnl', 0.0),
                    'win_rate': m.get('win_rate', 0.0),
                    'max_drawdown': m.get('max_drawdown', 0.0)
                }
            
            results_summary.append(result)
            
        except Exception as e:
            print(f"Error processing params w={w}, s={s}: {e}")
            result = {
                'window': w,
                'num_std_dev': s,
                'total_trades': 0,
                'total_pnl': 0.0,
                'win_rate': 0.0,
                'max_drawdown': 0.0
            }
            results_summary.append(result)
    
    # Convert results to DataFrame and sort by PnL
    results_df = pd.DataFrame(results_summary)
    results_df = results_df.sort_values('total_pnl', ascending=False)
    
    return results_df


def walk_forward_optimization(
    minute_data: pd.DataFrame,
    lookback_days: int = 30,
    optimization_interval_days: int = 7,
    window_start: int = 400,
    window_stop: int = 14400,
    window_step: int = 100,
    std_start: float = 0.5,
    std_stop: float = 3.0,
    std_step: float = 0.5,
    price_column: str = 'midprice'
) -> Dict[str, Any]:
    """
    Perform Walk Forward Optimization to avoid lookhead bias.
    
    This function systematically divides the data into sequential periods,
    optimizes parameters on historical data, then applies them to future
    unseen data to simulate realistic trading conditions.
    
    Algorithm approach:
    1. Use a rolling window of lookback_days for parameter optimization
    2. Apply optimized parameters to the next optimization_interval_days
    3. Repeat until all data is processed
    4. Combine results for comprehensive analysis
    
    Parameters:
    minute_data (pd.DataFrame): Complete minute-level market data with OHLC
    lookback_days (int): Number of days to use for optimization (default: 30)
    optimization_interval_days (int): How often to re-optimize in days (default: 7)  
    window_start (int): Starting window for Bollinger Bands optimization
    window_stop (int): Ending window for Bollinger Bands optimization
    window_step (int): Step size for window optimization
    std_start (float): Starting std dev for Bollinger Bands optimization
    std_stop (float): Ending std dev for Bollinger Bands optimization
    std_step (float): Step size for std dev optimization
    price_column (str): Column name for price data
    
    Returns:
    Dict[str, Any]: Dictionary containing WFO results and comprehensive analysis
        - optimization_periods: List of optimization time periods
        - trading_periods: List of trading time periods
        - optimal_parameters: List of best parameters for each period
        - period_performances: List of performance metrics per period
        - all_trades: List of all trades executed
        - summary_stats: Overall performance statistics
        - combined_trades: Combined DataFrame of all trades
    
    Raises:
    ValueError: If insufficient data or invalid parameters provided
    """
    # Convert days to minutes for easier calculation
    lookback_minutes = lookback_days * 24 * 60
    optimization_interval_minutes = optimization_interval_days * 24 * 60
    
    # Validate input parameters
    if lookback_days <= 0 or optimization_interval_days <= 0:
        raise ValueError("Lookback and optimization interval must be positive")
    
    if len(minute_data) < lookback_minutes:
        raise ValueError(f"Insufficient data: need at least {lookback_days} days")
    
    # Initialize results storage with proper structure
    wfo_results: Dict[str, Any] = {
        'optimization_periods': [],
        'trading_periods': [],
        'optimal_parameters': [],
        'period_performances': [],
        'all_trades': [],
        'summary_stats': {}
    }
    
    print(f"=== WALK FORWARD OPTIMIZATION ===")
    print(f"Lookback period: {lookback_days} days ({lookback_minutes} minutes)")
    print(f"Optimization interval: {optimization_interval_days} days")
    print(f"Total data period: {minute_data.index.min()} to {minute_data.index.max()}")
    
    # Calculate the first optimization start point
    # We need enough data for the lookback period
    start_idx = lookback_minutes
    data_length = len(minute_data)
    
    period_count = 0
    
    # Main WFO loop - ensures no lookhead bias
    while start_idx + optimization_interval_minutes < data_length:
        period_count += 1
        
        # Define optimization period (lookback data - historical only)
        opt_start_idx = start_idx - lookback_minutes
        opt_end_idx = start_idx
        
        # Define trading period (forward data - future unseen data)
        trade_start_idx = start_idx
        trade_end_idx = min(start_idx + optimization_interval_minutes, data_length)
        
        # Extract data for optimization and trading
        # This ensures strict temporal separation
        opt_data = minute_data.iloc[opt_start_idx:opt_end_idx].copy()
        trade_data = minute_data.iloc[trade_start_idx:trade_end_idx].copy()
        
        opt_start_time = opt_data.index.min()
        opt_end_time = opt_data.index.max()
        trade_start_time = trade_data.index.min()
        trade_end_time = trade_data.index.max()
        
        print(f"\n--- Period {period_count} ---")
        print(f"Optimization: {opt_start_time} to {opt_end_time}")
        print(f"Trading: {trade_start_time} to {trade_end_time}")
        
        # Optimize parameters on historical data only
        try:
            # Run optimization on the lookback period
            opt_results = _optimize_parameters_wfo(
                minute_data=opt_data,
                window_start=window_start,
                window_stop=window_stop,
                window_step=window_step,
                std_start=std_start,
                std_stop=std_stop,
                std_step=std_step,
                price_column=price_column
            )
            
            # Handle edge case: no optimization results
            if opt_results.empty:
                print(f"No optimization results for period {period_count}, skipping...")
                start_idx += optimization_interval_minutes
                continue
            
            # Get the best parameters from optimization
            best_params = opt_results.iloc[0]
            optimal_window = int(best_params['window'])
            optimal_std = float(best_params['num_std_dev'])
            
            print(f"Optimal parameters: window={optimal_window}, std_dev={optimal_std:.1f}")
            
            # Apply optimal parameters to forward trading period
            trade_data_with_bands = indicators.bollinger_bands(
                trade_data,
                price_column=price_column,
                window=optimal_window,
                num_std_dev=optimal_std
            ).dropna()
            
            # Handle edge case: insufficient trading data
            if len(trade_data_with_bands) < 10:
                print(f"Insufficient trading data for period {period_count}, skipping...")
                start_idx += optimization_interval_minutes
                continue
            
            # Run backtest on trading period with optimal parameters
            trade_backtester = backtest_engine.Backtest(trade_data_with_bands)
            trade_backtester.run()
            
            # Get trading results
            period_trades = trade_backtester.get_trades_dataframe()
            period_performance = trade_backtester.performance_metrics
            
            # Store results for analysis
            wfo_results['optimization_periods'].append({
                'start': opt_start_time,
                'end': opt_end_time,
                'period': period_count
            })
            
            wfo_results['trading_periods'].append({
                'start': trade_start_time,
                'end': trade_end_time,
                'period': period_count
            })
            
            wfo_results['optimal_parameters'].append({
                'period': period_count,
                'window': optimal_window,
                'std_dev': optimal_std,
                'opt_pnl': best_params['total_pnl']
            })
            
            wfo_results['period_performances'].append({
                'period': period_count,
                'total_pnl': period_performance['total_pnl'],
                'total_trades': period_performance['total_trades'],
                'win_rate': period_performance['win_rate'],
                'max_drawdown': period_performance['max_drawdown']
            })
            
            # Add period identifier to trades for tracking
            if not period_trades.empty:
                period_trades['period'] = period_count
                wfo_results['all_trades'].append(period_trades)
            
            print(f"Period {period_count} results: "
                  f"PnL={period_performance['total_pnl']:.2f} pips, "
                  f"Trades={period_performance['total_trades']}, "
                  f"Win Rate={period_performance['win_rate']:.1f}%")
            
        except Exception as e:
            print(f"Error in period {period_count}: {e}")
            # Continue to next period on error
        
        # Move to next period
        start_idx += optimization_interval_minutes
    
    # Combine all trades and calculate summary statistics
    if wfo_results['all_trades']:
        combined_trades = pd.concat(wfo_results['all_trades'], ignore_index=True)
        
        # Calculate overall WFO performance metrics
        total_pnl = combined_trades['PnL'].sum()
        total_trades = len(combined_trades)
        winning_trades = (combined_trades['PnL'] > 0).sum()
        losing_trades = (combined_trades['PnL'] < 0).sum()
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate maximum drawdown using cumulative approach
        cumulative_pnl = combined_trades['PnL'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = running_max - cumulative_pnl
        max_drawdown = drawdown.max()
        
        # Store comprehensive summary statistics
        wfo_results['summary_stats'] = {
            'total_periods': period_count,
            'total_pnl': total_pnl,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'avg_pnl_per_period': total_pnl / period_count if period_count > 0 else 0
        }
        
        wfo_results['combined_trades'] = combined_trades
    
    return wfo_results


def plot_wfo_results(wfo_results: Dict[str, Any]) -> None:
    """
    Plot comprehensive Walk Forward Optimization results.
    
    Creates a 2x2 subplot layout showing:
    1. Cumulative PnL over time
    2. PnL by period (bar chart)
    3. Parameter evolution over time
    4. Win rate by period
    
    Parameters:
    wfo_results (Dict[str, Any]): Results from walk_forward_optimization
    
    Raises:
    ValueError: If no trading results are available to plot
    """
    # Handle edge case: no trading results
    if not wfo_results['all_trades']:
        print("No trading results to plot.")
        return
    
    # Create comprehensive subplot layout
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Cumulative PnL over time
    combined_trades = wfo_results['combined_trades']
    axes[0, 0].plot(combined_trades.index, combined_trades['PnL'].cumsum(), 
                    linewidth=2, color='blue')
    axes[0, 0].set_title('WFO Cumulative PnL Over Time', fontsize=12)
    axes[0, 0].set_xlabel('Trade Number')
    axes[0, 0].set_ylabel('Cumulative PnL (pips)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: PnL by period with color coding
    period_pnls = [p['total_pnl'] for p in wfo_results['period_performances']]
    period_numbers = [p['period'] for p in wfo_results['period_performances']]
    
    # Color bars based on profit/loss
    colors = ['green' if p >= 0 else 'red' for p in period_pnls]
    axes[0, 1].bar(period_numbers, period_pnls, color=colors, alpha=0.7)
    axes[0, 1].set_title('PnL by Period', fontsize=12)
    axes[0, 1].set_xlabel('Period')
    axes[0, 1].set_ylabel('PnL (pips)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Plot 3: Parameter evolution over time
    windows = [p['window'] for p in wfo_results['optimal_parameters']]
    stds = [p['std_dev'] for p in wfo_results['optimal_parameters']]
    
    # Use twin axes for different scales
    ax3_twin = axes[1, 0].twinx()
    line1 = axes[1, 0].plot(period_numbers, windows, 'b-o', label='Window', markersize=4)
    line2 = ax3_twin.plot(period_numbers, stds, 'r-s', label='Std Dev', markersize=4)
    
    axes[1, 0].set_xlabel('Period')
    axes[1, 0].set_ylabel('Window Size', color='b')
    ax3_twin.set_ylabel('Std Dev', color='r')
    axes[1, 0].set_title('Parameter Evolution', fontsize=12)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Combine legends for both y-axes
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    axes[1, 0].legend(lines, labels, loc='upper left')
    
    # Plot 4: Win rate by period
    win_rates = [p['win_rate'] for p in wfo_results['period_performances']]
    axes[1, 1].bar(period_numbers, win_rates, color='lightblue', alpha=0.7)
    axes[1, 1].axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% line')
    axes[1, 1].set_title('Win Rate by Period', fontsize=12)
    axes[1, 1].set_xlabel('Period')
    axes[1, 1].set_ylabel('Win Rate (%)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_ylim(0, 100)
    
    plt.tight_layout()
    plt.show()
    
    # Print comprehensive summary statistics
    stats = wfo_results['summary_stats']
    print(f"\n=== WALK FORWARD OPTIMIZATION SUMMARY ===")
    print(f"Total Periods: {stats['total_periods']}")
    print(f"Total PnL: {stats['total_pnl']:.2f} pips")
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Winning Trades: {stats['winning_trades']}")
    print(f"Losing Trades: {stats['losing_trades']}")
    print(f"Win Rate: {stats['win_rate']:.2f}%")
    print(f"Max Drawdown: {stats['max_drawdown']:.2f} pips")
    print(f"Average PnL per Period: {stats['avg_pnl_per_period']:.2f} pips")
    
    # Calculate additional performance metrics
    if stats['total_trades'] > 0:
        avg_pnl_per_trade = stats['total_pnl'] / stats['total_trades']
        print(f"Average PnL per Trade: {avg_pnl_per_trade:.2f} pips")
    
    print("=" * 45)


# Export functions for easy import
__all__ = [
    'walk_forward_optimization',
    'plot_wfo_results'
]
