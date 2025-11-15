"""
Scenario 2: Deeper Trend Analysis Visualizations.

This module contains comprehensive trend analysis functions using workflow timestamps
and run times to understand customer usage patterns better.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..utils.config import COLORS


def visual5_workflow_creation_trends(df_wfs, df_runs):
    """
    Visual 5: Workflow Creation Trends Over Time
    
    Shows when workflows were created using WORKFLOW_TIMESTAMP.
    Helps identify if new workflows correlate with usage changes.
    
    Why this visual:
    - Reveals if new workflows are being introduced
    - Shows workflow lifecycle patterns
    - Can indicate platform expansion or changes
    """
    wfs_live = df_wfs[df_wfs['ENVIRONMENT'] == 'live'].copy()
    
    if wfs_live.empty:
        print("No LIVE workflows found.")
        return
    
    wfs_live['DATE'] = wfs_live['WORKFLOW_TIMESTAMP'].dt.date
    daily_workflows = wfs_live.groupby('DATE').size().reset_index(name='WORKFLOWS_CREATED')
    daily_workflows['DATE'] = pd.to_datetime(daily_workflows['DATE'])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(daily_workflows['DATE'], daily_workflows['WORKFLOWS_CREATED'],
           marker='o', markersize=6, linewidth=2, color=COLORS['primary'])
    
    ax.set_xlabel("Date", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Number of Workflows Created", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Daily Live Workflow Creation Trend",
                 fontsize=16, weight="bold", pad=20, color="black")
    plt.xticks(rotation=45, ha='right', fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual6_run_duration_analysis(df_runs):
    """
    Visual 6: Run Duration Analysis Over Time
    
    Shows run durations (STOP_TIME - START_TIME) over time.
    Helps identify if run times are changing, which might indicate issues.
    
    Why this visual:
    - Reveals operational efficiency trends
    - Long run times might indicate problems
    - Can explain usage declines if runs are taking longer
    """
    runs_live = df_runs[df_runs['ENVIRONMENT'] == 'live'].copy()
    
    if runs_live.empty:
        print("No LIVE runs found.")
        return
    
    # Calculate duration in hours
    runs_live['DURATION_HOURS'] = (runs_live['STOP_TIME'] - runs_live['START_TIME']).dt.total_seconds() / 3600
    
    # Filter to finished runs only
    runs_finished = runs_live[runs_live['OUTCOME'] == 'finished'].copy()
    
    if runs_finished.empty:
        print("No finished LIVE runs found.")
        return
    
    runs_finished['DATE'] = runs_finished['START_TIME'].dt.date
    daily_durations = runs_finished.groupby('DATE').agg(
        AVG_DURATION=('DURATION_HOURS', 'mean'),
        MEDIAN_DURATION=('DURATION_HOURS', 'median'),
        COUNT=('ID', 'count')
    ).reset_index()
    daily_durations['DATE'] = pd.to_datetime(daily_durations['DATE'])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(daily_durations['DATE'], daily_durations['AVG_DURATION'],
           marker='o', markersize=6, linewidth=2, color=COLORS['primary'],
           label='Average Duration')
    ax.plot(daily_durations['DATE'], daily_durations['MEDIAN_DURATION'],
           marker='s', markersize=5, linewidth=2, color=COLORS['success'],
           label='Median Duration', linestyle='--')
    
    ax.set_xlabel("Date", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Run Duration (Hours)", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Production Run Duration Trends Over Time",
                 fontsize=16, weight="bold", pad=20, color="black")
    plt.xticks(rotation=45, ha='right', fontsize=16)
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual7_daily_usage_timeline(checks_live_all):
    """
    Visual 7: Daily Usage Timeline (All Samples in LIVE Runs)
    
    Shows daily usage patterns using all samples in LIVE runs (not just pass QC).
    This is about customer usage, so we include all processing activity.
    
    Why this visual:
    - Shows actual customer usage patterns
    - Includes all processing activity regardless of QC outcome
    - Reveals daily volatility and patterns
    """
    data = checks_live_all.copy()
    data['DATE'] = data['TIMESTAMP'].dt.date
    daily_counts = data.groupby('DATE').size().reset_index(name='SAMPLES_PROCESSED')
    daily_counts['DATE'] = pd.to_datetime(daily_counts['DATE'])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.fill_between(daily_counts['DATE'], 0, daily_counts['SAMPLES_PROCESSED'],
                    alpha=0.3, color=COLORS['primary'])
    ax.plot(daily_counts['DATE'], daily_counts['SAMPLES_PROCESSED'],
           marker='o', markersize=5, linewidth=2.5, color=COLORS['primary'],
           markeredgecolor='white', markeredgewidth=1.5)
    
    # Add trend line
    z = np.polyfit(range(len(daily_counts)), daily_counts['SAMPLES_PROCESSED'], 1)
    p = np.poly1d(z)
    ax.plot(daily_counts['DATE'], p(range(len(daily_counts))),
           linestyle='--', linewidth=2, color=COLORS['neutral'], alpha=0.7,
           label='Overall Trend')
    
    ax.set_xlabel("Date", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Samples Processed Per Day", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Daily Customer Usage Timeline (All LIVE Processing Activity)",
                 fontsize=16, weight="bold", pad=20, color="black")
    plt.xticks(rotation=45, ha='right', fontsize=16)
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual8_weekly_patterns(df_runs, checks_live_all):
    """
    Visual 8: Weekly Usage Patterns
    
    Shows usage patterns by day of week to identify weekly cycles.
    Uses both run data and sample data to understand patterns.
    
    Why this visual:
    - Identifies weekly operational cycles
    - Reveals if certain days have higher/lower usage
    - Can indicate business operational patterns
    """
    # Analyze by day of week
    runs_live = df_runs[df_runs['ENVIRONMENT'] == 'live'].copy()
    runs_live['DAY_OF_WEEK'] = runs_live['START_TIME'].dt.day_name()
    
    checks_live_all_copy = checks_live_all.copy()
    checks_live_all_copy['DAY_OF_WEEK'] = checks_live_all_copy['TIMESTAMP'].dt.day_name()
    
    # Count runs and samples by day
    runs_daily = runs_live.groupby('DAY_OF_WEEK').size().reset_index(name='RUNS')
    samples_daily = checks_live_all_copy.groupby('DAY_OF_WEEK').size().reset_index(name='SAMPLES')
    
    # Order days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    runs_daily['DAY_OF_WEEK'] = pd.Categorical(runs_daily['DAY_OF_WEEK'], categories=day_order, ordered=True)
    samples_daily['DAY_OF_WEEK'] = pd.Categorical(samples_daily['DAY_OF_WEEK'], categories=day_order, ordered=True)
    runs_daily = runs_daily.sort_values('DAY_OF_WEEK')
    samples_daily = samples_daily.sort_values('DAY_OF_WEEK')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Runs by day
    x = np.arange(len(runs_daily))
    ax1.bar(x, runs_daily['RUNS'], color=COLORS['primary'], width=0.7, edgecolor='white', linewidth=1.5)
    ax1.set_xlabel("Day of Week", fontsize=16, weight="bold", color="black")
    ax1.set_ylabel("Number of Runs", fontsize=16, weight="bold", color="black")
    ax1.set_title("Production Runs by Day of Week", fontsize=16, weight="bold", color="black")
    ax1.set_xticks(x)
    ax1.set_xticklabels(runs_daily['DAY_OF_WEEK'], rotation=45, ha='right', fontsize=16)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_axisbelow(True)
    ax1.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # Samples by day
    x2 = np.arange(len(samples_daily))
    ax2.bar(x2, samples_daily['SAMPLES'], color=COLORS['success'], width=0.7, edgecolor='white', linewidth=1.5)
    ax2.set_xlabel("Day of Week", fontsize=16, weight="bold", color="black")
    ax2.set_ylabel("Number of Samples", fontsize=16, weight="bold", color="black")
    ax2.set_title("Samples Processed by Day of Week", fontsize=16, weight="bold", color="black")
    ax2.set_xticks(x2)
    ax2.set_xticklabels(samples_daily['DAY_OF_WEEK'], rotation=45, ha='right', fontsize=16)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_axisbelow(True)
    ax2.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    fig.suptitle("Scenario 2: Weekly Usage Patterns Analysis", fontsize=16, weight="bold", color="black", y=1.02)
    plt.tight_layout()
    plt.show()

