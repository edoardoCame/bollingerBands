"""
Performance Metrics Module for Dynamic Portfolio Optimization
============================================================

This module contains functions for calculating various performance metrics
including returns, volatility, Sharpe ratio, and maximum drawdown.

Functions:
----------
- calculate_performance_metrics: Main function to calculate all performance metrics
- calculate_total_return: Calculate total return over period
- calculate_annual_return: Calculate annualized return
- calculate_volatility: Calculate annualized volatility
- calculate_sharpe_ratio: Calculate Sharpe ratio
- calculate_max_drawdown: Calculate maximum drawdown

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import numpy as np
import pandas as pd
from typing import Tuple


def calculate_performance_metrics(returns_series: pd.Series) -> Tuple[float, float, float, float, float]:
    """
    Calcola tutte le metriche di performance principali per una serie di rendimenti.
    
    Parameters:
    -----------
    returns_series : pd.Series
        Serie temporale dei rendimenti (valori giornalieri)
    
    Returns:
    --------
    Tuple[float, float, float, float, float]
        Tupla contenente:
        - total_return: Rendimento totale del periodo
        - annual_return: Rendimento annualizzato
        - volatility: Volatilità annualizzata
        - sharpe_ratio: Sharpe ratio (assumendo risk-free rate = 0)
        - max_drawdown: Massimo drawdown del periodo
    
    Notes:
    ------
    - Assume dati giornalieri per l'annualizzazione (252 giorni di trading)
    - Risk-free rate assunto = 0 per il calcolo dello Sharpe ratio
    - Restituisce valori di default se ci sono meno di 5 osservazioni
    """
    returns = returns_series.values
    if len(returns) < 5:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    
    # Calcola tutte le metriche
    total_return = calculate_total_return(returns)
    annual_return = calculate_annual_return(returns)
    volatility = calculate_volatility(returns)
    sharpe_ratio = calculate_sharpe_ratio(annual_return, volatility)
    max_drawdown = calculate_max_drawdown(returns)
    
    return total_return, annual_return, volatility, sharpe_ratio, max_drawdown


def calculate_total_return(returns: np.ndarray) -> float:
    """
    Calcola il rendimento totale per l'intero periodo.
    
    Parameters:
    -----------
    returns : np.ndarray
        Array dei rendimenti giornalieri
    
    Returns:
    --------
    float
        Rendimento totale (es. 0.25 = 25%)
    """
    if len(returns) == 0:
        return 0.0
    return np.prod(1 + returns) - 1


def calculate_annual_return(returns: np.ndarray, trading_days_per_year: int = 252) -> float:
    """
    Calcola il rendimento annualizzato.
    
    Parameters:
    -----------
    returns : np.ndarray
        Array dei rendimenti giornalieri
    trading_days_per_year : int, default 252
        Numero di giorni di trading per anno
    
    Returns:
    --------
    float
        Rendimento annualizzato
    """
    if len(returns) == 0:
        return 0.0
    
    total_return = calculate_total_return(returns)
    n_years = len(returns) / trading_days_per_year
    
    if n_years <= 0:
        return 0.0
    
    return (1 + total_return) ** (1/n_years) - 1


def calculate_volatility(returns: np.ndarray, trading_days_per_year: int = 252) -> float:
    """
    Calcola la volatilità annualizzata.
    
    Parameters:
    -----------
    returns : np.ndarray
        Array dei rendimenti giornalieri
    trading_days_per_year : int, default 252
        Numero di giorni di trading per anno
    
    Returns:
    --------
    float
        Volatilità annualizzata
    """
    if len(returns) == 0:
        return 0.0
    
    return np.std(returns) * np.sqrt(trading_days_per_year)


def calculate_sharpe_ratio(annual_return: float, volatility: float, risk_free_rate: float = 0.0) -> float:
    """
    Calcola lo Sharpe ratio.
    
    Parameters:
    -----------
    annual_return : float
        Rendimento annualizzato
    volatility : float
        Volatilità annualizzata
    risk_free_rate : float, default 0.0
        Tasso risk-free annualizzato
    
    Returns:
    --------
    float
        Sharpe ratio
    """
    if volatility <= 0:
        return 0.0
    
    return (annual_return - risk_free_rate) / volatility


def calculate_max_drawdown(returns: np.ndarray) -> float:
    """
    Calcola il massimo drawdown per una serie di rendimenti.
    
    Parameters:
    -----------
    returns : np.ndarray
        Array dei rendimenti giornalieri
    
    Returns:
    --------
    float
        Massimo drawdown (valore negativo, es. -0.15 = -15%)
    
    Notes:
    ------
    Il drawdown è calcolato come (valore_corrente - picco_precedente) / picco_precedente
    """
    if len(returns) == 0:
        return 0.0
    
    # Calcola la serie dei valori cumulativi
    cumulative = np.cumprod(1 + returns)
    
    # Calcola i picchi raggiunti fino ad ogni punto
    peak = np.maximum.accumulate(cumulative)
    
    # Calcola il drawdown in ogni punto
    drawdown = (cumulative - peak) / peak
    
    # Restituisce il massimo drawdown (valore più negativo)
    return np.min(drawdown) if len(drawdown) > 0 else 0.0


def calculate_rolling_metrics(returns_series: pd.Series, window: int = 252) -> pd.DataFrame:
    """
    Calcola metriche di performance su base rolling.
    
    Parameters:
    -----------
    returns_series : pd.Series
        Serie temporale dei rendimenti
    window : int, default 252
        Finestra per il calcolo rolling (giorni)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con metriche rolling: sharpe, volatility, rolling_return
    """
    result_df = pd.DataFrame(index=returns_series.index)
    
    # Rolling Sharpe ratio
    rolling_mean = returns_series.rolling(window=window).mean() * 252
    rolling_std = returns_series.rolling(window=window).std() * np.sqrt(252)
    result_df['sharpe'] = rolling_mean / rolling_std
    
    # Rolling volatility
    result_df['volatility'] = rolling_std
    
    # Rolling return
    result_df['rolling_return'] = returns_series.rolling(window=window).apply(
        lambda x: np.prod(1 + x) - 1, raw=True
    )
    
    return result_df


def calculate_risk_metrics(returns_series: pd.Series, confidence_level: float = 0.05) -> dict:
    """
    Calcola metriche di rischio aggiuntive.
    
    Parameters:
    -----------
    returns_series : pd.Series
        Serie temporale dei rendimenti
    confidence_level : float, default 0.05
        Livello di confidenza per VaR e ES (5% = 95% confidence)
    
    Returns:
    --------
    dict
        Dizionario con metriche di rischio: VaR, Expected Shortfall, Skewness, Kurtosis
    """
    returns = returns_series.dropna()
    
    if len(returns) < 10:
        return {
            'VaR': 0.0,
            'Expected_Shortfall': 0.0,
            'Skewness': 0.0,
            'Kurtosis': 0.0
        }
    
    # Value at Risk (VaR)
    var = np.percentile(returns, confidence_level * 100)
    
    # Expected Shortfall (Conditional VaR)
    es = returns[returns <= var].mean()
    
    # Skewness e Kurtosis
    from scipy import stats
    skewness = stats.skew(returns)
    kurtosis = stats.kurtosis(returns, fisher=True)  # Excess kurtosis
    
    return {
        'VaR': var,
        'Expected_Shortfall': es,
        'Skewness': skewness,
        'Kurtosis': kurtosis
    }
