"""
Utility functions for backtesting analysis.

This module provides helper functions for performance analysis,
risk calculations, and other utility operations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import warnings


def calculate_sharpe_ratio(
    returns: pd.Series, 
    risk_free_rate: float = 0.0, 
    periods_per_year: int = 252
) -> float:
    """
    Calculate the Sharpe ratio for a series of returns.
    
    Parameters:
    returns (pd.Series): Series of returns.
    risk_free_rate (float): Risk-free rate (annualized).
    periods_per_year (int): Number of periods per year for annualization.
    
    Returns:
    float: Sharpe ratio.
    """
    if len(returns) == 0:
        return 0.0
    
    excess_returns = returns - risk_free_rate / periods_per_year
    
    if excess_returns.std() == 0:
        return 0.0
    
    return (excess_returns.mean() * np.sqrt(periods_per_year)) / excess_returns.std()


def calculate_maximum_drawdown(cumulative_returns: pd.Series) -> Tuple[float, pd.Timestamp, pd.Timestamp]:
    """
    Calculate maximum drawdown and the period over which it occurred.
    
    Parameters:
    cumulative_returns (pd.Series): Series of cumulative returns.
    
    Returns:
    Tuple[float, pd.Timestamp, pd.Timestamp]: Maximum drawdown, start date, end date.
    """
    if len(cumulative_returns) == 0:
        return 0.0, None, None
    
    # Calculate running maximum
    running_max = cumulative_returns.expanding().max()
    
    # Calculate drawdown
    drawdown = (cumulative_returns - running_max) / running_max
    
    # Find maximum drawdown
    max_dd = drawdown.min()
    
    # Find the period of maximum drawdown
    max_dd_end = drawdown.idxmin()
    max_dd_start = cumulative_returns.loc[:max_dd_end].idxmax()
    
    return max_dd, max_dd_start, max_dd_end


def calculate_calmar_ratio(
    returns: pd.Series, 
    periods_per_year: int = 252
) -> float:
    """
    Calculate the Calmar ratio (annual return / maximum drawdown).
    
    Parameters:
    returns (pd.Series): Series of returns.
    periods_per_year (int): Number of periods per year for annualization.
    
    Returns:
    float: Calmar ratio.
    """
    if len(returns) == 0:
        return 0.0
    
    # Calculate annualized return
    annualized_return = returns.mean() * periods_per_year
    
    # Calculate maximum drawdown
    cumulative_returns = (1 + returns).cumprod()
    max_dd, _, _ = calculate_maximum_drawdown(cumulative_returns)
    
    if max_dd == 0:
        return float('inf') if annualized_return > 0 else 0.0
    
    return annualized_return / abs(max_dd)


def calculate_win_loss_ratio(pnl_series: pd.Series) -> Dict[str, float]:
    """
    Calculate win/loss statistics.
    
    Parameters:
    pnl_series (pd.Series): Series of PnL values.
    
    Returns:
    Dict[str, float]: Dictionary with win/loss statistics.
    """
    if len(pnl_series) == 0:
        return {
            'win_rate': 0.0,
            'loss_rate': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'win_loss_ratio': 0.0,
            'profit_factor': 0.0
        }
    
    winning_trades = pnl_series[pnl_series > 0]
    losing_trades = pnl_series[pnl_series < 0]
    
    total_trades = len(pnl_series)
    win_count = len(winning_trades)
    loss_count = len(losing_trades)
    
    win_rate = (win_count / total_trades) * 100 if total_trades > 0 else 0.0
    loss_rate = (loss_count / total_trades) * 100 if total_trades > 0 else 0.0
    
    avg_win = winning_trades.mean() if len(winning_trades) > 0 else 0.0
    avg_loss = losing_trades.mean() if len(losing_trades) > 0 else 0.0
    
    win_loss_ratio = avg_win / abs(avg_loss) if avg_loss != 0 else float('inf')
    
    total_profits = winning_trades.sum() if len(winning_trades) > 0 else 0.0
    total_losses = abs(losing_trades.sum()) if len(losing_trades) > 0 else 0.0
    
    profit_factor = total_profits / total_losses if total_losses != 0 else float('inf')
    
    return {
        'win_rate': win_rate,
        'loss_rate': loss_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'win_loss_ratio': win_loss_ratio,
        'profit_factor': profit_factor
    }


def calculate_var_and_cvar(
    returns: pd.Series, 
    confidence_level: float = 0.05
) -> Tuple[float, float]:
    """
    Calculate Value at Risk (VaR) and Conditional Value at Risk (CVaR).
    
    Parameters:
    returns (pd.Series): Series of returns.
    confidence_level (float): Confidence level (e.g., 0.05 for 95% confidence).
    
    Returns:
    Tuple[float, float]: VaR and CVaR values.
    """
    if len(returns) == 0:
        return 0.0, 0.0
    
    # Calculate VaR
    var = returns.quantile(confidence_level)
    
    # Calculate CVaR (expected shortfall)
    cvar = returns[returns <= var].mean()
    
    return var, cvar


def analyze_trade_duration(
    trades_df: pd.DataFrame,
    timestamp_col: str = 'Exit_Time'
) -> Dict[str, Any]:
    """
    Analyze trade duration statistics.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame with trade data.
    timestamp_col (str): Column name containing timestamps.
    
    Returns:
    Dict[str, Any]: Dictionary with duration statistics.
    """
    if len(trades_df) == 0 or timestamp_col not in trades_df.columns:
        return {
            'avg_duration': pd.Timedelta(0),
            'median_duration': pd.Timedelta(0),
            'min_duration': pd.Timedelta(0),
            'max_duration': pd.Timedelta(0)
        }
    
    # Calculate trade durations (assuming consecutive trades)
    durations = []
    for i in range(1, len(trades_df)):
        duration = trades_df.iloc[i][timestamp_col] - trades_df.iloc[i-1][timestamp_col]
        durations.append(duration)
    
    if not durations:
        return {
            'avg_duration': pd.Timedelta(0),
            'median_duration': pd.Timedelta(0),
            'min_duration': pd.Timedelta(0),
            'max_duration': pd.Timedelta(0)
        }
    
    duration_series = pd.Series(durations)
    
    return {
        'avg_duration': duration_series.mean(),
        'median_duration': duration_series.median(),
        'min_duration': duration_series.min(),
        'max_duration': duration_series.max()
    }


def calculate_monthly_returns(
    trades_df: pd.DataFrame,
    timestamp_col: str = 'Exit_Time'
) -> pd.Series:
    """
    Calculate monthly returns from trade data.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame with trade data.
    timestamp_col (str): Column name containing timestamps.
    
    Returns:
    pd.Series: Monthly returns series.
    """
    if len(trades_df) == 0 or timestamp_col not in trades_df.columns:
        return pd.Series(dtype=float)
    
    # Set timestamp as index
    trades_monthly = trades_df.set_index(timestamp_col)
    
    # Group by month and sum PnL
    monthly_returns = trades_monthly['PnL'].resample('M').sum()
    
    return monthly_returns


def detect_regime_changes(
    price_series: pd.Series,
    window: int = 20,
    threshold: float = 0.02
) -> pd.Series:
    """
    Detect regime changes in price series using rolling volatility.
    
    Parameters:
    price_series (pd.Series): Price series.
    window (int): Rolling window for volatility calculation.
    threshold (float): Threshold for regime change detection.
    
    Returns:
    pd.Series: Boolean series indicating regime changes.
    """
    # Calculate rolling volatility
    rolling_vol = price_series.rolling(window=window).std()
    
    # Calculate volatility changes
    vol_change = rolling_vol.pct_change().abs()
    
    # Detect regime changes
    regime_changes = vol_change > threshold
    
    return regime_changes


def optimize_parameters(
    data: pd.DataFrame,
    param_ranges: Dict[str, List],
    backtest_function: callable,
    metric: str = 'total_pnl'
) -> Dict[str, Any]:
    """
    Simple parameter optimization using grid search.
    
    Parameters:
    data (pd.DataFrame): Input data for backtesting.
    param_ranges (Dict[str, List]): Dictionary of parameter ranges to test.
    backtest_function (callable): Function to run backtest with given parameters.
    metric (str): Metric to optimize (default: 'total_pnl').
    
    Returns:
    Dict[str, Any]: Best parameters and results.
    """
    best_result = None
    best_params = None
    best_metric_value = float('-inf')
    
    # Generate all parameter combinations
    import itertools
    param_names = list(param_ranges.keys())
    param_values = list(param_ranges.values())
    
    for param_combination in itertools.product(*param_values):
        params = dict(zip(param_names, param_combination))
        
        try:
            # Run backtest with current parameters
            result = backtest_function(data, **params)
            
            # Check if this is the best result so far
            if hasattr(result, 'performance_metrics'):
                metric_value = result.performance_metrics.get(metric, float('-inf'))
                
                if metric_value > best_metric_value:
                    best_metric_value = metric_value
                    best_params = params
                    best_result = result
        
        except Exception as e:
            warnings.warn(f"Error with parameters {params}: {str(e)}")
            continue
    
    return {
        'best_params': best_params,
        'best_result': best_result,
        'best_metric_value': best_metric_value
    }


def export_results_to_csv(
    trades_df: pd.DataFrame,
    performance_metrics: Dict[str, Any],
    filename: str
) -> None:
    """
    Export backtest results to CSV files.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame with trade results.
    performance_metrics (Dict[str, Any]): Performance metrics dictionary.
    filename (str): Base filename for the exports.
    """
    # Export trades
    trades_filename = f"{filename}_trades.csv"
    trades_df.to_csv(trades_filename, index=False)
    
    # Export performance metrics
    metrics_filename = f"{filename}_metrics.csv"
    metrics_df = pd.DataFrame([performance_metrics])
    metrics_df.to_csv(metrics_filename, index=False)
    
    print(f"Results exported to {trades_filename} and {metrics_filename}")


def create_performance_report(
    trades_df: pd.DataFrame,
    performance_metrics: Dict[str, Any],
    data_period: Tuple[str, str] = None
) -> str:
    """
    Create a comprehensive performance report as a formatted string.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame with trade results.
    performance_metrics (Dict[str, Any]): Performance metrics dictionary.
    data_period (Tuple[str, str]): Start and end dates of the data period.
    
    Returns:
    str: Formatted performance report.
    """
    report = []
    report.append("=" * 50)
    report.append("BACKTEST PERFORMANCE REPORT")
    report.append("=" * 50)
    
    if data_period:
        report.append(f"Data Period: {data_period[0]} to {data_period[1]}")
        report.append("-" * 50)
    
    # Basic metrics
    report.append("BASIC METRICS:")
    report.append(f"  Total Trades: {performance_metrics.get('total_trades', 0)}")
    report.append(f"  Total PnL: {performance_metrics.get('total_pnl', 0):.2f} pips")
    report.append(f"  Average Trade: {performance_metrics.get('average_trade', 0):.2f} pips")
    report.append(f"  Best Trade: {performance_metrics.get('best_trade', 0):.2f} pips")
    report.append(f"  Worst Trade: {performance_metrics.get('worst_trade', 0):.2f} pips")
    report.append("")
    
    # Win/Loss metrics
    report.append("WIN/LOSS METRICS:")
    report.append(f"  Win Rate: {performance_metrics.get('win_rate', 0):.2f}%")
    report.append(f"  Winning Trades: {performance_metrics.get('winning_trades', 0)}")
    report.append(f"  Losing Trades: {performance_metrics.get('losing_trades', 0)}")
    report.append("")
    
    # Risk metrics
    report.append("RISK METRICS:")
    report.append(f"  Maximum Drawdown: {performance_metrics.get('max_drawdown', 0):.2f} pips")
    report.append("")
    
    # Additional analysis if trades data is available
    if not trades_df.empty:
        pnl_series = trades_df['PnL']
        win_loss_stats = calculate_win_loss_ratio(pnl_series)
        
        report.append("ADDITIONAL ANALYSIS:")
        report.append(f"  Average Win: {win_loss_stats['avg_win']:.2f} pips")
        report.append(f"  Average Loss: {win_loss_stats['avg_loss']:.2f} pips")
        report.append(f"  Win/Loss Ratio: {win_loss_stats['win_loss_ratio']:.2f}")
        report.append(f"  Profit Factor: {win_loss_stats['profit_factor']:.2f}")
        report.append("")
    
    report.append("=" * 50)
    
    return "\n".join(report)
