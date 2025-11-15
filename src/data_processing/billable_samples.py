"""
Billable sample definition and processing.

This module defines what constitutes a "billable sample" and provides functions
to filter and process data according to billing logic.

Critical Assumption:
- Samples with missing QC_CHECK (NaN) are included as billable
- This assumes missing QC = no QC required = implicitly passed
- Alternative interpretation: missing QC = unknown status = not billable
- This assumption requires business validation
"""

import pandas as pd
import numpy as np


def get_checks_live_finished(df_checks, df_runs):
    """
    Gets all samples in finished LIVE runs (before QC filtering).
    
    This is an intermediate step used for:
    - Sensitivity analysis (comparing with/without missing QC)
    - Understanding run outcomes before QC filtering
    
    Args:
        df_checks: QC Checks dataframe (with ENVIRONMENT column)
        df_runs: Runs dataframe (with ENVIRONMENT column)
        
    Returns:
        DataFrame of all samples in finished LIVE runs
    """
    # Step 1: Filter to LIVE (production) environment only
    runs_live = df_runs[df_runs["ENVIRONMENT"] == "live"].copy()
    
    # Step 2: Merge QC checks with run outcomes
    checks_live = df_checks.merge(
        runs_live[["ID", "OUTCOME", "ENVIRONMENT", "START_TIME"]],
        left_on="RUN_ID",
        right_on="ID",
        how="inner",
    )
    
    # Step 3: Filter to only finished runs
    checks_live_finished = checks_live[checks_live["OUTCOME"] == "finished"].copy()
    
    return checks_live_finished


def get_billable_samples(df_checks, df_runs, df_wfs, include_missing_qc=True, return_intermediate=False):
    """
    Defines and extracts billable samples based on production billing logic.
    
    A sample is considered billable if ALL of the following are true:
    1. Sample is in a [LIVE] workflow (production environment)
    2. Sample is from a run with OUTCOME = "finished" (successfully completed)
    3. Sample has QC_CHECK = "pass" OR QC_CHECK is missing (if include_missing_qc=True)
    
    Why we filter this way:
    - Production only: Customer only processes production workloads for billing
    - Finished runs only: Only successfully completed work should be billed
    - QC handling: Passed QC indicates quality; missing QC requires assumption
    
    Args:
        df_checks: QC Checks dataframe (with ENVIRONMENT column)
        df_runs: Runs dataframe (with ENVIRONMENT column)
        df_wfs: Workflows dataframe (with ENVIRONMENT column) - not used but kept for API consistency
        include_missing_qc: If True, include samples with missing QC_CHECK
        return_intermediate: If True, also return checks_live_finished (all finished LIVE samples)
        
    Returns:
        DataFrame of billable samples with all relevant metadata
        If return_intermediate=True, returns (billable, checks_live_finished)
    """
    # Get intermediate step: all finished LIVE samples
    checks_live_finished = get_checks_live_finished(df_checks, df_runs)
    
    # Step 4: Filter to billable QC status
    if include_missing_qc:
        # Current assumption: missing QC = billable
        billable = checks_live_finished[
            (checks_live_finished["QC_CHECK"].isna()) |
            (checks_live_finished["QC_CHECK"] == "pass")
        ].copy()
    else:
        # Conservative approach: only explicit pass = billable
        billable = checks_live_finished[
            checks_live_finished["QC_CHECK"] == "pass"
        ].copy()
    
    # Add month column for time-based analysis
    billable["YEAR_MONTH"] = billable["TIMESTAMP"].dt.to_period("M")
    
    if return_intermediate:
        return billable, checks_live_finished
    return billable


def analyze_qc_sensitivity(checks_live_finished):
    """
    Performs sensitivity analysis on the impact of missing QC check assumption.
    
    What this does:
    - Compares two approaches: including vs excluding missing QC checks
    - Quantifies the billing impact of this assumption
    - Shows monthly comparison of both approaches
    
    Why this matters:
    - The assumption that missing QC = billable is critical but unvalidated
    - This analysis provides data for business stakeholders to make informed decision
    - Helps understand the financial impact of different approaches
    
    Args:
        checks_live_finished: DataFrame of all samples in finished LIVE runs
                             (must have QC_CHECK, TIMESTAMP columns)
    
    Returns:
        None (prints analysis results)
    """
    if checks_live_finished is None or checks_live_finished.empty:
        print("Run Scenario 1 cell first to create checks_live_success.")
        return
    
    # Current approach: Include missing QC as billable
    billable_current = checks_live_finished[
        (checks_live_finished["QC_CHECK"].isna()) | 
        (checks_live_finished["QC_CHECK"] == "pass")
    ]
    
    # Alternative approach: Exclude missing QC (treat as unknown)
    billable_conservative = checks_live_finished[
        checks_live_finished["QC_CHECK"] == "pass"
    ]
    
    # Statistics
    total_finished = len(checks_live_finished)
    missing_qc = checks_live_finished["QC_CHECK"].isna().sum()
    pass_qc = (checks_live_finished["QC_CHECK"] == "pass").sum()
    fail_qc = (checks_live_finished["QC_CHECK"] == "fail").sum()
    
    print(f"\nIn finished LIVE runs ({total_finished} samples):")
    print(f"  QC_CHECK = 'pass': {pass_qc} samples ({pass_qc/total_finished*100:.2f}%)")
    print(f"  QC_CHECK = 'fail': {fail_qc} samples ({fail_qc/total_finished*100:.2f}%)")
    print(f"  QC_CHECK = NaN (missing): {missing_qc} samples ({missing_qc/total_finished*100:.2f}%)")
    
    print(f"\n" + "-" * 80)
    print("BILLING IMPACT:")
    print("-" * 80)
    print(f"Current Approach (Include Missing QC):")
    print(f"  Billable samples: {len(billable_current):,}")
    print(f"  Includes: Pass QC ({pass_qc:,}) + Missing QC ({missing_qc:,})")
    
    print(f"\nAlternative Approach (Exclude Missing QC):")
    print(f"  Billable samples: {len(billable_conservative):,}")
    print(f"  Includes: Pass QC only ({pass_qc:,})")
    
    difference = len(billable_current) - len(billable_conservative)
    pct_impact = (difference / len(billable_current)) * 100 if len(billable_current) > 0 else 0
    
    print(f"\n" + "-" * 80)
    print("DIFFERENCE:")
    print("-" * 80)
    print(f"  Samples affected: {difference:,}")
    print(f"  Percentage impact: {pct_impact:.2f}% of current billable count")
    print(f"  Interpretation: {difference:,} samples have missing QC data")
    print(f"                These are currently included but could be excluded")
    
    # Monthly impact
    if len(billable_current) > 0:
        billable_current_copy = billable_current.copy()
        billable_conservative_copy = billable_conservative.copy()
        
        # Ensure TIMESTAMP is datetime
        if 'TIMESTAMP' in billable_current_copy.columns:
            billable_current_copy["YEAR_MONTH"] = pd.to_datetime(
                billable_current_copy["TIMESTAMP"]
            ).dt.to_period("M")
        if 'TIMESTAMP' in billable_conservative_copy.columns:
            billable_conservative_copy["YEAR_MONTH"] = pd.to_datetime(
                billable_conservative_copy["TIMESTAMP"]
            ).dt.to_period("M")
        
        monthly_current = billable_current_copy.groupby("YEAR_MONTH").size()
        monthly_conservative = billable_conservative_copy.groupby("YEAR_MONTH").size()
        
        print(f"\n" + "-" * 80)
        print("MONTHLY COMPARISON:")
        print("-" * 80)
        print(f"{'Month':<12} {'Include Missing':<15} {'Exclude Missing':<15} {'Difference':<12}")
        print("-" * 80)
        for month in sorted(set(list(monthly_current.index) + list(monthly_conservative.index))):
            curr = monthly_current.get(month, 0)
            cons = monthly_conservative.get(month, 0)
            diff = curr - cons
            print(f"{str(month):<12} {curr:<15,} {cons:<15,} {diff:<12,}")
        
        print(f"\nRECOMMENDATION:")
        print(f"   This assumption needs business validation.")
        print(f"   If uncertain, use conservative approach (exclude missing QC).")
        print(f"   Current analysis uses: INCLUDE missing QC as billable")

