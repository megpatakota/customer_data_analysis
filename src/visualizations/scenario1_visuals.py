"""
Scenario 1: Billing Reconciliation Visualizations.

This module contains all visualization functions for Scenario 1 analysis.
Each function creates a single, clean, presentation-ready chart.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ..utils.config import COLORS

from src.data_processing.data_loader import get_billable_data

billable_live = get_billable_data()


def visual1_billing_dispute():
    """
    Visual 1: The Billing Dispute (Executive Summary)
    
    Shows the core dispute: customer expectation vs actual invoice.
    Highlights the overbilling amount and percentage.
    
    CRITICAL: Uses billable_live directly to ensure consistency with all other visuals.
    Creates monthly aggregation internally from billable_live.
    
    Why this visual:
    - Immediately shows the problem at a glance
    - Clear comparison for stakeholders
    - Sets up the rest of the analysis
    """
    # Create monthly aggregation from billable_live (consistent with other visuals)
    billable_live = get_billable_data()
    monthly = (
        billable_live.groupby("YEAR_MONTH").agg(
            TOTAL_SAMPLES=("RUN_ID", "count"),
            BLOOD_SALIVA=(
                "SAMPLE_TYPE",
                lambda s: s.isin(["blood", "saliva"]).sum(),
            ),
        )
    )
    monthly["OTHER_TYPES"] = monthly["TOTAL_SAMPLES"] - monthly["BLOOD_SALIVA"]
    monthly["OVERBILLING_PCT"] = (
        monthly["OTHER_TYPES"]
        .div(monthly["BLOOD_SALIVA"].replace(0, np.nan))
        .mul(100)
        .round(2)
    )
    monthly["OVERBILLING_PCT"] = monthly["OVERBILLING_PCT"].fillna(0)
    
    monthly_plot = monthly.reset_index().copy()
    monthly_plot["YEAR_MONTH_STR"] = monthly_plot["YEAR_MONTH"].astype(str)
    latest_month = monthly_plot["YEAR_MONTH"].max()
    latest_row = monthly[monthly.index == latest_month].iloc[0]
    
    expected_val = latest_row["BLOOD_SALIVA"]
    actual_val = latest_row["TOTAL_SAMPLES"]
    other_val = latest_row["OTHER_TYPES"]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.bar(
        ["Customer Expectation\n(Blood + Saliva Only)", "Our Invoice\n(Including Other Types)"],
        [expected_val, actual_val],
        color=[COLORS["primary"], COLORS["danger"]],
        width=0.5,
        edgecolor="white",
        linewidth=2
    )
    
    # Value labels on bars - clear white text
    ax.text(0, expected_val/2, f"{int(expected_val):,}\nsamples",
            ha="center", va="center", fontsize=16, weight="bold", color="white")
    ax.text(1, actual_val/2, f"{int(actual_val):,}\nsamples",
            ha="center", va="center", fontsize=16, weight="bold", color="white")
    
    # Overbilling annotation - positioned clearly
    ax.annotate(f"Overbilled: +{int(other_val):,} samples\n({latest_row['OVERBILLING_PCT']:.1f}% overbilling)",
                xy=(1, actual_val), xytext=(1.4, actual_val * 0.7),
                ha="left", va="center", fontsize=16, weight="bold", color=COLORS["danger"],
                bbox=dict(boxstyle="round,pad=1", facecolor="white", edgecolor=COLORS["danger"], linewidth=3),
                arrowprops=dict(arrowstyle="->", color=COLORS["danger"], lw=3))
    
    ax.set_ylabel("Billable Samples", fontsize=16, weight="bold", color="black")
    ax.set_title(f"Scenario 1: {latest_month} Billing Dispute - Customer Claims 15% Overbilling",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.set_ylim(0, actual_val * 1.35)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    # Add grid lines for better readability
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual2_monthly_trend():
    """
    Visual 2: Monthly Billing Trend (Expected vs Actual)
    
    Shows the breakdown of expected vs overbilled samples across all months.
    Highlights the disputed month and shows overbilling percentages.
    
    CRITICAL: Uses billable_live directly to ensure consistency with all other visuals.
    Creates monthly aggregation internally from billable_live.
    
    Why this visual:
    - Demonstrates the issue is systemic, not isolated to one month
    - Shows the trend over time
    - Helps identify if the problem is getting worse
    """
    # Create monthly aggregation from billable_live (consistent with all visuals)
    
    monthly = (
        billable_live.groupby("YEAR_MONTH").agg(
            TOTAL_SAMPLES=("RUN_ID", "count"),
            BLOOD_SALIVA=(
                "SAMPLE_TYPE",
                lambda s: s.isin(["blood", "saliva"]).sum(),
            ),
            OTHER_TYPES=(
                "SAMPLE_TYPE",
                lambda s: (~s.isin(["blood", "saliva"])).sum(),
            ),
        )
    )
    monthly["OVERBILLING_PCT"] = (
        monthly["OTHER_TYPES"]
        .div(monthly["BLOOD_SALIVA"].replace(0, np.nan))
        .mul(100)
        .round(2)
    )
    monthly["OVERBILLING_PCT"] = monthly["OVERBILLING_PCT"].fillna(0)
    
    # Ensure monthly is a DataFrame (not Series)
    if isinstance(monthly, pd.Series):
        monthly = monthly.to_frame().T
    
    # CRITICAL: The monthly dataframe comes from groupby("YEAR_MONTH"), so the index is a PeriodIndex
    # Reset index to convert PeriodIndex to a column
    # When reset_index() is called on a DataFrame with a PeriodIndex, it creates a column with the index values
    monthly_plot = monthly.reset_index().copy()
    
    # Ensure we're working with all months (no filtering) - CRITICAL: Don't filter!
    # Sort by YEAR_MONTH to ensure chronological order
    monthly_plot = monthly_plot.sort_values("YEAR_MONTH").reset_index(drop=True)
    
    # Ensure all required columns exist
    required_cols = ["TOTAL_SAMPLES", "BLOOD_SALIVA", "OTHER_TYPES", "OVERBILLING_PCT"]
    missing_cols = [col for col in required_cols if col not in monthly_plot.columns]
    if missing_cols:
        raise ValueError(f"ERROR: Missing required columns in monthly dataframe: {missing_cols}")
    
    # Convert to string for display
    monthly_plot["YEAR_MONTH_STR"] = monthly_plot["YEAR_MONTH"].astype(str)
    latest_month = monthly_plot["YEAR_MONTH"].max()
    
    # Validate we have data
    if len(monthly_plot) == 0:
        raise ValueError("ERROR: monthly dataframe is empty. Cannot create visual.")
    
    # Ensure we're plotting ALL months - no filtering!
    # The monthly dataframe should contain all months from billable_live
    # Print info for debugging
    num_months = len(monthly_plot)
    if num_months == 0:
        raise ValueError("ERROR: Monthly dataframe is empty. Cannot create visual.")
    elif num_months == 1:
        print(f"WARNING: Only {num_months} month in monthly data. Expected multiple months.")
        print(f"  Month: {monthly_plot['YEAR_MONTH_STR'].iloc[0]}")
        print("  This might indicate that billable_live only has data from one month.")
    else:
        print(f"[OK] Plotting {num_months} months: {', '.join(monthly_plot['YEAR_MONTH_STR'].tolist())}")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    x_pos = np.arange(len(monthly_plot))
    
    # Calculate max value for proper scaling
    max_val = monthly_plot["TOTAL_SAMPLES"].max()
    label_offset = max_val * 0.08
    
    # Set y-axis limits FIRST so grid aligns properly
    ax.set_ylim(0, max_val * 1.3)
    
    # Enable grid BEFORE drawing bars - make it visible
    ax.set_axisbelow(True)  # Put grid behind bars
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # Stacked bars - drawn after grid
    ax.bar(x_pos, monthly_plot["BLOOD_SALIVA"], 
           label="Expected: Blood + Saliva", color=COLORS["primary"], width=0.7, edgecolor="white", linewidth=1.5, zorder=2)
    ax.bar(x_pos, monthly_plot["OTHER_TYPES"], 
           bottom=monthly_plot["BLOOD_SALIVA"],
           label="Overbilled: Bone Marrow + Other", color=COLORS["danger"], width=0.7, edgecolor="white", linewidth=1.5, zorder=2)
    
    # Add labels on top - spacing to avoid overlap
    for i, (idx, row) in enumerate(monthly_plot.iterrows()):
        total = row["TOTAL_SAMPLES"]
        pct = row["OVERBILLING_PCT"]
        
        # Total value label
        ax.text(i, total + label_offset, f"{int(total):,}", 
                ha="center", va="bottom", fontsize=16, weight="bold", color="black", zorder=3)
        
        # Overbilling percentage - only show if significant
        if pct > 5:
            ax.text(i, total + label_offset * 2.5, f"{pct:.1f}%", 
                    ha="center", va="bottom", fontsize=16, weight="bold", color=COLORS["danger"], zorder=3)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(monthly_plot["YEAR_MONTH_STR"], fontsize=16, weight="bold")
    ax.set_ylabel("Billable Samples", fontsize=16, weight="bold", color="black")
    ax.set_xlabel("Month", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Monthly Billing Breakdown - Expected vs Overbilled",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    plt.tight_layout()
    plt.show()


def visual3_sample_types():
    """
    Visual 3: Sample Type Breakdown
    
    Shows what types of samples are being billed: expected vs overbilled.
    Uses horizontal bars for easy reading of sample counts.
    
    Why this visual:
    - Clearly separates expected (blood/saliva) from overbilled (bone marrow/other)
    - Shows the magnitude of each category
    - Helps understand the composition of the billing issue
    """
    billable_live = get_billable_data()
    sample_counts = billable_live["SAMPLE_TYPE"].value_counts()
    
    blood = sample_counts.get("blood", 0)
    saliva = sample_counts.get("saliva", 0)
    bm = sample_counts.get("bone marrow", 0)
    other_samples = len(billable_live) - blood - saliva - bm
    
    # Prepare data
    labels = ["Blood", "Saliva", "Bone Marrow\n(Overbilled)", "Other\n(Overbilled)"]
    counts = [blood, saliva, bm, other_samples]
    colors_chart = [COLORS["primary"], COLORS["success"], COLORS["danger"], COLORS["neutral"]]
    
    # Sort by counts from high to low (highest at top, lowest at bottom)
    sorted_data = sorted(zip(counts, labels, colors_chart), key=lambda x: x[0], reverse=True)
    counts, labels, colors_chart = zip(*sorted_data)
    counts = list(counts)
    labels = list(labels)
    colors_chart = list(colors_chart)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Horizontal bar chart - first item (highest) at top, last item (lowest) at bottom
    # Reverse the y-positions so highest appears at top visually
    y_positions = list(range(len(labels)))
    bars = ax.barh(y_positions, counts, color=colors_chart, edgecolor='white', linewidth=2, height=0.7)
    
    # Y-axis labels - determine if expected or overbilled based on label content
    y_labels = []
    for label, count in zip(labels, counts):
        if "Overbilled" in label:
            status = "Overbilled"
        else:
            status = "Expected"
        pct = (count / sum(counts)) * 100
        y_labels.append(f"{label}\n{status}")
    
    # Set y-ticks in reverse order so highest bar appears at top
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(y_labels, fontsize=16, weight='bold')
    ax.invert_yaxis()  # Invert so highest values are at top
    
    # Value labels - positioned clearly
    max_count = max(counts)
    for i, (v, color) in enumerate(zip(counts, colors_chart)):
        pct = (v / sum(counts)) * 100
        # Label inside bar if bar is wide enough, outside otherwise
        if v > max_count * 0.15:
            ax.text(v/2, i, f"{v:,}\n({pct:.1f}%)", 
                   ha="center", va="center", fontsize=16, weight='bold', color='white')
        else:
            ax.text(v + max_count * 0.03, i, f"{v:,} ({pct:.1f}%)", 
                   va="center", fontsize=16, weight='bold', color=color)
    
    ax.set_xlabel("Number of Samples", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Sample Type Breakdown - Expected vs Overbilled Types",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.set_xlim(0, max_count * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    # Add grid lines for better readability
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual4_root_cause():
    """
    Visual 4: Root Cause Analysis - Top Workflows Processing Bone Marrow
    
    Identifies which specific workflows are contributing to the overbilling problem.
    Shows top workflows by bone marrow sample volume.
    
    Why this visual:
    - Provides actionable information (which workflows to fix)
    - Shows the concentration of the problem
    - Helps prioritize workflow reviews
    """
    billable_live = get_billable_data()
    bm_data = billable_live[billable_live["SAMPLE_TYPE"] == "bone marrow"]
    
    if len(bm_data) == 0:
        print("No bone marrow samples found in billable data.")
        return
    
    top_workflows = bm_data["WORKFLOW_NAME_wfs"].value_counts().head(8).sort_values()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    bars = ax.barh(range(len(top_workflows)), top_workflows.values, 
                  color=COLORS["danger"], edgecolor='white', linewidth=2)
    
    ax.set_yticks(range(len(top_workflows)))
    workflow_labels = []
    for name in top_workflows.index:
        if len(name) > 65:
            workflow_labels.append(name[:62] + "...")
        else:
            workflow_labels.append(name)
    ax.set_yticklabels(workflow_labels, fontsize=16, weight='bold')
    
    # Add value labels - positioned clearly
    max_val = max(top_workflows.values)
    for i, v in enumerate(top_workflows.values):
        label_x = v + max_val * 0.03
        ax.text(label_x, i, f"{v:,} samples", 
               va="center", fontsize=16, weight='bold', color=COLORS["danger"])
    
    ax.set_xlabel("Bone Marrow Samples Billed", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Root Cause Analysis - Top Live Workflows Billing Bone Marrow Samples",
                fontsize=16, weight="bold", pad=20, color="black")
    ax.set_xlim(0, max_val * 1.18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    # Add grid lines for better readability
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()

