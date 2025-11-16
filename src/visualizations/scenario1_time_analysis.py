"""
Scenario 1: Time-based Trend Analysis Visualizations.

This module contains time-based analysis functions to understand WHEN different
sample types are being processed, helping explain what happened.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..utils.config import COLORS
from src.data_processing.data_loader import get_billable_data

billable_live = get_billable_data()

def visual5_time_of_day_patterns():
    """
    Visual 5: Time of Day Patterns by Sample Type
    
    Shows what time of day different sample types are being processed.
    Helps identify if there are patterns in when bone marrow vs blood/saliva are run.
    
    NOTE: For Scenario 1 billing analysis, uses BILLABLE samples only:
    - LIVE environment
    - OUTCOME = 'finished'
    - QC_CHECK = 'pass' (excluding missing QC as per decision)
    
    Why this visual:
    - Reveals temporal patterns in sample processing
    - Helps understand if bone marrow samples run at specific times
    - Can indicate operational patterns or scheduling differences
    """
    data = billable_live.copy()
    data['HOUR'] = data['TIMESTAMP'].dt.hour
    
    # Classify sample types
    data['SAMPLE_CATEGORY'] = data['SAMPLE_TYPE'].apply(
        lambda x: 'Blood' if x == 'blood' 
        else 'Saliva' if x == 'saliva' 
        else 'Bone Marrow' if x == 'bone marrow'
        else 'Other'
    )
    
    # Count by hour and sample category
    hourly = data.groupby(['HOUR', 'SAMPLE_CATEGORY']).size().reset_index(name='COUNT')
    
    # Pivot for stacked bar chart
    hourly_pivot = hourly.pivot(index='HOUR', columns='SAMPLE_CATEGORY', values='COUNT').fillna(0)
    
    # Reorder columns: Blood, Saliva, Bone Marrow, Other
    category_order = ['Blood', 'Saliva', 'Bone Marrow', 'Other']
    hourly_pivot = hourly_pivot.reindex(columns=[c for c in category_order if c in hourly_pivot.columns], fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Stacked bar chart
    x = hourly_pivot.index
    width = 0.7
    bottom = np.zeros(len(hourly_pivot))
    
    colors_map = {
        'Blood': COLORS['primary'],
        'Saliva': COLORS['success'],
        'Bone Marrow': COLORS['danger'],
        'Other': COLORS['neutral']
    }
    
    for category in hourly_pivot.columns:
        values = hourly_pivot[category].values
        ax.bar(x, values, width, label=category, bottom=bottom, 
               color=colors_map.get(category, COLORS['neutral']),
               edgecolor='white', linewidth=1.5)
        bottom += values
    
    ax.set_xlabel("Hour of Day", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Number of Samples", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Time of Day Processing Patterns by Sample Type",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45, ha='right', fontsize=16)
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual6_day_of_week_patterns():
    """
    Visual 6: Day of Week Patterns by Sample Type
    
    Shows what day of week different sample types are being processed.
    Helps identify if there are patterns in when bone marrow vs blood/saliva are run.
    
    NOTE: For Scenario 1 billing analysis, uses BILLABLE samples only:
    - LIVE environment
    - OUTCOME = 'finished'
    - QC_CHECK = 'pass' (excluding missing QC as per decision)
    
    Why this visual:
    - Reveals weekly patterns in sample processing
    - Helps understand if bone marrow samples run on specific days
    - Can indicate operational schedules or batch processing patterns
    """
    data = billable_live.copy()
    data['DAY_OF_WEEK'] = data['TIMESTAMP'].dt.day_name()
    
    # Classify sample types
    data['SAMPLE_CATEGORY'] = data['SAMPLE_TYPE'].apply(
        lambda x: 'Blood' if x == 'blood' 
        else 'Saliva' if x == 'saliva' 
        else 'Bone Marrow' if x == 'bone marrow'
        else 'Other'
    )
    
    # Count by day and sample category
    daily = data.groupby(['DAY_OF_WEEK', 'SAMPLE_CATEGORY']).size().reset_index(name='COUNT')
    
    # Order days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily['DAY_OF_WEEK'] = pd.Categorical(daily['DAY_OF_WEEK'], categories=day_order, ordered=True)
    daily = daily.sort_values('DAY_OF_WEEK')
    
    # Pivot for stacked bar chart
    daily_pivot = daily.pivot(index='DAY_OF_WEEK', columns='SAMPLE_CATEGORY', values='COUNT').fillna(0)
    
    # Reorder columns: Blood, Saliva, Bone Marrow, Other
    category_order = ['Blood', 'Saliva', 'Bone Marrow', 'Other']
    daily_pivot = daily_pivot.reindex(columns=[c for c in category_order if c in daily_pivot.columns], fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Stacked bar chart
    x = np.arange(len(daily_pivot))
    width = 0.7
    bottom = np.zeros(len(daily_pivot))
    
    colors_map = {
        'Blood': COLORS['primary'],
        'Saliva': COLORS['success'],
        'Bone Marrow': COLORS['danger'],
        'Other': COLORS['neutral']
    }
    
    for category in daily_pivot.columns:
        values = daily_pivot[category].values
        ax.bar(x, values, width, label=category, bottom=bottom, 
               color=colors_map.get(category, COLORS['neutral']),
               edgecolor='white', linewidth=1.5)
        bottom += values
    
    ax.set_xlabel("Day of Week", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Number of Samples", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Day of Week Processing Patterns by Sample Type",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.set_xticks(x)
    ax.set_xticklabels(daily_pivot.index, rotation=45, ha='right', fontsize=16)
    ax.legend(loc="upper right", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual7_sample_type_timeline():
    """
    Visual 7: Sample Type Timeline Over Time
    
    Shows when different sample types are being processed over the entire time period.
    Uses sample type as legend to show patterns.
    
    NOTE: For Scenario 1 billing analysis, uses BILLABLE samples only:
    - LIVE environment
    - OUTCOME = 'finished'
    - QC_CHECK = 'pass' (excluding missing QC as per decision)
    
    Why this visual:
    - Reveals if bone marrow processing is increasing/decreasing over time
    - Shows relationship between different sample types processing patterns
    - Helps identify trends that might explain the billing issue
    """
    data = billable_live.copy()
    data['DATE'] = data['TIMESTAMP'].dt.date
    
    # Classify sample types
    data['SAMPLE_CATEGORY'] = data['SAMPLE_TYPE'].apply(
        lambda x: 'Blood' if x == 'blood' 
        else 'Saliva' if x == 'saliva' 
        else 'Bone Marrow' if x == 'bone marrow'
        else 'Other'
    )
    
    # Daily counts by category
    daily_counts = data.groupby(['DATE', 'SAMPLE_CATEGORY']).size().reset_index(name='COUNT')
    
    # Pivot for line plot
    daily_pivot = daily_counts.pivot(index='DATE', columns='SAMPLE_CATEGORY', values='COUNT').fillna(0)
    daily_pivot.index = pd.to_datetime(daily_pivot.index)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors_map = {
        'Blood': COLORS['primary'],
        'Saliva': COLORS['success'],
        'Bone Marrow': COLORS['danger'],
        'Other': COLORS['neutral']
    }
    
    for category in ['Blood', 'Saliva', 'Bone Marrow', 'Other']:
        if category in daily_pivot.columns:
            ax.plot(daily_pivot.index, daily_pivot[category], 
                   marker='o', markersize=4, linewidth=2, 
                   label=category, color=colors_map.get(category, COLORS['neutral']))
    
    ax.set_xlabel("Date", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Number of Samples", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Daily Processing Timeline by Sample Type",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    plt.xticks(rotation=45, ha='right', fontsize=16)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()

