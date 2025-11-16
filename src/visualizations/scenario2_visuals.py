"""
Scenario 2: Customer Health Visualizations.

This module contains all visualization functions for Scenario 2 analysis.
Each function creates a single, clean, presentation-ready chart.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ..utils.config import COLORS


def visual1_usage_trend(df):
    """
    Visual 1: Customer Usage Trend Over Time
    Runs determine the usage.
    
    Shows monthly processing samples with trend line (all samples in LIVE runs).
    Highlights significant drops that exceed risk threshold.
    
    Why this visual:
    - Shows overall growth trajectory
    - Identifies concerning drops at a glance
    - Provides context for month-over-month changes
    - Uses all samples (not just pass QC) to reflect actual customer usage
    """    
    usage_monthly = (
        df.groupby("YEAR_MONTH").agg(
            SAMPLES_PROCESSED=("RUN_ID", "count"),
            UNIQUE_RUNS=("RUN_ID", "nunique"),
        ).sort_index()
    )
    usage_monthly["MOM_CHANGE_PCT"] = usage_monthly["SAMPLES_PROCESSED"].pct_change() * 100
    um_plot = usage_monthly.reset_index().copy()
    um_plot["YEAR_MONTH_STR"] = um_plot["YEAR_MONTH"].astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Fill area under curve
    ax.fill_between(range(len(um_plot)), 0, um_plot["SAMPLES_PROCESSED"],
                     alpha=0.3, color=COLORS["primary"])
    
    # Main line
    ax.plot(range(len(um_plot)), um_plot["SAMPLES_PROCESSED"],
            marker="o", markersize=14, linewidth=4, color=COLORS["primary"], 
            label="Monthly samples processed", markeredgecolor='white', markeredgewidth=2)
    
    # Add trend line
    z = np.polyfit(range(len(um_plot)), um_plot["SAMPLES_PROCESSED"], 1)
    p = np.poly1d(z)
    ax.plot(range(len(um_plot)), p(range(len(um_plot))),
            linestyle="--", linewidth=3, color=COLORS["neutral"], alpha=0.6, label="Overall trend")
    
    # Highlight concerning drops and add annotations
    label_offset = max(um_plot["SAMPLES_PROCESSED"]) * 0.08
    
    for i, (idx, row) in enumerate(um_plot.iterrows()):
        val = row["SAMPLES_PROCESSED"]
        mom = row["MOM_CHANGE_PCT"]
        
        if mom < -15:
            # Marker for significant drop
            ax.scatter(i, val, s=500, color=COLORS["danger"], zorder=5, 
                      edgecolor="white", linewidth=3, marker='v')
            ax.annotate(f"ALERT\n{mom:.1f}% drop",
                        xy=(i, val), xytext=(i, val + 250),
                        ha="center", fontsize=16, weight="bold", color=COLORS["danger"],
                        bbox=dict(boxstyle="round,pad=0.8", facecolor="white", 
                                 edgecolor=COLORS["danger"], linewidth=2.5),
                        arrowprops=dict(arrowstyle="->", color=COLORS["danger"], lw=3))
        else:
            # Show value for normal months
            ax.text(i, val + label_offset, f"{int(val):,}", ha="center", fontsize=16, weight="bold", color="black")
    
    ax.set_xticks(range(len(um_plot)))
    ax.set_xticklabels(um_plot["YEAR_MONTH_STR"], fontsize=16, weight="bold")
    ax.set_ylabel("Samples Processed", fontsize=16, weight="bold", color="black")
    ax.set_xlabel("Month", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Production Usage Trend - Monthly Live Samples Processed Over Time",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.set_ylim(0, um_plot["SAMPLES_PROCESSED"].max() * 1.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    # Add grid lines for better readability
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual2_mom_growth(df):
    """
    Visual 2: Month-over-Month Growth Rate
    
    Shows percentage change from one month to the next.
    Color-coded bars indicate growth, decline, or stability patterns.
    
    Why this visual:
    - Makes volatility immediately visible
    - Highlights months that exceed risk thresholds
    - Complements the trend chart by showing rate of change
    - Uses all samples (not just pass QC) to reflect actual customer usage
    """
    
    usage_monthly = (
        df.groupby("YEAR_MONTH").agg(
            SAMPLES_PROCESSED=("RUN_ID", "count"),
        ).sort_index()
    )
    usage_monthly["MOM_CHANGE_PCT"] = usage_monthly["SAMPLES_PROCESSED"].pct_change() * 100
    um_plot = usage_monthly.reset_index().copy()
    um_plot["YEAR_MONTH_STR"] = um_plot["YEAR_MONTH"].astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Color bars based on thresholds
    colors_bar = []
    for v in um_plot["MOM_CHANGE_PCT"].fillna(0):
        if v < -15:
            colors_bar.append(COLORS["danger"])
        elif v > 20:
            colors_bar.append(COLORS["success"])
        elif v > 0:
            colors_bar.append(COLORS["primary"])
        else:
            colors_bar.append(COLORS["warning"])
    
    bars = ax.bar(range(len(um_plot)), um_plot["MOM_CHANGE_PCT"].fillna(0), 
                  color=colors_bar, width=0.7, edgecolor='white', linewidth=2)
    
    # Add reference lines
    ax.axhline(y=0, color="black", linewidth=2)
    ax.axhline(y=-15, color=COLORS["danger"], linestyle="--", linewidth=2, alpha=0.5)
    ax.axhline(y=20, color=COLORS["success"], linestyle="--", linewidth=2, alpha=0.5)
    
    # Add value labels
    for i, v in enumerate(um_plot["MOM_CHANGE_PCT"].fillna(0)):
        if abs(v) > 2:
            y_pos = v + (8 if v > 0 else -8)
            ax.text(i, y_pos, f"{v:.0f}%", ha="center", fontsize=16, weight="bold",
                   color=colors_bar[i])
    
    # Add threshold labels
    ax.text(len(um_plot) - 0.5, -15, "-15% Risk Threshold", ha="right", va="bottom",
           fontsize=16, color=COLORS["danger"], weight="bold",
           bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8))
    ax.text(len(um_plot) - 0.5, 20, "+20% Strong Growth", ha="right", va="bottom",
           fontsize=16, color=COLORS["success"], weight="bold",
           bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8))
    
    ax.set_xticks(range(len(um_plot)))
    ax.set_xticklabels(um_plot["YEAR_MONTH_STR"], fontsize=16, weight="bold")
    ax.set_ylabel("Month-over-Month Change (%)", fontsize=16, weight="bold", color="black")
    ax.set_xlabel("Month", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Month-over-Month Growth Analysis - Significant Drops vs Strong Growth",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    # Add grid lines for better readability
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual3_success_rate(df):
    """
    Visual 3: Production Run Success Rate
    
    Shows the percentage of runs that successfully finished over time.
    Includes threshold lines for target (90%) and warning (80%) levels.
    
    Why this visual:
    - Separates operational quality from usage trends
    - High success rate indicates good service delivery
    - Low success rate could explain usage decline
    """
    
    success_monthly = df.groupby("YEAR_MONTH").agg(
        # df (from data_loader) uses RUN_ID as the run identifier, not ID
        TOTAL_RUNS=("RUN_ID", "count"),
        FINISHED=("OUTCOME", lambda s: (s == "finished").sum()),
        FAILED=("OUTCOME", lambda s: (s == "failed").sum()),
        CANCELED=("OUTCOME", lambda s: (s == "canceled").sum())
    )
    success_monthly["SUCCESS_RATE"] = (success_monthly["FINISHED"] / success_monthly["TOTAL_RUNS"] * 100)
    sr_plot = success_monthly.reset_index().copy()
    sr_plot["YEAR_MONTH_STR"] = sr_plot["YEAR_MONTH"].astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Success rate line
    ax.plot(range(len(sr_plot)), sr_plot["SUCCESS_RATE"],
            marker="s", markersize=14, linewidth=4, color=COLORS["success"],
            label="Success Rate", markeredgecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(sr_plot)), 0, sr_plot["SUCCESS_RATE"],
                     alpha=0.2, color=COLORS["success"])
    
    # Threshold lines
    ax.axhline(y=90, color=COLORS["success"], linestyle="--", linewidth=2, alpha=0.5, label="90% Target")
    ax.axhline(y=80, color=COLORS["warning"], linestyle="--", linewidth=2, alpha=0.5, label="80% Warning")
    
    # Value labels - positioned clearly to avoid overlap
    for i, v in enumerate(sr_plot["SUCCESS_RATE"]):
        color = COLORS["success"] if v >= 90 else COLORS["warning"] if v >= 80 else COLORS["danger"]
        y_offset = 3 if v < 95 else -3
        ax.text(i, v + y_offset, f"{v:.1f}%", 
               ha="center", fontsize=16, weight="bold", color=color,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor=color, linewidth=1))
    
    ax.set_xticks(range(len(sr_plot)))
    ax.set_xticklabels(sr_plot["YEAR_MONTH_STR"], fontsize=16, weight="bold")
    ax.set_ylabel("Success Rate (%)", fontsize=16, weight="bold", color="black")
    ax.set_xlabel("Month", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Production Run Success Rate Trend",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.set_ylim(0, 105)
    ax.legend(loc="lower right", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    # Add grid lines for better readability
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    plt.tight_layout()
    plt.show()


def visual4_health_summary(df):
    """
    Visual 4: Customer Health Summary
    
    Provides a comprehensive scorecard with key health metrics.
    Calculates an overall health score based on multiple factors.
    
    Why this visual:
    - Single-page summary for executives
    - Combines multiple metrics into actionable insight
    - Clear visual indication of risk level
    - Uses all samples (not just pass QC) to reflect actual customer usage
    """
    # Calculate metrics
    
    usage_monthly = (
        df.groupby("YEAR_MONTH").agg(
            SAMPLES_PROCESSED=("RUN_ID", "count"),
        ).sort_index()
    )
    usage_monthly["MOM_CHANGE_PCT"] = usage_monthly["SAMPLES_PROCESSED"].pct_change() * 100
    
    df["YEAR_MONTH"] = df["START_TIME"].dt.to_period("M")
    success_monthly = df.groupby("YEAR_MONTH").agg(
        # df (from data_loader) uses RUN_ID as the run identifier, not ID
        TOTAL_RUNS=("RUN_ID", "count"),
        FINISHED=("OUTCOME", lambda s: (s == "finished").sum()),
    )
    success_monthly["SUCCESS_RATE"] = (success_monthly["FINISHED"] / success_monthly["TOTAL_RUNS"] * 100)
    
    # Latest metrics
    last_month_usage = usage_monthly.iloc[-1]["SAMPLES_PROCESSED"]
    last_mom = usage_monthly.iloc[-1]["MOM_CHANGE_PCT"]
    last_success = success_monthly.iloc[-1]["SUCCESS_RATE"]
    
    # Trend analysis
    first_month = usage_monthly.iloc[0]["SAMPLES_PROCESSED"]
    total_growth = ((last_month_usage / first_month) - 1) * 100
    
    last_3_avg = usage_monthly["SAMPLES_PROCESSED"].tail(3).mean()
    first_3_avg = usage_monthly["SAMPLES_PROCESSED"].head(3).mean()
    trend_3m = ((last_3_avg - first_3_avg) / first_3_avg * 100) if first_3_avg > 0 else 0
    
    # Calculate health score
    risk_score = 0
    if last_mom < -15: risk_score += 40
    elif last_mom < 0: risk_score += 20
    if last_success < 80: risk_score += 30
    elif last_success < 90: risk_score += 15
    if trend_3m < -10: risk_score += 30
    
    health_score = 100 - risk_score
    
    if health_score >= 75:
        status = "HEALTHY"
        status_color = COLORS["success"]
    elif health_score >= 50:
        status = "AT RISK"
        status_color = COLORS["warning"]
    else:
        status = "CRITICAL"
        status_color = COLORS["danger"]
    
    # Create simple summary visual
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis("off")
    
    # Create metric boxes
    metrics = [
        ["Last Month Usage", f"{int(last_month_usage):,} samples", COLORS["primary"]],
        ["Month-over-Month", f"{last_mom:+.1f}%", 
         COLORS["danger"] if last_mom < -15 else COLORS["success"] if last_mom > 20 else COLORS["neutral"]],
        ["3-Month Trend", f"{trend_3m:+.1f}%", 
         COLORS["success"] if trend_3m > 0 else COLORS["danger"]],
        ["Success Rate", f"{last_success:.1f}%", 
         COLORS["success"] if last_success >= 90 else COLORS["warning"] if last_success >= 80 else COLORS["danger"]],
        ["Overall Growth", f"{total_growth:+.1f}%", 
         COLORS["success"] if total_growth > 0 else COLORS["danger"]],
        ["Health Score", f"{health_score}/100", status_color]
    ]
    
    # Draw metric boxes
    box_width = 0.28
    box_height = 0.25
    start_x = 0.1
    start_y = 0.6
    
    for idx, (label, value, color) in enumerate(metrics):
        row = idx // 3
        col = idx % 3
        x = start_x + col * 0.32
        y = start_y - row * 0.3
        
        # Box
        rect = Rectangle((x, y), box_width, box_height, 
                        facecolor=color, alpha=0.15, edgecolor=color, linewidth=3,
                        transform=ax.transAxes)
        ax.add_patch(rect)
        
        # Text
        ax.text(x + box_width/2, y + box_height * 0.65, value,
               ha="center", va="center", fontsize=16, weight="bold", color=color,
               transform=ax.transAxes)
        ax.text(x + box_width/2, y + box_height * 0.25, label,
               ha="center", va="center", fontsize=16, weight="bold",
               transform=ax.transAxes)
    
    # Health status
    ax.text(0.5, 0.25, f"CUSTOMER HEALTH: {status}",
           ha="center", va="center", fontsize=16, weight="bold", color=status_color,
           bbox=dict(boxstyle="round,pad=1", facecolor=status_color, alpha=0.2, 
                    edgecolor=status_color, linewidth=3),
           transform=ax.transAxes)
    
    ax.set_title("Scenario 2: Customer Health Summary", fontsize=16, weight="bold", pad=20, color="black", transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.show()

