"""
Visualization Module for Dynamic Portfolio Optimization
======================================================

This module contains functions for creating various plots and visualizations
for portfolio analysis, including equity curves, weight allocations, performance
comparisons, and sensitivity analysis.

Functions:
----------
- plot_equity_curves: Plot equity curves for multiple strategies
- plot_weight_allocation: Plot weight allocation over time
- plot_performance_comparison: Compare performance metrics across strategies
- plot_sensitivity_analysis: Visualize parameter sensitivity
- plot_linearity_analysis: Visualize linearity metrics and results
- create_comprehensive_report: Generate comprehensive visualization report

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional, Tuple
from sklearn.linear_model import LinearRegression


def plot_equity_curves(results_dict: Dict[str, Any], 
                      title: str = "Portfolio Equity Curves",
                      show_legend: bool = True) -> go.Figure:
    """
    Crea un grafico delle equity curve per confrontare diverse strategie.
    
    Parameters:
    -----------
    results_dict : Dict[str, Any]
        Dizionario con i risultati delle strategie da confrontare
        Formato: {nome_strategia: result_dict}
    title : str, default "Portfolio Equity Curves"
        Titolo del grafico
    show_legend : bool, default True
        Se mostrare la legenda
    
    Returns:
    --------
    go.Figure
        Oggetto figura Plotly
    """
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set1
    
    for i, (strategy_name, result) in enumerate(results_dict.items()):
        portfolio_data = result['portfolio_data']
        method = result.get('method', 'unknown')
        lookback = result.get('lookback', 'unknown')
        
        fig.add_trace(
            go.Scatter(
                x=portfolio_data.index,
                y=portfolio_data['value'],
                mode='lines',
                name=f"{strategy_name} ({method}, LB={lookback})",
                line=dict(color=colors[i % len(colors)], width=2),
                hovertemplate="<b>%{fullData.name}</b><br>" +
                            "Data: %{x}<br>" +
                            "Valore: %{y:.2f}<br>" +
                            "<extra></extra>"
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Data",
        yaxis_title="Valore Portfolio",
        template="plotly_white",
        hovermode='x unified',
        showlegend=show_legend,
        height=600
    )
    
    return fig


def plot_weight_allocation(weights_df: pd.DataFrame,
                         title: str = "Allocazione Pesi nel Tempo",
                         plot_type: str = "stacked_area") -> go.Figure:
    """
    Visualizza l'allocazione dei pesi nel tempo.
    
    Parameters:
    -----------
    weights_df : pd.DataFrame
        DataFrame con i pesi delle strategie nel tempo
    title : str, default "Allocazione Pesi nel Tempo"
        Titolo del grafico
    plot_type : str, default "stacked_area"
        Tipo di grafico: "stacked_area", "heatmap", "line"
    
    Returns:
    --------
    go.Figure
        Oggetto figura Plotly
    """
    if plot_type == "stacked_area":
        fig = _plot_stacked_area_weights(weights_df, title)
    elif plot_type == "heatmap":
        fig = _plot_heatmap_weights(weights_df, title)
    elif plot_type == "line":
        fig = _plot_line_weights(weights_df, title)
    else:
        raise ValueError(f"plot_type '{plot_type}' non supportato. Usa: stacked_area, heatmap, line")
    
    return fig


def _plot_stacked_area_weights(weights_df: pd.DataFrame, title: str) -> go.Figure:
    """Crea grafico ad area impilata per i pesi."""
    fig = go.Figure()
    
    # Ricampiona per leggibilità se necessario
    if len(weights_df) > 50:
        weights_df_plot = weights_df.resample('M').ffill()
    else:
        weights_df_plot = weights_df
    
    for col in weights_df_plot.columns:
        fig.add_trace(go.Scatter(
            x=weights_df_plot.index,
            y=weights_df_plot[col],
            mode='lines',
            stackgroup='one',
            name=col,
            hovertemplate="<b>%{fullData.name}</b><br>" +
                        "Data: %{x}<br>" +
                        "Peso: %{y:.1%}<br>" +
                        "<extra></extra>"
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Data di Rebalance",
        yaxis_title="Peso",
        yaxis_tickformat='.1%',
        template="plotly_white",
        height=500
    )
    
    return fig


def _plot_heatmap_weights(weights_df: pd.DataFrame, title: str) -> go.Figure:
    """Crea heatmap per i pesi."""
    fig = go.Figure(data=go.Heatmap(
        z=weights_df.T.values,
        x=weights_df.index,
        y=weights_df.columns,
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate="Data: %{x}<br>" +
                     "Strategia: %{y}<br>" +
                     "Peso: %{z:.1%}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Data di Rebalance",
        yaxis_title="Strategia",
        template="plotly_white",
        height=600
    )
    
    return fig


def _plot_line_weights(weights_df: pd.DataFrame, title: str) -> go.Figure:
    """Crea grafico a linee per i pesi."""
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set1
    
    for i, col in enumerate(weights_df.columns):
        fig.add_trace(go.Scatter(
            x=weights_df.index,
            y=weights_df[col],
            mode='lines+markers',
            name=col,
            line=dict(color=colors[i % len(colors)]),
            hovertemplate="<b>%{fullData.name}</b><br>" +
                        "Data: %{x}<br>" +
                        "Peso: %{y:.1%}<br>" +
                        "<extra></extra>"
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Data di Rebalance",
        yaxis_title="Peso",
        yaxis_tickformat='.1%',
        template="plotly_white",
        height=500
    )
    
    return fig


def plot_performance_comparison(results_df: pd.DataFrame,
                              metrics: List[str] = None,
                              plot_type: str = "bar") -> go.Figure:
    """
    Confronta le metriche di performance tra diverse configurazioni.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame con i risultati dell'ottimizzazione
    metrics : List[str], default None
        Lista delle metriche da includere nel confronto
    plot_type : str, default "bar"
        Tipo di grafico: "bar", "scatter", "box"
    
    Returns:
    --------
    go.Figure
        Oggetto figura Plotly
    """
    if metrics is None:
        metrics = ['sharpe_ratio', 'annual_return', 'max_drawdown']
    
    if plot_type == "bar":
        return _plot_bar_performance(results_df, metrics)
    elif plot_type == "scatter":
        return _plot_scatter_performance(results_df)
    elif plot_type == "box":
        return _plot_box_performance(results_df, metrics)
    else:
        raise ValueError(f"plot_type '{plot_type}' non supportato")


def _plot_bar_performance(results_df: pd.DataFrame, metrics: List[str]) -> go.Figure:
    """Crea grafico a barre per confronto performance."""
    # Prendi i migliori risultati per metodo
    best_by_method = results_df.groupby('method').first().reset_index()
    
    fig = make_subplots(
        rows=1, cols=len(metrics),
        subplot_titles=[metric.replace('_', ' ').title() for metric in metrics],
        horizontal_spacing=0.1
    )
    
    for i, metric in enumerate(metrics):
        for j, row in best_by_method.iterrows():
            fig.add_trace(
                go.Bar(
                    x=[row['method']],
                    y=[row[metric]],
                    name=row['method'],
                    showlegend=(i == 0),
                    hovertemplate=f"<b>{row['method']}</b><br>" +
                                 f"Lookback: {row['lookback']}<br>" +
                                 f"{metric}: {row[metric]:.3f}<br>" +
                                 "<extra></extra>"
                ),
                row=1, col=i+1
            )
    
    fig.update_layout(
        title="Confronto Performance per Metodo",
        template="plotly_white",
        height=500
    )
    
    return fig


def _plot_scatter_performance(results_df: pd.DataFrame) -> go.Figure:
    """Crea scatter plot Sharpe vs Return."""
    fig = go.Figure()
    
    methods = results_df['method'].unique()
    colors = px.colors.qualitative.Set1
    
    for i, method in enumerate(methods):
        method_data = results_df[results_df['method'] == method]
        
        fig.add_trace(
            go.Scatter(
                x=method_data['annual_return'] * 100,
                y=method_data['sharpe_ratio'],
                mode='markers',
                name=method.upper(),
                marker=dict(
                    color=colors[i % len(colors)],
                    size=8,
                    opacity=0.7
                ),
                text=method_data['lookback'],
                hovertemplate="<b>%{fullData.name}</b><br>" +
                            "Return: %{x:.1f}%<br>" +
                            "Sharpe: %{y:.3f}<br>" +
                            "Lookback: %{text}<br>" +
                            "<extra></extra>"
            )
        )
    
    fig.update_layout(
        title="Sharpe Ratio vs Annual Return",
        xaxis_title="Annual Return (%)",
        yaxis_title="Sharpe Ratio",
        template="plotly_white",
        height=600
    )
    
    return fig


def _plot_box_performance(results_df: pd.DataFrame, metrics: List[str]) -> go.Figure:
    """Crea box plot per distribuzione performance."""
    fig = make_subplots(
        rows=1, cols=len(metrics),
        subplot_titles=[metric.replace('_', ' ').title() for metric in metrics]
    )
    
    for i, metric in enumerate(metrics):
        for method in results_df['method'].unique():
            method_data = results_df[results_df['method'] == method]
            
            fig.add_trace(
                go.Box(
                    y=method_data[metric],
                    name=method,
                    showlegend=(i == 0)
                ),
                row=1, col=i+1
            )
    
    fig.update_layout(
        title="Distribuzione Performance per Metodo",
        template="plotly_white",
        height=500
    )
    
    return fig


def plot_sensitivity_analysis(results_df: pd.DataFrame, 
                            method: str = None) -> go.Figure:
    """
    Crea grafici di analisi di sensibilità ai parametri.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame con risultati ottimizzazione
    method : str, default None
        Metodo specifico da analizzare. Se None, analizza tutti
    
    Returns:
    --------
    go.Figure
        Figura con grafici di sensibilità
    """
    if method is not None:
        method_data = results_df[results_df['method'] == method]
        return _plot_single_method_sensitivity(method_data, method)
    else:
        return _plot_multi_method_sensitivity(results_df)


def _plot_single_method_sensitivity(method_data: pd.DataFrame, method: str) -> go.Figure:
    """Plot sensibilità per singolo metodo."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Sharpe Ratio", "Annual Return", "Volatility", "Max Drawdown"),
        vertical_spacing=0.1
    )
    
    method_data_sorted = method_data.sort_values('lookback')
    
    # Sharpe Ratio
    fig.add_trace(
        go.Scatter(
            x=method_data_sorted['lookback'],
            y=method_data_sorted['sharpe_ratio'],
            mode='lines+markers',
            name='Sharpe Ratio',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    # Annual Return
    fig.add_trace(
        go.Scatter(
            x=method_data_sorted['lookback'],
            y=method_data_sorted['annual_return'] * 100,
            mode='lines+markers',
            name='Annual Return',
            line=dict(color='green'),
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Volatility
    fig.add_trace(
        go.Scatter(
            x=method_data_sorted['lookback'],
            y=method_data_sorted['volatility'] * 100,
            mode='lines+markers',
            name='Volatility',
            line=dict(color='orange'),
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Max Drawdown
    fig.add_trace(
        go.Scatter(
            x=method_data_sorted['lookback'],
            y=method_data_sorted['max_drawdown'] * 100,
            mode='lines+markers',
            name='Max Drawdown',
            line=dict(color='red'),
            showlegend=False
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        title=f"Analisi Sensibilità - Metodo {method.upper()}",
        template="plotly_white",
        height=600
    )
    
    # Update x-axis labels
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(title_text="Lookback (giorni)", row=i, col=j)
    
    return fig


def _plot_multi_method_sensitivity(results_df: pd.DataFrame) -> go.Figure:
    """Plot sensibilità per tutti i metodi."""
    fig = go.Figure()
    
    methods = results_df['method'].unique()
    colors = px.colors.qualitative.Set1
    
    for i, method in enumerate(methods):
        method_data = results_df[results_df['method'] == method].sort_values('lookback')
        
        fig.add_trace(
            go.Scatter(
                x=method_data['lookback'],
                y=method_data['sharpe_ratio'],
                mode='lines+markers',
                name=method.upper(),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6)
            )
        )
    
    fig.update_layout(
        title="Sensibilità Sharpe Ratio vs Lookback - Tutti i Metodi",
        xaxis_title="Lookback (giorni)",
        yaxis_title="Sharpe Ratio",
        template="plotly_white",
        height=600
    )
    
    return fig


def plot_linearity_analysis(linearity_results_df: pd.DataFrame,
                          top_n: int = 5) -> Tuple[go.Figure, go.Figure]:
    """
    Crea visualizzazioni per l'analisi di linearità.
    
    Parameters:
    -----------
    linearity_results_df : pd.DataFrame
        DataFrame con risultati ottimizzazione linearità
    top_n : int, default 5
        Numero di configurazioni top da visualizzare
    
    Returns:
    --------
    Tuple[go.Figure, go.Figure]
        (figura_equity_curves, figura_metriche)
    """
    # Seleziona le top N configurazioni
    top_configs = linearity_results_df.head(top_n)
    
    # Figura 1: Equity curves più lineari con trend
    fig1 = _plot_linear_equity_curves(top_configs)
    
    # Figura 2: Metriche di linearità
    fig2 = _plot_linearity_metrics(linearity_results_df)
    
    return fig1, fig2


def _plot_linear_equity_curves(top_configs: pd.DataFrame) -> go.Figure:
    """Plot equity curves più lineari con trend."""
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=[
            f"{row.method} | LB {row.lookback} | Linear: {row.linearity_score:.3f}"
            for _, row in top_configs.iterrows()
        ],
        vertical_spacing=0.1
    )
    
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    
    for i, (_, row) in enumerate(top_configs.iterrows()):
        # Nota: Qui avremmo bisogno del rebalancer per ricalcolare
        # Per ora mostriamo un placeholder
        
        r = i // 2 + 1
        c = i % 2 + 1
        
        # Placeholder per equity curve
        fig.add_annotation(
            text=f"Equity curve per {row['method']}<br>Lookback: {row['lookback']}",
            x=0.5, y=0.5,
            xref=f"x{i+1} domain", yref=f"y{i+1} domain",
            showarrow=False,
            row=r, col=c
        )
    
    fig.update_layout(
        height=1000,
        title="TOP Configurazioni con Equity Curve più Lineari",
        template="plotly_white"
    )
    
    return fig


def _plot_linearity_metrics(linearity_results_df: pd.DataFrame) -> go.Figure:
    """Plot metriche di linearità."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Linearity Score", "R²", "Correlation", "Residual Std"),
        vertical_spacing=0.1
    )
    
    methods = linearity_results_df['method'].unique()
    colors = px.colors.qualitative.Set1
    
    for i, method in enumerate(methods):
        method_data = linearity_results_df[linearity_results_df['method'] == method].sort_values('lookback')
        color = colors[i % len(colors)]
        
        # Linearity Score
        fig.add_trace(
            go.Scatter(
                x=method_data['lookback'],
                y=method_data['linearity_score'],
                mode='lines+markers',
                name=method.upper(),
                line=dict(color=color),
                showlegend=True
            ),
            row=1, col=1
        )
        
        # R²
        fig.add_trace(
            go.Scatter(
                x=method_data['lookback'],
                y=method_data['r_squared'],
                mode='lines+markers',
                name=method.upper(),
                line=dict(color=color),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Correlation
        fig.add_trace(
            go.Scatter(
                x=method_data['lookback'],
                y=method_data['correlation'],
                mode='lines+markers',
                name=method.upper(),
                line=dict(color=color),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Residual Std (limitato per leggibilità)
        residual_std_limited = np.clip(method_data['residual_std'], 0, 1)
        fig.add_trace(
            go.Scatter(
                x=method_data['lookback'],
                y=residual_std_limited,
                mode='lines+markers',
                name=method.upper(),
                line=dict(color=color),
                showlegend=False
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        height=800,
        title="Analisi Metriche di Linearità per Metodo",
        template="plotly_white"
    )
    
    # Update x-axis labels
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(title_text="Lookback (giorni)", row=i, col=j)
    
    return fig


def create_comprehensive_report(results_dict: Dict[str, Any]) -> List[go.Figure]:
    """
    Crea un report completo con tutte le visualizzazioni principali.
    
    Parameters:
    -----------
    results_dict : Dict[str, Any]
        Dizionario contenente tutti i risultati delle analisi
    
    Returns:
    --------
    List[go.Figure]
        Lista di figure per il report completo
    """
    figures = []
    
    # 1. Equity curves comparison
    if 'equity_results' in results_dict:
        fig1 = plot_equity_curves(results_dict['equity_results'], 
                                 title="Confronto Equity Curves")
        figures.append(fig1)
    
    # 2. Performance comparison
    if 'optimization_results' in results_dict:
        fig2 = plot_performance_comparison(results_dict['optimization_results'])
        figures.append(fig2)
    
    # 3. Sensitivity analysis
    if 'optimization_results' in results_dict:
        fig3 = plot_sensitivity_analysis(results_dict['optimization_results'])
        figures.append(fig3)
    
    # 4. Weight allocation
    if 'best_weights' in results_dict:
        fig4 = plot_weight_allocation(results_dict['best_weights'])
        figures.append(fig4)
    
    # 5. Linearity analysis
    if 'linearity_results' in results_dict:
        fig5a, fig5b = plot_linearity_analysis(results_dict['linearity_results'])
        figures.extend([fig5a, fig5b])
    
    print(f"📊 Report completo generato con {len(figures)} visualizzazioni")
    
    return figures
