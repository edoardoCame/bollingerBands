"""
Visualization utilities for backtesting results.

This module provides functions to create various charts and plots
for analyzing backtest performance and market data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, List, Tuple, Dict, Any


def plot_price_with_bollinger_bands(
    data: pd.DataFrame,
    title: str = "Price with Bollinger Bands",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Plot price data with Bollinger Bands using matplotlib.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing price and Bollinger Bands data.
    title (str): Title for the plot.
    figsize (Tuple[int, int]): Figure size (width, height).
    save_path (Optional[str]): Path to save the plot (if provided).
    """
    # Check required columns
    required_columns = ['midprice', 'upper_band', 'lower_band', 'middle_band']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    plt.figure(figsize=figsize)
    
    # Plot price and bands
    plt.plot(data.index, data['midprice'], label='Price', color='black', linewidth=1)
    plt.plot(data.index, data['upper_band'], label='Upper Band', color='red', linestyle='--')
    plt.plot(data.index, data['lower_band'], label='Lower Band', color='blue', linestyle='--')
    plt.plot(data.index, data['middle_band'], label='Middle Band', color='green', linestyle='-')
    
    # Fill between bands
    plt.fill_between(data.index, data['lower_band'], data['upper_band'], alpha=0.1, color='gray')
    
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_cumulative_pnl(
    trades_df: pd.DataFrame,
    title: str = "Cumulative PnL",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Plot cumulative PnL over time using matplotlib.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame containing trade results with 'Cumulative_PnL' column.
    title (str): Title for the plot.
    figsize (Tuple[int, int]): Figure size (width, height).
    save_path (Optional[str]): Path to save the plot (if provided).
    """
    if 'Cumulative_PnL' not in trades_df.columns:
        raise ValueError("DataFrame must contain 'Cumulative_PnL' column")
    
    plt.figure(figsize=figsize)
    
    # Plot cumulative PnL
    plt.plot(trades_df.index, trades_df['Cumulative_PnL'], 
             label='Cumulative PnL', color='blue', linewidth=2)
    
    # Add zero line
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.title(title)
    plt.xlabel('Trade Number')
    plt.ylabel('Cumulative PnL (pips)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_interactive_price_bands(
    data: pd.DataFrame,
    title: str = "Interactive Price with Bollinger Bands"
) -> None:
    """
    Create an interactive plot of price data with Bollinger Bands using Plotly.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing price and Bollinger Bands data.
    title (str): Title for the plot.
    """
    # Check required columns
    required_columns = ['midprice', 'upper_band', 'lower_band', 'middle_band']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['midprice'],
        mode='lines',
        name='Price',
        line=dict(color='black', width=1)
    ))
    
    # Add Bollinger Bands
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['upper_band'],
        mode='lines',
        name='Upper Band',
        line=dict(color='red', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['lower_band'],
        mode='lines',
        name='Lower Band',
        line=dict(color='blue', dash='dash'),
        fill='tonexty',
        fillcolor='rgba(128, 128, 128, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['middle_band'],
        mode='lines',
        name='Middle Band',
        line=dict(color='green')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        template='plotly_white',
        hovermode='x unified'
    )
    
    fig.show()


def plot_interactive_cumulative_pnl(
    trades_df: pd.DataFrame,
    title: str = "Interactive Cumulative PnL"
) -> None:
    """
    Create an interactive plot of cumulative PnL using Plotly.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame containing trade results.
    title (str): Title for the plot.
    """
    if 'Cumulative_PnL' not in trades_df.columns:
        raise ValueError("DataFrame must contain 'Cumulative_PnL' column")
    
    fig = go.Figure()
    
    # Add cumulative PnL line
    fig.add_trace(go.Scatter(
        x=trades_df.index,
        y=trades_df['Cumulative_PnL'],
        mode='lines',  # Solo linea continua
        name='Cumulative PnL',
        line=dict(color='blue', width=2)
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title=title,
        xaxis_title='Trade Number',
        yaxis_title='Cumulative PnL (pips)',
        template='plotly_white',
        hovermode='x unified'
    )
    
    fig.show()


def compare_backtest_vs_real_balance(
    trades_df: pd.DataFrame,
    balance_df: pd.DataFrame,
    title: str = "Backtest vs Real Balance Comparison"
) -> None:
    """
    Compare backtest results with real trading balance using Plotly.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame with backtest results including timestamp.
    balance_df (pd.DataFrame): DataFrame with real trading balance data.
    title (str): Title for the plot.
    """
    if 'Cumulative_PnL' not in trades_df.columns:
        raise ValueError("trades_df must contain 'Cumulative_PnL' column")
    
    if '<BALANCE>' not in balance_df.columns:
        raise ValueError("balance_df must contain '<BALANCE>' column")
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add backtest PnL
    fig.add_trace(
        go.Scatter(
            x=trades_df.index if 'Exit_Time' not in trades_df.columns else trades_df['Exit_Time'],
            y=trades_df['Cumulative_PnL'],
            mode='lines+markers',
            name='Backtest PnL (pips)',
            line=dict(color='blue', width=2)
        ),
        secondary_y=False,
    )
    
    # Add real balance
    fig.add_trace(
        go.Scatter(
            x=balance_df.index,
            y=balance_df['<BALANCE>'],
            mode='lines',
            name='Real Balance',
            line=dict(color='red', width=2)
        ),
        secondary_y=True,
    )
    
    # Update axes
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Cumulative PnL (pips)", secondary_y=False)
    fig.update_yaxes(title_text="Balance", secondary_y=True)
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        hovermode='x unified'
    )
    
    fig.show()


def plot_trade_distribution(
    trades_df: pd.DataFrame,
    title: str = "Trade PnL Distribution",
    figsize: Tuple[int, int] = (10, 6),
    bins: int = 30
) -> None:
    """
    Plot histogram of trade PnL distribution.
    
    Parameters:
    trades_df (pd.DataFrame): DataFrame containing trade results with 'PnL' column.
    title (str): Title for the plot.
    figsize (Tuple[int, int]): Figure size (width, height).
    bins (int): Number of bins for the histogram.
    """
    if 'PnL' not in trades_df.columns:
        raise ValueError("DataFrame must contain 'PnL' column")
    
    plt.figure(figsize=figsize)
    
    # Create histogram
    plt.hist(trades_df['PnL'], bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
    
    # Add vertical line at zero
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Break-even')
    
    # Add statistics
    mean_pnl = trades_df['PnL'].mean()
    plt.axvline(x=mean_pnl, color='green', linestyle='--', alpha=0.7, label=f'Mean: {mean_pnl:.2f}')
    
    plt.title(title)
    plt.xlabel('PnL (pips)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.show()


def create_performance_dashboard(
    data: pd.DataFrame,
    trades_df: pd.DataFrame,
    performance_metrics: Dict[str, Any]
) -> None:
    """
    Create a comprehensive performance dashboard with multiple subplots.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing price and indicator data.
    trades_df (pd.DataFrame): DataFrame containing trade results.
    performance_metrics (Dict[str, Any]): Dictionary with performance statistics.
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Price with Bollinger Bands
    axes[0, 0].plot(data.index, data['midprice'], label='Price', color='black', linewidth=1)
    axes[0, 0].plot(data.index, data['upper_band'], label='Upper Band', color='red', linestyle='--')
    axes[0, 0].plot(data.index, data['lower_band'], label='Lower Band', color='blue', linestyle='--')
    axes[0, 0].fill_between(data.index, data['lower_band'], data['upper_band'], alpha=0.1, color='gray')
    axes[0, 0].set_title('Price with Bollinger Bands')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Cumulative PnL
    if not trades_df.empty:
        axes[0, 1].plot(trades_df.index, trades_df['Cumulative_PnL'], 
                       label='Cumulative PnL', color='blue', linewidth=2)
        axes[0, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        axes[0, 1].set_title('Cumulative PnL')
        axes[0, 1].set_ylabel('PnL (pips)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Trade Distribution
    if not trades_df.empty:
        axes[1, 0].hist(trades_df['PnL'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[1, 0].axvline(x=0, color='red', linestyle='--', alpha=0.7)
        axes[1, 0].set_title('Trade PnL Distribution')
        axes[1, 0].set_xlabel('PnL (pips)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Performance Metrics Summary
    axes[1, 1].axis('off')
    metrics_text = f"""
    PERFORMANCE SUMMARY
    
    Total Trades: {performance_metrics.get('total_trades', 0)}
    Total PnL: {performance_metrics.get('total_pnl', 0):.2f} pips
    Average Trade: {performance_metrics.get('average_trade', 0):.2f} pips
    Win Rate: {performance_metrics.get('win_rate', 0):.2f}%
    Max Drawdown: {performance_metrics.get('max_drawdown', 0):.2f} pips
    Best Trade: {performance_metrics.get('best_trade', 0):.2f} pips
    Worst Trade: {performance_metrics.get('worst_trade', 0):.2f} pips
    """
    axes[1, 1].text(0.1, 0.9, metrics_text, transform=axes[1, 1].transAxes, 
                   fontsize=12, verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.show()
