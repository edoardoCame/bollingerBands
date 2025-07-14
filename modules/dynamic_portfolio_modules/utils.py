"""
Utility Functions for Dynamic Portfolio Optimization
===================================================

This module contains utility functions for normalizing scores and calculating
various types of portfolio weights using numba-compiled functions for performance.

Functions:
----------
- normalize_scores: Normalizes returns between 0 and 1
- calculate_momentum_weights: Calculates momentum-based weights
- calculate_sharpe_momentum_weights: Calculates Sharpe-adjusted momentum weights
- calculate_top_n_ranking_weights: Calculates top-N ranking weights

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import numpy as np
from numba import jit


@jit(nopython=True)
def normalize_scores(returns, method='minmax'):
    """
    Normalizza i rendimenti tra 0 e 1 usando il metodo min-max.
    
    Parameters:
    -----------
    returns : np.ndarray
        Array dei rendimenti da normalizzare
    method : str, default 'minmax'
        Metodo di normalizzazione (attualmente solo 'minmax' supportato)
    
    Returns:
    --------
    np.ndarray
        Array dei rendimenti normalizzati tra 0 e 1
        
    Notes:
    ------
    Se tutti i valori sono uguali, restituisce pesi uguali.
    Compilata con numba per performance ottimali.
    """
    if len(returns) == 0:
        return returns
    min_val = np.min(returns)
    max_val = np.max(returns)
    if max_val == min_val:
        return np.ones_like(returns) / len(returns)
    return (returns - min_val) / (max_val - min_val)


@jit(nopython=True)
def calculate_momentum_weights(returns_matrix, lookback):
    """
    Calcola i pesi basati su momentum normalizzato.
    Esclude completamente le strategie in perdita (rendimento negativo).
    Se tutte sono in perdita, restituisce un array di zeri (non investire).
    
    Parameters:
    -----------
    returns_matrix : np.ndarray
        Matrice dei rendimenti [giorni, strategie]
        IMPORTANTE: deve contenere SOLO i rendimenti del periodo lookback rilevante!
    lookback : int
        Periodo di lookback in giorni (usato per controllo validità)
    
    Returns:
    --------
    np.ndarray
        Array dei pesi per ogni strategia, normalizzati tra 0 e 1
        
    Notes:
    ------
    - Esclude strategie con rendimento cumulativo <= 0
    - Se tutte le strategie sono in perdita, non investe in nessuna
    - I pesi sono normalizzati per sommare a 1
    """
    n_assets = returns_matrix.shape[1]
    weights = np.zeros(n_assets)
    
    if len(returns_matrix) < lookback:
        return np.ones(n_assets) / n_assets
    
    # Usa TUTTI i rendimenti passati (sono già il periodo lookback corretto)
    recent_returns = returns_matrix
    cum_returns = np.zeros(n_assets)
    
    for i in range(n_assets):
        cum_returns[i] = np.prod(1 + recent_returns[:, i]) - 1
    
    # Esclude strategie in perdita (rendimento cumulativo <= 0)
    positive_returns_mask = cum_returns > 0
    
    # Se tutte le strategie sono in perdita, non investire in nessuna
    if not np.any(positive_returns_mask):
        return np.zeros(n_assets)
    
    # Considera solo strategie in profitto
    filtered_returns = np.where(positive_returns_mask, cum_returns, 0)
    
    # Normalizza tra 0 e 1
    weights = normalize_scores(filtered_returns)
    
    # Assicura che non ci siano pesi per strategie in perdita
    weights = np.where(positive_returns_mask, weights, 0)
    
    # Assicura che la somma sia 1
    total = np.sum(weights)
    if total > 0:
        weights = weights / total
    
    return weights


@jit(nopython=True)
def calculate_sharpe_momentum_weights(returns_matrix, lookback):
    """
    Calcola i pesi basati su Sharpe-adjusted momentum.
    Usa lo Sharpe ratio per pesare le strategie invece dei semplici rendimenti.
    Esclude completamente le strategie con Sharpe negativo.
    Se tutte hanno Sharpe negativo, restituisce un array di zeri (non investire).
    
    Parameters:
    -----------
    returns_matrix : np.ndarray
        Matrice dei rendimenti [giorni, strategie]
        IMPORTANTE: deve contenere SOLO i rendimenti del periodo lookback rilevante!
    lookback : int
        Periodo di lookback in giorni (usato per controllo validità)
    
    Returns:
    --------
    np.ndarray
        Array dei pesi per ogni strategia basati su Sharpe ratio
        
    Notes:
    ------
    - Calcola Sharpe ratio annualizzato (assumendo dati giornalieri)
    - Esclude strategie con Sharpe <= 0
    - Se tutte hanno Sharpe negativo, non investe in nessuna
    """
    n_assets = returns_matrix.shape[1]
    weights = np.zeros(n_assets)
    
    if len(returns_matrix) < lookback:
        return np.ones(n_assets) / n_assets
    
    # Usa TUTTI i rendimenti passati (sono già il periodo lookback corretto)
    recent_returns = returns_matrix
    sharpe_ratios = np.zeros(n_assets)
    
    for i in range(n_assets):
        asset_returns = recent_returns[:, i]
        
        # Calcola media e std dei rendimenti
        mean_return = np.mean(asset_returns)
        std_return = np.std(asset_returns)
        
        # Calcola Sharpe ratio (assumendo risk-free rate = 0)
        if std_return > 0:
            # Annualizza il Sharpe ratio (assumendo dati giornalieri)
            sharpe_ratios[i] = (mean_return * 252) / (std_return * np.sqrt(252))
        else:
            sharpe_ratios[i] = 0.0
    
    # Esclude strategie con Sharpe negativo o zero
    positive_sharpe_mask = sharpe_ratios > 0
    
    # Se tutte le strategie hanno Sharpe negativo, non investire in nessuna
    if not np.any(positive_sharpe_mask):
        return np.zeros(n_assets)
    
    # Considera solo strategie con Sharpe positivo
    filtered_sharpe = np.where(positive_sharpe_mask, sharpe_ratios, 0)
    
    # Normalizza tra 0 e 1
    weights = normalize_scores(filtered_sharpe)
    
    # Assicura che non ci siano pesi per strategie con Sharpe negativo
    weights = np.where(positive_sharpe_mask, weights, 0)
    
    # Assicura che la somma sia 1
    total = np.sum(weights)
    if total > 0:
        weights = weights / total
    
    return weights


@jit(nopython=True)
def calculate_top_n_ranking_weights(returns_matrix, lookback, n_top=5):
    """
    Calcola i pesi per le top N strategie basate su rendimento cumulativo.
    Seleziona le migliori N strategie nel periodo lookback e le pesa ugualmente.
    
    Parameters:
    -----------
    returns_matrix : np.ndarray
        Matrice dei rendimenti [giorni, strategie]
        IMPORTANTE: deve contenere SOLO i rendimenti del periodo lookback rilevante!
    lookback : int
        Periodo di lookback in giorni (usato per controllo validità)
    n_top : int, default 5
        Numero di strategie top da selezionare
    
    Returns:
    --------
    np.ndarray
        Array dei pesi con peso uguale per le top N strategie
        
    Notes:
    ------
    - Seleziona solo strategie con rendimenti positivi
    - Assegna pesi uguali alle migliori N strategie selezionate
    - Se non ci sono abbastanza strategie positive, usa tutte quelle disponibili
    """
    n_assets = returns_matrix.shape[1]
    weights = np.zeros(n_assets)
    
    if len(returns_matrix) < lookback:
        return np.ones(n_assets) / n_assets
    
    # Usa TUTTI i rendimenti passati (sono già il periodo lookback corretto)
    recent_returns = returns_matrix
    cum_returns = np.zeros(n_assets)
    
    for i in range(n_assets):
        cum_returns[i] = np.prod(1 + recent_returns[:, i]) - 1
    
    # Esclude strategie in perdita
    positive_returns_mask = cum_returns > 0
    
    # Se non ci sono strategie positive, non investire
    if not np.any(positive_returns_mask):
        return np.zeros(n_assets)
    
    # Trova gli indici delle top N strategie con rendimenti positivi
    # Ordina gli indici per rendimento decrescente
    sorted_indices = np.argsort(cum_returns)[::-1]  # Ordine decrescente
    
    # Seleziona solo le strategie con rendimenti positivi
    top_indices = []
    for idx in sorted_indices:
        if positive_returns_mask[idx] and len(top_indices) < n_top:
            top_indices.append(idx)
    
    # Se non ci sono abbastanza strategie positive, usa tutte quelle disponibili
    if len(top_indices) == 0:
        return np.zeros(n_assets)
    
    # Assegna pesi uguali alle top N strategie
    equal_weight = 1.0 / len(top_indices)
    for idx in top_indices:
        weights[idx] = equal_weight
    
    return weights
