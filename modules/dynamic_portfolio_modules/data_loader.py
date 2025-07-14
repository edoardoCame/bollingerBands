"""
Data Loading Module for Dynamic Portfolio Optimization
=====================================================

This module handles loading, preprocessing and combining trading strategy data
from CSV files, with proper error handling and data validation.

Functions:
----------
- load_trading_data: Main function to load all trading strategy data
- _process_csv_file: Helper function to process individual CSV files
- _combine_dataframes: Helper function to combine multiple strategy DataFrames

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional


def load_trading_data(data_path: str = "/home/edocame/Desktop/bollingerBands/DATA") -> Tuple[Dict, pd.DataFrame, pd.DataFrame]:
    """
    Carica tutti i file CSV di trading dalla cartella specificata e li combina
    in un dataset coerente per l'analisi di portfolio.
    
    Parameters:
    -----------
    data_path : str, default "/workspaces/bollingerBands/DATA"
        Percorso della cartella contenente i file CSV delle strategie
    
    Returns:
    --------
    Tuple[Dict, pd.DataFrame, pd.DataFrame]
        - strategies: Dizionario con i dati individuali di ogni strategia
        - combined_df: DataFrame combinato con i bilanci di tutte le strategie
        - returns_df: DataFrame con i rendimenti giornalieri di tutte le strategie
        
    Notes:
    ------
    - I file devono essere in formato CSV con encoding UTF-16
    - La prima colonna deve contenere le date, la seconda i bilanci
    - I dati vengono resampleati a frequenza giornaliera
    - Gli outlier nei rendimenti (>50% o <-50%) vengono sostituiti con 0
    """
    # Trova tutti i file CSV nella cartella
    files = [f for f in os.listdir(data_path) if f.lower().endswith('.csv')]
    if not files:
        print(f"Nessun file CSV trovato in {data_path}")
        return {}, pd.DataFrame(), pd.DataFrame()
    
    # Dizionari per tenere traccia dei dati separati
    dfs = {}
    strategy_names = []
    
    print(f"Trovati {len(files)} file CSV da processare...")
    
    for file in files:
        try:
            processed_df, strategy_name = _process_csv_file(os.path.join(data_path, file), file)
            if processed_df is not None:
                dfs[strategy_name] = processed_df
                strategy_names.append(strategy_name)
                print(f"✓ Caricato {file}: {len(processed_df)} righe -> Strategia: {strategy_name}")
        except Exception as e:
            print(f"✗ Errore caricando {file}: {e}")
    
    if not dfs:
        print("Nessun file valido caricato!")
        return {}, pd.DataFrame(), pd.DataFrame()
    
    # Combina tutti i dataframe
    combined_df = _combine_dataframes(dfs)
    
    # Calcola i rendimenti
    returns_df = combined_df.pct_change().fillna(0)
    
    # Filtra rendimenti outlier
    returns_df = _filter_outlier_returns(returns_df)
    
    # Crea dizionario finale delle strategie
    strategies = _create_strategy_dict(combined_df, returns_df, strategy_names)
    
    print(f"\n✅ Caricamento completato!")
    print(f"   DataFrame combinato: {combined_df.shape[0]} righe, {combined_df.shape[1]} colonne")
    print(f"   Periodo: da {combined_df.index.min()} a {combined_df.index.max()}")
    print(f"   Indice unico: {returns_df.index.is_unique}")
    
    return strategies, combined_df, returns_df


def _process_csv_file(file_path: str, filename: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Processa un singolo file CSV e restituisce il DataFrame processato e il nome della strategia.
    
    Parameters:
    -----------
    file_path : str
        Percorso completo del file CSV
    filename : str
        Nome del file (usato per generare il nome della strategia)
    
    Returns:
    --------
    Tuple[Optional[pd.DataFrame], Optional[str]]
        DataFrame processato e nome della strategia, o (None, None) se errore
    """
    try:
        # Leggi file con encoding UTF-16
        with open(file_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()
        
        # Estrai dati dal file
        dates = []
        balances = []
        
        for line in lines[1:]:  # Salta l'header
            parts = line.strip().split('\t')
            if len(parts) >= 2:  # Verifica che ci siano almeno 2 parti
                date_str = parts[0].strip()
                try:
                    balance = float(parts[1].strip())
                    dates.append(date_str)
                    balances.append(balance)
                except ValueError:
                    continue
        
        if not dates:
            return None, None
        
        # Crea DataFrame e assicurati che l'indice sia unico
        df = pd.DataFrame({
            'BALANCE': balances
        }, index=pd.to_datetime(dates))
        
        # Ordina l'indice e gestisci i duplicati (prendi l'ultimo valore per ogni data)
        df = df.sort_index()
        df = df[~df.index.duplicated(keep='last')]
        
        # Usa il nome completo del file (senza estensione) come strategia
        # Esempio: eurgbp_7200_02.csv -> EURGBP_7200_02
        strategy_name = filename.replace('.csv', '').upper()
        
        return df, strategy_name
        
    except Exception as e:
        print(f"Errore nel processare {filename}: {e}")
        return None, None


def _combine_dataframes(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Combina tutti i DataFrame delle strategie in un singolo DataFrame.
    
    Parameters:
    -----------
    dfs : Dict[str, pd.DataFrame]
        Dizionario con i DataFrame delle singole strategie
    
    Returns:
    --------
    pd.DataFrame
        DataFrame combinato con tutte le strategie
    """
    # Combinare tutti i dataframe con un outer join
    combined_df = None
    for name, df in dfs.items():
        if combined_df is None:
            combined_df = df.rename(columns={'BALANCE': name})
        else:
            combined_df = combined_df.join(df.rename(columns={'BALANCE': name}), how='outer')
    
    # Forward fill per i valori mancanti
    combined_df = combined_df.fillna(method='ffill')
    
    # Inizializza solo la prima riga con 10k per strategie senza dati iniziali
    if combined_df.iloc[0].isna().any():
        combined_df.iloc[0] = combined_df.iloc[0].fillna(10000)
        # Ripropaga in avanti dopo aver inizializzato la prima riga
        combined_df = combined_df.fillna(method='ffill')
    
    # Resample a frequenza giornaliera per evitare buchi e assicurare dati regolari
    combined_df = combined_df.resample('D').last().fillna(method='ffill')
    
    return combined_df


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


def _create_strategy_dict(combined_df: pd.DataFrame, returns_df: pd.DataFrame, 
                         strategy_names: list) -> Dict[str, pd.DataFrame]:
    """
    Crea il dizionario finale delle strategie con bilanci e rendimenti.
    
    Parameters:
    -----------
    combined_df : pd.DataFrame
        DataFrame combinato con i bilanci
    returns_df : pd.DataFrame
        DataFrame con i rendimenti
    strategy_names : list
        Lista dei nomi delle strategie
    
    Returns:
    --------
    Dict[str, pd.DataFrame]
        Dizionario con i dati completi di ogni strategia
    """
    strategies = {}
    for name in strategy_names:
        strategies[name] = pd.DataFrame({
            'BALANCE': combined_df[name],
            'returns': returns_df[name]
        })
    
    return strategies
