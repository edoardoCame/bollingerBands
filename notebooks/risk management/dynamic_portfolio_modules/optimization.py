"""
Optimization Module for Dynamic Portfolio Optimization
=====================================================

This module contains functions for grid search optimization and parallel
execution of portfolio backtesting across different parameters.

Functions:
----------
- optimize_single_config: Optimize a single configuration of lookback and method
- grid_search_optimization: Perform comprehensive grid search optimization
- _get_default_parameters: Get default parameter ranges for optimization

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from joblib import Parallel, delayed
from .performance_metrics import calculate_performance_metrics


def optimize_single_config(lookback: int, method: str, rebalancer) -> Optional[Dict[str, Any]]:
    """
    Ottimizza una singola configurazione di lookback e metodo.
    
    Parameters:
    -----------
    lookback : int
        Periodo di lookback in giorni
    method : str
        Metodo di ribilanciamento
    rebalancer : DynamicPortfolioRebalancer
        Istanza del rebalancer
    
    Returns:
    --------
    Optional[Dict[str, Any]]
        Dizionario con i risultati dell'ottimizzazione o None se errore
        Contiene: lookback, method, metriche di performance, result completo
    """
    try:
        # Esegui backtest
        result = rebalancer.backtest_strategy(lookback, method)
        portfolio_data = result['portfolio_data']
        
        # Calcola metriche di performance
        total_ret, annual_ret, vol, sharpe, max_dd = calculate_performance_metrics(portfolio_data['returns'])
        
        return {
            'lookback': lookback,
            'method': method,
            'total_return': total_ret,
            'annual_return': annual_ret,
            'volatility': vol,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'final_value': result['final_value'],
            'result': result
        }
    except Exception as e:
        print(f"Errore con lookback={lookback}, method={method}: {e}")
        return None


def grid_search_optimization(rebalancer, 
                           lookback_range: Optional[List[int]] = None,
                           methods: Optional[List[str]] = None,
                           n_jobs: int = 1) -> pd.DataFrame:
    """
    Esegue grid search parallelo per trovare i migliori parametri di portfolio.
    
    Parameters:
    -----------
    rebalancer : DynamicPortfolioRebalancer
        Istanza del rebalancer configurato con i dati
    lookback_range : Optional[List[int]], default None
        Lista dei periodi di lookback da testare. Se None, usa valori di default
    methods : Optional[List[str]], default None
        Lista dei metodi da testare. Se None, usa metodi di default
    n_jobs : int, default 1
        Numero di processi paralleli (1 = sequenziale)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con i risultati di tutte le configurazioni testate,
        ordinato per Sharpe ratio decrescente
    
    Notes:
    ------
    - Se n_jobs > 1, utilizza joblib per parallelizzazione
    - Filtra automaticamente i risultati non validi
    - Include parametri di default ottimali se non specificati
    """
    # Usa parametri di default se non specificati
    if lookback_range is None:
        lookback_range = _get_default_lookback_range()
    
    if methods is None:
        methods = _get_default_methods()
    
    # Crea tutte le combinazioni di parametri
    configs = []
    for lookback in lookback_range:
        for method in methods:
            configs.append((lookback, method, rebalancer))
    
    print(f"🔍 Avvio ottimizzazione grid search...")
    print(f"   Configurazioni da testare: {len(configs)}")
    print(f"   Lookback range: {min(lookback_range)}-{max(lookback_range)} giorni")
    print(f"   Metodi: {', '.join(methods)}")
    print(f"   Parallelizzazione: {'Sì' if n_jobs > 1 else 'No'} ({n_jobs} processi)")
    
    # Esegui ottimizzazione
    if n_jobs > 1:
        print("   Esecuzione in parallelo...")
        results = Parallel(n_jobs=n_jobs, verbose=1)(
            delayed(optimize_single_config)(*config) for config in configs
        )
    else:
        print("   Esecuzione sequenziale...")
        results = []
        for i, config in enumerate(configs):
            if i % 10 == 0:
                print(f"   Progresso: {i}/{len(configs)} ({i/len(configs)*100:.1f}%)")
            result = optimize_single_config(*config)
            if result:
                results.append(result)
    
    # Filtra risultati validi
    valid_results = [r for r in results if r is not None]
    
    if not valid_results:
        print("❌ Nessun risultato valido trovato!")
        return pd.DataFrame()
    
    # Converti in DataFrame
    results_df = pd.DataFrame(valid_results)
    
    # Ordina per Sharpe ratio decrescente
    results_df = results_df.sort_values('sharpe_ratio', ascending=False)
    
    print(f"✅ Ottimizzazione completata!")
    print(f"   Configurazioni valide: {len(results_df)}")
    print(f"   Miglior Sharpe ratio: {results_df.iloc[0]['sharpe_ratio']:.3f}")
    print(f"   Migliore configurazione: {results_df.iloc[0]['method']} | Lookback {results_df.iloc[0]['lookback']}")
    
    return results_df


def _get_default_lookback_range() -> List[int]:
    """
    Restituisce il range di default per i periodi di lookback.
    
    Returns:
    --------
    List[int]
        Lista dei lookback periods da testare
    """
    return [5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 240, 300, 360, 420, 480, 540, 600]


def _get_default_methods() -> List[str]:
    """
    Restituisce la lista di default dei metodi di ribilanciamento.
    
    Returns:
    --------
    List[str]
        Lista dei metodi da testare
    """
    return ['momentum', 'sharpe_momentum', 'top_n_ranking', 'equal', 'risk_parity']


def analyze_optimization_results(results_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analizza i risultati dell'ottimizzazione e fornisce insights.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame con i risultati dell'ottimizzazione
    
    Returns:
    --------
    Dict[str, Any]
        Dizionario con analisi e insights sui risultati
    """
    if len(results_df) == 0:
        return {"error": "Nessun risultato da analizzare"}
    
    analysis = {}
    
    # Migliore configurazione assoluta
    best_config = results_df.iloc[0]
    analysis['best_overall'] = {
        'method': best_config['method'],
        'lookback': best_config['lookback'],
        'sharpe_ratio': best_config['sharpe_ratio'],
        'annual_return': best_config['annual_return'],
        'max_drawdown': best_config['max_drawdown']
    }
    
    # Migliore per ogni metodo
    best_by_method = {}
    for method in results_df['method'].unique():
        method_data = results_df[results_df['method'] == method]
        best_method = method_data.iloc[0]  # Già ordinato per Sharpe
        best_by_method[method] = {
            'lookback': best_method['lookback'],
            'sharpe_ratio': best_method['sharpe_ratio'],
            'annual_return': best_method['annual_return'],
            'max_drawdown': best_method['max_drawdown']
        }
    analysis['best_by_method'] = best_by_method
    
    # Statistiche generali
    analysis['statistics'] = {
        'total_configs': len(results_df),
        'avg_sharpe': results_df['sharpe_ratio'].mean(),
        'std_sharpe': results_df['sharpe_ratio'].std(),
        'avg_annual_return': results_df['annual_return'].mean(),
        'avg_max_drawdown': results_df['max_drawdown'].mean(),
        'methods_tested': list(results_df['method'].unique()),
        'lookback_range': [results_df['lookback'].min(), results_df['lookback'].max()]
    }
    
    # Top 5 configurazioni
    analysis['top_5'] = results_df.head(5)[['method', 'lookback', 'sharpe_ratio', 'annual_return', 'max_drawdown']].to_dict('records')
    
    # Analisi sensibilità per metodo migliore
    best_method = best_config['method']
    method_results = results_df[results_df['method'] == best_method]
    
    analysis['sensitivity'] = {
        'best_method': best_method,
        'sharpe_std': method_results['sharpe_ratio'].std(),
        'sharpe_cv': method_results['sharpe_ratio'].std() / method_results['sharpe_ratio'].mean(),
        'stable_lookback_range': _find_stable_lookback_range(method_results)
    }
    
    return analysis


def _find_stable_lookback_range(method_results: pd.DataFrame, top_percent: float = 0.3) -> List[int]:
    """
    Trova il range di lookback più stabile per un metodo.
    
    Parameters:
    -----------
    method_results : pd.DataFrame
        Risultati per un singolo metodo
    top_percent : float, default 0.3
        Percentuale top di risultati da considerare per stabilità
    
    Returns:
    --------
    List[int]
        Range di lookback stabili [min, max]
    """
    # Prendi il top 30% delle configurazioni
    n_top = int(len(method_results) * top_percent)
    top_configs = method_results.head(n_top)
    
    return [top_configs['lookback'].min(), top_configs['lookback'].max()]


def quick_comparison(rebalancer, lookback: int = 30, methods: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Esegue un confronto rapido tra metodi con un lookback fisso.
    
    Parameters:
    -----------
    rebalancer : DynamicPortfolioRebalancer
        Istanza del rebalancer
    lookback : int, default 30
        Periodo di lookback fisso da utilizzare
    methods : Optional[List[str]], default None
        Metodi da confrontare. Se None, usa tutti i metodi di default
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con confronto delle performance per metodo
    """
    if methods is None:
        methods = _get_default_methods()
    
    print(f"🚀 Confronto rapido con lookback = {lookback} giorni")
    
    comparison_results = []
    
    for method in methods:
        result = optimize_single_config(lookback, method, rebalancer)
        if result:
            comparison_results.append({
                'Method': method.replace('_', ' ').title(),
                'Sharpe Ratio': f"{result['sharpe_ratio']:.3f}",
                'Annual Return': f"{result['annual_return']:.2%}",
                'Volatility': f"{result['volatility']:.2%}",
                'Max Drawdown': f"{result['max_drawdown']:.2%}",
                'Final Value': f"{result['final_value']:.2f}"
            })
    
    comparison_df = pd.DataFrame(comparison_results)
    print("📊 Risultati confronto rapido:")
    print(comparison_df.to_string(index=False))
    
    return comparison_df
