# Customer Data Analysis - Presentation Slides

---

## SLIDE 1: Title Slide

**Title:** Customer Data Analysis: Billing Reconciliation & Health Assessment

**Subtitle:** Technical Task - Data Analyst Position

**Date:** [Current Date]
**Presenter:** [Your Name]

---

## SLIDE 2: Executive Summary

**Key Findings:**

1. **Scenario 1 - Billing Dispute:**
   - Customer correctly identified 15.4% overbilling in latest month
   - Root cause: Bone marrow samples incorrectly included in production billing

2. **Scenario 2 - Customer Health:**
   - Strong overall growth trend (62.5% from May to August)
   - Single month decline (18.8% in August) - monitor closely
   - Customer health status: AT RISK (requires attention)

**Visual:** Use Scenario 1 Visual 1 (Billing Dispute comparison)

---

## SLIDE 3: Agenda

1. **Scenario 1: Billing Reconciliation**
   - Investigation of customer dispute
   - Root cause analysis
   - Recommendations

2. **Scenario 2: Customer Health Assessment**
   - Usage trend analysis
   - Risk indicators
   - Health scorecard

3. **Conclusions & Next Steps**

---

## PART 1: SCENARIO 1 - BILLING RECONCILIATION

---

## SLIDE 4: The Problem Statement

**Customer Dispute:**

"Customer claims 15% overbilling last month. They only process blood and saliva samples in production workloads, but the invoice includes other sample types."

**Question:** Is the customer correct?

**Visual:** Scenario 1 Visual 1 - The Billing Dispute (Executive Summary)

**Key Point:** 
- Customer expects: 883 samples (blood + saliva only)
- We invoiced: 1,019 samples
- **Overbilling: 15.4%** ✓ Customer is correct

---

## SLIDE 5: Monthly Billing Breakdown

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

## SLIDE 6: Sample Type Breakdown

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

## SLIDE 7: Root Cause Analysis

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

## SLIDE 8: Scenario 1 - Recommendations

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

## SLIDE 9: Customer Usage Trend

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

## SLIDE 10: Month-over-Month Growth Analysis

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

## SLIDE 11: Production Run Success Rate

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

## SLIDE 12: Customer Health Summary

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

## SLIDE 13: Scenario 2 - Risk Assessment

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

## SLIDE 14: Scenario 2 - Recommendations

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

## SLIDE 15: Key Takeaways

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

## SLIDE 16: Action Items

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

## SLIDE 17: Questions & Discussion

**Key Questions for Discussion:**

1. What is the historical context for customer's usage patterns?
2. Are there known seasonal variations we should account for?
3. What are the workflow classification rules?
4. How can we improve billing accuracy going forward?
5. What retention strategies should we prepare?

**Open for Questions**

---

## SLIDE 18: Thank You

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
- **Scenario 1 Visual 1:** Slide 4 (The Problem)
- **Scenario 1 Visual 2:** Slide 5 (Monthly Breakdown)
- **Scenario 1 Visual 3:** Slide 6 (Sample Types)
- **Scenario 1 Visual 4:** Slide 7 (Root Cause)

- **Scenario 2 Visual 1:** Slide 9 (Usage Trend)
- **Scenario 2 Visual 2:** Slide 10 (Growth Analysis)
- **Scenario 2 Visual 3:** Slide 11 (Success Rate)
- **Scenario 2 Visual 4:** Slide 12 (Health Summary)

### Presentation Tips:
1. Each visual should fill most of the slide
2. Add 2-3 bullet points below each visual
3. Keep text minimal - let the visuals tell the story
4. Use consistent color scheme throughout
5. Practice transitions between scenarios

### Estimated Presentation Time:
- Total: 15-20 minutes
- Scenario 1: 6-8 minutes
- Scenario 2: 6-8 minutes
- Conclusions: 2-3 minutes
- Q&A: 5-10 minutes

