"""
Scenario 2: Deeper Trend Analysis Visualizations.

This module contains comprehensive trend analysis functions using workflow timestamps
and run times to understand customer usage patterns better.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..utils.config import COLORS


def visual5_workflow_creation_trends(df):
    """
    Visual 5: Workflow Creation Trends Over Time
    
    Shows when workflows were created using WORKFLOW_TIMESTAMP.
    Helps identify if new workflows correlate with usage changes.
    
    Why this visual:
    - Reveals if new workflows are being introduced
    - Shows workflow lifecycle patterns
    - Can indicate platform expansion or changes
    
    Args:
        df: Merged dataframe - will be filtered to LIVE workflows only
    """
    # Filter to LIVE workflows only
    df_live = df[df["ENVIRONMENT_wfs"] == "live"].copy() if "ENVIRONMENT_wfs" in df.columns else df.copy()
    
    df_live['DATE'] = df_live['WORKFLOW_TIMESTAMP'].dt.date
    daily_workflows = df_live.groupby('DATE').size().reset_index(name='WORKFLOWS_CREATED')
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


def visual6_run_duration_analysis(df):
    """
    Visual 6: Run Duration Analysis Over Time
    
    Shows run durations (STOP_TIME - START_TIME) over time.
    Helps identify if run times are changing, which might indicate issues.
    
    Why this visual:
    - Reveals operational efficiency trends
    - Long run times might indicate problems
    - Can explain usage declines if runs are taking longer
    
    Args:
        df: Merged dataframe - will be filtered to LIVE runs only
    """
    # Filter to LIVE runs only
    df_live = df[df["ENVIRONMENT_runs"] == "live"].copy() if "ENVIRONMENT_runs" in df.columns else df.copy()
    
    # Calculate duration in hours
    df_live['DURATION_HOURS'] = (df_live['STOP_TIME'] - df_live['START_TIME']).dt.total_seconds() / 3600
    
    df_live['DATE'] = df_live['START_TIME'].dt.date
    daily_durations = df_live.groupby('DATE').agg(
        AVG_DURATION=('DURATION_HOURS', 'mean'),
        MEDIAN_DURATION=('DURATION_HOURS', 'median'),
        COUNT=('RUN_ID', 'count')
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


def visual7_daily_usage_timeline(df):
    """
    Visual 7: Daily Usage Timeline (All Samples in LIVE Runs)
    
    Shows daily usage patterns using all samples in LIVE runs (not just pass QC).
    This is about customer usage, so we include all processing activity.
    
    Why this visual:
    - Shows actual customer usage patterns
    - Includes all processing activity regardless of QC outcome
    - Reveals daily volatility and patterns
    """
    daily_counts = df.groupby('DATE').size().reset_index(name='SAMPLES_PROCESSED')
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


def visual8_weekly_patterns(df):
    """
    Visual 8: Weekly Usage Patterns
    
    Shows usage patterns by day of week to identify weekly cycles.
    Uses both run data and sample data to understand patterns.
    
    Why this visual:
    - Identifies weekly operational cycles
    - Reveals if certain days have higher/lower usage
    - Can indicate business operational patterns
    
    Args:
        df: Merged dataframe with run and sample data (e.g., usage_live from Scenario 2)
            Should have START_TIME (for runs) and TIMESTAMP (for samples)
    """
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    # For runs: use START_TIME to get day of week
    if 'START_TIME' in df.columns:
        df['RUN_DAY_OF_WEEK'] = df['START_TIME'].dt.day_name()
        # Count unique runs by day of week
        runs_daily = df.groupby('RUN_DAY_OF_WEEK')['RUN_ID'].nunique().reset_index(name='RUNS')
        runs_daily = runs_daily.rename(columns={'RUN_DAY_OF_WEEK': 'DAY_OF_WEEK'})
    else:
        # Fallback: create empty dataframe
        runs_daily = pd.DataFrame(columns=['DAY_OF_WEEK', 'RUNS'])
    
    # For samples: use TIMESTAMP to get day of week
    if 'TIMESTAMP' in df.columns:
        df['SAMPLE_DAY_OF_WEEK'] = df['TIMESTAMP'].dt.day_name()
        # Count all samples by day of week
        samples_daily = df.groupby('SAMPLE_DAY_OF_WEEK').size().reset_index(name='SAMPLES')
        samples_daily = samples_daily.rename(columns={'SAMPLE_DAY_OF_WEEK': 'DAY_OF_WEEK'})
    else:
        # Fallback: create empty dataframe
        samples_daily = pd.DataFrame(columns=['DAY_OF_WEEK', 'SAMPLES'])
    
    # Order days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if not runs_daily.empty:
        runs_daily['DAY_OF_WEEK'] = pd.Categorical(runs_daily['DAY_OF_WEEK'], categories=day_order, ordered=True)
        runs_daily = runs_daily.sort_values('DAY_OF_WEEK')
    if not samples_daily.empty:
        samples_daily['DAY_OF_WEEK'] = pd.Categorical(samples_daily['DAY_OF_WEEK'], categories=day_order, ordered=True)
        samples_daily = samples_daily.sort_values('DAY_OF_WEEK')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Runs by day
    if not runs_daily.empty:
        x = np.arange(len(runs_daily))
        ax1.bar(x, runs_daily['RUNS'], color=COLORS['primary'], width=0.7, edgecolor='white', linewidth=1.5)
        ax1.set_xticks(x)
        ax1.set_xticklabels(runs_daily['DAY_OF_WEEK'], rotation=45, ha='right', fontsize=16)
    else:
        ax1.text(0.5, 0.5, 'No run data available', ha='center', va='center', transform=ax1.transAxes, fontsize=14)
    ax1.set_xlabel("Day of Week", fontsize=16, weight="bold", color="black")
    ax1.set_ylabel("Number of Runs", fontsize=16, weight="bold", color="black")
    ax1.set_title("Production Runs by Day of Week", fontsize=16, weight="bold", color="black")
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_axisbelow(True)
    ax1.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # Samples by day
    if not samples_daily.empty:
        x2 = np.arange(len(samples_daily))
        ax2.bar(x2, samples_daily['SAMPLES'], color=COLORS['success'], width=0.7, edgecolor='white', linewidth=1.5)
        ax2.set_xticks(x2)
        ax2.set_xticklabels(samples_daily['DAY_OF_WEEK'], rotation=45, ha='right', fontsize=16)
    else:
        ax2.text(0.5, 0.5, 'No sample data available', ha='center', va='center', transform=ax2.transAxes, fontsize=14)
    ax2.set_xlabel("Day of Week", fontsize=16, weight="bold", color="black")
    ax2.set_ylabel("Number of Samples", fontsize=16, weight="bold", color="black")
    ax2.set_title("Samples Processed by Day of Week", fontsize=16, weight="bold", color="black")
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_axisbelow(True)
    ax2.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    fig.suptitle("Scenario 2: Weekly Usage Patterns Analysis", fontsize=16, weight="bold", color="black", y=1.02)
    plt.tight_layout()
    plt.show()

