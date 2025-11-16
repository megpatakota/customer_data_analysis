"""
Billable sample definition and processing.

This module defines what constitutes a "billable sample" and provides functions
to filter and process data according to billing logic.

Billing Analysis Criteria (STRICTLY ENFORCED):
1. LIVE environment only
2. OUTCOME = 'finished' only
3. QC_CHECK = 'pass' only (excluding missing QC)

These criteria must be applied consistently across ALL billing analysis and visuals.
"""

import pandas as pd
import numpy as np


def get_checks_live_finished(df_checks, df_runs, df_wfs=None):
    """
    Gets all samples in finished LIVE runs (before QC filtering).
    
    This is an intermediate step used for:
    - Sensitivity analysis (comparing with/without missing QC)
    - Understanding run outcomes before QC filtering
    
    CRITICAL: Uses ENVIRONMENT from df_wfs (authoritative source), not from df_runs.
    
    Args:
        df_checks: QC Checks dataframe (should have ENVIRONMENT from df_wfs)
        df_runs: Runs dataframe (with ENVIRONMENT column)
        df_wfs: Workflows dataframe (optional, but should be provided for consistency)
        
    Returns:
        DataFrame of all samples in finished LIVE runs
    """
    # Step 1: Ensure df_checks has ENVIRONMENT from df_wfs (authoritative source)
    df_checks_copy = df_checks.copy()
    if "ENVIRONMENT" not in df_checks_copy.columns:
        if df_wfs is None or "ENVIRONMENT" not in df_wfs.columns:
            raise ValueError("ERROR: df_checks missing ENVIRONMENT and df_wfs not provided. Run data preparation cell first.")
        # Merge ENVIRONMENT from df_wfs
        df_checks_copy = df_checks_copy.merge(
            df_wfs[['WORKFLOW_ID', 'ENVIRONMENT']],
            on='WORKFLOW_ID',
            how='left'
        )
    
    # Step 2: Filter to LIVE (production) environment only using ENVIRONMENT from df_wfs
    checks_live = df_checks_copy[df_checks_copy["ENVIRONMENT"] == "live"].copy()
    
    # Step 3: Merge with run outcomes to get OUTCOME status (don't use ENVIRONMENT from df_runs)
    if "OUTCOME" not in df_runs.columns:
        raise ValueError("ERROR: OUTCOME column missing in df_runs.")
    
    checks_live = checks_live.merge(
        df_runs[["ID", "OUTCOME", "START_TIME"]],
        left_on="RUN_ID",
        right_on="ID",
        how="inner",
    )
    
    # Step 4: Filter to only finished runs
    checks_live_finished = checks_live[checks_live["OUTCOME"] == "finished"].copy()
    
    return checks_live_finished


def analyze_qc_sensitivity():
    """
    Performs sensitivity analysis on the impact of missing QC check assumption.
    
    Uses the canonical billable dataset from get_billable_data() as the
    conservative definition (QC_CHECK = 'pass' only). Compares this against a
    looser definition that also includes missing QC checks.
    
    Prints overall and monthly differences.
    """
    from .data_loader import final_merge, get_billable_data
    
    # Conservative/baseline: strictly billable as per canonical logic
    billable_conservative = get_billable_data()
    if billable_conservative is None or billable_conservative.empty:
        print("No billable data found. Ensure data is loaded and prepared.")
        return
    
    # Build "checks_live_finished" from merged data to compute the inclusive variant
    df = final_merge()
    checks_live_finished = df[
        (
            (df["ENVIRONMENT_runs"] == "live")
            | (df["ENVIRONMENT_wfs"] == "live")
        )
        & (df["OUTCOME"] == "finished")
    ].copy()
    if checks_live_finished.empty:
        print("No finished LIVE runs found.")
        return
    
    # Current approach: Include missing QC as billable
    billable_current = checks_live_finished[
        checks_live_finished["QC_CHECK"].isna()
        | (checks_live_finished["QC_CHECK"] == "pass")
    ].copy()
    
    # Stats
    total_finished = len(checks_live_finished)
    missing_qc = checks_live_finished["QC_CHECK"].isna().sum()
    pass_qc = (checks_live_finished["QC_CHECK"] == "pass").sum()
    fail_qc = (checks_live_finished["QC_CHECK"] == "fail").sum()
    
    print(f"\nIn finished LIVE runs ({total_finished} samples):")
    print(f"  QC_CHECK = 'pass': {pass_qc} samples ({(pass_qc/total_finished*100):.2f}%)")
    print(f"  QC_CHECK = 'fail': {fail_qc} samples ({(fail_qc/total_finished*100):.2f}%)")
    print(f"  QC_CHECK = NaN (missing): {missing_qc} samples ({(missing_qc/total_finished*100):.2f}%)")
    
    print("\n" + "-" * 80)
    print("BILLING IMPACT:")
    print("-" * 80)
    print("Current Approach (Include Missing QC):")
    print(f"  Billable samples: {len(billable_current):,}")
    print(f"  Includes: Pass QC ({pass_qc:,}) + Missing QC ({missing_qc:,})")
    
    print("\nAlternative Approach (Exclude Missing QC via get_billable_data):")
    print(f"  Billable samples: {len(billable_conservative):,}")
    print("  Includes: Pass QC only")
    
    difference = len(billable_current) - len(billable_conservative)
    pct_impact = (difference / len(billable_current) * 100) if len(billable_current) > 0 else 0
    
    print("\n" + "-" * 80)
    print("DIFFERENCE:")
    print("-" * 80)
    print(f"  Samples affected: {difference:,}")
    print(f"  Percentage impact: {pct_impact:.2f}% of current billable count")
    print("  Interpretation: Samples with missing QC are included in current approach but excluded in conservative.")
    
    # Monthly impact comparison
    if len(billable_current) > 0:
        billable_current_copy = billable_current.copy()
        billable_conservative_copy = billable_conservative.copy()
        
        if "TIMESTAMP" in billable_current_copy.columns:
            billable_current_copy["YEAR_MONTH"] = pd.to_datetime(
                billable_current_copy["TIMESTAMP"]
            ).dt.to_period("M")
        if "TIMESTAMP" in billable_conservative_copy.columns:
            billable_conservative_copy["YEAR_MONTH"] = pd.to_datetime(
                billable_conservative_copy["TIMESTAMP"]
            ).dt.to_period("M")
        
        monthly_current = billable_current_copy.groupby("YEAR_MONTH").size()
        monthly_conservative = billable_conservative_copy.groupby("YEAR_MONTH").size()
        
        print("\n" + "-" * 80)
        print("MONTHLY COMPARISON:")
        print("-" * 80)
        print(f"{'Month':<12} {'Include Missing':<15} {'Exclude Missing':<15} {'Difference':<12}")
        print("-" * 80)
        for month in sorted(set(list(monthly_current.index) + list(monthly_conservative.index))):
            curr = monthly_current.get(month, 0)
            cons = monthly_conservative.get(month, 0)
            diff = curr - cons
            print(f"{str(month):<12} {curr:<15,} {cons:<15,} {diff:<12,}")

