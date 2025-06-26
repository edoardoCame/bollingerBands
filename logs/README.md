# Logs Directory

This directory contains log files generated during the execution of trading strategy analyses, backtesting runs, and optimization processes for the Bollinger Bands project.

## Log File Types

### System Logs
- **cufile.log**: GPU operations and CUDA-related performance logs from cuDF/cuML libraries
- **execution_logs**: Trading strategy execution and backtesting run logs
- **optimization_logs**: Parameter grid search and optimization process logs

### Analysis Logs
- **backtest_results**: Detailed backtesting output with performance metrics
- **error_logs**: Exception handling and debugging information
- **performance_metrics**: Timing and resource usage statistics

## Log Usage

- **Debugging**: Identify issues during strategy execution or data processing
- **Performance Monitoring**: Track GPU utilization and processing times
- **Reproducibility**: Maintain records of parameter settings and results
- **Optimization Tracking**: Monitor progress during grid search operations

## Log Retention

- Logs are automatically generated during notebook execution
- Old logs may be archived or cleaned periodically
- Critical results are preserved for analysis reproducibility

For detailed analysis workflows and log interpretation, refer to the main project documentation and individual notebook guides.
