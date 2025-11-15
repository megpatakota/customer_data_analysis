"""
Scenario 1: Deep Investigation Visualizations.

Visuals to investigate why bone marrow is in LIVE workflows.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..utils.config import COLORS


def visual8_bone_marrow_workflow_investigation(investigation_results):
    """
    Visual 8: Bone Marrow Workflow Investigation
    
    Shows which workflows are processing bone marrow and their characteristics.
    """
    if 'workflows_processing_bm' not in investigation_results:
        print("No bone marrow investigation data available.")
        return
    
    bm_workflows = investigation_results['workflows_processing_bm'].copy()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Top workflows by bone marrow volume
    top_workflows = bm_workflows.nlargest(8, 'BONE_MARROW_COUNT').copy()
    y_pos = np.arange(len(top_workflows))
    
    # Use WORKFLOW_NAME column if it exists, otherwise use index
    if 'WORKFLOW_NAME' in top_workflows.columns:
        workflow_names = top_workflows['WORKFLOW_NAME'].values
    else:
        workflow_names = top_workflows.index.values
    
    ax1.barh(y_pos, top_workflows['BONE_MARROW_COUNT'], color=COLORS['danger'], edgecolor='white', linewidth=1.5)
    ax1.set_yticks(y_pos)
    workflow_labels = [name[:50] + '...' if len(str(name)) > 50 else str(name) for name in workflow_names]
    ax1.set_yticklabels(workflow_labels, fontsize=16)
    ax1.set_xlabel("Bone Marrow Samples", fontsize=16, weight="bold", color="black")
    ax1.set_title("Top Workflows Processing Bone Marrow", fontsize=16, weight="bold", color="black")
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_axisbelow(True)
    ax1.grid(True, which='major', axis='x', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # Add value labels
    for i, v in enumerate(top_workflows['BONE_MARROW_COUNT']):
        ax1.text(v + max(top_workflows['BONE_MARROW_COUNT']) * 0.02, i, f"{int(v)}", 
                va="center", fontsize=16, weight="bold", color="black")
    
    # 2. Bone marrow timeline
    if 'bm_timeline' in investigation_results:
        bm_timeline = investigation_results['bm_timeline']
        bm_timeline.index = bm_timeline.index.astype(str)
        
        ax2.bar(range(len(bm_timeline)), bm_timeline.values, color=COLORS['danger'], edgecolor='white', linewidth=1.5)
        ax2.set_xticks(range(len(bm_timeline)))
        ax2.set_xticklabels(bm_timeline.index, rotation=45, ha='right', fontsize=16)
        ax2.set_ylabel("Bone Marrow Samples", fontsize=16, weight="bold", color="black")
        ax2.set_xlabel("Month", fontsize=16, weight="bold", color="black")
        ax2.set_title("Bone Marrow Processing Timeline", fontsize=16, weight="bold", color="black")
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.set_axisbelow(True)
        ax2.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # 3. Workflow type comparison
    if 'bm_workflow_types' in investigation_results and 'non_bm_workflow_types' in investigation_results:
        bm_types = investigation_results['bm_workflow_types']
        non_bm_types = investigation_results['non_bm_workflow_types']
        
        all_types = set(bm_types.index) | set(non_bm_types.index)
        bm_counts = [bm_types.get(t, 0) for t in all_types]
        non_bm_counts = [non_bm_types.get(t, 0) for t in all_types]
        
        x = np.arange(len(all_types))
        width = 0.35
        
        ax3.bar(x - width/2, bm_counts, width, label='With Bone Marrow', color=COLORS['danger'], edgecolor='white', linewidth=1.5)
        ax3.bar(x + width/2, non_bm_counts, width, label='Without Bone Marrow', color=COLORS['primary'], edgecolor='white', linewidth=1.5)
        ax3.set_xticks(x)
        ax3.set_xticklabels(all_types, rotation=45, ha='right', fontsize=16)
        ax3.set_ylabel("Number of Workflows", fontsize=16, weight="bold", color="black")
        ax3.set_title("Workflow Types: With vs Without Bone Marrow", fontsize=16, weight="bold", color="black")
        ax3.legend(loc="upper left", frameon=True, fontsize=16)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.set_axisbelow(True)
        ax3.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    # 4. QC comparison
    if 'bm_qc_distribution' in investigation_results and 'blood_saliva_qc_distribution' in investigation_results:
        bm_qc = investigation_results['bm_qc_distribution']
        bs_qc = investigation_results['blood_saliva_qc_distribution']
        
        # Calculate percentages
        bm_qc_pct = (bm_qc / bm_qc.sum() * 100).round(1)
        bs_qc_pct = (bs_qc / bs_qc.sum() * 100).round(1)
        
        all_qc = set(bm_qc_pct.index) | set(bs_qc_pct.index)
        x = np.arange(len(all_qc))
        width = 0.35
        
        bm_vals = [bm_qc_pct.get(qc, 0) for qc in all_qc]
        bs_vals = [bs_qc_pct.get(qc, 0) for qc in all_qc]
        
        ax4.bar(x - width/2, bm_vals, width, label='Bone Marrow', color=COLORS['danger'], edgecolor='white', linewidth=1.5)
        ax4.bar(x + width/2, bs_vals, width, label='Blood/Saliva', color=COLORS['primary'], edgecolor='white', linewidth=1.5)
        ax4.set_xticks(x)
        ax4.set_xticklabels(all_qc, fontsize=16)
        ax4.set_ylabel("Percentage (%)", fontsize=16, weight="bold", color="black")
        ax4.set_title("QC Check Distribution Comparison", fontsize=16, weight="bold", color="black")
        ax4.legend(loc="upper left", frameon=True, fontsize=16)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.set_axisbelow(True)
        ax4.grid(True, which='major', axis='y', alpha=0.5, color='#cccccc', linewidth=1.0, linestyle='-', zorder=0)
    
    fig.suptitle("Scenario 1: Deep Investigation - Why is Bone Marrow in LIVE Workflows?",
                 fontsize=16, weight="bold", color="black", y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.show()


def visual9_workflow_sample_type_matrix(checks_live_success):
    """
    Visual 9: Workflow-Sample Type Matrix
    
    Shows which workflows process which sample types - reveals patterns.
    """
    # Create matrix of workflows vs sample types
    workflow_sample_matrix = pd.crosstab(
        checks_live_success['WORKFLOW_NAME'],
        checks_live_success['SAMPLE_TYPE'],
        margins=True
    )
    
    # Remove the 'All' row and column for visualization
    matrix_viz = workflow_sample_matrix.iloc[:-1, :-1]
    
    fig, ax = plt.subplots(figsize=(14, max(8, len(matrix_viz) * 0.4)))
    
    # Create heatmap
    im = ax.imshow(matrix_viz.values, cmap='YlOrRd', aspect='auto', vmin=0)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(matrix_viz.columns)))
    ax.set_yticks(np.arange(len(matrix_viz.index)))
    ax.set_xticklabels(matrix_viz.columns, rotation=45, ha='right', fontsize=16)
    
    # Truncate workflow names for display
    workflow_labels = [name[:40] + '...' if len(name) > 40 else name for name in matrix_viz.index]
    ax.set_yticklabels(workflow_labels, fontsize=16)
    
    # Add text annotations
    for i in range(len(matrix_viz.index)):
        for j in range(len(matrix_viz.columns)):
            value = matrix_viz.iloc[i, j]
            if value > 0:
                text_color = 'white' if value > matrix_viz.values.max() * 0.5 else 'black'
                ax.text(j, i, int(value), ha="center", va="center",
                       color=text_color, fontsize=16, weight="bold")
    
    ax.set_xlabel("Sample Type", fontsize=16, weight="bold", color="black")
    ax.set_ylabel("Workflow Name", fontsize=16, weight="bold", color="black")
    ax.set_title("Scenario 1: Workflow-Sample Type Processing Matrix\n(Shows which workflows process which sample types)",
                 fontsize=16, weight="bold", pad=20, color="black")
    
    plt.colorbar(im, ax=ax, label='Number of Samples')
    plt.tight_layout()
    plt.show()

