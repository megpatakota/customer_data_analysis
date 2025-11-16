"""
Scenario 2: Real-World Customer Health Metrics.

This module calculates real-world metrics used in customer success and account management.
"""

import pandas as pd
import numpy as np


def calculate_customer_health_metrics(usage_live, df_runs, df_wfs):
    """
    Calculates comprehensive real-world customer health metrics.
    
    Metrics include:
    1. Churn Risk Indicators
    2. Engagement Metrics
    3. Growth Velocity
    4. Operational Health
    5. Usage Concentration
    6. Platform Maturity
    """
    metrics = {}
    
    # Prepare data
    usage_live_copy = usage_live.copy()
    usage_live_copy["YEAR_MONTH"] = usage_live_copy["TIMESTAMP"].dt.to_period("M")
    
    runs_live = df_runs[df_runs["ENVIRONMENT"] == "live"].copy()
    runs_live["YEAR_MONTH"] = runs_live["START_TIME"].dt.to_period("M")
    
    wfs_live = df_wfs[df_wfs["ENVIRONMENT"] == "live"].copy()
    
    # 1. CHURN RISK INDICATORS
    usage_monthly = usage_live_copy.groupby("YEAR_MONTH").agg(
        SAMPLES=("RUN_ID", "count"),
        UNIQUE_RUNS=("RUN_ID", "nunique"),
        UNIQUE_WORKFLOWS=("WORKFLOW_NAME", "nunique")
    ).sort_index()
    
    usage_monthly["MOM_CHANGE"] = usage_monthly["SAMPLES"].pct_change() * 100
    
    # Consecutive declines
    consecutive_declines = 0
    for i in range(1, len(usage_monthly)):
        if usage_monthly.iloc[i]["MOM_CHANGE"] < 0:
            consecutive_declines += 1
        else:
            break
    
    metrics['churn_risk'] = {
        'consecutive_monthly_declines': consecutive_declines,
        'latest_mom_change': usage_monthly.iloc[-1]["MOM_CHANGE"] if len(usage_monthly) > 0 else 0,
        'three_month_trend': usage_monthly["SAMPLES"].tail(3).mean() - usage_monthly["SAMPLES"].head(3).mean() if len(usage_monthly) >= 6 else None,
        'risk_level': 'HIGH' if consecutive_declines >= 2 or (usage_monthly.iloc[-1]["MOM_CHANGE"] < -20 if len(usage_monthly) > 0 else False) else 'MEDIUM' if consecutive_declines >= 1 or (usage_monthly.iloc[-1]["MOM_CHANGE"] < -10 if len(usage_monthly) > 0 else False) else 'LOW'
    }
    
    # 2. ENGAGEMENT METRICS
    active_workflows = usage_live_copy["WORKFLOW_NAME"].nunique()
    total_workflows = len(wfs_live)
    workflow_utilization = active_workflows / total_workflows * 100 if total_workflows > 0 else 0
    
    # Workflow diversity (how evenly distributed is usage)
    workflow_distribution = usage_live_copy["WORKFLOW_NAME"].value_counts()
    workflow_diversity = 1 - (workflow_distribution / workflow_distribution.sum()).pow(2).sum()  # Herfindahl index
    
    metrics['engagement'] = {
        'active_workflows': active_workflows,
        'total_workflows': total_workflows,
        'workflow_utilization_pct': workflow_utilization,
        'workflow_diversity_index': workflow_diversity,  # 0-1, higher = more diverse
        'avg_samples_per_workflow': usage_live_copy.groupby("WORKFLOW_NAME").size().mean()
    }
    
    # 3. GROWTH VELOCITY
    if len(usage_monthly) >= 2:
        recent_growth = usage_monthly["SAMPLES"].tail(2).pct_change().iloc[-1] * 100
        overall_growth = (usage_monthly["SAMPLES"].iloc[-1] / usage_monthly["SAMPLES"].iloc[0] - 1) * 100 if usage_monthly["SAMPLES"].iloc[0] > 0 else 0
        
        # Growth acceleration/deceleration
        if len(usage_monthly) >= 3:
            growth_rates = usage_monthly["SAMPLES"].pct_change().dropna()
            if len(growth_rates) >= 2:
                acceleration = growth_rates.iloc[-1] - growth_rates.iloc[-2]
            else:
                acceleration = None
        else:
            acceleration = None
    else:
        recent_growth = None
        overall_growth = None
        acceleration = None
    
    metrics['growth'] = {
        'recent_growth_pct': recent_growth,
        'overall_growth_pct': overall_growth,
        'growth_acceleration': acceleration,
        'growth_trajectory': 'ACCELERATING' if acceleration and acceleration > 0.05 else 'DECELERATING' if acceleration and acceleration < -0.05 else 'STABLE' if acceleration else 'INSUFFICIENT_DATA'
    }
    
    # 4. OPERATIONAL HEALTH
    success_monthly = runs_live.groupby("YEAR_MONTH").agg(
        # NOTE: df_runs (from data_loader) uses RUN_ID as the run identifier, not ID.
        # Align to that schema here so Scenario 2 metrics work with the same dataset setup.
        TOTAL_RUNS=("RUN_ID", "count"),
        FINISHED=("OUTCOME", lambda x: (x == "finished").sum()),
        FAILED=("OUTCOME", lambda x: (x == "failed").sum()),
        CANCELED=("OUTCOME", lambda x: (x == "canceled").sum())
    )
    success_monthly["SUCCESS_RATE"] = (success_monthly["FINISHED"] / success_monthly["TOTAL_RUNS"] * 100)
    
    latest_success_rate = success_monthly["SUCCESS_RATE"].iloc[-1] if len(success_monthly) > 0 else None
    avg_success_rate = success_monthly["SUCCESS_RATE"].mean()
    
    # Success rate trend
    if len(success_monthly) >= 2:
        success_rate_trend = success_monthly["SUCCESS_RATE"].iloc[-1] - success_monthly["SUCCESS_RATE"].iloc[-2]
    else:
        success_rate_trend = None
    
    metrics['operational_health'] = {
        'latest_success_rate': latest_success_rate,
        'avg_success_rate': avg_success_rate,
        'success_rate_trend': success_rate_trend,
        'total_failed_runs': success_monthly["FAILED"].sum() if len(success_monthly) > 0 else 0,
        'total_canceled_runs': success_monthly["CANCELED"].sum() if len(success_monthly) > 0 else 0,
        'operational_status': 'HEALTHY' if latest_success_rate and latest_success_rate >= 90 else 'WARNING' if latest_success_rate and latest_success_rate >= 80 else 'CRITICAL' if latest_success_rate else 'UNKNOWN'
    }
    
    # 5. USAGE CONCENTRATION
    # How dependent is customer on top workflows?
    top_3_workflows_pct = (workflow_distribution.head(3).sum() / workflow_distribution.sum() * 100) if len(workflow_distribution) > 0 else 0
    top_workflow_pct = (workflow_distribution.iloc[0] / workflow_distribution.sum() * 100) if len(workflow_distribution) > 0 else 0
    
    metrics['concentration'] = {
        'top_3_workflows_pct': top_3_workflows_pct,
        'top_workflow_pct': top_workflow_pct,
        'concentration_risk': 'HIGH' if top_workflow_pct > 50 else 'MEDIUM' if top_workflow_pct > 30 else 'LOW',
        'workflow_count': len(workflow_distribution)
    }
    
    # 6. PLATFORM MATURITY
    # New vs established workflows
    wfs_live_copy = wfs_live.copy()
    wfs_live_copy["WORKFLOW_AGE_DAYS"] = (pd.Timestamp.now() - wfs_live_copy["WORKFLOW_TIMESTAMP"]).dt.days
    
    # Active workflows age
    active_wf_names = usage_live_copy["WORKFLOW_NAME"].unique()
    active_wfs_metadata = wfs_live_copy[wfs_live_copy["WORKFLOW_NAME"].isin(active_wf_names)]
    
    avg_workflow_age = active_wfs_metadata["WORKFLOW_AGE_DAYS"].mean() if not active_wfs_metadata.empty else None
    new_workflows_count = len(active_wfs_metadata[active_wfs_metadata["WORKFLOW_AGE_DAYS"] < 30]) if not active_wfs_metadata.empty else 0
    
    metrics['maturity'] = {
        'avg_workflow_age_days': avg_workflow_age,
        'new_workflows_count': new_workflows_count,
        'established_workflows_count': len(active_wfs_metadata) - new_workflows_count if not active_wfs_metadata.empty else 0,
        'maturity_level': 'MATURE' if avg_workflow_age and avg_workflow_age > 90 else 'GROWING' if avg_workflow_age and avg_workflow_age > 30 else 'NEW' if avg_workflow_age else 'UNKNOWN'
    }
    
    return metrics

