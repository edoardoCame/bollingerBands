# 📊 Analisi MetaTrader 5 - Notebook Universale

## 🎯 Overview

Questa cartella contiene il **notebook universale** per l'analisi automatica dei risultati di ottimizzazione MetaTrader 5.

## 📁 File Disponibili

- **`mt5_analysis_clean.ipynb`** - **NOTEBOOK UNIVERSALE PRINCIPALE** ⭐
- **`deals.ipynb`** - Analisi deals specifici
- **`README.md`** - Questa documentazione

> ✅ **Pulizia completata**: Rimossi tutti i notebook non necessari. Usa solo `mt5_analysis_clean.ipynb` per le analisi di ottimizzazione MT5.

## 🚀 Come Usare il Notebook Universale

### 1. Apri il Notebook
Apri `mt5_analysis_clean.ipynb` in VS Code o Jupyter

### 2. Configura il File XML
Modifica **SOLO** questa riga nella seconda cella:
```python
xml_file_path = '/percorso/al/tuo/file.xml'
```

### 3. Esegui Tutto
- **VS Code**: Usa "Run All" 
- **Jupyter**: Cell → Run All

### 4. Analizza i Risultati
Il notebook genererà automaticamente tutte le analisi!

## 🛡️ Caratteristiche Universali

### ✅ Compatibile con Qualsiasi File XML MT5
- **Tutte le coppie valute**: EUR/GBP, EUR/CHF, USD/JPY, ecc.
- **Tutti i timeframe**: M1, M5, H1, D1, ecc.
- **Qualsiasi EA**: Con parametri Bollinger Bands
- **Dati completi o parziali**: Si adatta automaticamente

### ✅ Protezioni Anti-Errore Complete
- Controllo esistenza file
- Verifica colonne disponibili
- Gestione valori mancanti
- Fallback per errori di parsing
- Visualizzazioni adattive

### ✅ Analisi Automatiche Incluse

1. **📈 Performance Analysis**
   - Migliore e peggiore strategia
   - Top 10 per profitto e Sharpe Ratio
   - Distribuzione profitti e risk metrics

2. **⚙️ Parameter Optimization**
   - Analisi BB Period e BB Deviation
   - Heatmap combinazioni parametri
   - Identificazione parametri ottimali

3. **🎨 Visualizations**
   - 6 grafici matplotlib standard
   - Heatmap avanzate con correlazioni
   - Dashboard interattivi (se Plotly disponibile)

4. **🏆 Recommendations**
   - Strategia ottimale automatica
   - Analisi rischio/rendimento
   - Report finale con insights

## 📊 Output Garantiti

Il notebook produce **sempre** questi risultati:

- ✅ **Statistiche complete** delle performance
- ✅ **Strategia raccomandata** con parametri ottimali  
- ✅ **Visualizzazioni** adattate ai dati disponibili
- ✅ **Analisi rischio** con drawdown e recovery factor
- ✅ **Report finale** con raccomandazioni actionable

## 🔧 Requisiti

### Obbligatori (già installati):
- pandas, numpy, matplotlib, seaborn

### Opzionali per funzionalità avanzate:
```bash
pip install plotly  # Dashboard interattivi 3D
```

## 🌟 Esempi di File Supportati

Il notebook riconosce automaticamente:

```
✅ eurgbp_ottimizzato.xml
✅ EURCHF_optimization_results.xml  
✅ usdjpy_bb_backtest.xml
✅ AnyPair_AnyName.xml
```

## ⚡ Quick Start

1. **Scarica il tuo file XML** da MetaTrader 5 (Strategy Tester → Results → Export)
2. **Apri** `mt5_analysis_clean.ipynb`
3. **Cambia** il path nella cella 2
4. **Esegui** "Run All"
5. **Goditi** l'analisi completa! 🎉

## 🆘 Troubleshooting

### Problema: "File non trovato"
**Soluzione**: Controlla che il path sia corretto e usi `/` invece di `\`

### Problema: "Colonna non trovata"  
**Soluzione**: Normale! Il notebook si adatta automaticamente

### Problema: "Errore parsing XML"
**Soluzione**: Assicurati che il file sia esportato correttamente da MT5

### Problema: Grafici non vengono mostrati
**Soluzione**: Riavvia il kernel e riesegui tutte le celle

## 📞 Support

Se incontri problemi:
1. Controlla il path del file XML
2. Verifica che il file sia un XML valido di MT5
3. Riavvia il kernel e riprova
4. Il notebook è progettato per non crashare mai!

---
**🎉 Analizza qualsiasi ottimizzazione MT5 senza limiti!**
