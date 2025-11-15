"""
Data loading and initial preparation.

This module handles:
- Loading data from Excel files
- Basic data type conversions (timestamps)
- Initial data structure validation
"""

import pandas as pd


def load_data(file_path="data-analyst-technical-task-data.xlsx"):
    """
    Loads all three datasets from the Excel workbook.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        Tuple of (df_checks, df_wfs, df_runs)
    """
    df_checks = pd.read_excel(file_path, sheet_name="QC Checks")
    df_wfs = pd.read_excel(file_path, sheet_name="Workflows")
    df_runs = pd.read_excel(file_path, sheet_name="Runs")
    
    return df_checks, df_wfs, df_runs


def prepare_timestamps(df_checks, df_wfs, df_runs):
    """
    Converts timestamp columns to datetime objects for time-based analysis.
    
    Why we do this:
    - Enables time-based filtering and grouping
    - Allows calculation of time differences
    - Supports period-based aggregations (e.g., monthly)
    
    Args:
        df_checks: QC Checks dataframe
        df_wfs: Workflows dataframe
        df_runs: Runs dataframe
        
    Returns:
        DataFrames with converted timestamp columns
    """
    df_checks = df_checks.copy()
    df_wfs = df_wfs.copy()
    df_runs = df_runs.copy()
    
    df_checks['TIMESTAMP'] = pd.to_datetime(df_checks['TIMESTAMP'])
    df_wfs['WORKFLOW_TIMESTAMP'] = pd.to_datetime(df_wfs['WORKFLOW_TIMESTAMP'])
    df_runs['START_TIME'] = pd.to_datetime(df_runs['START_TIME'])
    df_runs['STOP_TIME'] = pd.to_datetime(df_runs['STOP_TIME'])
    
    return df_checks, df_wfs, df_runs

