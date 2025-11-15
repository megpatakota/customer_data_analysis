"""
Scenario 2: Real-World Customer Health Metrics Visualizations.

Visuals based on real-world customer success and account management metrics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ..utils.config import COLORS


def visual9_customer_health_dashboard(health_metrics):
    """
    Visual 9: Comprehensive Customer Health Dashboard
    
    Real-world metrics dashboard used in customer success.
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Churn Risk Indicator (Top Left)
    ax1 = fig.add_subplot(gs[0, 0])
    risk_level = health_metrics['churn_risk']['risk_level']
    risk_colors = {'HIGH': COLORS['danger'], 'MEDIUM': COLORS['warning'], 'LOW': COLORS['success']}
    risk_color = risk_colors.get(risk_level, COLORS['neutral'])
    
    ax1.text(0.5, 0.6, risk_level, ha='center', va='center', fontsize=16, weight='bold',
            color=risk_color, transform=ax1.transAxes)
    ax1.text(0.5, 0.3, 'CHURN RISK', ha='center', va='center', fontsize=16, weight='bold',
            color='black', transform=ax1.transAxes)
    ax1.text(0.5, 0.1, f"{health_metrics['churn_risk']['consecutive_monthly_declines']} consecutive declines",
            ha='center', va='center', fontsize=16, color='black', transform=ax1.transAxes)
    ax1.add_patch(Rectangle((0.1, 0.1), 0.8, 0.7, fill=False, edgecolor=risk_color, 
                           linewidth=3, transform=ax1.transAxes))
    ax1.axis('off')
    
    # 2. Growth Velocity (Top Middle)
    ax2 = fig.add_subplot(gs[0, 1])
    growth = health_metrics['growth']
    if growth['recent_growth_pct'] is not None:
        growth_val = growth['recent_growth_pct']
        growth_color = COLORS['success'] if growth_val > 0 else COLORS['danger'] if growth_val < -10 else COLORS['warning']
        ax2.text(0.5, 0.6, f"{growth_val:+.1f}%", ha='center', va='center', fontsize=16, weight='bold',
                color=growth_color, transform=ax2.transAxes)
        ax2.text(0.5, 0.3, 'RECENT GROWTH', ha='center', va='center', fontsize=16, weight='bold',
                color='black', transform=ax2.transAxes)
        ax2.text(0.5, 0.1, growth['growth_trajectory'], ha='center', va='center', fontsize=16,
                color='black', transform=ax2.transAxes)
    else:
        ax2.text(0.5, 0.5, 'INSUFFICIENT\nDATA', ha='center', va='center', fontsize=16, weight='bold',
                color=COLORS['neutral'], transform=ax2.transAxes)
    ax2.axis('off')
    
    # 3. Operational Health (Top Right)
    ax3 = fig.add_subplot(gs[0, 2])
    op_health = health_metrics['operational_health']
    if op_health['latest_success_rate'] is not None:
        success_rate = op_health['latest_success_rate']
        success_color = COLORS['success'] if success_rate >= 90 else COLORS['warning'] if success_rate >= 80 else COLORS['danger']
        ax3.text(0.5, 0.6, f"{success_rate:.1f}%", ha='center', va='center', fontsize=16, weight='bold',
                color=success_color, transform=ax3.transAxes)
        ax3.text(0.5, 0.3, 'SUCCESS RATE', ha='center', va='center', fontsize=16, weight='bold',
                color='black', transform=ax3.transAxes)
        ax3.text(0.5, 0.1, op_health['operational_status'], ha='center', va='center', fontsize=16,
                color='black', transform=ax3.transAxes)
    else:
        ax3.text(0.5, 0.5, 'NO DATA', ha='center', va='center', fontsize=16, weight='bold',
                color=COLORS['neutral'], transform=ax3.transAxes)
    ax3.axis('off')
    
    # 4. Engagement Metrics (Middle Left)
    ax4 = fig.add_subplot(gs[1, 0])
    engagement = health_metrics['engagement']
    ax4.barh(['Active\nWorkflows', 'Total\nWorkflows'], 
            [engagement['active_workflows'], engagement['total_workflows']],
            color=[COLORS['primary'], COLORS['neutral']], edgecolor='white', linewidth=2)
    ax4.set_xlabel("Count", fontsize=16, weight="bold", color="black")
    ax4.set_title("Workflow Engagement", fontsize=16, weight="bold", color="black")
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.set_axisbelow(True)
    ax4.grid(True, which='major', axis='x', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # 5. Usage Concentration (Middle)
    ax5 = fig.add_subplot(gs[1, 1])
    concentration = health_metrics['concentration']
    categories = ['Top Workflow', 'Top 3 Workflows']
    values = [concentration['top_workflow_pct'], concentration['top_3_workflows_pct']]
    colors_bar = [COLORS['danger'] if v > 50 else COLORS['warning'] if v > 30 else COLORS['success'] for v in values]
    
    bars = ax5.barh(categories, values, color=colors_bar, edgecolor='white', linewidth=2)
    ax5.set_xlabel("Percentage of Total Usage", fontsize=16, weight="bold", color="black")
    ax5.set_title("Usage Concentration Risk", fontsize=16, weight="bold", color="black")
    ax5.set_xlim(0, 100)
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    ax5.set_axisbelow(True)
    ax5.grid(True, which='major', axis='x', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax5.text(val + 2, i, f"{val:.1f}%", va="center", fontsize=16, weight="bold", color="black")
    
    # 6. Platform Maturity (Middle Right)
    ax6 = fig.add_subplot(gs[1, 2])
    maturity = health_metrics['maturity']
    if maturity['avg_workflow_age_days'] is not None:
        age_days = maturity['avg_workflow_age_days']
        maturity_levels = ['New\n(<30 days)', 'Growing\n(30-90 days)', 'Mature\n(>90 days)']
        maturity_counts = [
            maturity['new_workflows_count'],
            maturity['established_workflows_count'] - len([x for x in [maturity['new_workflows_count']] if x > 0]),
            len([x for x in [maturity['established_workflows_count']] if x > 0])
        ]
        # Simplified for visualization
        ax6.pie([maturity['new_workflows_count'], maturity['established_workflows_count']],
               labels=['New', 'Established'], autopct='%1.0f', startangle=90,
               colors=[COLORS['warning'], COLORS['success']])
        ax6.set_title("Platform Maturity", fontsize=16, weight="bold", color="black")
    else:
        ax6.text(0.5, 0.5, 'NO DATA', ha='center', va='center', fontsize=16, weight='bold',
                color=COLORS['neutral'], transform=ax6.transAxes)
        ax6.axis('off')
    
    # 7. Key Metrics Summary (Bottom - Full Width)
    ax7 = fig.add_subplot(gs[2, :])
    ax7.axis('off')
    
    recent_growth = f"{health_metrics['growth']['recent_growth_pct']:+.1f}%" if health_metrics['growth']['recent_growth_pct'] is not None else 'N/A'
    success_rate = f"{health_metrics['operational_health']['latest_success_rate']:.1f}%" if health_metrics['operational_health']['latest_success_rate'] is not None else 'N/A'
    
    metrics_text = f"""
    CHURN RISK: {health_metrics['churn_risk']['risk_level']} | 
    RECENT GROWTH: {recent_growth} | 
    SUCCESS RATE: {success_rate} | 
    WORKFLOW UTILIZATION: {health_metrics['engagement']['workflow_utilization_pct']:.1f}% | 
    CONCENTRATION RISK: {health_metrics['concentration']['concentration_risk']} | 
    MATURITY: {health_metrics['maturity']['maturity_level']}
    """
    
    ax7.text(0.5, 0.5, metrics_text, ha='center', va='center', fontsize=16, weight='bold',
            color='black', transform=ax7.transAxes, family='monospace')
    
    fig.suptitle("Scenario 2: Real-World Customer Health Dashboard", fontsize=16, weight="bold", 
                color="black", y=0.98)
    plt.show()


def visual10_churn_risk_timeline(usage_live, health_metrics):
    """
    Visual 10: Churn Risk Timeline
    
    Shows usage trends with churn risk indicators.
    """
    usage_live_copy = usage_live.copy()
    usage_live_copy["YEAR_MONTH"] = usage_live_copy["TIMESTAMP"].dt.to_period("M")
    
    monthly = usage_live_copy.groupby("YEAR_MONTH").agg(
        SAMPLES=("RUN_ID", "count")
    ).sort_index()
    monthly["MOM_CHANGE"] = monthly["SAMPLES"].pct_change() * 100
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = range(len(monthly))
    monthly_str = monthly.index.astype(str)
    
    # Plot usage with color coding based on change
    colors_line = []
    for change in monthly["MOM_CHANGE"].fillna(0):
        if change < -15:
            colors_line.append(COLORS['danger'])
        elif change < 0:
            colors_line.append(COLORS['warning'])
        elif change > 20:
            colors_line.append(COLORS['success'])
        else:
            colors_line.append(COLORS['primary'])
    
    # Main line
    ax.plot(x, monthly["SAMPLES"], marker='o', markersize=12, linewidth=3, 
           color=COLORS['primary'], markeredgecolor='white', markeredgewidth=2, zorder=3)
    
    # Highlight risk periods
    for i, (idx, row) in enumerate(monthly.iterrows()):
        change = row["MOM_CHANGE"]
        if pd.notna(change) and change < -15:
            ax.scatter(i, row["SAMPLES"], s=400, color=COLORS['danger'], 
                      zorder=5, edgecolor='white', linewidth=3, marker='v')
            ax.annotate(f"RISK\n{change:.1f}%", xy=(i, row["SAMPLES"]), 
                       xytext=(i, row["SAMPLES"] + max(monthly["SAMPLES"]) * 0.1),
                       ha="center", fontsize=16, weight="bold", color=COLORS['danger'],
                       bbox=dict(boxstyle="round,pad=0.6", facecolor="white", 
                               edgecolor=COLORS['danger'], linewidth=2.5),
                       arrowprops=dict(arrowstyle="->", color=COLORS['danger'], lw=2))
    
    # Add threshold lines
    ax.axhline(y=monthly["SAMPLES"].mean(), color=COLORS['neutral'], linestyle='--', 
              linewidth=2, alpha=0.7, label='Average Usage', zorder=1)
    
    ax.set_xticks(x)
    ax.set_xticklabels(monthly_str, rotation=45, ha='right', fontsize=16, weight="bold")
    ax.set_ylabel("Samples Processed", fontsize=16, weight="bold", color="black")
    ax.set_xlabel("Month", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 2: Churn Risk Timeline - Usage Trends with Risk Indicators",
                 fontsize=16, weight="bold", pad=20, color="black")
    ax.legend(loc="upper left", frameon=True, fontsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_axisbelow(True)
    ax.grid(True, which='major', axis='both', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # Add risk level annotation
    risk_level = health_metrics['churn_risk']['risk_level']
    risk_color = COLORS['danger'] if risk_level == 'HIGH' else COLORS['warning'] if risk_level == 'MEDIUM' else COLORS['success']
    ax.text(0.02, 0.98, f"Current Risk Level: {risk_level}", transform=ax.transAxes,
           fontsize=16, weight="bold", color=risk_color, va='top',
           bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=risk_color, linewidth=2))
    
    plt.tight_layout()
    plt.show()

