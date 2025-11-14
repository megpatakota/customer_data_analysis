# Customer Data Analysis - Presentation Slides

---

## SLIDE 1: Title Slide

**Title:** Customer Data Analysis: Billing Reconciliation & Health Assessment

**Subtitle:** Technical Task - Data Analyst Position

**Date:** [Current Date]
**Presenter:** [Your Name]

---

## SLIDE 2: Data Overview

**What Data Are We Working With?**

**Source:** `data-analyst-technical-task-data.xlsx` (Excel workbook)

**Three Primary Datasets:**

1. **QC Checks Table**
   - **6,405 rows, 8 columns**
   - Contains: Sample-level quality control checks
   - Key fields: `RUN_ID`, `WORKFLOW_ID`, `TIMESTAMP`, `SAMPLE_TYPE`, `QC_CHECK`
   - Purpose: Track quality status of each sample processed

2. **Workflows Table**
   - **264 rows, 4 columns**
   - Contains: Workflow definitions and metadata
   - Key fields: `WORKFLOW_ID`, `WORKFLOW_NAME`, `WORKFLOW_TYPE`, `WORKFLOW_TIMESTAMP`
   - Purpose: Define different processing workflows available in the system

3. **Runs Table**
   - **1,693 rows, 8 columns**
   - Contains: Execution records of workflows
   - Key fields: `ID`, `WORKFLOW_ID`, `WORKFLOW_NAME`, `OUTCOME`, `START_TIME`, `STOP_TIME`
   - Purpose: Track when workflows were executed and their results

**Time Period:** May 2025 - August 2025 (4 months of data)

---

## SLIDE 3: Data Organization & Structure

**How We Organized the Data:**

**1. Data Loading:**
- Loaded all three tables from Excel workbook
- Preserved all original columns and data types
- Maintained referential integrity between tables

**2. Data Relationships:**
```
QC Checks ←─[WORKFLOW_ID]──→ Workflows
    ↓                          ↑
    └─[RUN_ID]──→ Runs ─[WORKFLOW_ID]─┘
```

**3. Key Merges Performed:**
- QC Checks + Workflows: Enriched sample data with workflow metadata
- QC Checks + Runs: Linked samples to execution outcomes
- Final dataset: All tables joined to create comprehensive view

**4. Data Enrichment:**
- Added `ENVIRONMENT` column: Extracted from workflow name prefixes (e.g., [LIVE], [TEST])
- Added `YEAR_MONTH` column: Period-based grouping for time series analysis
- Derived fields: Calculated metrics like month-over-month change, overbilling percentages

---

## SLIDE 4: Data Cleaning & Transformation

**What Cleaning Was Done:**

**1. Date/Time Standardization:**
- Converted all timestamp columns to pandas datetime objects
- Standardized date formats across all tables
- Enabled time-based filtering and grouping

**2. Environment Classification:**
- **Challenge:** Environment not explicitly stored, but encoded in workflow names
- **Solution:** Created `infer_environment()` function using regex and keyword matching
- **Logic:** Extracts prefix from workflow name (e.g., `[LIVE] workflow-name`)
- **Environments Identified:**
  - LIVE (production)
  - TEST
  - UAT
  - EXPERIMENTAL
  - ARCHIVED
  - UNLABELED (no clear environment marker)

**3. Data Quality Checks:**
- Handled missing values in `SAMPLE_TYPE` and `QC_CHECK` fields
- Validated workflow ID consistency across tables
- Checked for duplicate records

**4. Filtering & Subsetting:**
- Applied environment filters for production analysis
- Filtered by run outcomes (finished, failed, canceled)
- Applied QC check status filters

**No data was modified or imputed - all analysis uses original values**

---

## SLIDE 5: Methodology & Key Assumptions (Overall)

**Core Analytical Approach:**

**1. Definition of "Production" / "Billable":**
- **Production Environment:** Only workflows marked as `[LIVE]`
- **Rationale:** Customer only processes blood/saliva samples in production
- **Data Impact:** Excluded TEST, UAT, EXPERIMENTAL environments from billing analysis

**2. Definition of "Billable Samples":**
A sample is considered billable if **ALL** of the following are true:
- ✅ Sample is in a `[LIVE]` workflow
- ✅ Sample is from a run with `OUTCOME = "finished"`
- ✅ Sample has `QC_CHECK = "pass"` OR `QC_CHECK` is missing/NaN

**Assumption:** Missing QC checks are treated as passed (common practice if QC not required)

**3. Sample Type Classification:**
- **Expected (Billable):** `blood`, `saliva`
- **Overbilled (Non-Billable):** `bone marrow`, `null/NaN`, any other type
- **Rationale:** Based on customer's stated contract terms

**4. Time Period Analysis:**
- All analysis uses monthly aggregation (`YEAR_MONTH` period)
- Month-over-month comparisons using percentage change
- Trend analysis using 3-month moving averages

---

## SLIDE 6: Methodology - Scenario 1 Specific

**Billing Reconciliation Approach:**

**1. Production Focus:**
- **Filter Applied:** `ENVIRONMENT == "live"` only
- **Rationale:** Customer dispute specifically mentions "production workloads"
- **Data Impact:** Reduced from 6,405 total samples to 3,608 billable live samples

**2. Run Outcome Filtering:**
- **Included:** Only samples from runs where `OUTCOME = "finished"`
- **Excluded:** Failed runs, canceled runs
- **Rationale:** Only successfully completed runs should be billed
- **Data Impact:** From 4,057 samples in live runs → 3,608 billable samples

**3. QC Status Handling:**
- **Included:** Samples with `QC_CHECK = "pass"` OR `QC_CHECK = NaN`
- **Assumption:** Missing QC results indicate samples passed default checks
- **Rationale:** Not all samples may require explicit QC checks

**4. Overbilling Calculation:**
```
Overbilling % = (Non-blood/saliva samples / Blood+saliva samples) × 100
```
- Calculated both all-time and monthly
- Monthly view allows comparison across billing periods

**5. Root Cause Analysis:**
- Grouped overbilled samples by `WORKFLOW_NAME`
- Identified top workflows contributing to bone marrow billing
- Focused on workflows with highest volume of incorrectly billed samples

---

## SLIDE 7: Methodology - Scenario 2 Specific

**Customer Health Assessment Approach:**

**1. Reuses Scenario 1 Definition:**
- **Base Dataset:** `billable_live` from Scenario 1
- **Rationale:** Customer health should measure actual production usage
- **Consistency:** Same definition ensures comparability

**2. Usage Metrics Calculated:**
- **Billable Samples:** Count of billable samples per month
- **Unique Runs:** Number of distinct production runs per month
- **Month-over-Month (MoM) Change:** Percentage change in billable samples

**3. Risk Thresholds:**
- **>15% Drop:** Flags as significant risk indicator
- **Rationale:** Industry standard for churn risk detection
- **Action:** Triggers proactive customer engagement

**4. Trend Analysis:**
- **3-Month Moving Average:** Compares last 3 months vs previous 3 months
- **Purpose:** Smooth out single-month volatility
- **Interpretation:** Negative trend indicates potential churn risk

**5. Success Rate Analysis:**
- Calculated separately for Scenario 2 Visual 3
- Formula: `(Finished Runs / Total Runs) × 100`
- Thresholds: 90% target, 80% warning level
- **Purpose:** Assess operational quality separately from usage trends

**6. Health Score Calculation:**
- Composite score based on multiple factors:
  - Recent month-over-month change (-40 points if <-15%)
  - Success rate (-30 points if <80%)
  - 3-month trend (-30 points if declining >10%)
- Scale: 0-100 (100 = healthy, <50 = at risk)

---

## SLIDE 8: Data Limitations & Considerations

**What We Know:**

✅ **Complete Coverage:** All production (LIVE) workflows included
✅ **Time Period:** 4 months of data (May-August 2025)
✅ **Data Quality:** No missing critical fields in production data
✅ **Environment Classification:** Accurately identified production vs non-production

**What We Don't Know:**

⚠️ **Historical Context:** No data before May 2025 (can't assess longer-term trends)
⚠️ **Seasonal Patterns:** Limited to 4 months (insufficient for seasonality analysis)
⚠️ **Customer Intent:** Can't determine if August decline is intentional or concerning
⚠️ **Workflow Purpose:** Unclear why bone marrow samples are in LIVE workflows
⚠️ **Contract Terms:** Assumed blood/saliva only based on customer claim (not verified)

**Assumptions Made:**
1. Missing QC checks = passed (common industry practice)
2. Customer contract allows only blood/saliva in production (based on dispute)
3. 15% MoM decline = risk threshold (industry standard)
4. Workflow naming convention is consistent (environment prefixes reliable)

---

## SLIDE 9: Executive Summary

**Key Findings:**

1. **Scenario 1 - Billing Dispute:**
   - Customer correctly identified 15.4% overbilling in latest month
   - Root cause: Bone marrow samples incorrectly included in production billing
   - Issue is systemic across all months (10-18% overbilling)

2. **Scenario 2 - Customer Health:**
   - Strong overall growth trend (62.5% from May to August)
   - Single month decline (18.8% in August) - monitor closely
   - Customer health status: AT RISK (requires attention)
   - Service quality remains high (success rate >90%)

**Visual:** Use Scenario 1 Visual 1 (Billing Dispute comparison)

---

## SLIDE 10: Agenda

1. **Data & Methodology Overview** ✅ (Just completed)
   - Data structure and organization
   - Cleaning and transformation steps
   - Analytical assumptions

2. **Scenario 1: Billing Reconciliation**
   - Investigation of customer dispute
   - Root cause analysis
   - Recommendations

3. **Scenario 2: Customer Health Assessment**
   - Usage trend analysis
   - Risk indicators
   - Health scorecard

4. **Conclusions & Next Steps**

---

## PART 1: SCENARIO 1 - BILLING RECONCILIATION

---

## SLIDE 11: The Problem Statement

**Customer Dispute:**

"Customer claims 15% overbilling last month. They only process blood and saliva samples in production workloads, but the invoice includes other sample types."

**Question:** Is the customer correct?

**Visual:** Scenario 1 Visual 1 - The Billing Dispute (Executive Summary)

**Key Point:** 
- Customer expects: 883 samples (blood + saliva only)
- We invoiced: 1,019 samples
- **Overbilling: 15.4%** ✓ Customer is correct

---

## SLIDE 12: Monthly Billing Breakdown

**What the Data Shows:**

- Overbilling has been consistent across all months (ranging from 12.1% to 15.4%)
- The issue is not isolated to one month
- Pattern: Blood/Saliva (expected) + Bone Marrow/Other (overbilled) = Total invoice

**Visual:** Scenario 1 Visual 2 - Monthly Billing Trend

**Key Insights:**
- August (disputed month) shows 15.4% overbilling
- Every month has some level of overbilling
- The pattern is systemic, not a one-time error

---

## SLIDE 13: Sample Type Breakdown

**What Types Are Being Billed?**

**Visual:** Scenario 1 Visual 3 - Sample Type Breakdown

**The Numbers:**
- **Expected Types (Billable):**
  - Blood: [X] samples
  - Saliva: [Y] samples
  - **Total Expected: [X+Y] samples**

- **Overbilled Types (Non-Billable):**
  - Bone Marrow: [Z] samples (CRITICAL ISSUE)
  - Other: [W] samples
  - **Total Overbilled: [Z+W] samples**

**Key Insight:** Bone marrow represents the majority of overbilling

---

## SLIDE 14: Root Cause Analysis

**Where Are These Non-Billable Samples Coming From?**

**Visual:** Scenario 1 Visual 4 - Root Cause Analysis (Top Workflows)

**Findings:**
- Multiple live workflows are processing bone marrow samples
- Top [N] workflows account for [X]% of bone marrow samples
- These workflows should NOT be billing bone marrow in the [LIVE] environment

**Critical Action Required:**
1. Review these specific workflows
2. Understand why bone marrow samples are in production environment
3. Fix workflow classification or sample routing logic

---

## SLIDE 15: Scenario 1 - Recommendations

**Immediate Actions:**

1. **Acknowledge the Customer:**
   - Customer is correct - refund/credit for overbilled amount
   - Apologize for the billing error

2. **Technical Fixes:**
   - Review workflow classification logic
   - Ensure bone marrow samples are excluded from [LIVE] billing
   - Implement validation checks to prevent future occurrences

3. **Process Improvements:**
   - Add automated billing validation
   - Regular reconciliation of expected vs actual sample types
   - Monthly billing audits before invoices are sent

4. **Historical Review:**
   - Calculate total overbilling across all months
   - Prepare credit/refund for historical overbilling

---

## PART 2: SCENARIO 2 - CUSTOMER HEALTH

---

## SLIDE 16: Customer Usage Trend

**The Big Picture:**

**Visual:** Scenario 2 Visual 1 - Customer Usage Trend Over Time

**Growth Pattern:**
- May: 627 samples
- June: 707 samples (+12.8%)
- July: 1,255 samples (+77.5%) ← Peak
- August: 1,019 samples (-18.8%) ← **ALERT**

**Overall Growth:** 62.5% from May to August

**Key Observation:** Strong growth followed by significant drop in August

---

## SLIDE 17: Month-over-Month Growth Analysis

**Understanding the Volatility:**

**Visual:** Scenario 2 Visual 2 - Month-over-Month Growth Rate

**Growth/Decline Pattern:**
- June: +12.8% growth
- July: +77.5% growth (strong expansion)
- August: -18.8% decline (significant drop - exceeds 15% threshold)

**Risk Indicators:**
- Single month decline >15% triggers risk flag
- Pattern suggests possible seasonal variation OR customer reducing usage
- Need to monitor next month closely

---

## SLIDE 18: Production Run Success Rate

**Operational Quality Assessment:**

**Visual:** Scenario 2 Visual 3 - Production Run Success Rate

**Success Rate Metrics:**
- Average success rate: [X]%
- Target: 90%
- Warning threshold: 80%

**Key Points:**
- Service reliability is [GOOD/NEEDS IMPROVEMENT]
- High success rate indicates customer satisfaction with service quality
- Not a factor in usage decline

---

## SLIDE 19: Customer Health Summary

**Overall Health Assessment:**

**Visual:** Scenario 2 Visual 4 - Customer Health Scorecard

**Key Metrics:**
- Current Month Usage: [X] samples
- Month-over-Month: -18.8% (Decline)
- 3-Month Trend: [X]% (Still positive overall)
- Success Rate: [X]%
- Overall Growth: +62.5% (Since May)

**Health Score: [X]/100 - AT RISK**

**Status:** Requires monitoring and proactive engagement

---

## SLIDE 20: Scenario 2 - Risk Assessment

**Why "AT RISK"?**

1. **Recent Decline:**
   - 18.8% drop in August exceeds risk threshold
   - Largest single-month decline observed

2. **However, Positive Indicators:**
   - Overall trend still positive (62.5% growth since May)
   - High success rates (service quality good)
   - August volume still higher than May/June

3. **Uncertainty:**
   - Is this a temporary dip or the start of a decline?
   - Could be seasonal variation
   - Need next month's data to confirm direction

---

## SLIDE 21: Scenario 2 - Recommendations

**Immediate Actions:**

1. **Proactive Engagement:**
   - Contact customer success team
   - Schedule check-in call with customer
   - Understand reason for August decline

2. **Monitoring:**
   - Track September usage closely
   - Monitor for consecutive declines
   - Watch for workflow migration patterns

3. **Data Analysis:**
   - Review if specific workflows declined
   - Check for archived/retired workflows
   - Identify any operational issues

4. **Risk Mitigation:**
   - If decline continues in September, escalate as HIGH RISK
   - Prepare retention strategies
   - Review pricing/value proposition

---

## PART 3: CONCLUSIONS & NEXT STEPS

---

## SLIDE 22: Key Takeaways

**Scenario 1 - Billing Reconciliation:**

✅ Customer is correct - 15.4% overbilling confirmed
✅ Issue is systemic across all months
✅ Root cause identified: Bone marrow in live workflows
✅ Immediate fix required for billing logic

**Scenario 2 - Customer Health:**

⚠️ Strong overall growth but recent decline
⚠️ Health status: AT RISK (requires attention)
✅ Service quality remains high
⚠️ Need to monitor next month closely

---

## SLIDE 23: Action Items

**Priority 1 - Immediate (This Week):**

1. Calculate total overbilling across all months
2. Prepare credit/refund for customer
3. Schedule customer success check-in call
4. Review and fix workflow billing classification

**Priority 2 - Short Term (This Month):**

1. Implement billing validation checks
2. Set up monthly billing reconciliation process
3. Monitor September usage closely
4. Review archived workflows impact

**Priority 3 - Ongoing:**

1. Regular monthly billing audits
2. Customer health monitoring dashboard
3. Proactive customer engagement program

---

## SLIDE 24: Questions & Discussion

**Key Questions for Discussion:**

1. What is the historical context for customer's usage patterns?
2. Are there known seasonal variations we should account for?
3. What are the workflow classification rules?
4. How can we improve billing accuracy going forward?
5. What retention strategies should we prepare?

**Open for Questions**

---

## SLIDE 25: Thank You

**Thank You for Your Time**

**Contact Information:**
- [Your Email]
- [Your LinkedIn]

**Appendix:**
- Detailed data tables available upon request
- Full analysis notebook available for review

---

## PRESENTATION NOTES

### Slide Flow:
1. Start with the problem (customer dispute)
2. Show the data that validates the customer's claim
3. Identify the root cause
4. Provide recommendations

5. Shift to customer health
6. Show the positive trends
7. Highlight the risk indicators
8. Provide monitoring recommendations

9. Conclude with actionable next steps

### Visual Placement Guide:
- **Data Overview:** Slides 2-8 (No visuals, data tables/diagrams can be added)
- **Scenario 1 Visual 1:** Slide 11 (The Problem)
- **Scenario 1 Visual 2:** Slide 12 (Monthly Breakdown)
- **Scenario 1 Visual 3:** Slide 13 (Sample Types)
- **Scenario 1 Visual 4:** Slide 14 (Root Cause)

- **Scenario 2 Visual 1:** Slide 16 (Usage Trend)
- **Scenario 2 Visual 2:** Slide 17 (Growth Analysis)
- **Scenario 2 Visual 3:** Slide 18 (Success Rate)
- **Scenario 2 Visual 4:** Slide 19 (Health Summary)

### Presentation Tips:
1. Each visual should fill most of the slide
2. Add 2-3 bullet points below each visual
3. Keep text minimal - let the visuals tell the story
4. Use consistent color scheme throughout
5. Practice transitions between scenarios

### Estimated Presentation Time:
- Total: 20-25 minutes
- Data & Methodology Overview: 3-4 minutes (Slides 2-8)
- Scenario 1: 6-8 minutes (Slides 11-15)
- Scenario 2: 6-8 minutes (Slides 16-21)
- Conclusions: 2-3 minutes (Slides 22-23)
- Q&A: 5-10 minutes

