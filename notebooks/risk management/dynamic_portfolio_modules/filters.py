"""
Filtering Module for Dynamic Portfolio Optimization
==================================================

This module contains filtering mechanisms to protect strategies from excessive
losses, including rolling drawdown filters and other risk management tools.

Functions:
----------
- apply_rolling_drawdown_filter: Apply rolling drawdown filter to strategy
- apply_filter_to_all_strategies: Apply filter to multiple strategies
- create_filtered_rebalancer: Create rebalancer with filtered strategies

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def apply_rolling_drawdown_filter(balance_series: pd.Series, 
                                 window_days: int = 90,
                                 stop_threshold_usd: float = -5.0,
                                 restart_multiplier: float = 0.5) -> pd.Series:
    """
    Applica il filtro drawdown rolling a una serie di bilanci.
    
    Il filtro ferma il trading quando il drawdown supera una soglia fissa
    e riprende quando le condizioni migliorano.
    
    Parameters:
    -----------
    balance_series : pd.Series
        Serie pandas con i bilanci della strategia
    window_days : int, default 90
        Giorni per la finestra rolling del drawdown
    stop_threshold_usd : float, default -5.0
        Soglia di stop in dollari assoluti (negativa)
    restart_multiplier : float, default 0.5
        Moltiplicatore per la soglia di restart (0.5 = metà della soglia stop)
    
    Returns:
    --------
    pd.Series
        Serie pandas con i bilanci filtrati
        
    Notes:
    ------
    - Il filtro calcola il drawdown in dollari assoluti su una finestra rolling
    - Quando il drawdown supera la soglia, il trading si ferma
    - Il trading riprende quando il drawdown migliora oltre la soglia di restart
    - Durante il fermo, il bilancio rimane costante
    """
    df_temp = pd.DataFrame({
        'BALANCE': balance_series,
        'DATE': balance_series.index
    })
    
    # Calcola rolling drawdown in dollari assoluti
    df_temp['rolling_max'] = df_temp['BALANCE'].rolling(window=window_days, min_periods=1).max()
    df_temp['rolling_drawdown_usd'] = df_temp['BALANCE'] - df_temp['rolling_max']
    
    # Inizializza variabili
    df_temp['active'] = True
    df_temp['adjusted_balance'] = df_temp['BALANCE'].copy()
    
    restart_threshold_usd = stop_threshold_usd * restart_multiplier
    
    # Variabili di stato
    is_active = True
    balance_when_stopped = df_temp['BALANCE'].iloc[0]
    current_active_balance = df_temp['BALANCE'].iloc[0]
    restart_next_period = False
    
    for i in range(len(df_temp)):
        current_dd_usd = df_temp['rolling_drawdown_usd'].iloc[i]
        
        # Gestisci restart dal periodo precedente
        if restart_next_period:
            is_active = True
            current_active_balance = balance_when_stopped
            restart_next_period = False
        
        if is_active:
            # Strategia attiva - aggiorna progressivamente
            if i > 0:
                balance_change = df_temp['BALANCE'].iloc[i] - df_temp['BALANCE'].iloc[i-1]
                current_active_balance += balance_change
            df_temp.loc[df_temp.index[i], 'adjusted_balance'] = current_active_balance
            
            # Verifica condizione di stop (drawdown in dollari)
            if current_dd_usd < stop_threshold_usd:
                is_active = False
                balance_when_stopped = current_active_balance
        else:
            # Strategia fermata - mantieni bilancio di stop
            df_temp.loc[df_temp.index[i], 'adjusted_balance'] = balance_when_stopped
            
            # Verifica condizione di restart - ma riprendi dal periodo successivo
            if current_dd_usd > restart_threshold_usd:
                restart_next_period = True
        
        df_temp.loc[df_temp.index[i], 'active'] = is_active
    
    return df_temp['adjusted_balance']


def apply_filter_to_all_strategies(strategies_data: Dict[str, pd.DataFrame],
                                  filter_params: Dict[str, any] = None) -> Tuple[Dict, pd.DataFrame, pd.DataFrame]:
    """
    Applica il filtro drawdown a tutte le strategie nel dataset.
    
    Parameters:
    -----------
    strategies_data : Dict[str, pd.DataFrame]
        Dizionario con i dati delle strategie originali
    filter_params : Dict[str, any], default None
        Parametri per il filtro. Se None, usa parametri di default
    
    Returns:
    --------
    Tuple[Dict, pd.DataFrame, pd.DataFrame]
        - filtered_strategies: Dizionario con strategie filtrate
        - filtered_combined_df: DataFrame combinato con bilanci filtrati
        - filtered_returns_df: DataFrame con rendimenti filtrati
    """
    # Parametri di default per il filtro
    if filter_params is None:
        filter_params = {
            'window_days': 90,
            'stop_threshold_usd': -5.0,
            'restart_multiplier': 0.5
        }
    
    print("🛡️ Applicazione filtro drawdown rolling a tutte le strategie...")
    print(f"   Parametri: Window={filter_params['window_days']}d, ")
    print(f"             Stop=${filter_params['stop_threshold_usd']}, ")
    print(f"             Restart={filter_params['restart_multiplier']}")
    
    # Dizionari per le strategie filtrate
    filtered_strategies = {}
    
    print("\n📊 Applicazione filtro per strategia:")
    print("-" * 70)
    
    for strategy_name, strategy_data in strategies_data.items():
        # Estrai la serie dei bilanci
        balance_series = strategy_data['BALANCE']
        
        # Applica il filtro
        filtered_balance = apply_rolling_drawdown_filter(
            balance_series, 
            **filter_params
        )
        
        # Calcola statistiche di confronto
        original_final = balance_series.iloc[-1]
        filtered_final = filtered_balance.iloc[-1]
        improvement = filtered_final - original_final
        improvement_pct = (improvement / original_final) * 100
        
        # Salva le strategie filtrate
        filtered_strategies[strategy_name] = pd.DataFrame({
            'BALANCE': filtered_balance,
            'returns': filtered_balance.pct_change().fillna(0)
        })
        
        # Stampa statistiche
        print(f"{strategy_name:20} | Original: ${original_final:8.2f} | "
              f"Filtered: ${filtered_final:8.2f} | Δ: {improvement:+7.2f} ({improvement_pct:+6.2f}%)")
    
    # Crea DataFrame combinati delle strategie filtrate
    filtered_combined_df = pd.DataFrame()
    filtered_returns_df = pd.DataFrame()
    
    for name, strategy_data in filtered_strategies.items():
        filtered_combined_df[name] = strategy_data['BALANCE']
        filtered_returns_df[name] = strategy_data['returns']
    
    # Filtra rendimenti outlier anche per le strategie filtrate
    filtered_returns_df = _filter_outlier_returns(filtered_returns_df)
    
    print(f"\n✅ Filtro applicato a {len(filtered_strategies)} strategie")
    print(f"📈 DataFrame filtrato: {filtered_combined_df.shape[0]} righe, {filtered_combined_df.shape[1]} colonne")
    
    return filtered_strategies, filtered_combined_df, filtered_returns_df


def create_filtered_rebalancer(strategies_data: Dict[str, pd.DataFrame],
                              filter_params: Dict[str, any] = None):
    """
    Crea un rebalancer con strategie filtrate.
    
    Parameters:
    -----------
    strategies_data : Dict[str, pd.DataFrame]
        Dizionario con i dati delle strategie originali
    filter_params : Dict[str, any], default None
        Parametri per il filtro
    
    Returns:
    --------
    DynamicPortfolioRebalancer
        Rebalancer configurato con strategie filtrate
    """
    from .portfolio_rebalancer import DynamicPortfolioRebalancer
    
    # Applica filtro a tutte le strategie
    _, _, filtered_returns_df = apply_filter_to_all_strategies(strategies_data, filter_params)
    
    # Crea e restituisci rebalancer
    filtered_rebalancer = DynamicPortfolioRebalancer(filtered_returns_df)
    print("🚀 Rebalancer con strategie filtrate creato con successo!")
    
    return filtered_rebalancer


def _filter_outlier_returns(returns_df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Filtra i rendimenti outlier sostituendoli con 0.
    
    Parameters:
    -----------
    returns_df : pd.DataFrame
        DataFrame con i rendimenti
    threshold : float, default 0.5
        Soglia per identificare outlier (±50%)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con outlier filtrati
    """
    for col in returns_df.columns:
        returns_df[col] = np.where(
            (returns_df[col] < -threshold) | (returns_df[col] > threshold),
            0,  # Sostituisci outlier con 0
            returns_df[col]
        )
    
    return returns_df


def calculate_filter_effectiveness(original_strategies: Dict[str, pd.DataFrame],
                                 filtered_strategies: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Calcola l'efficacia del filtro confrontando strategie originali e filtrate.
    
    Parameters:
    -----------
    original_strategies : Dict[str, pd.DataFrame]
        Strategie originali
    filtered_strategies : Dict[str, pd.DataFrame]
        Strategie filtrate
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con statistiche comparative di efficacia
    """
    from .performance_metrics import calculate_performance_metrics
    
    comparison_data = []
    
    for strategy_name in original_strategies.keys():
        if strategy_name in filtered_strategies:
            # Calcola metriche per strategia originale
            orig_returns = original_strategies[strategy_name]['returns']
            orig_total, orig_annual, orig_vol, orig_sharpe, orig_maxdd = calculate_performance_metrics(orig_returns)
            
            # Calcola metriche per strategia filtrata
            filt_returns = filtered_strategies[strategy_name]['returns']
            filt_total, filt_annual, filt_vol, filt_sharpe, filt_maxdd = calculate_performance_metrics(filt_returns)
            
            comparison_data.append({
                'Strategy': strategy_name,
                'Original_Sharpe': orig_sharpe,
                'Filtered_Sharpe': filt_sharpe,
                'Sharpe_Improvement': filt_sharpe - orig_sharpe,
                'Original_MaxDD': orig_maxdd,
                'Filtered_MaxDD': filt_maxdd,
                'MaxDD_Improvement': filt_maxdd - orig_maxdd,  # Improvement = less negative
                'Original_Return': orig_annual,
                'Filtered_Return': filt_annual,
                'Return_Difference': filt_annual - orig_annual
            })
    
    effectiveness_df = pd.DataFrame(comparison_data)
    
    print("\n📊 Efficacia del filtro drawdown:")
    print(f"   Strategie migrate: {len(effectiveness_df)}")
    print(f"   Miglioramento Sharpe medio: {effectiveness_df['Sharpe_Improvement'].mean():.3f}")
    print(f"   Miglioramento MaxDD medio: {effectiveness_df['MaxDD_Improvement'].mean():.3f}")
    print(f"   Strategie con Sharpe migliorato: {(effectiveness_df['Sharpe_Improvement'] > 0).sum()}")
    
    return effectiveness_df
