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


def visual1_billing_dispute(monthly, billable_live):
    """
    Visual 1: The Billing Dispute (Executive Summary)
    
    Shows the core dispute: customer expectation vs actual invoice.
    Highlights the overbilling amount and percentage.
    
    Why this visual:
    - Immediately shows the problem at a glance
    - Clear comparison for stakeholders
    - Sets up the rest of the analysis
    """
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
            ha="center", va="center", fontsize=18, weight="bold", color="white")
    ax.text(1, actual_val/2, f"{int(actual_val):,}\nsamples",
            ha="center", va="center", fontsize=18, weight="bold", color="white")
    
    # Overbilling annotation - positioned clearly
    ax.annotate(f"Overbilled: +{int(other_val):,} samples\n({latest_row['OVERBILLING_PCT']:.1f}% overbilling)",
                xy=(1, actual_val), xytext=(1.4, actual_val * 0.7),
                ha="left", va="center", fontsize=14, weight="bold", color=COLORS["danger"],
                bbox=dict(boxstyle="round,pad=1", facecolor="white", edgecolor=COLORS["danger"], linewidth=3),
                arrowprops=dict(arrowstyle="->", color=COLORS["danger"], lw=3))
    
    ax.set_ylabel("Billable Samples", fontsize=14, weight="bold")
    ax.set_title(f"Scenario 1: {latest_month} Billing Dispute - Customer Claims 15% Overbilling",
                 fontsize=16, weight="bold", pad=20)
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


def visual2_monthly_trend(monthly):
    """
    Visual 2: Monthly Billing Trend (Expected vs Actual)
    
    Shows the breakdown of expected vs overbilled samples across all months.
    Highlights the disputed month and shows overbilling percentages.
    
    Why this visual:
    - Demonstrates the issue is systemic, not isolated to one month
    - Shows the trend over time
    - Helps identify if the problem is getting worse
    """
    monthly_plot = monthly.reset_index().copy()
    monthly_plot["YEAR_MONTH_STR"] = monthly_plot["YEAR_MONTH"].astype(str)
    latest_month = monthly_plot["YEAR_MONTH"].max()
    
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
                ha="center", va="bottom", fontsize=11, weight="bold", color="black", zorder=3)
        
        # Overbilling percentage - only show if significant
        if pct > 5:
            ax.text(i, total + label_offset * 2.5, f"{pct:.1f}%", 
                    ha="center", va="bottom", fontsize=10, weight="bold", color=COLORS["danger"], zorder=3)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(monthly_plot["YEAR_MONTH_STR"], fontsize=12, weight="bold")
    ax.set_ylabel("Billable Samples", fontsize=14, weight="bold")
    ax.set_xlabel("Month", fontsize=14, weight="bold")
    ax.set_title("Scenario 1: Monthly Billing Breakdown - Expected (Blue) vs Overbilled (Red)",
                 fontsize=16, weight="bold", pad=20)
    ax.legend(loc="upper left", frameon=True, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    plt.tight_layout()
    plt.show()


def visual3_sample_types(billable_live):
    """
    Visual 3: Sample Type Breakdown
    
    Shows what types of samples are being billed: expected vs overbilled.
    Uses horizontal bars for easy reading of sample counts.
    
    Why this visual:
    - Clearly separates expected (blood/saliva) from overbilled (bone marrow/other)
    - Shows the magnitude of each category
    - Helps understand the composition of the billing issue
    """
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
    ax.set_yticklabels(y_labels, fontsize=12, weight='bold')
    ax.invert_yaxis()  # Invert so highest values are at top
    
    # Value labels - positioned clearly
    max_count = max(counts)
    for i, (v, color) in enumerate(zip(counts, colors_chart)):
        pct = (v / sum(counts)) * 100
        # Label inside bar if bar is wide enough, outside otherwise
        if v > max_count * 0.15:
            ax.text(v/2, i, f"{v:,}\n({pct:.1f}%)", 
                   ha="center", va="center", fontsize=12, weight='bold', color='white')
        else:
            ax.text(v + max_count * 0.03, i, f"{v:,} ({pct:.1f}%)", 
                   va="center", fontsize=11, weight='bold', color=color)
    
    ax.set_xlabel("Number of Samples", fontsize=14, weight="bold")
    ax.set_title("Scenario 1: Sample Type Breakdown - Expected vs Overbilled Types",
                 fontsize=16, weight="bold", pad=20)
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


def visual4_root_cause(billable_live):
    """
    Visual 4: Root Cause Analysis - Top Workflows Processing Bone Marrow
    
    Identifies which specific workflows are contributing to the overbilling problem.
    Shows top workflows by bone marrow sample volume.
    
    Why this visual:
    - Provides actionable information (which workflows to fix)
    - Shows the concentration of the problem
    - Helps prioritize workflow reviews
    """
    bm_data = billable_live[billable_live["SAMPLE_TYPE"] == "bone marrow"]
    
    if len(bm_data) == 0:
        print("No bone marrow samples found in billable data.")
        return
    
    top_workflows = bm_data["WORKFLOW_NAME"].value_counts().head(8).sort_values()
    
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
    ax.set_yticklabels(workflow_labels, fontsize=11, weight='bold')
    
    # Add value labels - positioned clearly
    max_val = max(top_workflows.values)
    for i, v in enumerate(top_workflows.values):
        label_x = v + max_val * 0.03
        ax.text(label_x, i, f"{v:,} samples", 
               va="center", fontsize=11, weight='bold', color=COLORS["danger"])
    
    ax.set_xlabel("Bone Marrow Samples Billed", fontsize=14, weight="bold")
    ax.set_title("Scenario 1: Root Cause Analysis - Top Live Workflows Billing Bone Marrow Samples",
                fontsize=16, weight="bold", pad=20, color=COLORS["danger"])
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

