import pandas as pd


def clean_agent_data(txns, agents):
    """
    Clean mobile-money transaction data and merge it with the agent register.

    Returns:
        clean_df: cleaned transaction DataFrame
        log: list of data quality issues and affected row counts
    """

    # Work on copies so the original DataFrames are not modified
    clean_df = txns.copy()
    agent_df = agents.copy()

    log = []

    # 1. Record duplicate transaction IDs
    duplicate_count = clean_df.duplicated(subset="txn_id").sum()

    log.append({
        "issue": "Duplicate transaction IDs",
        "dimension": "Uniqueness",
        "column": "txn_id",
        "rows_affected": int(duplicate_count)
    })

    # Remove duplicates, keeping the first occurrence
    clean_df = clean_df.drop_duplicates(
        subset="txn_id",
        keep="first"
    ).copy()

    # 2. Standardise transaction types
    original_types = clean_df["txn_type"].copy()

    clean_df["txn_type"] = (
        clean_df["txn_type"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    valid_types = ["Deposit", "Withdrawal"]

    invalid_types = ~clean_df["txn_type"].isin(valid_types)

    log.append({
        "issue": "Inconsistent or invalid transaction types",
        "dimension": "Consistency",
        "column": "txn_type",
        "rows_affected": int(
            (original_types != clean_df["txn_type"]).sum()
        )
    })

    # 3. Convert amounts to numeric values
    clean_df["amount"] = pd.to_numeric(
        clean_df["amount"],
        errors="coerce"
    )

    missing_amounts = clean_df["amount"].isna()

    log.append({
        "issue": "Missing or invalid transaction amounts",
        "dimension": "Completeness",
        "column": "amount",
        "rows_affected": int(missing_amounts.sum())
    })

    # Create an imputation flag before filling missing values
    clean_df["amount_imputed"] = missing_amounts

    # Fill missing amounts using the median for each transaction type
    type_medians = clean_df.groupby("txn_type")["amount"].transform("median")

    overall_median = clean_df["amount"].median()

    clean_df["amount"] = clean_df["amount"].fillna(
        type_medians.fillna(overall_median)
    )

    # 4. Convert transaction dates into datetime values
    clean_df["txn_date"] = pd.to_datetime(
        clean_df["txn_date"],
        format="mixed",
        errors="coerce"
    )

    log.append({
        "issue": "Missing or invalid transaction dates",
        "dimension": "Validity",
        "column": "txn_date",
        "rows_affected": int(clean_df["txn_date"].isna().sum())
    })

    # 5. Detect outliers using the IQR method
    Q1 = clean_df["amount"].quantile(0.25)
    Q3 = clean_df["amount"].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    clean_df["is_outlier"] = (
        (clean_df["amount"] < lower_bound) |
        (clean_df["amount"] > upper_bound)
    )

    log.append({
        "issue": "Potential transaction amount outliers",
        "dimension": "Accuracy",
        "column": "amount",
        "rows_affected": int(clean_df["is_outlier"].sum())
    })

    # 6. Merge transactions with the official agent register
    clean_df = clean_df.merge(
        agent_df[["agent_id", "county"]],
        on="agent_id",
        how="left"
    )

    # Flag transactions belonging to unknown agents
    clean_df["unknown_agent"] = clean_df["county"].isna()

    log.append({
        "issue": "Unknown agent references",
        "dimension": "Validity",
        "column": "agent_id",
        "rows_affected": int(clean_df["unknown_agent"].sum())
    })

    # Return the cleaned dataset and audit log
    return clean_df, log
