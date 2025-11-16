"""
Scenario 1: Deep Investigation - Why is Bone Marrow in LIVE Workflows?

This module investigates the root cause of bone marrow samples appearing in
production (LIVE) workflows when the customer claims they only process blood/saliva.

CRITICAL: All functions use get_billable_data() to ensure consistency
with billing criteria (LIVE + finished + pass QC only).
"""

import pandas as pd
import numpy as np
from .data_loader import get_billable_data


def investigate_bone_marrow_in_live(df_checks, df_runs, df_wfs):
    """
    Deep investigation into why bone marrow samples are in LIVE workflows.
    
    CRITICAL: Uses get_billable_data() to ensure consistent criteria:
    - LIVE environment only
    - OUTCOME = 'finished' only
    - QC_CHECK = 'pass' only (excluding missing QC)
    
    Then filters by sample type as required for analysis.
    
    Key questions:
    1. Which specific workflows are processing bone marrow?
    2. Are these workflows supposed to be LIVE or misclassified?
    3. When did bone marrow processing start?
    4. Are there patterns in workflow names that indicate misconfiguration?
    5. Do bone marrow samples have different characteristics?
    
    Args:
        df_checks: QC Checks dataframe
        df_runs: Runs dataframe (must have ENVIRONMENT column)
        df_wfs: Workflows dataframe
    
    Returns:
        dict with investigation results
    """
    results = {}
    
    # Get billable samples using consistent function
    billable_live = get_billable_data()
    
    # 1. Which workflows process bone marrow?
    # Filter billable_live by sample type: bone marrow
    bm_samples = billable_live[billable_live["SAMPLE_TYPE"] == "bone marrow"].copy()
    
    if bm_samples.empty:
        results['error'] = "No bone marrow samples found in LIVE workflows"
        return results
    
    # Get workflow details for bone marrow samples
    bm_workflows = bm_samples.groupby("WORKFLOW_NAME").agg(
        BONE_MARROW_COUNT=("SAMPLE_TYPE", "count"),
        FIRST_BM_DATE=("TIMESTAMP", "min"),
        LAST_BM_DATE=("TIMESTAMP", "max"),
        TOTAL_SAMPLES=("RUN_ID", "count")
    ).sort_values("BONE_MARROW_COUNT", ascending=False).reset_index()
    
    # Merge with workflow metadata
    bm_workflows = bm_workflows.merge(
        df_wfs[['WORKFLOW_NAME', 'WORKFLOW_TYPE', 'WORKFLOW_TIMESTAMP', 'ENVIRONMENT']],
        on='WORKFLOW_NAME',
        how='left'
    )
    
    # Set WORKFLOW_NAME as index for easier access
    bm_workflows = bm_workflows.set_index('WORKFLOW_NAME')
    
    results['workflows_processing_bm'] = bm_workflows
    results['total_bm_samples'] = len(bm_samples)
    results['unique_workflows_with_bm'] = len(bm_workflows)
    
    # 2. Compare workflows with bone marrow vs those without
    all_live_workflows = billable_live["WORKFLOW_NAME"].unique()
    workflows_with_bm = bm_samples["WORKFLOW_NAME"].unique()
    workflows_without_bm = [w for w in all_live_workflows if w not in workflows_with_bm]
    
    # Get sample type distribution for each workflow
    workflow_sample_types = billable_live.groupby("WORKFLOW_NAME")["SAMPLE_TYPE"].apply(
        lambda x: x.value_counts().to_dict()
    )
    
    results['workflow_sample_type_distribution'] = workflow_sample_types
    results['workflows_with_bm'] = list(workflows_with_bm)
    results['workflows_without_bm'] = workflows_without_bm
    
    # 3. Check if bone marrow workflows have different characteristics
    bm_workflow_names = bm_samples["WORKFLOW_NAME"].unique()
    non_bm_workflow_names = [w for w in all_live_workflows if w not in bm_workflow_names]
    
    # Compare workflow types
    bm_wf_types = df_wfs[df_wfs["WORKFLOW_NAME"].isin(bm_workflow_names)]["WORKFLOW_TYPE"].value_counts()
    non_bm_wf_types = df_wfs[df_wfs["WORKFLOW_NAME"].isin(non_bm_workflow_names)]["WORKFLOW_TYPE"].value_counts()
    
    results['bm_workflow_types'] = bm_wf_types
    results['non_bm_workflow_types'] = non_bm_wf_types
    
    # 4. Check when bone marrow processing started
    bm_samples["YEAR_MONTH"] = bm_samples["TIMESTAMP"].dt.to_period("M")
    bm_by_month = bm_samples.groupby("YEAR_MONTH").size()
    results['bm_timeline'] = bm_by_month
    
    # 5. Check if bone marrow samples have different QC patterns
    # Filter billable_live by sample type: blood and saliva
    # NOTE: All samples in billable_live are pass QC (by definition of get_billable_live_samples)
    # This ensures consistent comparison within the same dataset
    bm_qc = bm_samples["QC_CHECK"].value_counts()
    blood_saliva_samples = billable_live[
        billable_live["SAMPLE_TYPE"].isin(["blood", "saliva"])
    ].copy()
    blood_saliva_qc = blood_saliva_samples["QC_CHECK"].value_counts()
    
    results['bm_qc_distribution'] = bm_qc
    results['blood_saliva_qc_distribution'] = blood_saliva_qc
    
    # 6. Check workflow naming patterns
    bm_workflow_names_list = list(bm_workflow_names)
    results['bm_workflow_name_patterns'] = {
        'contains_dna': sum(1 for w in bm_workflow_names_list if 'dna' in w.lower()),
        'contains_extraction': sum(1 for w in bm_workflow_names_list if 'extraction' in w.lower()),
        'contains_pcr': sum(1 for w in bm_workflow_names_list if 'pcr' in w.lower()),
        'contains_normalisation': sum(1 for w in bm_workflow_names_list if 'normalisation' in w.lower() or 'normalization' in w.lower()),
    }
    
    return results


def analyze_workflow_configuration_anomalies(df_checks, df_runs, df_wfs):
    """
    Analyzes if workflows processing bone marrow have configuration anomalies.
    
    CRITICAL: Uses get_billable_data() to ensure consistent criteria:
    - LIVE environment only
    - OUTCOME = 'finished' only
    - QC_CHECK = 'pass' only (excluding missing QC)
    
    Then filters by sample type as required for analysis.
    
    Checks:
    - Are bone marrow workflows newer/older than blood/saliva workflows?
    - Do they have different workflow types?
    - Are there naming inconsistencies?
    
    Args:
        df_checks: QC Checks dataframe
        df_runs: Runs dataframe (must have ENVIRONMENT column)
        df_wfs: Workflows dataframe
    
    Returns:
        dict with analysis results
    """
    # Get billable samples using consistent function
    billable_live = get_billable_data(df_checks, df_runs, df_wfs)
    
    if billable_live.empty:
        return {
            'bm_workflow_count': 0,
            'bs_workflow_count': 0,
            'bm_avg_creation_date': None,
            'bs_avg_creation_date': None,
            'bm_workflow_types': {},
            'bs_workflow_types': {},
        }
    
    # Filter billable_live by sample type: bone marrow
    bm_samples = billable_live[billable_live["SAMPLE_TYPE"] == "bone marrow"].copy()
    
    # Filter billable_live by sample type: blood and saliva
    blood_saliva_samples = billable_live[
        billable_live["SAMPLE_TYPE"].isin(["blood", "saliva"])
    ].copy()
    
    bm_workflows = bm_samples["WORKFLOW_NAME"].unique()
    bs_workflows = blood_saliva_samples["WORKFLOW_NAME"].unique()
    
    # Get workflow creation dates
    bm_wf_metadata = df_wfs[df_wfs["WORKFLOW_NAME"].isin(bm_workflows)].copy()
    bs_wf_metadata = df_wfs[df_wfs["WORKFLOW_NAME"].isin(bs_workflows)].copy()
    
    results = {
        'bm_workflow_count': len(bm_workflows),
        'bs_workflow_count': len(bs_workflows),
        'bm_avg_creation_date': bm_wf_metadata["WORKFLOW_TIMESTAMP"].mean() if not bm_wf_metadata.empty else None,
        'bs_avg_creation_date': bs_wf_metadata["WORKFLOW_TIMESTAMP"].mean() if not bs_wf_metadata.empty else None,
        'bm_workflow_types': bm_wf_metadata["WORKFLOW_TYPE"].value_counts().to_dict() if not bm_wf_metadata.empty else {},
        'bs_workflow_types': bs_wf_metadata["WORKFLOW_TYPE"].value_counts().to_dict() if not bs_wf_metadata.empty else {},
    }
    
    return results

