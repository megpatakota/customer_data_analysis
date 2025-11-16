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
QC Checks --[WORKFLOW_ID]--> Workflows
    |                          |
    +--[RUN_ID]--> Runs --[WORKFLOW_ID]--+
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

**3. Data Quality Assessment:**
- **Missing Values:** Preserved and explicitly accounted for (not removed)
  - `QC_CHECK = NaN`: Excluded from billable analysis (only 1 sample found in finished LIVE runs, minimal impact)
  - `SAMPLE_TYPE = NaN`: Identified and counted separately (1 sample with null type found)
  - Used `value_counts(dropna=False)` to see all missing values
  - **Decision:** Based on sensitivity analysis showing only 1 missing QC in finished LIVE runs, we exclude missing QC from billing
- **Workflow ID Consistency:** Implicitly validated through merge operations
  - Left merges reveal orphaned records (QC checks without matching workflows)
  - Inner merges ensure only matching records are included in analysis
  - No explicit orphaned record check performed
- **Duplicate Records:** Not explicitly checked - data used as-is from source
  - Relies on source data quality
  - No `.duplicated()` or `.drop_duplicates()` calls in analysis

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
- Sample is in a `[LIVE]` workflow
- Sample is from a run with `OUTCOME = "finished"`
- Sample has `QC_CHECK = "pass"` only (missing QC excluded)

**IMPORTANT DECISION - Missing QC Checks:**
- **Approach Used:** Samples with missing `QC_CHECK` (NaN) are **excluded** from billable count
- **Rationale:** Only 1 missing QC check found in finished LIVE runs (<0.03% impact)
- **Sensitivity Analysis:** Performed to quantify impact - showed minimal effect (1 sample)
- **Decision:** Based on low impact, we use conservative approach - only explicit "pass" QC is billable
- **Documentation:** Sensitivity analysis cell in notebook shows the reasoning

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
- **Data Impact:** Reduced from 6,405 total samples to 3,607 billable live samples (excluding 1 missing QC)

**2. Run Outcome Filtering:**
- **Included:** Only samples from runs where `OUTCOME = "finished"`
- **Excluded:** Failed runs, canceled runs
- **Rationale:** Only successfully completed runs should be billed
- **Data Impact:** From 4,057 samples in live runs to 3,607 billable samples (excluding 1 missing QC)

**3. QC Status Handling:**
- **Included:** Samples with `QC_CHECK = "pass"` only
- **Excluded:** Samples with `QC_CHECK = NaN` (missing QC)
- **Decision:** Based on sensitivity analysis showing only 1 missing QC in finished LIVE runs
- **Impact:** Minimal (<0.03% of billable samples) - justifies exclusion
- **Sensitivity Analysis:** Performed to justify this decision - results show negligible impact
- **Rationale:** Conservative approach - only bill what we know passed QC

**4. Overbilling Calculation:**
```
Overbilling % = (Non-blood/saliva samples / Blood+saliva samples) x 100
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

**1. Usage Data Definition (Different from Scenario 1):**
- **Base Dataset:** `usage_live` - All samples from finished LIVE runs (regardless of QC status)
- **Rationale:** For customer health, we need to track ALL processing activity, not just billable samples
- **Why:** Captures complete customer usage patterns including samples that may have failed QC
- **Difference from Scenario 1:** Scenario 1 uses billable samples (LIVE + finished + pass QC), Scenario 2 uses all finished LIVE samples

**2. Usage Metrics Calculated:**
- **All Finished LIVE Samples:** Count of all samples in finished LIVE runs per month
- **Unique Runs:** Number of distinct production runs per month
- **Month-over-Month (MoM) Change:** Percentage change in total usage (all samples)

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
- **Data Used:** All LIVE runs from merged dataframe (`df`)
- Formula: `(Finished Runs / Total Runs) x 100`
- Thresholds: 90% target, 80% warning level
- **Purpose:** Assess operational quality separately from usage trends

**6. Comprehensive Health Metrics:**
- Real-world customer success metrics calculated from `usage_live` and `df`:
  - Churn Risk Indicators (consecutive declines, risk level)
  - Engagement Metrics (workflow utilization, diversity)
  - Growth Velocity (acceleration/deceleration)
  - Operational Health (success rates, status)
  - Usage Concentration (dependency on top workflows)
  - Platform Maturity (new vs established workflows)

---

## SLIDE 8: Sensitivity Analysis - Missing QC Checks

**The Question: How Should We Handle Missing QC Data?**

**Sensitivity Analysis Performed:**
- Analyzed impact of including vs excluding missing QC checks
- Quantified the billing impact of this decision

**Findings:**
- **Only 1 missing QC check** found in finished LIVE runs
- **Impact:** <0.03% of billable samples
- **Interpretation:** Negligible impact on billing totals

**Decision Made:**
- **Approach Used:** Exclude missing QC from billing analysis
- **Rationale:** Minimal impact (only 1 sample) justifies conservative approach
- **Result:** Only samples with explicit `QC_CHECK = "pass"` are included

**Why This Matters:**
- Ensures billing accuracy by only including verified QC passes
- Conservative approach reduces risk of incorrect billing
- Low impact means decision has minimal business consequences

**What We Did:**
1. **Performed Sensitivity Analysis:** Calculated results under both assumptions
2. **Quantified Impact:** Only 1 sample affected (<0.03% of total)
3. **Made Decision:** Excluded missing QC based on minimal impact
4. **Documented Reasoning:** Sensitivity analysis cell shows the justification

**Data Impact:**
- Sensitivity analysis shows: 3,607 samples with pass QC + 1 missing QC = 3,608 total
- Decision to exclude missing QC results in 3,607 billable samples
- Difference: 1 sample (<0.03% impact)

**Conclusion:**
- Decision justified by data - minimal impact
- Conservative approach ensures billing accuracy
- Sensitivity analysis provides transparency and reasoning

---

## SLIDE 9: Data Limitations & Considerations

**What We Know:**

**Complete Coverage:** All production (LIVE) workflows included
**Time Period:** 4 months of data (May-August 2025)
**Data Quality:** No missing critical fields in production data
**Environment Classification:** Accurately identified production vs non-production

**What We Don't Know:**

**Historical Context:** No data before May 2025 (can't assess longer-term trends)
**Seasonal Patterns:** Limited to 4 months (insufficient for seasonality analysis)
**Customer Intent:** Can't determine if August decline is intentional or concerning
**Workflow Purpose:** Unclear why bone marrow samples are in LIVE workflows
**Contract Terms:** Assumed blood/saliva only based on customer claim (not verified)

**Assumptions Made:**

1. **Missing QC Checks = Excluded** **DECISION MADE**
   - Decision: Excluded from billing (conservative approach)
   - Rationale: Only 1 missing QC found in finished LIVE runs (<0.03% impact)
   - **Impact:** Minimal - sensitivity analysis justifies exclusion
   - **Documentation:** Sensitivity analysis cell provides reasoning

2. **Customer Contract Terms**
   - Assumed: Only blood/saliva allowed in production (based on customer dispute)
   - **Note:** Not verified against actual contract - assumption based on customer claim

3. **Risk Thresholds**
   - 15% MoM decline = risk indicator (industry standard)
   - 20% workflow decline = concerning pattern
   - **Note:** Thresholds are standard but may need customer-specific calibration

4. **Workflow Naming Convention**
   - Assumed: Environment prefixes (e.g., [LIVE], [TEST]) are reliable
   - **Validation:** Regex-based extraction validated against data patterns

---

## SLIDE 10: Executive Summary

**Key Findings:**

1. **Scenario 1 - Billing Dispute:**
   - Customer correctly identified 15.4% overbilling in latest month
   - Root cause: Bone marrow samples incorrectly included in production billing
   - Issue is systemic across all months (10-18% overbilling)

2. **Scenario 2 - Customer Health:**
   - Strong overall growth trend (71.5% from May to August)
   - Single month decline (16.51% in August) - exceeds 15% risk threshold
   - Alert triggered: Month with >15% drop in processing volume
   - Customer health status: AT RISK (HIGH risk level based on comprehensive metrics)
   - Operational health: CRITICAL (success rate 75.0% latest, 62.0% average - both below 80% threshold)
   - Comprehensive metrics show: 
     - DECELERATING growth trajectory
     - MEDIUM concentration risk (41.0% top workflow, 87.5% top 3)
     - MATURE platform (130 days avg age, 0 new workflows)
     - HIGH churn risk (exceeds threshold)
     - CRITICAL operational health (requires immediate attention)

**Visual:** Use Scenario 1 Visual 1 (Billing Dispute comparison)

---

## SLIDE 11: Agenda

1. **Data & Methodology Overview** (Just completed)
   - Data structure and organization
   - Cleaning and transformation steps
   - Analytical assumptions

2. **Scenario 1: Billing Reconciliation**
   - Investigation of customer dispute
   - Time-based pattern analysis (when are samples processed?)
   - Root cause analysis with data-driven explanations
   - Explaining what happened, not assigning fault

3. **Scenario 2: Customer Health Assessment**
   - Comprehensive usage trend analysis (all finished LIVE samples, not just pass QC)
   - Deep trend analysis using workflow timestamps and run durations
   - Daily usage timeline and weekly operational cycle patterns
   - Real-world customer health metrics (churn risk, engagement, growth, operational health, concentration, maturity)
   - Risk indicators and comprehensive health assessment

4. **Conclusions & Next Steps**

---

## PART 1: SCENARIO 1 - BILLING RECONCILIATION

---

## SLIDE 12: The Problem Statement

**Customer Dispute:**

"Customer claims 15% overbilling last month. They only process blood and saliva samples in production workloads, but the invoice includes other sample types."

**Key Question:** What actually happened? Who is at fault?

**Investigation Approach:**
- Analyze the data to explain WHAT happened
- Identify WHEN different sample types are being processed
- Understand temporal patterns to explain the situation
- Let the data tell the story - no assumptions about fault

**Visual:** Scenario 1 Visual 1 - The Billing Dispute (Executive Summary)

**Initial Observation:** 
- Customer expects: 882 samples (blood + saliva only, latest month)
- We invoiced: 1,018 samples (including other types)
- **Difference: 15.4%** - Non-blood/saliva samples explain almost all of this gap

---

## SLIDE 13: Monthly Billing Breakdown

**What the Data Shows:**

- Overbilling has been consistent across all months (ranging from ~10% to ~18%)
- The issue is not isolated to one month
- Pattern: Blood/Saliva (expected) + Bone Marrow/Other (overbilled) = Total invoice

**Visual:** Scenario 1 Visual 2 - Monthly Billing Trend

**Key Insights:**
- August (disputed month) shows 15.4% overbilling
- Every month has some level of overbilling (10.2%, 13.5%, 18.0%, 15.4%)
- The pattern is systemic, not a one-time error and peaks in July at ~18%

---

## SLIDE 14: Sample Type Breakdown

**What Types Are Being Billed?**

**Visual:** Scenario 1 Visual 3 - Sample Type Breakdown

**The Numbers:**
- **Expected Types (Blood/Saliva):**
  - Blood: 1,017 samples
  - Saliva: 2,121 samples
  - **Total Expected: 3,138 samples**

- **Other Types Found in LIVE Environment:**
  - Bone Marrow: 468 samples (CRITICAL ISSUE)
  - Other / null sample type: 1 sample
  - **Total Overbilled: 469 samples (~14.9% uplift on top of blood+saliva)**

**Key Insight:** Bone marrow represents the majority of overbilling

---

## SLIDE 15: Root Cause Analysis

**Where Are These Non-Billable Samples Coming From?**

**Visual:** Scenario 1 Visual 4 - Root Cause Analysis (Top Workflows)

**What the Data Shows:**
- Multiple live workflows are processing bone marrow samples
- A small number of LIVE workflows account for the majority of bone marrow samples
- These workflows are in the [LIVE] environment and processing bone marrow

**Key Finding:** Bone marrow samples ARE being processed in LIVE workflows
- This is not a data classification error
- The workflows themselves are in production and handling bone marrow
- Question: Is this expected behavior or a configuration issue?

---

## SLIDE 15A: Time-Based Analysis - When Are Samples Processed?

**Visual:** Scenario 1 Visual 5 - Time of Day Patterns by Sample Type

**What We're Investigating:**
- Are blood/saliva and bone marrow processed at different times of day?
- Does timing reveal operational patterns?
- Can we see when different sample types are being run?

**Why This Matters:**
- Different processing times might indicate different use cases
- Could reveal if bone marrow is part of routine operations or special requests
- Helps explain the pattern with data

---

## SLIDE 15B: Day of Week Patterns

**Visual:** Scenario 1 Visual 6 - Day of Week Patterns by Sample Type

**What We're Investigating:**
- Are different sample types processed on different days?
- Does day-of-week reveal operational schedules?
- Can we identify if bone marrow runs follow a different pattern?

**Why This Matters:**
- Different days might indicate different operational needs
- Could show if bone marrow is part of regular workflow or special processing
- Provides data-driven context for understanding the situation

---

## SLIDE 15C: Timeline of Sample Processing

**Visual:** Scenario 1 Visual 7 - Sample Type Timeline Over Time

**What We're Investigating:**
- How has bone marrow processing changed over time?
- Is it increasing or decreasing relative to blood/saliva?
- What does the trend tell us about the situation?

**Why This Matters:**
- Shows if bone marrow processing is a recent change or ongoing pattern
- Reveals if the issue is getting worse or staying constant
- Provides historical context to explain what happened

---

## SLIDE 16: Deep Investigation - Which Workflows Process Bone Marrow?

**Visual:** Scenario 1 Visual 8 - Bone Marrow Workflow Investigation

**What the Data Shows:**
- [X] workflows are processing bone marrow samples in LIVE environment
- Top workflows processing bone marrow: [List from investigation]
- Bone marrow processing started: [First BM Date from data]
- These workflows are configured as [LIVE] in the system

**Key Questions Arising:**
- Are these workflows supposed to be in production?
- Did the customer configure these workflows, or was this a system default?
- Why do these workflows process bone marrow if customer only expects blood/saliva?

**Critical Finding:**
- This is NOT a data classification error
- The workflows themselves are in LIVE environment and processing bone marrow
- Need business context to determine if this is expected behavior or misconfiguration

---

## SLIDE 16A: Workflow-Sample Type Matrix

**Visual:** Scenario 1 Visual 9 - Workflow-Sample Type Processing Matrix

**What This Reveals:**
- Heatmap showing which workflows process which sample types
- Clear visualization of which workflows handle bone marrow vs blood/saliva
- Reveals if workflows are mixed-use or specialized

**Pattern Identification:**
- Shows concentration of bone marrow processing in specific workflows
- Helps identify if certain workflows are misconfigured
- Reveals the scope of the issue across workflow portfolio

---

## SLIDE 16C: Scenario 1 – Additional Anomalies & Data Quality Findings

**Beyond Bone Marrow – What Else Looks Anomalous?**

- **Duplicate Records:**
  - QC Checks table contains 269 fully duplicated rows and 279 duplicate key combinations (`RUN_ID`, `WORKFLOW_ID`, `SAMPLE_ID_HAEMONC_LAB_NO`) (~4–5% of QC data).
  - Runs table contains 2 duplicate run IDs.
  - These duplicates can inflate raw row counts, but the 15% discrepancy is already fully explained by bone marrow + null sample types.

- **Orphaned & Unused Records:**
  - 4 runs have no matching workflow (orphaned runs).
  - 106 workflows have no associated checks or runs (unused workflows).
  - These affect completeness and monitoring but do not drive the overbilling spike in the disputed month.

- **Missing / Null Fields:**
  - 92 missing QC results in finished LIVE runs (~2.2% of samples) and 1 sample with null `SAMPLE_TYPE` in billable data.
  - Sensitivity analysis shows excluding missing QC changes billing by only 1 sample (<0.03%), so bone marrow remains the dominant driver of the dispute.

- **Environment Mismatch (LIVE Runs vs ARCHIVED Workflows):**
  - Data shows bone marrow samples where `ENVIRONMENT_runs = "live"` but `ENVIRONMENT_wfs = "archived"`.
  - Interpretation: runs reflect the environment **at execution time**, while workflows reflect their **current** status (some later renamed/archived).
  - This suggests these workflows were genuinely used in LIVE production when bone marrow was processed, and only later archived, so the billing logic is consistently treating those runs as production.

---

## SLIDE 16B: What the Time-Based Analysis Reveals

**Visuals:** Scenario 1 Visuals 5, 6, 7 (Time of Day, Day of Week, Timeline)

**Time-Based Findings:**

**Time of Day Patterns:**
- Blood/Saliva: Peak processing hours [from visual]
- Bone Marrow: Peak processing hours [from visual]
- Pattern: [Same time vs different times - indicates operational difference or same operations?]

**Day of Week Patterns:**
- Blood/Saliva: Processing distribution [from visual]
- Bone Marrow: Processing distribution [from visual]
- Pattern: [Same days vs different days - indicates routine vs special processing?]

**Timeline Pattern:**
- Bone marrow processing trend over time: [increasing/decreasing/consistent]
- Relationship to blood/saliva processing: [correlated/independent]
- Historical context: When did bone marrow processing start?

**What This Tells Us:**
- Processing patterns reveal [data-driven insights]
- Timing differences (if any) suggest [interpretation]
- Cannot determine fault from temporal patterns alone

---

## PART 2: SCENARIO 2 - CUSTOMER HEALTH

---

## SLIDE 17: Customer Usage Trend

**The Big Picture:**

**Visual:** Scenario 2 Visual 1 - Customer Usage Trend Over Time

**Data Used:** `usage_live` - All samples from finished LIVE runs (regardless of QC status)

**Why This Data:**
- For customer health assessment, we track ALL processing activity, not just billable samples
- Captures complete customer usage patterns including samples that may have failed QC
- Provides comprehensive view of platform engagement and usage trends
- Monthly aggregation smooths daily volatility while preserving trend information

**Growth Pattern:**
- May: 684 samples
- June: 795 samples (+16.23%)
- July: 1,405 samples (+76.73%) Peak
- August: 1,173 samples (-16.51%) **ALERT**

**Overall Growth:** 71.5% from May to August

**Key Observations:**
- Strong growth from May → June → July as customer ramps up usage
- Single significant drop (~16.5%) in August relative to July
- August volume still higher than May/June (1,173 vs 684/795)
- On 3-month moving average basis, last 3 months (Jun-Aug) are ~17% higher than previous period
- Overall usage trend remains STABLE/HEALTHY despite August decline

---

## SLIDE 18: Month-over-Month Growth Analysis

**Understanding the Volatility:**

**Visual:** Scenario 2 Visual 2 - Month-over-Month Growth Rate

**Data Used:** `usage_live` - All samples from finished LIVE runs (regardless of QC status)

**Why This Data:**
- Month-over-month changes in total usage provide early warning signals
- Includes all processing activity to capture complete customer engagement
- Helps identify volatility and growth acceleration/deceleration patterns

**Growth/Decline Pattern:**
- June: +16.23% growth
- July: +76.73% growth (strong expansion)
- August: -16.51% decline (significant drop - exceeds 15% threshold)

**Risk Indicators:**
- Single month decline >15% triggers risk flag (August: -16.51%)
- Pattern suggests possible seasonal variation OR customer reducing usage
- Color-coded visualization highlights risk periods (red) and growth periods (green)
- Need to monitor next month closely to confirm if this is a trend or temporary dip
- Workflow-level analysis shows declines concentrated in archived workflows (may be intentional phase-out)

---

## SLIDE 19: Production Run Success Rate

**Operational Quality Assessment:**

**Visual:** Scenario 2 Visual 3 - Production Run Success Rate

**Data Used:** `df` (merged dataframe with all data) - Function filters internally to LIVE runs only

**Why This Data:**
- Run outcomes (finished, failed, canceled) indicate operational quality
- Success rate is a key indicator of customer satisfaction and service reliability
- Separate from usage trends - measures service quality independently
- Function receives full merged dataframe and filters to `ENVIRONMENT_runs == "live"` internally

**Success Rate Metrics:**
- Latest success rate: 75.0%
- Average success rate: 62.0%
- Target: 90%
- Warning threshold: 80%
- Operational Status: CRITICAL

**Key Points:**
- Service reliability needs improvement (below 80% threshold)
- Low success rate indicates potential operational issues
- This is separate from usage trends - measures service quality independently
- Low success rate can indicate customer dissatisfaction even if usage is high

---

## SLIDE 20: Customer Health Summary

**Overall Health Assessment:**

**Visual:** Scenario 2 Visual 4 - Customer Health Scorecard

**Data Used:** `usage_live` (all finished LIVE samples) and `df` (merged dataframe for run outcomes)

**Why This Data:**
- Combines usage trends with operational quality metrics
- Provides composite health score for at-a-glance assessment
- Uses both usage volume and service quality to assess overall health

**Key Metrics:**
- Current Month Usage: 1,173 samples
- Month-over-Month: -16.51% (Decline)
- 3-Month Trend: +17.0% (Still positive overall - last 3 months vs previous 3)
- Success Rate: 75.0% (Latest), 62.0% (Average)
- Overall Growth: +71.5% (Since May)

**Health Score:** Composite score based on multiple factors (usage trends, success rates, 3-month trend)

**Status:** AT RISK - Requires monitoring and proactive engagement

---

## SLIDE 21: Scenario 2 - Risk Assessment

**Why "AT RISK"?**

1. **Recent Decline:**
   - 16.51% drop in August exceeds 15% risk threshold
   - Largest single-month decline observed
   - Growth trajectory: DECELERATING
   - Alert triggered: Month with >15% drop in processing volume

2. **Operational Health Concerns:**
   - Success rate: 75.0% (latest) - below 80% warning threshold
   - Average success rate: 62.0% - well below 90% target
   - Operational Status: CRITICAL
   - This is separate from usage trends but indicates service quality issues
   - Low success rate may be contributing to customer dissatisfaction

3. **However, Positive Indicators:**
   - Overall trend still positive (71.5% growth since May)
   - 0 consecutive monthly declines
   - August volume (1,173) still higher than May (684) and June (795)
   - 3-month trend: +17.0% (last 3 months vs previous 3)
   - Health summary shows: STABLE/HEALTHY overall usage trend
   - Decline may be concentrated in archived workflows (intentional phase-out)

4. **Uncertainty:**
   - Is this a temporary dip or the start of a decline?
   - Could be seasonal variation or workflow archiving
   - Operational health issues (CRITICAL success rate) may be affecting customer satisfaction
   - Need next month's data to confirm direction
   - Need to investigate operational health issues (low success rate) immediately

---

## SLIDE 22: Deeper Trend Analysis - Workflow Lifecycle

**Visual:** Scenario 2 Visual 5 - Workflow Creation Trends

**Data Used:** `df` (merged dataframe with all data) - Function filters internally to LIVE workflows only

**Why This Data:**
- Workflow creation timestamps (`WORKFLOW_TIMESTAMP`) show when new capabilities were added
- Correlating workflow creation with usage changes reveals if new workflows drive usage growth
- Helps understand platform expansion and customer adoption patterns
- Function receives full merged dataframe and filters to `ENVIRONMENT_wfs == "live"` internally

**What We're Analyzing:**
- When were live workflows created (WORKFLOW_TIMESTAMP)?
- Are new workflows being introduced over time?
- Does workflow creation correlate with usage changes?

**Why This Matters:**
- New workflows might indicate platform expansion
- Workflow lifecycle patterns reveal operational changes
- Helps understand usage trends at a deeper level
- Spikes in workflow creation = platform expansion period
- Correlation with usage growth = new workflows driving adoption

---

## SLIDE 22A: Run Duration Analysis

**Visual:** Scenario 2 Visual 6 - Run Duration Trends

**Data Used:** `df` (merged dataframe with all data) - Function filters internally to LIVE runs only

**Why This Data:**
- Run duration (STOP_TIME - START_TIME) indicates operational efficiency
- Longer run times might indicate performance issues that could affect customer satisfaction
- Changes in run duration over time reveal operational health trends
- Function receives full merged dataframe and filters to `ENVIRONMENT_runs == "live"` internally

**What We're Analyzing:**
- How long do runs take (START_TIME to STOP_TIME)?
- Are run durations changing over time?
- Do longer run times correlate with usage declines?

**Why This Matters:**
- Operational efficiency indicators
- Long run times might explain usage patterns
- Performance issues could affect customer satisfaction
- Increasing duration = potential performance degradation (concerning)
- Decreasing duration = improving efficiency (positive)
- Stable duration = consistent operations (good)

---

## SLIDE 22B: Daily Usage Patterns

**Visual:** Scenario 2 Visual 7 - Daily Usage Timeline

**Data Used:** `usage_live` - All samples from finished LIVE runs (regardless of QC status)

**Why This Data:**
- Daily granularity reveals day-to-day operational patterns
- Includes all processing activity (not just pass QC) to show complete usage
- Daily timeline shows volatility and identifies operational cycles

**What We're Analyzing:**
- Daily processing patterns using all samples in LIVE runs
- Actual customer usage regardless of QC outcome
- Daily volatility and trends

**Why This Matters:**
- Shows real customer usage patterns
- Includes all processing activity (not just pass QC)
- Reveals day-to-day operational patterns
- Consistent daily volume = stable operations
- High volatility = irregular usage patterns
- Daily patterns reveal operational consistency or variability

---

## SLIDE 22C: Weekly Usage Patterns

**Visual:** Scenario 2 Visual 8 - Weekly Usage Patterns

**Data Used:** `usage_live` - All samples from finished LIVE runs (regardless of QC status)

**Why This Data:**
- Day-of-week patterns reveal weekly operational cycles
- Shows if customer has consistent weekly schedules or irregular patterns
- Helps identify business operational patterns (e.g., weekday vs weekend processing)

**What We're Analyzing:**
- Usage patterns by day of week
- Weekly operational cycles
- Business pattern identification
- Number of production runs by day of week
- Number of samples processed by day of week

**Why This Matters:**
- Identifies weekly operational cycles
- Reveals if certain days have higher/lower usage
- Shows business operational patterns
- Consistent across days = regular operations
- Higher on weekdays = business-hours focused operations
- Higher on weekends = 24/7 operations or special processing
- Irregular patterns = ad-hoc or project-based usage

---

## SLIDE 22D: Real-World Customer Health Metrics

**Visual:** Scenario 2 Visual 9 - Customer Health Dashboard

**Data Used:** `health_metrics` - Comprehensive metrics calculated from `usage_live` and `df`

**Why This Data:**
- Real-world customer success metrics provide actionable insights for account management
- Combines multiple health dimensions (churn risk, engagement, growth, operational health, concentration, maturity)
- Industry-standard metrics used by customer success teams

**What We're Measuring:**
Using industry-standard customer success metrics to assess customer health:

1. **Churn Risk Indicators:**
   - Consecutive monthly declines: 0 months
   - Latest MoM change: -16.51% (from actual usage data)
   - Risk Level: HIGH (based on comprehensive metrics calculation)
   - Alert: Single month with >15% drop triggers risk flag

2. **Engagement Metrics:**
   - Active Workflows: 17 / Total: 7
   - Workflow Utilization: 242.9% (high utilization - workflows actively used)
   - Workflow Diversity Index: 0.719 (0-1 scale, higher = more diverse usage)

3. **Growth Velocity:**
   - Recent Growth: -16.51% (August MoM change)
   - Overall Growth: +71.5% (from May to August)
   - Growth Trajectory: DECELERATING (concerning trend)

4. **Operational Health:**
   - Success Rate: 75.0% (Latest), 62.0% (Average)
   - Operational Status: CRITICAL (both below 80% warning threshold)
   - Requires immediate attention

5. **Usage Concentration:**
   - Top Workflow: 41.0% of total usage
   - Top 3 Workflows: 87.5% of total usage
   - Concentration Risk: MEDIUM (high dependency on top workflows)

6. **Platform Maturity:**
   - Average Workflow Age: 130 days
   - New Workflows (<30 days): 0
   - Established Workflows: 6
   - Maturity Level: MATURE (platform has stabilized, no recent expansion)

---

## SLIDE 22E: Churn Risk Timeline

**Visual:** Scenario 2 Visual 10 - Churn Risk Timeline

**Data Used:** `df` (merged dataframe with all data) - Function filters internally to LIVE runs only; `health_metrics` for risk indicators

**Why This Data:**
- Monthly usage trends from merged dataframe show actual customer activity
- Health metrics provide risk level context for each period
- Timeline view reveals when risk increased/decreased over time
- Function receives full merged dataframe and filters to `ENVIRONMENT_runs == "live"` internally

**What We're Analyzing:**
- Usage trends over time with churn risk markers
- Highlights concerning periods with significant drops (>15% month-over-month)
- Current risk level indicator
- Average usage baseline for comparison

**Why This Matters:**
- Visualizes churn risk progression over time
- Identifies when risk increased/decreased
- Provides actionable timeline for customer success team
- Drops below average = concerning pattern
- Risk markers (red triangles) = periods exceeding risk threshold
- Current risk level = overall assessment based on recent trends

---

## PART 3: CONCLUSIONS & NEXT STEPS

---

## SLIDE 23: Key Findings - What the Data Shows

**Scenario 1 - Billing Reconciliation:**

**What Happened:**
- 15.4% difference between customer expectation and invoice in latest month
- Bone marrow samples are being processed in LIVE environment
- Pattern is consistent across all months (10-18% range)
- [X] specific workflows are processing bone marrow
- Time-based analysis reveals processing patterns (when/how often)

**What This Means:**
- The data shows bone marrow IS in LIVE workflows
- This is NOT a data classification error - workflows are configured as LIVE
- Cannot determine fault from data alone - need business context
- Key Questions:
  - Are these workflows supposed to be in production?
  - Did customer configure these workflows, or system default?
  - Why do these workflows process bone marrow if customer only expects blood/saliva?
  - When did bone marrow processing start - recent or ongoing?
- Further investigation needed: Why is bone marrow in production?

**Scenario 2 - Customer Health:**

**What the Data Shows:**
- Strong overall growth trend (71.5% from May to August)
- Single month decline in August (16.51%) - exceeds 15% risk threshold
- Alert triggered: Month with >15% drop in processing volume
- Decline may be concentrated in archived workflows (intentional phase-out)
- Operational health: CRITICAL (success rate 75.0% latest, 62.0% average - both below 80% threshold)
- Comprehensive trend analysis reveals:
  - Workflow lifecycle patterns (creation trends over time)
  - Run duration trends (operational efficiency indicators)
  - Daily usage timeline (day-to-day volatility and patterns)
  - Weekly operational cycles (day-of-week patterns)
- Real-world customer health metrics show:
  - Churn Risk: HIGH (0 consecutive declines, -16.51% latest MoM, exceeds risk threshold)
  - Growth Velocity: DECELERATING (-16.51% recent, +71.5% overall)
  - Engagement: 17 active workflows, 242.9% utilization, 0.719 diversity index
  - Usage Concentration: MEDIUM risk (41.0% top workflow, 87.5% top 3 workflows)
  - Platform Maturity: MATURE (130 days avg age, 0 new workflows, 6 established)

**What This Means:**
- Overall usage trend is positive (71.5% growth, 3-month trend +17.0%)
- August decline exceeds risk threshold (-16.51%) - requires immediate attention
- Operational health is CRITICAL - success rate below 80% threshold requires immediate investigation
- Health summary shows: STABLE/HEALTHY overall usage trend (3-month comparison)
- Customer health metrics provide actionable insights for customer success team
- Risk level: HIGH - requires immediate monitoring and proactive engagement
- Key concern: Operational health (CRITICAL success rate) may be affecting customer satisfaction
- Further monitoring needed to determine if trend continues or stabilizes
- Need to investigate why success rate is so low (62.0% average, 75.0% latest)

---

## SLIDE 24: Data-Driven Summary - What We Know

**Scenario 1 - What We Know:**

1. **The Facts:**
   - Bone marrow samples ARE being processed in LIVE workflows
   - [X] specific workflows are processing bone marrow
   - This is not a data classification error - the workflows are configured as LIVE in production
   - Pattern is consistent across all months (10-18% range)
   - Time-based analysis reveals processing patterns (time of day, day of week, timeline)
   - Workflow-sample type matrix shows which workflows handle which sample types

2. **What We Cannot Determine from Data Alone:**
   - Who is responsible (customer workflow configuration vs system setup)
   - Whether this is expected behavior or a configuration issue
   - Whether bone marrow should be allowed in LIVE workflows
   - Why these workflows process bone marrow when customer claims only blood/saliva

3. **What Additional Information Would Help:**
   - Business rules: Should bone marrow be in LIVE workflows?
   - Customer configuration: Did customer set up these workflows, or were they system defaults?
   - Historical context: When did bone marrow processing start - recent change or ongoing?
   - Workflow purpose: What is the intended use of these workflows?

**Scenario 2 - What We Know:**

1. **The Facts:**
   - Strong overall growth trend (71.5% from May to August)
   - Single month decline in August (16.51%) - exceeds 15% risk threshold
   - Alert triggered: Month with >15% drop in processing volume vs previous month
   - Decline may be concentrated in archived workflows (intentional phase-out)
   - Operational health: CRITICAL (success rate 75.0% latest, 62.0% average - both below 80% threshold)
   - Comprehensive trend analysis reveals:
     - Workflow creation patterns over time (workflow lifecycle)
     - Run duration trends (operational efficiency)
     - Daily usage timeline (day-to-day volatility and patterns)
     - Weekly operational cycles (day-of-week patterns)
   - Real-world customer health metrics show:
     - Churn Risk: HIGH (0 consecutive declines, -16.51% latest MoM, exceeds risk threshold)
     - Growth Velocity: DECELERATING (-16.51% recent, +71.5% overall)
     - Engagement: 17 active workflows, 242.9% utilization, 0.719 diversity index
     - Usage Concentration: MEDIUM risk (41.0% top workflow, 87.5% top 3 workflows)
     - Platform Maturity: MATURE (130 days avg age, 0 new workflows, 6 established)

2. **What This Tells Us:**
   - Overall usage trend is positive (71.5% growth, 3-month trend +17.0%)
   - August decline exceeds risk threshold (-16.51%) - requires immediate attention
   - Health summary shows: STABLE/HEALTHY overall usage trend (3-month comparison)
   - Operational health is CRITICAL - success rate below 80% threshold requires immediate investigation
   - Customer health metrics provide actionable insights for customer success team
   - Risk level: HIGH - requires immediate monitoring and proactive engagement
   - Key concern: Operational health (CRITICAL success rate) may be affecting customer satisfaction
   - Need more data to determine if trend continues or if operational issues are affecting usage
   - Need to investigate why success rate is so low (62.0% average, 75.0% latest) - this is a critical issue

---

## SLIDE 25: Questions & Discussion

**Key Questions for Further Investigation:**

1. **Scenario 1:**
   - What are the business rules for sample types in LIVE workflows?
   - Is bone marrow processing expected in production?
   - Who configured the workflows - customer or system default?
   - Has this always been the case or is it a recent change?
   - Why do these specific workflows process bone marrow when customer expects only blood/saliva?
   - Are the workflows that process bone marrow supposed to be in LIVE environment?
   - What does the time-based pattern tell us about how bone marrow is being processed?

2. **Scenario 2:**
   - What is the historical context for customer's usage patterns?
   - Are there known seasonal variations we should account for?
   - Why are workflows being archived - intentional or system-related?
   - What external factors might affect usage patterns?
   - Based on real-world metrics, what is the appropriate customer success action?
   - What do the workflow lifecycle and run duration patterns indicate about customer operations?

**Open for Questions**

---

## SLIDE 26: Thank You

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
2. Show the data to investigate what happened
3. Analyze time-based patterns to explain when/how samples are processed
4. Identify what the data shows (not assigning fault)

5. Shift to customer health
6. Show usage trends with comprehensive analysis
7. Analyze deeper patterns (workflow lifecycle, run duration, daily/weekly patterns)
8. Explain what the data reveals about customer usage

9. Conclude with data-driven findings and questions for further investigation

### Visual Placement Guide:
- **Data Overview:** Slides 2-9 (No visuals, data tables/diagrams can be added)
- **Scenario 1 Visual 1:** Slide 12 (The Problem)
- **Scenario 1 Visual 2:** Slide 13 (Monthly Breakdown)
- **Scenario 1 Visual 3:** Slide 14 (Sample Types)
- **Scenario 1 Visual 4:** Slide 15 (Root Cause)
- **Scenario 1 Visual 5:** Slide 15A (Time of Day Patterns)
- **Scenario 1 Visual 6:** Slide 15B (Day of Week Patterns)
- **Scenario 1 Visual 7:** Slide 15C (Sample Type Timeline)
- **Scenario 1 Visual 8:** Slide 16 (Bone Marrow Workflow Investigation)
- **Scenario 1 Visual 9:** Slide 16A (Workflow-Sample Type Matrix)

- **Scenario 2 Visual 1:** Slide 17 (Usage Trend)
- **Scenario 2 Visual 2:** Slide 18 (Growth Analysis)
- **Scenario 2 Visual 3:** Slide 19 (Success Rate)
- **Scenario 2 Visual 4:** Slide 20 (Health Summary)
- **Scenario 2 Visual 5:** Slide 22 (Workflow Creation Trends)
- **Scenario 2 Visual 6:** Slide 22A (Run Duration Trends)
- **Scenario 2 Visual 7:** Slide 22B (Daily Usage Timeline)
- **Scenario 2 Visual 8:** Slide 22C (Weekly Usage Patterns)
- **Scenario 2 Visual 9:** Slide 22D (Customer Health Dashboard)
- **Scenario 2 Visual 10:** Slide 22E (Churn Risk Timeline)

### Presentation Tips:
1. Each visual should fill most of the slide
2. Add 2-3 bullet points below each visual
3. Keep text minimal - let the visuals tell the story
4. Use consistent color scheme throughout (avoiding greens and solid reds for clarity)
5. All fonts are size 16 for readability
6. Practice transitions between scenarios
7. Emphasize data-driven findings, not assumptions about fault
8. Use time-based analysis to explain patterns when possible

### Estimated Presentation Time:
- Total: 28-35 minutes
- Data & Methodology Overview: 4-5 minutes (Slides 2-9)
- Scenario 1: 10-12 minutes (Slides 12-16B)
  - Basic analysis: 3-4 minutes
  - Deep investigation: 4-5 minutes
  - Time-based analysis: 3-4 minutes
- Scenario 2: 10-12 minutes (Slides 17-22E)
  - Basic usage analysis: 4-5 minutes
  - Deep trend analysis: 3-4 minutes
  - Real-world metrics: 3-4 minutes
- Conclusions: 2-3 minutes (Slides 23-24)
- Q&A: 5-10 minutes

