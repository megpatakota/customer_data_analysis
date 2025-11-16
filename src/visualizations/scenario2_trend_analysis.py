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
    
    df['DATE'] = df['WORKFLOW_TIMESTAMP'].dt.date
    daily_workflows = df.groupby('DATE').size().reset_index(name='WORKFLOWS_CREATED')
    daily_workflows['DATE'] = pd.to_datetime(daily_workflows['DATE'])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(daily_workflows['DATE'], daily_workflows['WORKFLOWS_CREATED'],
           marker='o', markersize=6, linewidth=2, color=COLORS['primary'])
    
    ax.set_xlabel("Date", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Number of Workflows Created", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Daily Workflow Creation Trend",
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
    df = df[df["ENVIRONMENT_runs"] == "live"].copy() if "ENVIRONMENT_runs" in df.columns else df.copy()
    
    # Calculate duration in hours
    df['DURATION_HOURS'] = (df['STOP_TIME'] - df['START_TIME']).dt.total_seconds() / 3600
    
    df['DATE'] = df['START_TIME'].dt.date
    daily_durations = df.groupby('DATE').agg(
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


def visual8_weekly_patterns(df, usage_live):
    """
    Visual 8: Weekly Usage Patterns
    
    Shows usage patterns by day of week to identify weekly cycles.
    Analyzes both production runs and individual samples processed.
    
    Why this visual:
    - Identifies weekly operational cycles
    - Reveals if certain days have higher/lower usage
    - Can indicate business operational patterns
    
    Args:
        df: Merged dataframe with all data - used for all runs analysis
            Must have START_TIME (run start time) and RUN_ID
        usage_live: Sample-level dataframe from get_usage_live_data()
            Contains LIVE + finished runs only - used for live successful runs analysis
            Must have START_TIME (run start time) and RUN_ID
    """
    # Make copies to avoid modifying the originals
    df = df.copy()
    usage_live = usage_live.copy()
    
    # Left Chart: All Runs Analysis
    # Count unique runs per day of week from all data (all environments, all outcomes)
    # Get unique runs: for each RUN_ID, take the first START_TIME (they should all be the same for a given run)
    df_runs_unique = df[['RUN_ID', 'START_TIME']].drop_duplicates(subset=['RUN_ID'], keep='first')
    df_runs_unique = df_runs_unique[df_runs_unique['START_TIME'].notna()]  # Only runs with START_TIME
    df_runs_unique['RUN_DAY_OF_WEEK'] = df_runs_unique['START_TIME'].dt.day_name()
    runs_daily = df_runs_unique.groupby('RUN_DAY_OF_WEEK')['RUN_ID'].nunique().reset_index(name='RUNS')
    runs_daily = runs_daily.rename(columns={'RUN_DAY_OF_WEEK': 'DAY_OF_WEEK'})
    
    # Right Chart: Live Successful Runs Analysis
    # Count unique runs per day of week from usage_live (LIVE + finished only)
    # Get unique runs: for each RUN_ID, take the first START_TIME (they should all be the same for a given run)
    usage_live_runs_unique = usage_live[['RUN_ID', 'START_TIME']].drop_duplicates(subset=['RUN_ID'], keep='first')
    usage_live_runs_unique = usage_live_runs_unique[usage_live_runs_unique['START_TIME'].notna()]  # Only runs with START_TIME
    usage_live_runs_unique['RUN_DAY_OF_WEEK'] = usage_live_runs_unique['START_TIME'].dt.day_name()
    live_runs_daily = usage_live_runs_unique.groupby('RUN_DAY_OF_WEEK')['RUN_ID'].nunique().reset_index(name='RUNS')
    live_runs_daily = live_runs_daily.rename(columns={'RUN_DAY_OF_WEEK': 'DAY_OF_WEEK'})
    
    # Merge the dataframes to create stacked chart data
    # Ensure both have all days of week for consistent comparison
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Convert DAY_OF_WEEK to string to avoid categorical issues during merge
    runs_daily['DAY_OF_WEEK'] = runs_daily['DAY_OF_WEEK'].astype(str)
    live_runs_daily['DAY_OF_WEEK'] = live_runs_daily['DAY_OF_WEEK'].astype(str)
    
    # Create complete day list
    all_days = pd.DataFrame({'DAY_OF_WEEK': day_order})
    
    # Merge with all days to ensure all days are present, fill numeric columns with 0
    runs_daily = all_days.merge(runs_daily, on='DAY_OF_WEEK', how='left')
    runs_daily['RUNS'] = runs_daily['RUNS'].fillna(0).astype(int)
    
    live_runs_daily = all_days.merge(live_runs_daily, on='DAY_OF_WEEK', how='left')
    live_runs_daily['RUNS'] = live_runs_daily['RUNS'].fillna(0).astype(int)
    
    # Merge all runs and live runs data
    # Use left merge to ensure we have all days from runs_daily
    merged_data = runs_daily.merge(live_runs_daily, on='DAY_OF_WEEK', how='left', suffixes=('_all', '_live'))
    merged_data['RUNS_all'] = merged_data['RUNS_all'].fillna(0).astype(int)
    merged_data['RUNS_live'] = merged_data['RUNS_live'].fillna(0).astype(int)
    
    # Ensure all runs >= live runs (usage_live is a subset of df)
    # If live runs > all runs, something is wrong - cap it
    merged_data['RUNS_live'] = merged_data[['RUNS_all', 'RUNS_live']].min(axis=1)
    
    # Convert to categorical for proper ordering
    merged_data['DAY_OF_WEEK'] = pd.Categorical(merged_data['DAY_OF_WEEK'], categories=day_order, ordered=True)
    merged_data = merged_data.sort_values('DAY_OF_WEEK')
    
    # Create grouped bar chart for clearer comparison
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(merged_data))
    width = 0.35  # Width for each bar group
    
    # All Runs bar (left side of each pair)
    bars1 = ax.bar(x - width/2, merged_data['RUNS_all'], width, label='All Runs', 
                   color=COLORS['primary'], edgecolor='white', linewidth=1.5)
    
    # Live Runs bar (right side of each pair)
    bars2 = ax.bar(x + width/2, merged_data['RUNS_live'], width, label='Live Runs', 
                   color=COLORS['success'], edgecolor='white', linewidth=1.5)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=12, weight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(merged_data['DAY_OF_WEEK'], rotation=45, ha='right', fontsize=16)
    ax.set_xlabel("Day of Week", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Number of Runs", fontsize=16, weight="bold", color="black")
    ax.set_title("Weekly Usage Patterns: All Runs vs Live Successful Runs", 
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()

