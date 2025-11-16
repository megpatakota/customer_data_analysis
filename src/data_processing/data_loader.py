"""
Data loading and initial preparation.

This module handles:
- Loading data from Excel files
- Basic data type conversions (timestamps)
- Initial data structure validation
- Environment classification from workflow names
- Creating billable data subsets
"""

import pandas as pd
import re

# Keywords for environment classification
ENVIRONMENT_KEYWORDS = [
    ("live", "live"),
    ("success", "live"),
    ("testing", "test"),
    ("test", "test"),
    ("uat", "uat"),
    ("qa/uat", "qa/uat"),
    ("qa", "qa"),
    ("experimental", "experimental"),
    ("archive", "archived"),
    ("archived", "archived"),
    ("fail", "failed"),
]


def data_load_clean():
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
    df_checks = pd.read_excel(
        "data-analyst-technical-task-data.xlsx", sheet_name="QC Checks"
    )
    df_wfs = pd.read_excel(
        "data-analyst-technical-task-data.xlsx", sheet_name="Workflows"
    )
    df_runs = pd.read_excel("data-analyst-technical-task-data.xlsx", sheet_name="Runs")
    df_checks["TIMESTAMP"] = pd.to_datetime(df_checks["TIMESTAMP"])
    df_checks["YEAR_MONTH"] = df_checks["TIMESTAMP"].dt.to_period("M")
    df_wfs["WORKFLOW_TIMESTAMP"] = pd.to_datetime(df_wfs["WORKFLOW_TIMESTAMP"])
    df_runs["START_TIME"] = pd.to_datetime(df_runs["START_TIME"])
    df_runs["STOP_TIME"] = pd.to_datetime(df_runs["STOP_TIME"])
    df_runs.rename(
        columns={"WORKFLOW_ID": "WORKFLOW_ID_LONG", "ID": "RUN_ID"}, inplace=True
    )
    df_runs["WORKFLOW_ID"] = df_runs["WORKFLOW_ID_LONG"].str.split(" ").str[0]

    # remove rows without RUN_ID in df_runs
    df_runs = df_runs[df_runs["RUN_ID"].notna()]

    def infer_environment(workflow_name):
        text = str(workflow_name).strip()

        # Try to extract prefix from brackets
        match = re.match(r"^\s*\[([^\]]+)\]", text)
        candidate = match.group(1).strip().lower() if match else ""

        # Search in the prefix first, then in the full text
        search_space = candidate or text.lower()

        # Check against known keywords
        for keyword, label in ENVIRONMENT_KEYWORDS:
            if keyword in search_space:
                return label

        # If we found a prefix but no keyword match, return the prefix
        if candidate:
            return candidate

    df_wfs["ENVIRONMENT_wfs"] = df_wfs["WORKFLOW_NAME"].apply(infer_environment)
    df_runs["ENVIRONMENT_runs"] = df_runs["WORKFLOW_NAME"].apply(infer_environment)

    return df_checks, df_wfs, df_runs


def final_merge():
    """
    Merges the three datasets into a final dataframe.

    Args:
        df_checks: QC Checks dataframe
        df_wfs: Workflows dataframe
        df_runs: Runs dataframe
    """
    df_checks, df_wfs, df_runs = data_load_clean()
    df_merged = df_wfs.merge(
        df_runs, on="WORKFLOW_ID", how="left", suffixes=("_wfs", "_runs")
    )
    df_merged = df_merged.merge(
        df_checks, on="RUN_ID", how="left", suffixes=("", "_checks")
    )

    return df_merged


def get_billable_data():
    """
    Creates a subset of billable data from the main datasets.

    Billable samples must meet all three criteria:
    1. LIVE environment only
    2. OUTCOME = 'finished' only
    3. QC_CHECK = 'pass' only (excluding missing QC)

    Args:
        df_checks: QC Checks dataframe (optional if file_path provided)
        df_runs: Runs dataframe (optional if file_path provided)
        df_wfs: Workflows dataframe (optional if file_path provided)
        file_path: Path to Excel file (if provided, loads and prepares data)

    Returns:
        DataFrame of billable samples meeting all criteria
    """
    df_billable = final_merge()

    # Filter to LIVE environment
    df_billable = df_billable[
        (df_billable["ENVIRONMENT_runs"] == "live")
        # | (df_billable["ENVIRONMENT_wfs"] == "live")
        & (df_billable["OUTCOME"] == "finished")
        & (df_billable["QC_CHECK"] == "pass")
    ]

    return df_billable

def get_usage_data():
    """
    Creates a subset of USAGE data (Scenario 2) from the main datasets.

    Usage samples must meet two criteria:
    1. LIVE environment only
    2. OUTCOME = 'finished' only
    
    It intentionally INCLUDES all QC_CHECK statuses (pass, fail, null)
    and all SAMPLE_TYPEs, as this represents all processing activity.

    Returns:
        DataFrame of usage samples meeting the criteria
    """
    df_usage = final_merge()

    # Filter for Scenario 2: Usage
    df_usage = df_usage[
        (df_usage["ENVIRONMENT_runs"] == "live")
        & (df_usage["OUTCOME"] == "finished")
    ]

    return df_usage