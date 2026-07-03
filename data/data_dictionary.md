# Data Dictionary & Schema

**Source file:** `customer_shopping_behavior.csv`

**Grain:** One row per customer purchase record

| Column | Type (raw) | Type (cleaned) | Description | Notes / Expected Values |
|---|---|---|---|---|
| Customer ID | int | int (PK) | Unique customer identifier | Check for duplicates |
| Age | int | int | Customer age in years | Sanity range ~18–70 |
| Gender | string | category | Customer gender | Male / Female |
| Item Purchased | string | category | Specific product name | High cardinality (~25 items) |
| Category | string | category | Product category | Clothing, Footwear, Outerwear, Accessories |
| Purchase Amount (USD) | float | float | Transaction value in USD | Check for outliers/negative values |
| Location | string | category | Customer's state/region | US states |
| Size | string | category (ordinal) | Product size | S, M, L, XL |
| Color | string | category | Product color | ~25 colors |
| Season | string | category | Season of purchase | Spring, Summer, Fall, Winter |
| Review Rating | float | float | Customer rating of item | Typically 1.0–5.0 |
| Subscription Status | string | boolean | Whether customer is subscribed | Yes/No → 1/0 |
| Shipping Type | string | category | Delivery method | Standard, Express, Free Shipping, Next Day Air, 2-Day Shipping, Store Pickup |
| Discount Applied | string | boolean | Whether a discount was applied | Yes/No → 1/0 |
| Promo Code Used | string | boolean | Whether a promo code was used | Yes/No → 1/0 |
| Previous Purchases | int | int | Count of prior purchases by this customer | Behavioral proxy for loyalty |
| Payment Method | string | category | How the customer paid | Credit Card, PayPal, Cash, Debit Card, Venmo, Bank Transfer |
| Frequency of Purchases | string | category (ordinal) | Self-reported/derived purchase cadence | Weekly, Fortnightly, Monthly, Every 3 Months, Quarterly, Annually |

## Derived / Engineered Fields (created in Python, see `03_data_preparation`)

| Field | Logic | Purpose |
|---|---|---|
| `age_band` | Bucket Age into 18-24, 25-34, 35-44, 45-54, 55-64, 65+ | Segmentation |
| `promo_group` | 'Discount+Promo', 'Discount Only', 'Promo Only', 'Full Price' from Discount Applied + Promo Code Used | Promo effectiveness analysis |
| `loyalty_tier` | Bucket `Previous Purchases` into New (0-5), Growing (6-15), Loyal (16-30), Champion (30+) | Segmentation |
| `is_subscriber` | Subscription Status mapped to 1/0 | Modeling-friendly flag |
| `low_rating_flag` | 1 if Review Rating < 3, else 0 | Diagnostic analysis on dissatisfaction |
| `at_risk_flag` | 1 if `loyalty_tier` in (Loyal, Champion) AND `frequency` in (Quarterly, Annually) AND `low_rating_flag`=1 | Composite "high value, disengaging" risk segment |

## Suggested SQL Table DDL

See `04_sql_analysis/analysis_queries.sql` for the full `CREATE TABLE` statement matching this schema.
