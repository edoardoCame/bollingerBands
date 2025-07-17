# Installation and Setup Guide

Complete guide for setting up the Bollinger Bands Trading Suite on your system.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Environment Setup](#environment-setup)
- [Data Setup](#data-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

## System Requirements

### Python Version
- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **64-bit Python** for better Numba performance

### Operating System
- **Windows 10/11** (tested)
- **macOS 10.15+** (tested)
- **Linux Ubuntu 18.04+** (tested)

### Hardware Recommendations
- **RAM**: Minimum 8GB, recommended 16GB+ for large datasets
- **CPU**: Multi-core processor for parallel optimization
- **Storage**: 5GB+ free space for data and dependencies

## Installation Methods

### Method 1: pip Installation (Recommended)

```bash
# Update pip first
pip install --upgrade pip

# Install core dependencies
pip install pandas numpy matplotlib plotly numba scikit-learn tqdm

# Install optional dependencies for advanced features
pip install scipy seaborn jupyter notebook ipywidgets

# For MT5 integration (Windows only)
pip install MetaTrader5
```

### Method 2: Conda Installation

```bash
# Create new environment
conda create -n bollinger_bands python=3.9
conda activate bollinger_bands

# Install dependencies
conda install pandas numpy matplotlib plotly numba scikit-learn tqdm
conda install -c conda-forge ipywidgets jupyter

# Install additional packages with pip
pip install plotly
```

### Method 3: Requirements File

Create a `requirements.txt` file:

```txt
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
plotly>=5.0.0
numba>=0.56.0
scikit-learn>=1.0.0
tqdm>=4.60.0
scipy>=1.7.0
seaborn>=0.11.0
jupyter>=1.0.0
ipywidgets>=7.6.0
MetaTrader5>=5.0.0  # Windows only
```

Install using:
```bash
pip install -r requirements.txt
```

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/edoardoCame/bollingerBands.git
cd bollingerBands
```

### 2. Python Path Setup

Add the repository to your Python path:

**Option A: Environment Variable (Recommended)**
```bash
# Linux/macOS
export PYTHONPATH="${PYTHONPATH}:/path/to/bollingerBands"

# Windows
set PYTHONPATH=%PYTHONPATH%;C:\path\to\bollingerBands
```

**Option B: sys.path in Python**
```python
import sys
sys.path.append('/path/to/bollingerBands')
```

### 3. Jupyter Setup (Optional)

```bash
# Install Jupyter extensions
jupyter nbextension enable --py widgetsnbextension

# Start Jupyter
jupyter notebook
```

## Data Setup

### 1. Data Directory Structure

Ensure your data follows this structure:
```
DATA/
├── audjpy_1440_01.csv
├── eurusd_1440_01.csv
├── gbpusd_1440_01.csv
└── ...
```

### 2. Data Format Requirements

CSV files must have these columns:
```csv
datetime,bid,ask,volume
2023-01-01 00:00:00,1.0500,1.0502,1000
2023-01-01 00:01:00,1.0501,1.0503,1200
```

### 3. Data Conversion Tools

Use the provided tools to convert your data:

```python
# Convert from other formats
from temp_tools.convert_to_parquet import convert_csv_to_parquet

convert_csv_to_parquet('your_data.csv', 'output.parquet')
```

## Verification

### 1. Test Basic Installation

```python
# Test 1: Import modules
try:
    from modules.backtester import data_loader, indicators, backtest_engine
    print("✓ Backtester modules imported successfully")
except ImportError as e:
    print(f"✗ Backtester import failed: {e}")

try:
    from modules.dynamic_portfolio_modules import DynamicPortfolioRebalancer
    print("✓ Portfolio modules imported successfully")
except ImportError as e:
    print(f"✗ Portfolio modules import failed: {e}")
```

### 2. Test Numba Compilation

```python
# Test Numba acceleration
import numpy as np
from modules.backtester.backtest_engine import backtest_core

# Create dummy data
dummy_data = np.random.random(1000)
try:
    # This will trigger Numba compilation
    result = backtest_core(dummy_data, dummy_data, dummy_data, 
                          dummy_data, dummy_data, dummy_data)
    print("✓ Numba compilation successful")
except Exception as e:
    print(f"✗ Numba compilation failed: {e}")
```

### 3. Test Data Loading

```python
# Test data loading
try:
    from modules.dynamic_portfolio_modules import load_trading_data
    
    # Test with sample data
    strategies, combined_df, returns_df = load_trading_data('DATA/')
    print(f"✓ Data loaded successfully: {len(strategies)} strategies found")
except Exception as e:
    print(f"✗ Data loading failed: {e}")
```

### 4. Run Complete Test

```python
# Complete functionality test
def run_complete_test():
    try:
        # Import modules
        from modules.backtester import data_loader, indicators, backtest_engine
        from modules.dynamic_portfolio_modules import DynamicPortfolioRebalancer
        
        # Load data
        strategies, combined_df, returns_df = load_trading_data('DATA/')
        
        # Create portfolio
        rebalancer = DynamicPortfolioRebalancer(returns_df)
        
        # Run quick backtest
        result = rebalancer.backtest(method='equal', rebalance_frequency=7)
        
        print("✓ Complete test passed - system is ready!")
        return True
        
    except Exception as e:
        print(f"✗ Complete test failed: {e}")
        return False

run_complete_test()
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'modules'`

**Solutions**:
```bash
# Ensure you're in the correct directory
cd /path/to/bollingerBands

# Check Python path
python -c "import sys; print(sys.path)"

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. Numba Compilation Issues

**Problem**: Numba compilation fails or is very slow

**Solutions**:
```bash
# Clear Numba cache
python -c "import numba; numba.config.CACHE_DIR"
# Delete the cache directory shown

# Update Numba
pip install --upgrade numba

# For Windows, install VS Build Tools
# Download from Microsoft Visual Studio website
```

#### 3. Memory Issues

**Problem**: Out of memory errors during backtesting

**Solutions**:
```python
# Reduce data size
data_subset = data.iloc[::10]  # Use every 10th row

# Process data in chunks
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process chunk
    pass

# Use data types optimization
data = data.astype({'volume': 'float32'})  # Reduce precision
```

#### 4. Plotting Issues

**Problem**: Plots not displaying in Jupyter

**Solutions**:
```python
# Enable inline plotting
%matplotlib inline

# For Plotly
import plotly.io as pio
pio.renderers.default = 'notebook'

# Install Jupyter extensions
jupyter nbextension enable --py widgetsnbextension
```

#### 5. MetaTrader 5 Connection Issues (Windows)

**Problem**: MT5 connection fails

**Solutions**:
```python
# Check MT5 installation
import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    
# Run as administrator
# Ensure MT5 is not running
# Check firewall settings
```

### Performance Issues

#### 1. Slow Backtesting

**Symptoms**: Backtests take very long to complete

**Solutions**:
```python
# Enable parallel processing
from multiprocessing import Pool
import os

# Set number of cores
n_cores = os.cpu_count() - 1  # Leave one core free

# Use smaller datasets for testing
test_data = data.tail(1000)  # Use last 1000 rows for testing

# Optimize Numba settings
import numba
numba.config.THREADING_LAYER = 'tbb'
```

#### 2. Memory Usage

**Symptoms**: High memory consumption

**Solutions**:
```python
# Monitor memory usage
import psutil
import gc

def print_memory_usage():
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")

# Force garbage collection
gc.collect()

# Use memory-efficient data types
data = pd.read_csv('file.csv', dtype={'price': 'float32'})
```

### Environment-Specific Issues

#### Windows

```bash
# Install Visual Studio Build Tools for Numba
# Download from: https://visualstudio.microsoft.com/downloads/

# Use Anaconda for easier dependency management
conda install numba

# For long path issues
git config --system core.longpaths true
```

#### macOS

```bash
# Install Xcode command line tools
xcode-select --install

# Use Homebrew for dependencies
brew install python

# For M1 Macs, use conda-forge
conda install -c conda-forge numba
```

#### Linux

```bash
# Install build essentials
sudo apt-get update
sudo apt-get install build-essential python3-dev

# For CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

## Performance Optimization

### 1. Numba Optimization

```python
# Pre-compile functions
from modules.backtester.backtest_engine import backtest_core
import numpy as np

# Warm up Numba
dummy_data = np.ones(100)
backtest_core(dummy_data, dummy_data, dummy_data, 
              dummy_data, dummy_data, dummy_data)
```

### 2. Data Optimization

```python
# Use Parquet format for faster loading
data.to_parquet('data.parquet')
data = pd.read_parquet('data.parquet')

# Optimize data types
data = data.astype({
    'bid': 'float32',
    'ask': 'float32',
    'volume': 'int32'
})
```

### 3. Parallel Processing

```python
# Enable parallel optimization
from modules.dynamic_portfolio_modules.optimization import grid_search_optimization

results = grid_search_optimization(
    rebalancer,
    methods=['momentum', 'equal'],
    parallel=True,
    n_jobs=-1  # Use all cores
)
```

### 4. Caching

```python
# Cache expensive calculations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param1, param2):
    # Your calculation here
    return result
```

## Getting Help

### 1. Check Documentation
- Read `README.md` for overview
- Check `docs/API_REFERENCE.md` for detailed API docs
- Review notebooks in `notebooks/` for examples

### 2. Common Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(pandas|numpy|numba)"

# Check system resources
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().total/1e9:.1f}GB')"

# Test imports
python -c "from modules.backtester import backtest_engine; print('OK')"
```

### 3. Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable Numba debug
import numba
numba.config.DEBUG = True
```

This guide should help you set up and troubleshoot the Bollinger Bands Trading Suite effectively. For additional help, refer to the example notebooks and API documentation.