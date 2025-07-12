"""
Linearity Analysis Module for Dynamic Portfolio Optimization
===========================================================

This module implements a novel optimization approach that finds portfolio 
configurations with the most linear equity curves possible. Instead of optimizing 
for Sharpe ratio or returns, this method seeks the smoothest, most predictable 
growth patterns.

Functions:
----------
- calculate_linearity_metrics: Calculate linearity metrics for equity curve
- optimize_single_config_linearity: Optimize single config for linearity
- grid_search_optimization_linearity: Grid search for linearity optimization
- analyze_linearity_results: Analyze and interpret linearity results

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

from .performance_metrics import calculate_performance_metrics


def calculate_linearity_metrics(portfolio_values: pd.Series) -> Dict[str, float]:
    """
    Calcola metriche di linearità per l'equity curve di un portfolio.
    
    Parameters:
    -----------
    portfolio_values : pd.Series
        Serie temporale dei valori del portfolio
        
    Returns:
    --------
    Dict[str, float]
        Dizionario con metriche di linearità:
        - r_squared: Coefficiente di determinazione R²
        - correlation: Correlazione di Pearson con trend lineare
        - linearity_score: Score combinato di linearità
        - slope: Pendenza della regressione lineare
        - residual_std: Deviazione standard dei residui (normalizzata)
        
    Notes:
    ------
    - Il linearity_score combina R² e correlazione positiva
    - Valori più alti indicano equity curve più lineari
    - residual_std normalizzato permette confronto tra portfolio diversi
    """
    if len(portfolio_values) < 10:
        return {
            'r_squared': 0.0,
            'correlation': 0.0,
            'linearity_score': 0.0,
            'slope': 0.0,
            'residual_std': float('inf')
        }
    
    # Converti in array numpy
    values = np.array(portfolio_values)
    x = np.arange(len(values)).reshape(-1, 1)
    
    # Fit regressione lineare
    reg = LinearRegression()
    reg.fit(x, values)
    
    # Predizioni
    y_pred = reg.predict(x)
    
    # Calcola metriche
    r_squared = r2_score(values, y_pred)
    
    # Correlazione di Pearson
    correlation, _ = stats.pearsonr(np.arange(len(values)), values)
    
    # Deviazione standard dei residui (normalizzata)
    residuals = values - y_pred
    residual_std = np.std(residuals) / np.mean(values) if np.mean(values) != 0 else float('inf')
    
    # Score di linearità combinato (R² pesato per correlazione positiva)
    linearity_score = r_squared * max(0, correlation)
    
    return {
        'r_squared': r_squared,
        'correlation': correlation,
        'linearity_score': linearity_score,
        'slope': reg.coef_[0],
        'residual_std': residual_std
    }


def optimize_single_config_linearity(lookback: int, method: str, rebalancer) -> Optional[Dict[str, Any]]:
    """
    Ottimizza una configurazione basandosi sulla linearità dell'equity curve.
    
    Parameters:
    -----------
    lookback : int
        Periodo di lookback per la strategia
    method : str
        Metodo di ribilanciamento
    rebalancer : DynamicPortfolioRebalancer
        Oggetto DynamicPortfolioRebalancer
        
    Returns:
    --------
    Optional[Dict[str, Any]]
        Risultati dell'ottimizzazione con metriche di linearità o None se errore
        Contiene metriche standard + metriche di linearità
    """
    try:
        # Esegui backtest
        result = rebalancer.backtest_strategy(lookback, method)
        portfolio_data = result['portfolio_data']
        
        # Calcola metriche standard
        total_ret, annual_ret, vol, sharpe, max_dd = calculate_performance_metrics(portfolio_data['returns'])
        
        # Calcola metriche di linearità
        linearity_metrics = calculate_linearity_metrics(portfolio_data['value'])
        
        return {
            'lookback': lookback,
            'method': method,
            'total_return': total_ret,
            'annual_return': annual_ret,
            'volatility': vol,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'final_value': result['final_value'],
            'result': result,
            # Metriche di linearità
            'r_squared': linearity_metrics['r_squared'],
            'correlation': linearity_metrics['correlation'],
            'linearity_score': linearity_metrics['linearity_score'],
            'slope': linearity_metrics['slope'],
            'residual_std': linearity_metrics['residual_std']
        }
    except Exception as e:
        print(f"Errore con lookback={lookback}, method={method}: {e}")
        return None


def grid_search_optimization_linearity(rebalancer, 
                                     lookback_range: Optional[List[int]] = None,
                                     methods: Optional[List[str]] = None,
                                     n_jobs: int = 1) -> pd.DataFrame:
    """
    Grid search per trovare la configurazione con equity curve più lineare.
    
    Parameters:
    -----------
    rebalancer : DynamicPortfolioRebalancer
        Oggetto DynamicPortfolioRebalancer configurato
    lookback_range : Optional[List[int]], default None
        Lista dei periodi di lookback da testare
    methods : Optional[List[str]], default None
        Lista dei metodi da testare
    n_jobs : int, default 1
        Numero di processi paralleli
        
    Returns:
    --------
    pd.DataFrame
        Risultati ordinati per linearità decrescente
        
    Notes:
    ------
    - Utilizza le stesse configurazioni dell'ottimizzazione standard
    - Ordina i risultati per linearity_score decrescente
    - Include tutte le metriche standard + metriche di linearità
    """
    from .optimization import _get_default_lookback_range, _get_default_methods
    
    # Usa parametri di default se non specificati
    if lookback_range is None:
        lookback_range = _get_default_lookback_range()
    
    if methods is None:
        methods = _get_default_methods()
    
    # Crea tutte le combinazioni
    configs = []
    for lookback in lookback_range:
        for method in methods:
            configs.append((lookback, method, rebalancer))
    
    print(f"🎯 Avvio ottimizzazione basata su LINEARITÀ...")
    print(f"   Configurazioni da testare: {len(configs)}")
    print(f"   Obiettivo: Trovare equity curve più lineari possibili")
    print(f"   Lookback range: {min(lookback_range)}-{max(lookback_range)} giorni")
    print(f"   Metodi: {', '.join(methods)}")
    
    # Esegui ottimizzazione
    results = []
    for i, config in enumerate(configs):
        if i % 10 == 0:
            print(f"   Progresso: {i}/{len(configs)} ({i/len(configs)*100:.1f}%)")
        result = optimize_single_config_linearity(*config)
        if result:
            results.append(result)
    
    # Filtra risultati validi
    valid_results = [r for r in results if r is not None]
    
    if not valid_results:
        print("❌ Nessun risultato valido trovato!")
        return pd.DataFrame()
    
    # Converti in DataFrame
    results_df = pd.DataFrame(valid_results)
    
    # Ordina per linearità (linearity_score)
    results_df = results_df.sort_values('linearity_score', ascending=False)
    
    print(f"✅ Ottimizzazione per linearità completata!")
    print(f"   Configurazioni valide: {len(results_df)}")
    print(f"   Miglior linearity score: {results_df.iloc[0]['linearity_score']:.4f}")
    print(f"   Migliore configurazione: {results_df.iloc[0]['method']} | Lookback {results_df.iloc[0]['lookback']}")
    
    return results_df


def analyze_linearity_results(linearity_results_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analizza i risultati dell'ottimizzazione per linearità e fornisce insights.
    
    Parameters:
    -----------
    linearity_results_df : pd.DataFrame
        DataFrame con i risultati dell'ottimizzazione per linearità
    
    Returns:
    --------
    Dict[str, Any]
        Dizionario con analisi dettagliata dei risultati
    """
    if len(linearity_results_df) == 0:
        return {"error": "Nessun risultato da analizzare"}
    
    analysis = {}
    
    # Migliore configurazione per linearità
    best_linear = linearity_results_df.iloc[0]
    analysis['best_linearity'] = {
        'method': best_linear['method'],
        'lookback': best_linear['lookback'],
        'linearity_score': best_linear['linearity_score'],
        'r_squared': best_linear['r_squared'],
        'correlation': best_linear['correlation'],
        'annual_return': best_linear['annual_return'],
        'sharpe_ratio': best_linear['sharpe_ratio'],
        'max_drawdown': best_linear['max_drawdown']
    }
    
    # Migliore per ogni metodo (ordinato per linearità)
    best_by_method_linear = {}
    for method in linearity_results_df['method'].unique():
        method_data = linearity_results_df[linearity_results_df['method'] == method]
        best_method = method_data.iloc[0]  # Già ordinato per linearità
        best_by_method_linear[method] = {
            'lookback': best_method['lookback'],
            'linearity_score': best_method['linearity_score'],
            'r_squared': best_method['r_squared'],
            'correlation': best_method['correlation'],
            'sharpe_ratio': best_method['sharpe_ratio'],
            'annual_return': best_method['annual_return']
        }
    analysis['best_by_method_linearity'] = best_by_method_linear
    
    # Statistiche di linearità
    analysis['linearity_statistics'] = {
        'avg_linearity_score': linearity_results_df['linearity_score'].mean(),
        'std_linearity_score': linearity_results_df['linearity_score'].std(),
        'avg_r_squared': linearity_results_df['r_squared'].mean(),
        'avg_correlation': linearity_results_df['correlation'].mean(),
        'max_linearity_score': linearity_results_df['linearity_score'].max(),
        'max_r_squared': linearity_results_df['r_squared'].max(),
        'max_correlation': linearity_results_df['correlation'].max()
    }
    
    # Top 5 configurazioni per linearità
    analysis['top_5_linearity'] = linearity_results_df.head(5)[
        ['method', 'lookback', 'linearity_score', 'r_squared', 'correlation', 
         'annual_return', 'sharpe_ratio', 'max_drawdown']
    ].to_dict('records')
    
    # Analisi sensibilità per metodo migliore
    best_method = best_linear['method']
    method_results = linearity_results_df[linearity_results_df['method'] == best_method]
    
    linearity_mean = method_results['linearity_score'].mean()
    linearity_std = method_results['linearity_score'].std()
    cv_linearity = linearity_std / linearity_mean if linearity_mean != 0 else 0
    
    analysis['linearity_sensitivity'] = {
        'best_method': best_method,
        'linearity_mean': linearity_mean,
        'linearity_std': linearity_std,
        'linearity_cv': cv_linearity,
        'stability_assessment': _assess_linearity_stability(cv_linearity),
        'stable_lookback_range': _find_stable_linearity_range(method_results)
    }
    
    return analysis


def _assess_linearity_stability(cv_linearity: float) -> Tuple[str, str]:
    """
    Valuta la stabilità della linearità basata sul coefficiente di variazione.
    
    Parameters:
    -----------
    cv_linearity : float
        Coefficiente di variazione della linearità
    
    Returns:
    --------
    Tuple[str, str]
        (livello_stabilità, interpretazione)
    """
    if cv_linearity < 0.1:
        return "MOLTO ALTA", "Equity curve estremamente consistenti"
    elif cv_linearity < 0.2:
        return "ALTA", "Equity curve molto stabili tra parametri diversi"
    elif cv_linearity < 0.4:
        return "MEDIA", "Stabilità moderata della linearità"
    else:
        return "BASSA", "Linearità molto sensibile ai parametri"


def _find_stable_linearity_range(method_results: pd.DataFrame, top_percent: float = 0.3) -> List[int]:
    """
    Trova il range di lookback con linearità più stabile.
    
    Parameters:
    -----------
    method_results : pd.DataFrame
        Risultati per un singolo metodo
    top_percent : float, default 0.3
        Percentuale top di risultati da considerare
    
    Returns:
    --------
    List[int]
        Range di lookback stabili [min, max]
    """
    n_top = int(len(method_results) * top_percent)
    top_configs = method_results.head(n_top)
    
    return [top_configs['lookback'].min(), top_configs['lookback'].max()]


def compare_linearity_vs_sharpe(linearity_results_df: pd.DataFrame, 
                               sharpe_results_df: pd.DataFrame) -> pd.DataFrame:
    """
    Confronta i risultati dell'ottimizzazione per linearità vs Sharpe ratio.
    
    Parameters:
    -----------
    linearity_results_df : pd.DataFrame
        Risultati ottimizzazione per linearità
    sharpe_results_df : pd.DataFrame
        Risultati ottimizzazione per Sharpe ratio
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con confronto side-by-side
    """
    comparison_data = []
    
    methods = set(linearity_results_df['method'].unique()) & set(sharpe_results_df['method'].unique())
    
    for method in methods:
        # Migliore per linearità
        linear_data = linearity_results_df[linearity_results_df['method'] == method]
        best_linear = linear_data.iloc[0] if len(linear_data) > 0 else None
        
        # Migliore per Sharpe
        sharpe_data = sharpe_results_df[sharpe_results_df['method'] == method]
        best_sharpe = sharpe_data.iloc[0] if len(sharpe_data) > 0 else None
        
        if best_linear is not None and best_sharpe is not None:
            comparison_data.append({
                'Method': method.upper(),
                'Linear_Lookback': best_linear['lookback'],
                'Linear_Score': best_linear['linearity_score'],
                'Linear_R2': best_linear['r_squared'],
                'Linear_Sharpe': best_linear['sharpe_ratio'],
                'Linear_Return': best_linear['annual_return'],
                'Sharpe_Lookback': best_sharpe['lookback'],
                'Sharpe_Ratio': best_sharpe['sharpe_ratio'],
                'Sharpe_Return': best_sharpe['annual_return'],
                'Approach_Difference': 'Linearity prefers different params' if best_linear['lookback'] != best_sharpe['lookback'] else 'Same optimal params'
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\n🔍 Confronto Ottimizzazione: Linearità vs Sharpe Ratio")
    print("=" * 80)
    print("LINEARITÀ ottimizza per equity curve più lineari possibili")
    print("SHARPE RATIO ottimizza per rendimento risk-adjusted")
    print("-" * 80)
    
    return comparison_df
