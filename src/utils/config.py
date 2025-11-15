"""
Configuration and constants for the customer data analysis.

This module contains:
- Color scheme for consistent visualizations
- Matplotlib configuration settings
- Display options for pandas
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Global visual style - clean, presentation-ready
sns.set_style("white")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.color"] = "#f0f0f0"
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["grid.linewidth"] = 0.5
plt.rcParams["xtick.labelsize"] = 16
plt.rcParams["ytick.labelsize"] = 16
plt.rcParams["font.family"] = "sans-serif"

# Color palette for consistency across all visualizations
# Avoiding greens and solid reds to prevent misleading interpretations
COLORS = {
    "primary": "#0066CC",      # blue - expected/good
    "success": "#0084B8",      # teal/cyan - positive/healthy (replaced green)
    "warning": "#FF9900",      # orange - warning
    "danger": "#FF6B4A",       # coral/salmon - problem/overbilled (replaced solid red)
    "neutral": "#666666",      # gray - neutral
    "light": "#CCCCCC"         # light gray
}

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', '{:.2f}'.format)

