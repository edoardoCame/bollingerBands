"""
Core backtesting engine with optimized trading logic.

This module provides the main backtesting functionality using Numba
for performance optimization.
"""

import pandas as pd
import numpy as np
from numba import njit
from typing import List, Tuple, Dict, Any, Optional
import concurrent.futures
import os
from tqdm import tqdm


@njit
def backtest_core(
    bid: np.ndarray,
    ask: np.ndarray,
    midprice: np.ndarray,
    upper_band: np.ndarray,
    lower_band: np.ndarray,
    middle_band: np.ndarray,
    dates_array: np.ndarray = None  # New parameter for dates information
) -> List[Tuple[float, int, int, int]]:
    """
    Core backtesting logic implemented in Numba for performance.
    
    This function implements a Bollinger Bands mean reversion strategy:
    - Enter long when price crosses below lower band
    - Exit long when price crosses above middle band
    - Enter short when price crosses above upper band
    - Exit short when price crosses below middle band
    
    Additional Friday close logic:
    - Close all positions 15 minutes before market close on Friday
    - Don't open new positions during the last 15 minutes on Friday
    
    Parameters:
    bid (np.ndarray): Bid prices array.
    ask (np.ndarray): Ask prices array.
    midprice (np.ndarray): Midprice array.
    upper_band (np.ndarray): Upper Bollinger Band array.
    lower_band (np.ndarray): Lower Bollinger Band array.
    middle_band (np.ndarray): Middle Bollinger Band array.
    dates_array (np.ndarray): Array with encoded date information for Friday closing logic.
                             Each element is an integer with format:
                             - 1 for Friday in last 15 minutes
                             - 0 for all other times
    
    Returns:
    List[Tuple[float, int, int, int]]: List of trades with (PnL, Direction, Entry_idx, Exit_idx).
        - PnL: Profit/Loss in pips
        - Direction: 1 for long, -1 for short
        - Entry_idx: Index of entry point
        - Exit_idx: Index of exit point
    """
    n = len(midprice)
    trades = []
    position = 0  # 0 = flat, 1 = long, -1 = short
    entry_idx = -1
    entry_price = 0.0
    
    # If no dates array is provided, create a default one (no Friday closing)
    friday_close = np.zeros(n, dtype=np.int32) if dates_array is None else dates_array

    for i in range(1, n - 1):
        # Check if we're in the last 15 minutes of Friday
        is_friday_close_period = friday_close[i] == 1
        
        # Force close any open positions during Friday's last 15 minutes
        if is_friday_close_period and position != 0:
            exit_idx = i
            if exit_idx < n:
                if position == 1:  # Close long position
                    exit_price = bid[exit_idx]  # Sell at bid
                    pnl = (exit_price - entry_price) * 10000  # PnL in pips
                    trades.append((pnl, 1, entry_idx, exit_idx))
                else:  # Close short position
                    exit_price = ask[exit_idx]  # Buy at ask
                    pnl = (entry_price - exit_price) * 10000  # PnL in pips
                    trades.append((pnl, -1, entry_idx, exit_idx))
                
                position = 0
                entry_idx = -1
                entry_price = 0.0
                continue

        # Entry logic - only if we're not in Friday's last 15 minutes
        if position == 0 and not is_friday_close_period:
            # Long entry: cross below lower band
            if midprice[i-1] > lower_band[i-1] and midprice[i] < lower_band[i]:
                position = 1
                entry_idx = i + 1  # Enter at next bar
                if entry_idx < n:
                    entry_price = ask[entry_idx]  # Buy at ask
            # Short entry: cross above upper band
            elif midprice[i-1] < upper_band[i-1] and midprice[i] > upper_band[i]:
                position = -1
                entry_idx = i + 1  # Enter at next bar
                if entry_idx < n:
                    entry_price = bid[entry_idx]  # Sell at bid

        # Exit logic
        elif position == 1:
            # Exit long: cross above middle band (mean reversion)
            if midprice[i-1] < middle_band[i-1] and midprice[i] > middle_band[i]:
                exit_idx = i + 1
                if exit_idx < n:
                    exit_price = bid[exit_idx]  # Sell at bid
                    pnl = (exit_price - entry_price) * 10000  # PnL in pips
                    trades.append((pnl, 1, entry_idx, exit_idx))
                position = 0
                entry_idx = -1
                entry_price = 0.0

        elif position == -1:
            # Exit short: cross below middle band (mean reversion)
            if midprice[i-1] > middle_band[i-1] and midprice[i] < middle_band[i]:
                exit_idx = i + 1
                if exit_idx < n:
                    exit_price = ask[exit_idx]  # Buy at ask
                    pnl = (entry_price - exit_price) * 10000  # PnL in pips
                    trades.append((pnl, -1, entry_idx, exit_idx))
                position = 0
                entry_idx = -1
                entry_price = 0.0

    # Handle open position at the end (force close at last available price)
    if position == 1 and entry_idx < n:
        exit_price = bid[n-1]
        pnl = (exit_price - entry_price) * 10000
        trades.append((pnl, 1, entry_idx, n-1))
    elif position == -1 and entry_idx < n:
        exit_price = ask[n-1]
        pnl = (entry_price - exit_price) * 10000
        trades.append((pnl, -1, entry_idx, n-1))

    return trades


class Backtest:
    """
    Main backtesting class for running trading strategies on financial data.
    
    This class provides a high-level interface for backtesting trading strategies
    with proper data validation and result management.
    
    Attributes:
        data (pd.DataFrame): The input financial data with all required columns.
        results (List[Tuple]): List of trade results after running the backtest.
        performance_metrics (Dict): Dictionary containing performance statistics.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initialize the Backtest class with the provided data.

        Parameters:
        data (pd.DataFrame): DataFrame containing financial data with required columns:
                            'bid', 'ask', 'midprice', 'upper_band', 'lower_band', 'middle_band'.
        
        Raises:
        ValueError: If required columns are missing from the data.
        """
        # Required columns for backtesting
        required_columns = ['bid', 'ask', 'midprice', 'upper_band', 'lower_band', 'middle_band']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Store cleaned data (remove any NaN values)
        self.data = data.dropna()
        self.results: List[Tuple[float, int, int, int]] = []
        self.performance_metrics: Dict[str, Any] = {}
        
        # Validate data size
        if len(self.data) < 3:
            raise ValueError(
                f"Not enough data to run backtest: "
                f"need at least 3 rows, got {len(self.data)}."
            )

    def run(self) -> pd.DataFrame:
        """
        Execute the backtest using the Bollinger Bands strategy.

        Returns:
        pd.DataFrame: The original DataFrame with all data intact.
        
        Raises:
        ValueError: If there is insufficient data to run the backtest.
        """
        # Convert DataFrame columns to numpy arrays for Numba compatibility
        bid = self.data['bid'].to_numpy()
        ask = self.data['ask'].to_numpy()
        midprice = self.data['midprice'].to_numpy()
        upper_band = self.data['upper_band'].to_numpy()
        lower_band = self.data['lower_band'].to_numpy()
        middle_band = self.data['middle_band'].to_numpy()

        # Prepare the Friday closing time array
        friday_close_array = self._prepare_friday_close_array()

        # Execute the core backtesting logic
        self.results = backtest_core(bid, ask, midprice, upper_band, lower_band, middle_band, friday_close_array)
        
        # Calculate performance metrics
        self._calculate_performance_metrics()

        return self.data
        
    def _prepare_friday_close_array(self) -> np.ndarray:
        """
        Prepare an array that marks the last 15 minutes of data available on Fridays.
        In forex, markets operate 24 hours, so we simply take the last 15 minutes 
        available in the data for each Friday.
        
        Returns:
        np.ndarray: Array with 1's for Friday's last 15 minutes, 0's otherwise.
        """
        # Create an array filled with zeros
        friday_close = np.zeros(len(self.data), dtype=np.int32)
        
        # Check if the DataFrame has a datetime index
        if not isinstance(self.data.index, pd.DatetimeIndex):
            return friday_close
        
        # Find all Fridays (weekday=4 in pandas)
        fridays = self.data.index.weekday == 4
        if not np.any(fridays):
            return friday_close
        
        # Get Friday dates and their positions
        friday_dates = self.data.index[fridays].normalize()
        # Group by normalized date and get last 15 indices for each Friday
        # Use pandas groupby for vectorized operation
        idx = self.data.index
        friday_df = pd.DataFrame({'idx': idx, 'date': idx.normalize(), 'is_friday': fridays})
        # Only Fridays
        friday_df = friday_df[friday_df['is_friday']]
        # Group by date and get last 15 indices for each Friday
        last_15_idx = friday_df.groupby('date')['idx'].apply(lambda x: x[-15:]).explode().values
        # Mark these indices in our array
        friday_close[self.data.index.isin(last_15_idx)] = 1
        return friday_close



    def _calculate_performance_metrics(self) -> None:
        """
        Calculate various performance metrics from the trading results.
        
        This method calculates key performance indicators including:
        - Total PnL, number of trades, win rate, average trade
        - Maximum drawdown, Sharpe ratio, and other risk metrics
        """
        if not self.results:
            self.performance_metrics = {
                'total_trades': 0,
                'total_pnl': 0.0,
                'average_trade': 0.0,
                'win_rate': 0.0,
                'max_drawdown': 0.0,
                'winning_trades': 0,
                'losing_trades': 0
            }
            return

        # Extract PnL values
        pnl_values = [trade[0] for trade in self.results]
        
        # Basic metrics
        total_trades = len(self.results)
        total_pnl = sum(pnl_values)
        average_trade = total_pnl / total_trades if total_trades > 0 else 0.0
        
        # Win/Loss statistics
        winning_trades = sum(1 for pnl in pnl_values if pnl > 0)
        losing_trades = sum(1 for pnl in pnl_values if pnl < 0)
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0.0
        
        # Calculate maximum drawdown
        cumulative_pnl = np.cumsum(pnl_values)
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdown = running_max - cumulative_pnl
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0.0
        
        # Store metrics
        self.performance_metrics = {
            'total_trades': total_trades,
            'total_pnl': total_pnl,
            'average_trade': average_trade,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'best_trade': max(pnl_values) if pnl_values else 0.0,
            'worst_trade': min(pnl_values) if pnl_values else 0.0
        }

    def get_trades_dataframe(self) -> pd.DataFrame:
        """
        Convert trading results to a pandas DataFrame for easier analysis.
        
        Returns:
        pd.DataFrame: DataFrame with columns for PnL, Direction, Entry_idx, Exit_idx,
                     and additional calculated columns like cumulative PnL.
        """
        if not self.results:
            return pd.DataFrame()

        # Create DataFrame from results
        trades_df = pd.DataFrame(
            self.results, 
            columns=["PnL", "Direction", "Entry_idx", "Exit_idx"]
        )

        # Add cumulative PnL
        trades_df["Cumulative_PnL"] = trades_df["PnL"].cumsum()

        # Add timestamp information if available
        if len(self.results) > 0:
            exit_timestamps = []
            entry_timestamps = []
            for trade in self.results:
                entry_idx = trade[2]  # Entry index
                exit_idx = trade[3]   # Exit index
                # Entry time
                if entry_idx < len(self.data):
                    entry_time = self.data.index[entry_idx]
                else:
                    entry_time = self.data.index[-1]
                entry_timestamps.append(entry_time)
                # Exit time
                if exit_idx < len(self.data):
                    exit_time = self.data.index[exit_idx]
                else:
                    exit_time = self.data.index[-1]
                exit_timestamps.append(exit_time)
            trades_df['Entry_Time'] = entry_timestamps
            trades_df['Exit_Time'] = exit_timestamps

        return trades_df

    def print_performance_summary(self) -> None:
        """
        Print a comprehensive summary of the backtest performance.
        """
        print("=== BACKTEST PERFORMANCE SUMMARY ===")
        print(f"Total Trades: {self.performance_metrics['total_trades']}")
        print(f"Total PnL: {self.performance_metrics['total_pnl']:.2f} pips")
        print(f"Average Trade: {self.performance_metrics['average_trade']:.2f} pips")
        print(f"Win Rate: {self.performance_metrics['win_rate']:.2f}%")
        print(f"Winning Trades: {self.performance_metrics['winning_trades']}")
        print(f"Losing Trades: {self.performance_metrics['losing_trades']}")
        print(f"Best Trade: {self.performance_metrics['best_trade']:.2f} pips")
        print(f"Worst Trade: {self.performance_metrics['worst_trade']:.2f} pips")
        print(f"Maximum Drawdown: {self.performance_metrics['max_drawdown']:.2f} pips")
        print("=" * 40)


# Optimization functions - moved outside the class
def process_params_worker(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Worker function that calculates performance for a parameter set.
    
    This function is executed in parallel for each parameter combination
    during multicore optimization.
    
    Parameters:
    params (Dict[str, Any]): Dictionary containing parameters to test:
        - 'window': Time window for Bollinger Bands
        - 'num_std_dev': Number of standard deviations
        - 'minute_data': DataFrame with market data
        - 'price_column': Name of the price column to use
    
    Returns:
    Dict[str, Any]: Dictionary with performance results:
        - 'window': Tested time window
        - 'num_std_dev': Tested standard deviations
        - 'total_trades': Total number of trades
        - 'total_pnl': Total PnL in pips
        - 'win_rate': Percentage of winning trades
        - 'max_drawdown': Maximum drawdown
    """
    # Local imports to avoid pickling issues
    import sys
    import os
    sys.path.append('/home/edocame/Desktop/bollingerBands')
    from modules.backtester import indicators
    
    w = params['window']
    s = params['num_std_dev']
    minute_data = params['minute_data']
    price_column = params['price_column']
    
    # Calculate Bollinger Bands for current parameters
    df = indicators.bollinger_bands(
        minute_data, 
        price_column=price_column, 
        window=w, 
        num_std_dev=s
    ).dropna()
    
    # Return empty results if insufficient data
    if len(df) <= 100:
        return {
            'window': w,
            'num_std_dev': s,
            'total_trades': 0,
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'max_drawdown': 0.0
        }
    
    # Execute backtest
    bt = Backtest(df)
    bt.run()
    m = bt.performance_metrics
    
    return {
        'window': w,
        'num_std_dev': s,
        'total_trades': m.get('total_trades', 0),
        'total_pnl': m.get('total_pnl', 0.0),
        'win_rate': m.get('win_rate', 0.0),
        'max_drawdown': m.get('max_drawdown', 0.0)
    }


def optimize_parameters(
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
    Optimize Bollinger Bands parameters using multiprocessing.
    
    This function performs grid search optimization on Bollinger Bands parameters
    using all available CPU cores to maximize performance.
    
    Parameters:
    minute_data (pd.DataFrame): DataFrame with minute-level market data
    window_start (int): Starting value for time window
    window_stop (int): Ending value for time window
    window_step (int): Step size for time window
    std_start (float): Starting value for standard deviations
    std_stop (float): Ending value for standard deviations
    std_step (float): Step size for standard deviations
    price_column (str): Name of the price column to use
    
    Returns:
    pd.DataFrame: DataFrame with optimization results sorted by PnL
    
    Example:
    >>> results = optimize_parameters(
    ...     minute_data=data,
    ...     window_start=60,
    ...     window_stop=1440,
    ...     window_step=100,
    ...     std_start=1.0,
    ...     std_stop=3.0,
    ...     std_step=0.5
    ... )
    """
    import numpy as np
    
    # Generate parameter ranges to test
    window_range = np.arange(window_start, window_stop + window_step, window_step, dtype=int)
    std_range = np.arange(std_start, std_stop + std_step, std_step)
    
    # Create list of parameters to test
    parameters_to_test = [
        {
            'window': w,
            'num_std_dev': s,
            'minute_data': minute_data,
            'price_column': price_column
        }
        for w in window_range
        for s in std_range
    ]
    
    print(f"Starting optimization with {len(parameters_to_test)} parameter combinations...")
    print(f"Using {os.cpu_count()} cores for parallel computation.")
    
    # Execute multicore optimization
    results_summary = []
    max_workers = os.cpu_count() or 1
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Use executor.map with tqdm to monitor progress
        for result in tqdm(
            executor.map(process_params_worker, parameters_to_test),
            total=len(parameters_to_test),
            desc='Parameter optimization'
        ):
            results_summary.append(result)
    
    # Convert results to DataFrame and sort by PnL
    results_df = pd.DataFrame(results_summary)
    results_df = results_df.sort_values('total_pnl', ascending=False)
    
    print(f"\n=== OPTIMIZATION COMPLETED ===")
    print(f"Tested {len(results_df)} parameter sets")
    if not results_df.empty:
        print(f"Best result: {results_df.iloc[0]['total_pnl']:.2f} pips")
        print(f"Optimal parameters: window={results_df.iloc[0]['window']}, "
              f"std_dev={results_df.iloc[0]['num_std_dev']}")
    
    return results_df


def plot_top_equity_curves(
    results_df: pd.DataFrame,
    minute_data: pd.DataFrame,
    top_n: int = 5,
    price_column: str = 'midprice'
) -> None:
    """
    Plot equity curves for the top N parameter configurations.
    
    Parameters:
    results_df (pd.DataFrame): DataFrame with optimization results
    minute_data (pd.DataFrame): DataFrame with original market data
    top_n (int): Number of equity curves to plot (default: 5)
    price_column (str): Name of the price column to use
    
    Raises:
    ImportError: If matplotlib is not available
    """
    try:
        import matplotlib.pyplot as plt
        import sys
        sys.path.append('/home/edocame/Desktop/bollingerBands')
        from modules.backtester import indicators
    except ImportError as e:
        print(f"Error importing required libraries: {e}")
        return
    
    if results_df.empty:
        print("No results available for plotting.")
        return
    
    # Select top N parameters
    best_params = results_df.head(top_n)
    
    plt.figure(figsize=(14, 8))
    
    for i, (_, row) in enumerate(best_params.iterrows()):
        w, s = int(row['window']), float(row['num_std_dev'])
        
        # Recalculate Bollinger Bands and run backtest
        df_opt = indicators.bollinger_bands(
            minute_data, 
            price_column=price_column, 
            window=w, 
            num_std_dev=s
        ).dropna()
        
        if len(df_opt) > 100:  # Verify sufficient data
            bt_opt = Backtest(df_opt)
            bt_opt.run()
            trades_opt = bt_opt.get_trades_dataframe()
            
            if not trades_opt.empty:
                # Plot equity curve
                equity_series = trades_opt.set_index('Exit_Time')['Cumulative_PnL']
                plt.plot(
                    equity_series.index, 
                    equity_series.values,
                    label=f"#{i+1}: w={w}, std={s:.1f} (PnL: {row['total_pnl']:.1f})",
                    linewidth=2
                )
    
    plt.title(f"Top {top_n} Equity Curves - Parameter Optimization", fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Cumulative PnL (pips)", fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print(f"\n=== TOP {top_n} CONFIGURATIONS ===")
    for i, (_, row) in enumerate(best_params.iterrows()):
        print(f"#{i+1}: Window={int(row['window'])}, Std={row['num_std_dev']:.1f} "
              f"-> PnL: {row['total_pnl']:.2f} pips, "
              f"Trades: {row['total_trades']}, "
              f"Win Rate: {row['win_rate']:.1f}%")


# Export functions for easy import
__all__ = [
    'Backtest',
    'backtest_core',
    'process_params_worker',
    'optimize_parameters', 
    'plot_top_equity_curves'
]
