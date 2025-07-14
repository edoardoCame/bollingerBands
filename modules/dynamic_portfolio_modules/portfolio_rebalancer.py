"""
Portfolio Rebalancer Module for Dynamic Portfolio Optimization
==============================================================

This module contains the main DynamicPortfolioRebalancer class that implements
various portfolio rebalancing strategies with automatic Sunday rebalancing.

Classes:
--------
- DynamicPortfolioRebalancer: Main class for dynamic portfolio rebalancing

Author: Portfolio Optimization Team
Version: 1.0.0
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from .utils import (
    calculate_momentum_weights,
    calculate_sharpe_momentum_weights, 
    calculate_top_n_ranking_weights
)


class DynamicPortfolioRebalancer:
    """
    Classe principale per il ribilanciamento dinamico del portfolio.
    
    Implementa diverse strategie di allocazione dei pesi con ribilanciamento
    automatico ogni domenica (quando il mercato è chiuso).
    
    Attributes:
    -----------
    returns_df : pd.DataFrame
        DataFrame con i rendimenti di ogni strategia
    strategy_names : list
        Lista dei nomi delle strategie
    returns_matrix : np.ndarray
        Matrice numpy dei rendimenti [giorni, strategie]
    dates : pd.DatetimeIndex
        Indice delle date
    """
    
    def __init__(self, returns_df: pd.DataFrame):
        """
        Inizializza il rebalancer usando il DataFrame dei rendimenti combinato.
        
        Parameters:
        -----------
        returns_df : pd.DataFrame
            DataFrame con i rendimenti di ogni strategia
            
        Notes:
        ------
        Il ribilanciamento avviene automaticamente ogni domenica per evitare
        il trading durante le ore di mercato.
        """
        self.returns_df = returns_df
        self.strategy_names = list(returns_df.columns)
        
        # Verifica che l'indice sia unico
        if not returns_df.index.is_unique:
            print("ATTENZIONE: Indice non unico, potrebbe causare problemi!")
            self.returns_df = self.returns_df[~self.returns_df.index.duplicated(keep='last')]
        
        # Converti il DataFrame in una matrice numpy
        self.returns_matrix = self.returns_df.values  # [giorni, strategie]
        self.dates = self.returns_df.index
        
        print(f"Rebalancer inizializzato:")
        print(f"  Matrice rendimenti: {self.returns_matrix.shape}")
        print(f"  Periodo: da {self.dates.min()} a {self.dates.max()}")
        print(f"  Strategie: {len(self.strategy_names)}")
    
    def backtest_strategy(self, lookback_days: int, method: str = 'momentum') -> Dict[str, Any]:
        """
        Esegue il backtest della strategia di ribilanciamento specificata.
        
        Parameters:
        -----------
        lookback_days : int
            Periodo di lookback in giorni per il calcolo dei pesi
        method : str, default 'momentum'
            Metodo di ribilanciamento:
            - 'momentum': Pesi basati su momentum normalizzato
            - 'sharpe_momentum': Pesi basati su Sharpe-adjusted momentum
            - 'top_n_ranking': Pesi uguali per le top N strategie
            - 'equal': Pesi uguali escludendo strategie in perdita
            - 'risk_parity': Pesi basati su risk parity
        
        Returns:
        --------
        Dict[str, Any]
            Dizionario contenente:
            - 'portfolio_data': DataFrame con rendimenti e valori del portfolio
            - 'weights': DataFrame con i pesi di ribilanciamento nel tempo
            - 'final_value': Valore finale del portfolio
            - 'lookback': Periodo di lookback utilizzato
            - 'method': Metodo di ribilanciamento utilizzato
        """
        n_days = len(self.returns_matrix)
        
        # Verifica che ci siano abbastanza dati
        if n_days < lookback_days:
            print(f"AVVISO: Non ci sono abbastanza dati ({n_days} giorni) per lookback di {lookback_days}!")
            lookback_days = max(5, n_days // 10)  # Usa almeno 5 giorni di lookback
            print(f"Utilizzando lookback ridotto: {lookback_days}")
        
        weights_history = []
        rebalance_dates_idx = []
        rebalance_dates = []
        
        # Trova date di ribilanciamento ogni domenica (weekday=6)
        start_idx = lookback_days
        while start_idx < n_days:
            if self.dates[start_idx].weekday() == 6:  # 6 = domenica
                break
            start_idx += 1
        
        # Genera una sequenza di indici per il ribilanciamento ogni domenica
        for i in range(start_idx, n_days, 7):  # Ogni 7 giorni dalla prima domenica
            # Verifica che sia effettivamente una domenica (controllo aggiuntivo)
            if self.dates[i].weekday() != 6:
                # Se non è domenica, cerca la domenica più vicina nei 7 giorni successivi
                for j in range(i, min(i + 7, n_days)):
                    if self.dates[j].weekday() == 6:
                        i = j
                        break
                else:
                    continue  # Salta se non trova una domenica nei prossimi 7 giorni
            
            rebalance_dates_idx.append(i)
            rebalance_dates.append(self.dates[i])
            
            # Calcola i pesi in base al metodo scelto
            weights = self._calculate_weights(i, lookback_days, method)
            weights_history.append(weights)
        
        # Verifica che ci siano pesi calcolati
        if not weights_history:
            print("Nessun periodo di ribilanciamento trovato!")
            weights_history = [np.ones(len(self.strategy_names)) / len(self.strategy_names)]
            
            if len(rebalance_dates_idx) == 0:
                rebalance_dates_idx = [lookback_days]
                rebalance_dates = [self.dates[lookback_days]]
        
        # Calcola performance
        weights_history = np.array(weights_history)
        
        portfolio_returns, portfolio_values = self._calculate_portfolio_performance(
            self.returns_matrix, weights_history, rebalance_dates_idx
        )
        
        # Crea DataFrame con i risultati
        portfolio_data = pd.DataFrame({
            'returns': portfolio_returns,
            'value': portfolio_values[1:]  # Elimina il valore iniziale
        }, index=self.dates)
        
        # Crea DataFrame con i pesi
        weights_df = pd.DataFrame(
            weights_history, 
            columns=self.strategy_names,
            index=rebalance_dates
        )
        
        return {
            'portfolio_data': portfolio_data,
            'weights': weights_df,
            'final_value': portfolio_values[-1],
            'lookback': lookback_days,
            'method': method
        }
    
    def _calculate_weights(self, current_day: int, lookback: int, method: str) -> np.ndarray:
        """
        Calcola i pesi per il ribilanciamento in base al metodo specificato.
        
        Parameters:
        -----------
        current_day : int
            Indice del giorno corrente
        lookback : int
            Periodo di lookback in giorni
        method : str
            Metodo di calcolo dei pesi
        
        Returns:
        --------
        np.ndarray
            Array dei pesi per ogni strategia
        """
        if method == 'momentum':
            # Passa SOLO i rendimenti del periodo lookback rilevante
            relevant_returns = self.returns_matrix[max(0, current_day-lookback):current_day]
            weights = calculate_momentum_weights(relevant_returns, lookback)
        elif method == 'sharpe_momentum':
            # Passa SOLO i rendimenti del periodo lookback rilevante
            relevant_returns = self.returns_matrix[max(0, current_day-lookback):current_day]
            weights = calculate_sharpe_momentum_weights(relevant_returns, lookback)
        elif method == 'top_n_ranking':
            # Passa SOLO i rendimenti del periodo lookback rilevante
            relevant_returns = self.returns_matrix[max(0, current_day-lookback):current_day]
            weights = calculate_top_n_ranking_weights(relevant_returns, lookback)
        elif method == 'equal':
            weights = self._calculate_equal_weights_exclude_losing(current_day, lookback)
        elif method == 'risk_parity':
            weights = self._calculate_risk_parity_weights(current_day, lookback)
        else:
            # Default to equal weights
            weights = np.ones(len(self.strategy_names)) / len(self.strategy_names)
        
        return weights
    
    def _calculate_portfolio_performance(self, returns_matrix: np.ndarray, 
                                       weights_history: np.ndarray, 
                                       rebalance_dates_idx: list) -> tuple:
        """
        Calcola la performance del portfolio nel tempo.
        
        Parameters:
        -----------
        returns_matrix : np.ndarray
            Matrice dei rendimenti [giorni, strategie]
        weights_history : np.ndarray
            Storico dei pesi di ribilanciamento
        rebalance_dates_idx : list
            Indici delle date di ribilanciamento
        
        Returns:
        --------
        tuple
            (portfolio_returns, portfolio_values)
        """
        n_days = returns_matrix.shape[0]
        portfolio_value = np.ones(n_days + 1)  # Includi valore iniziale = 1.0
        portfolio_returns = np.zeros(n_days)
        
        current_weights = weights_history[0] if len(weights_history) > 0 else np.ones(returns_matrix.shape[1]) / returns_matrix.shape[1]
        rebal_idx = 0
        
        for day in range(n_days):
            # Ribilancia se necessario
            if day in rebalance_dates_idx and rebal_idx < len(weights_history):
                current_weights = weights_history[rebal_idx]
                rebal_idx += 1
            
            # Calcola rendimento giornaliero del portfolio
            daily_return = np.dot(current_weights, returns_matrix[day])
            portfolio_returns[day] = daily_return
            portfolio_value[day + 1] = portfolio_value[day] * (1 + daily_return)
        
        return portfolio_returns, portfolio_value
    
    def _calculate_equal_weights_exclude_losing(self, current_day: int, lookback: int) -> np.ndarray:
        """
        Calcola pesi equi escludendo le strategie in perdita.
        
        Parameters:
        -----------
        current_day : int
            Indice del giorno corrente
        lookback : int
            Periodo di lookback
        
        Returns:
        --------
        np.ndarray
            Array dei pesi
        """
        if current_day < lookback:
            return np.ones(len(self.strategy_names)) / len(self.strategy_names)
        
        # Calcola rendimenti cumulati nell'ultimo lookback
        recent_returns = self.returns_matrix[current_day-lookback:current_day]
        cum_returns = np.zeros(len(self.strategy_names))
        
        for i in range(len(self.strategy_names)):
            cum_returns[i] = np.prod(1 + recent_returns[:, i]) - 1
        
        # Identifica strategie in profitto (cum_return > 0)
        profitable = cum_returns > 0
        n_profitable = np.sum(profitable)
        
        # Se tutte sono in perdita, non investire in nessuna
        if n_profitable == 0:
            return np.zeros(len(self.strategy_names))
        
        # Calcola pesi uguali per le strategie redditizie
        weights = np.zeros(len(self.strategy_names))
        weights[profitable] = 1.0 / n_profitable
        
        return weights
    
    def _calculate_risk_parity_weights(self, current_day: int, lookback: int) -> np.ndarray:
        """
        Calcola pesi basati su risk parity, escludendo strategie in perdita.
        
        Parameters:
        -----------
        current_day : int
            Indice del giorno corrente
        lookback : int
            Periodo di lookback
        
        Returns:
        --------
        np.ndarray
            Array dei pesi basati su risk parity
        """
        if current_day < lookback:
            return np.ones(len(self.strategy_names)) / len(self.strategy_names)
        
        # Calcola rendimenti cumulati e volatilità nell'ultimo lookback
        recent_returns = self.returns_matrix[current_day-lookback:current_day]
        cum_returns = np.zeros(len(self.strategy_names))
        volatilities = np.std(recent_returns, axis=0)
        
        for i in range(len(self.strategy_names)):
            cum_returns[i] = np.prod(1 + recent_returns[:, i]) - 1
        
        # Identifica strategie in profitto (cum_return > 0)
        profitable = cum_returns > 0
        
        # Se tutte sono in perdita, non investire in nessuna
        if not np.any(profitable):
            return np.zeros(len(self.strategy_names))
        
        # Evita divisione per zero e considera solo strategie profittevoli
        masked_volatilities = np.where(profitable & (volatilities > 0), volatilities, np.inf)
        
        # Pesi inversamente proporzionali alla volatilità
        inv_vol = np.where(masked_volatilities < np.inf, 1.0 / masked_volatilities, 0.0)
        total_inv_vol = np.sum(inv_vol)
        
        # Normalizza i pesi
        weights = np.zeros(len(self.strategy_names))
        if total_inv_vol > 0:
            weights = inv_vol / total_inv_vol
        
        return weights
