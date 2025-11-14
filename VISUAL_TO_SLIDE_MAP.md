# Visual to Slide Mapping Guide

## Quick Reference: Which Visual Goes Where

---

## SCENARIO 1: BILLING RECONCILIATION

### Slide 11: The Problem Statement
**Use:** Scenario 1 Visual 1 - The Billing Dispute (Executive Summary)
- **What it shows:** Side-by-side comparison of customer expectation vs actual invoice
- **Key message:** Customer is correct - 15.4% overbilling confirmed
- **Copy from:** Cell 10 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

### Slide 12: Monthly Billing Breakdown
**Use:** Scenario 1 Visual 2 - Monthly Billing Trend
- **What it shows:** Stacked bars showing expected (blue) vs overbilled (red) samples each month
- **Key message:** Overbilling is consistent across all months, not just August
- **Copy from:** Cell 7 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

### Slide 13: Sample Type Breakdown
**Use:** Scenario 1 Visual 3 - Sample Type Breakdown
- **What it shows:** Horizontal bars showing blood, saliva, bone marrow, and other samples
- **Key message:** Bone marrow is the main source of overbilling
- **Copy from:** Cell 8 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

### Slide 14: Root Cause Analysis
**Use:** Scenario 1 Visual 4 - Root Cause Analysis
- **What it shows:** Top workflows that are billing bone marrow samples
- **Key message:** These specific workflows need to be fixed
- **Copy from:** Cell 9 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

## SCENARIO 2: CUSTOMER HEALTH

### Slide 16: Customer Usage Trend
**Use:** Scenario 2 Visual 1 - Customer Usage Trend Over Time
- **What it shows:** Line chart with trend showing monthly billable samples, highlighting August drop
- **Key message:** Overall growth of 62.5%, but August shows significant decline
- **Copy from:** Cell 12 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

### Slide 17: Month-over-Month Growth Analysis
**Use:** Scenario 2 Visual 2 - Month-over-Month Growth Rate
- **What it shows:** Bar chart showing growth/decline percentages per month (color-coded)
- **Key message:** August drop (-18.8%) exceeds risk threshold (-15%)
- **Copy from:** Cell 13 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

### Slide 18: Production Run Success Rate
**Use:** Scenario 2 Visual 3 - Production Run Success Rate
- **What it shows:** Line chart showing success rate over time with target thresholds
- **Key message:** Service quality is good (high success rates), not causing decline
- **Copy from:** Cell 14 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

### Slide 19: Customer Health Summary
**Use:** Scenario 2 Visual 4 - Customer Health Summary
- **What it shows:** Summary dashboard with 6 key metrics and overall health status
- **Key message:** Health score: AT RISK - requires attention but overall trend positive
- **Copy from:** Cell 15 in main.ipynb
- **How to insert:** Right-click visual → Copy → Paste into slide

---

## HOW TO COPY VISUALS FROM JUPYTER

### Method 1: Direct Copy (Recommended)
1. Run the notebook cell containing the visual
2. Right-click on the visual/plot
3. Select "Copy Image" or "Save Image As"
4. Paste directly into PowerPoint/Google Slides

### Method 2: Screenshot
1. Run the notebook cell
2. Take a screenshot of the visual
3. Crop to remove notebook UI
4. Insert into presentation

### Method 3: Export to File
1. Modify the notebook cell to add:
   ```python
   plt.savefig('scenario1_visual1.png', dpi=300, bbox_inches='tight')
   ```
2. Insert the saved PNG file into presentation

---

## PRESENTATION TIPS

### Visual Sizing:
- Make visuals large (70-80% of slide)
- Leave space for 2-3 bullet points below
- Use consistent sizing across all slides

### Slide Layout:
```
┌─────────────────────────────┐
│   SLIDE TITLE               │
├─────────────────────────────┤
│                             │
│   [VISUAL - LARGE]          │
│                             │
│   • Key point 1             │
│   • Key point 2             │
│   • Key point 3             │
└─────────────────────────────┘
```

### Color Consistency:
- All visuals use the same color scheme
- Primary: Blue (#0066CC)
- Success: Green (#00AA55)
- Warning: Orange (#FF9900)
- Danger: Red (#DD3333)

### Text on Slides:
- Keep bullet points concise (5-7 words max)
- Let visuals tell the story
- Use visual annotations instead of separate text boxes when possible

---

## CELL LOCATIONS IN NOTEBOOK

| Visual | Cell Number | Visual Name |
|--------|-------------|-------------|
| S1-V1  | Cell 10     | Billing Dispute |
| S1-V2  | Cell 7      | Monthly Billing Trend |
| S1-V3  | Cell 8      | Sample Type Breakdown |
| S1-V4  | Cell 9      | Root Cause Analysis |
| S2-V1  | Cell 12     | Usage Trend |
| S2-V2  | Cell 13     | Growth Rate |
| S2-V3  | Cell 14     | Success Rate |
| S2-V4  | Cell 15     | Health Summary |

---

## VISUAL CHECKLIST

Before presenting, verify:

- [ ] All 8 visuals copied correctly
- [ ] Visuals are high resolution (300 DPI minimum)
- [ ] Text on visuals is readable
- [ ] Colors match presentation theme
- [ ] Visuals are properly sized on slides
- [ ] All annotations and labels are visible
- [ ] No overlapping text in visuals
- [ ] Consistent formatting across all slides

---

## BACKUP PLAN

If a visual doesn't copy well:

1. **Use screenshot method** - Always works
2. **Export as PNG** - Modify cell to save file
3. **Use PDF export** - Export notebook to PDF and extract images
4. **Re-run cell** - Sometimes re-executing fixes display issues

---

## PRESENTATION FLOW RECOMMENDATIONS

**Opening (Slides 1-3):**
- Set context
- Show executive summary with S1-V1
- Outline agenda

**Scenario 1 (Slides 4-8):**
- Tell the story: Problem → Data → Root Cause → Solution
- Use visuals in order: V1 → V2 → V3 → V4
- Build narrative progressively

**Scenario 2 (Slides 9-14):**
- Start with overall trend (V1)
- Show volatility (V2)
- Address quality (V3)
- Summarize health (V4)

**Closing (Slides 15-18):**
- Reinforce key messages
- Provide clear action items
- Leave time for questions

---

## TIME ALLOCATION PER SLIDE

- **Title/Agenda:** 30 seconds each
- **Visual slides:** 1-2 minutes each
- **Recommendation slides:** 1 minute each
- **Conclusion:** 2 minutes
- **Q&A:** 5-10 minutes

**Total: 15-20 minutes**

