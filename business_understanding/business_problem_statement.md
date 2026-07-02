# Business Problem Statement
## Customer Retention & Revenue Risk Analysis

---

### 1. Background

The company sells apparel and accessories across multiple categories (Clothing, Footwear, Outerwear, Accessories) through an online/retail channel. Marketing runs frequent discount and promo-code campaigns, and offers a paid subscription program. Leadership has noticed rising promotional spend without a clear read on whether it is improving customer loyalty or simply discounting purchases that would have happened anyway.

### 2. Stakeholder

**VP of Retention Marketing** — owns the subscription program and promotional budget, and is accountable for repeat-purchase rate and customer lifetime value (CLV).

### 3. Problem Statement

> Leadership does not currently know which customer segments are most likely to churn or reduce spend, or whether discount and promo-code usage is building repeat purchase behavior versus eroding margin on customers who would have converted regardless. Without this, promotional budget and retention efforts are allocated on intuition rather than evidence.

### 4. Business Objectives

1. Identify customer segments (by demographics, category, subscription status, and purchase frequency) with the highest and lowest retention/repeat-purchase behavior.
2. Quantify whether discounts and promo codes correlate with increased repeat purchases, or mainly attract one-off, price-sensitive buyers.
3. Surface operational drivers (shipping type, payment method, review ratings) associated with customer dissatisfaction or drop-off.
4. Identify seasonal and geographic demand patterns to support inventory and campaign planning.

### 5. Key Business Questions

| # | Question | Analysis Type |
|---|----------|---------------|
| 1 | Which customer segments (age band, gender, category, location) have the highest previous-purchase counts and purchase frequency? | Segmentation |
| 2 | Do subscribers behave differently from non-subscribers in spend, frequency, and ratings? | Comparative |
| 3 | Is there a measurable difference in repeat-purchase behavior between customers who used a discount/promo code and those who didn't? | Promo effectiveness |
| 4 | Which combinations of shipping type and payment method correlate with lower review ratings? | Diagnostic |
| 5 | How does purchase volume and category mix shift across seasons and locations? | Trend/seasonality |
| 6 | Can we build a simple risk segmentation (e.g., high-value/low-engagement = "at risk") from existing fields? | Segmentation/scoring |

### 6. Success Metrics (KPIs)

- Repeat purchase rate by segment
- Average purchase amount by discount-usage group
- Review rating distribution by shipping type / payment method
- Share of revenue from subscribers vs. non-subscribers
- % of "at-risk" customers identified and their revenue contribution

### 7. Scope

**In scope:** Exploratory analysis, segmentation, descriptive and diagnostic statistics, dashboarding, and a recommendations report based on the provided transactional/customer dataset.

**Out of scope:** Predictive churn modeling (ML), real-time scoring, A/B test design for future promos (this is a retrospective/diagnostic project, though findings can inform one).

### 8. Deliverables & Tools

| Stage | Tool |
|---|---|
| Business framing & schema | Markdown / this document |
| Data cleaning & feature engineering | Python (pandas) |
| Structured analysis | SQL |
| Visualization & dashboard | Tableau |
| Reporting | Executive summary + slide deck |
| Version control / portfolio | GitHub |

### 9. Assumptions & Constraints

- Dataset is a snapshot (not time-series transaction log), so "Previous Purchases" and "Frequency of Purchases" are treated as customer-level behavioral proxies rather than derived from raw transaction history.
- One row = one customer's most recent/representative purchase record (confirm against actual data; if multiple rows per `Customer ID` exist, treat as transaction-level and aggregate accordingly).
- No cost/margin data is available, so "profitability" of discounts is inferred directionally from spend and frequency, not true margin impact.
