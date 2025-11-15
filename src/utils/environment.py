"""
Environment classification utilities.

This module extracts environment information from workflow names using regex pattern matching.
Environments are inferred from prefixes in workflow names (e.g., [LIVE], [TEST], [UAT]).
"""

import pandas as pd
import re

# Keywords for environment classification
ENVIRONMENT_KEYWORDS = [
    ('live', 'live'),
    ('success', 'live'),
    ('testing', 'test'),
    ('test', 'test'),
    ('uat', 'uat'),
    ('qa/uat', 'qa/uat'),
    ('qa', 'qa'),
    ('experimental', 'experimental'),
    ('archive', 'archived'),
    ('archived', 'archived'),
    ('fail', 'failed')
]


def infer_environment(workflow_name: str) -> str:
    """
    Infers the environment from a workflow name.
    
    Logic:
    1. Extracts prefix from workflow name if it's in brackets (e.g., [LIVE] workflow-name)
    2. Searches for environment keywords in the prefix or full name
    3. Returns the matching environment label, or 'unlabeled' if no match
    
    Args:
        workflow_name: The workflow name string
        
    Returns:
        Environment label (live, test, uat, etc.) or 'unlabeled'
    """
    if pd.isna(workflow_name):
        return 'unknown'
    
    text = str(workflow_name).strip()
    
    # Try to extract prefix from brackets
    match = re.match(r'^\s*\[([^\]]+)\]', text)
    candidate = match.group(1).strip().lower() if match else ''
    
    # Search in the prefix first, then in the full text
    search_space = candidate or text.lower()
    
    # Check against known keywords
    for keyword, label in ENVIRONMENT_KEYWORDS:
        if keyword in search_space:
            return label
    
    # If we found a prefix but no keyword match, return the prefix
    if candidate:
        return candidate
    
    return 'unlabeled'


def add_environment_column(df, workflow_name_col='WORKFLOW_NAME'):
    """
    Adds an ENVIRONMENT column to a dataframe based on workflow names.
    
    Args:
        df: DataFrame with workflow name column
        workflow_name_col: Name of the column containing workflow names
        
    Returns:
        DataFrame with added ENVIRONMENT column
    """
    df = df.copy()
    df['ENVIRONMENT'] = df[workflow_name_col].apply(infer_environment)
    return df

