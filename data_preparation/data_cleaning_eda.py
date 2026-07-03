'''
Customer Behavior Analysis — Data Preparation & Feature Engineering
--------------------------------------------------------------------
Stage 2 of the project: cleans the raw customer dataset, engineers
behavioral features, runs baseline EDA, and exports:
  1. A cleaned CSV for SQL loading / Tableau
  2. A summary stats report (txt)
  3. Quick-look EDA plots (png)
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {df.shape[0]:,} rows, {df.shape[1]} columns from {path}")
    return df


# ---------------------------------------------------------------------------
# 2. CLEAN
# ---------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names: spaces -> underscores, lowercase
    df.columns = (
        df.columns.str.strip()
        .str.replace(r"[()]", "", regex=True)
        .str.replace(" ", "_")
        .str.lower()
    )
    
    # --- Duplicates ---
    dup_ids = df["customer_id"].duplicated().sum()
    print(f"Duplicate customer_id rows: {dup_ids}")
    df = df.drop_duplicates()

    # --- Missing values ---
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        print("Missing values found:\n", missing)
    # Numeric: fill with median; Categorical: fill with mode
    # Fill missing numeric values EXCEPT review_rating (leave NaNs — don't fabricate reviews)
    numeric_cols = df.select_dtypes(include=np.number).columns.drop("review_rating", errors="ignore")
    for col in numeric_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    # review_rating stays NaN where missing — track it explicitly instead
    df["rating_missing_flag"] = df["review_rating"].isna().astype(int)

    for col in df.select_dtypes(include="object").columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # --- Type fixes ---
    if "purchase_amount_usd" in df.columns:
        df["purchase_amount_usd"] = pd.to_numeric(df["purchase_amount_usd"], errors="coerce")

    # --- Outlier check (purchase amount, age) via IQR flag (not removed, just flagged) ---
    for col in ["purchase_amount_usd", "age"]:
        if col in df.columns:
            q1, q3 = df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            n_out = ((df[col] < lower) | (df[col] > upper)).sum()
            print(f"Outliers in {col} (IQR method): {n_out}")

    # --- Standardize Yes/No fields to boolean ints ---
    yes_no_cols = ["subscription_status", "discount_applied", "promo_code_used"]
    for col in yes_no_cols:
        if col in df.columns:
            df[col + "_flag"] = df[col].str.strip().str.lower().map({"yes": 1, "no": 0})
    df["frequency_of_purchases"] = df["frequency_of_purchases"].replace({"Bi-Weekly": "Fortnightly"})
    return df


# ---------------------------------------------------------------------------
# 3. FEATURE ENGINEERING
# ---------------------------------------------------------------------------
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Age bands
    bins = [17, 24, 34, 44, 54, 64, 100]
    labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    df["age_band"] = pd.cut(df["age"], bins=bins, labels=labels)

    # Promo group (4-way segmentation of promotional exposure)
    def promo_group(row):
        d, p = row["discount_applied_flag"], row["promo_code_used_flag"]
        if d == 1 and p == 1:
            return "Discount+Promo"
        elif d == 1:
            return "Discount Only"
        elif p == 1:
            return "Promo Only"
        return "Full Price"

    df["promo_group"] = df.apply(promo_group, axis=1)

    # Loyalty tier from previous purchases
    df["loyalty_tier"] = pd.qcut(
        df["previous_purchases"],
        q=4,
        labels=["Low", "Medium", "High", "Very High"],
    )

    # Rename subscriber flag for clarity
    df["is_subscriber"] = df["subscription_status_flag"]

    rating_p25 = df["review_rating"].quantile(0.25)
    df["low_rating_flag"] = (df["review_rating"] < rating_p25).astype(int)

    # Composite at-risk flag: high loyalty tier + infrequent purchasing + low rating
    infrequent = df["frequency_of_purchases"].isin(["Quarterly", "Annually", "Every 3 Months"])
    high_loyalty = df["loyalty_tier"].isin(["High", "Very High"])
    df["at_risk_flag"] = ((infrequent) & (high_loyalty) & (df["low_rating_flag"] == 1)).astype(int)

    return df


# ---------------------------------------------------------------------------
# 4. QUICK EDA
# ---------------------------------------------------------------------------
def run_eda(df: pd.DataFrame, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)

    # Summary stats to text file
    with open(os.path.join(out_dir, "summary_stats.txt"), "w") as f:
        f.write("=== Numeric Summary ===\n")
        f.write(df.describe().to_string())
        f.write("\n\n=== Category Counts: Category ===\n")
        f.write(df["category"].value_counts().to_string())
        f.write("\n\n=== Promo Group Counts ===\n")
        f.write(df["promo_group"].value_counts().to_string())
        f.write("\n\n=== Subscriber Split ===\n")
        f.write(df["is_subscriber"].value_counts().to_string())
        f.write("\n\n=== At-Risk Customers ===\n")
        f.write(f"{df['at_risk_flag'].sum()} of {len(df)} customers flagged at-risk "
                 f"({df['at_risk_flag'].mean()*100:.1f}%)\n")

    # Plot: spend distribution by promo group
    fig, ax = plt.subplots(figsize=(8, 5))
    df.boxplot(column="purchase_amount_usd", by="promo_group", ax=ax)
    plt.title("Purchase Amount by Promo Group")
    plt.suptitle("")
    plt.ylabel("Purchase Amount (USD)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "spend_by_promo_group.png"))
    plt.close()

    # Plot: repeat purchases by loyalty tier & subscription
    fig, ax = plt.subplots(figsize=(8, 5))
    df.groupby(["loyalty_tier", "is_subscriber"], observed=True)["previous_purchases"].mean().unstack().plot(
        kind="bar", ax=ax
    )
    plt.title("Avg Previous Purchases by Loyalty Tier & Subscription")
    plt.ylabel("Avg Previous Purchases")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "loyalty_by_subscription.png"))
    plt.close()

    print(f"EDA artifacts written to {out_dir}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    input = "C:/Users/Artophilic/Analysis Projects/Customer Behavior Data Analysis Portfolio Project/data/customer_shopping_behavior.csv"
    output = "C:/Users/Artophilic/Analysis Projects/Customer Behavior Data Analysis Portfolio Project/data/cleaned_customer_data.csv"
    eda_dir = "C:/Users/Artophilic/Analysis Projects/Customer Behavior Data Analysis Portfolio Project/data/eda"

    df = load_data(input)
    df = clean_data(df)
    df = engineer_features(df)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Cleaned dataset written to {output} ({df.shape[0]:,} rows, {df.shape[1]} cols)")

    run_eda(df, eda_dir)


if __name__ == "__main__":
    main()

