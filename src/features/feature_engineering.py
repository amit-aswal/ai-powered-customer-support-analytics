from pathlib import Path
import re
import pandas as pd
import numpy as np


BRONZE_FILE = Path("data/bronze/support_tickets_raw.parquet")
SILVER_DIR = Path("data/silver")
REPORT_DIR = Path("reports/phase2")

SILVER_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def load_bronze_data() -> pd.DataFrame:
    """
    Loads raw customer support tickets from the bronze layer.
    """
    if not BRONZE_FILE.exists():
        raise FileNotFoundError(
            "Bronze file not found. Run Phase 1 ingestion first."
        )

    df = pd.read_parquet(BRONZE_FILE)
    print(f"Bronze data loaded successfully. Shape: {df.shape}")
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names to lowercase snake_case.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def clean_text_value(value) -> str:
    """
    Cleans a single text value by removing excessive whitespace and control characters.
    """
    if pd.isna(value):
        return ""

    value = str(value)
    value = value.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    value = re.sub(r"\s+", " ", value)
    value = value.strip()

    return value


def create_clean_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates cleaned versions of text fields.
    """
    for col in ["subject", "body", "answer"]:
        if col in df.columns:
            df[f"{col}_clean"] = df[col].apply(clean_text_value)
        else:
            df[f"{col}_clean"] = ""

    df["combined_text"] = (
        df["subject_clean"] + " " + df["body_clean"]
    ).str.strip()

    df["combined_text_length"] = df["combined_text"].str.len()

    return df


def create_ticket_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates unique ticket IDs.
    """
    df.insert(
        0,
        "ticket_id",
        ["TKT-" + str(i).zfill(6) for i in range(1, len(df) + 1)]
    )

    return df


def clean_categorical_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates cleaned versions of key categorical fields.
    """
    categorical_columns = ["type", "queue", "priority", "language", "version"]

    for col in categorical_columns:
        if col in df.columns:
            df[f"{col}_clean"] = (
                df[col]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .str.lower()
            )
        else:
            df[f"{col}_clean"] = "unknown"

    return df


def create_created_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulates realistic ticket creation dates across an 18-month reporting period.
    """
    start_date = pd.Timestamp("2024-01-01")
    end_date = pd.Timestamp("2025-06-30 23:00:00")

    total_hours = int((end_date - start_date).total_seconds() // 3600)

    random_hours = np.random.randint(0, total_hours, size=len(df))

    df["created_date"] = start_date + pd.to_timedelta(random_hours, unit="h")
    df["created_date"] = pd.to_datetime(df["created_date"])

    return df


def create_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulates ticket status using realistic support operations distribution.
    """
    statuses = ["Closed", "Open", "Pending", "Escalated"]

    probabilities = [0.70, 0.15, 0.10, 0.05]

    df["status"] = np.random.choice(
        statuses,
        size=len(df),
        p=probabilities
    )

    return df


def generate_resolution_time(priority: str) -> int:
    """
    Generates resolution time based on ticket priority.
    """
    priority = str(priority).lower().strip()

    if "critical" in priority or "urgent" in priority:
        return np.random.randint(1, 12)
    elif "high" in priority:
        return np.random.randint(2, 30)
    elif "medium" in priority or "normal" in priority:
        return np.random.randint(12, 96)
    elif "low" in priority:
        return np.random.randint(24, 168)
    else:
        return np.random.randint(12, 120)


def create_resolution_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates resolved_date and resolution_time_hours.
    Only closed tickets get resolved dates.
    """
    df["resolution_time_hours"] = df["priority_clean"].apply(generate_resolution_time)

    df["resolved_date"] = df.apply(
        lambda row: row["created_date"] + pd.to_timedelta(row["resolution_time_hours"], unit="h")
        if row["status"] == "Closed"
        else pd.NaT,
        axis=1
    )

    df.loc[df["status"] != "Closed", "resolution_time_hours"] = np.nan

    return df


def assign_agent_by_queue(queue: str) -> str:
    """
    Assigns a support agent based on queue.
    """
    queue = str(queue).lower()

    technical_agents = [
        "Amit Sharma",
        "Priya Mehta",
        "Rahul Verma",
        "Neha Joshi"
    ]

    billing_agents = [
        "Sneha Kapoor",
        "Rohan Singh",
        "Anjali Nair",
        "Karan Malhotra"
    ]

    account_agents = [
        "Meera Iyer",
        "Kabir Khan",
        "Isha Gupta",
        "Vikram Rao"
    ]

    general_agents = [
        "Arjun Das",
        "Pooja Menon",
        "Ritika Sinha",
        "Nikhil Bansal"
    ]

    if any(word in queue for word in ["tech", "software", "bug", "it", "system"]):
        return np.random.choice(technical_agents)
    elif any(word in queue for word in ["bill", "payment", "invoice", "refund"]):
        return np.random.choice(billing_agents)
    elif any(word in queue for word in ["account", "login", "user", "profile"]):
        return np.random.choice(account_agents)
    else:
        return np.random.choice(general_agents)


def create_agent_name(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates agent assignment.
    """
    df["agent_name"] = df["queue_clean"].apply(assign_agent_by_queue)
    return df


def get_sla_target(priority: str) -> int:
    """
    Creates SLA target hours based on ticket priority.
    """
    priority = str(priority).lower().strip()

    if "critical" in priority or "urgent" in priority:
        return 12
    elif "high" in priority:
        return 24
    elif "medium" in priority or "normal" in priority:
        return 72
    elif "low" in priority:
        return 120
    else:
        return 96


def create_sla_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates SLA target and SLA status.
    """
    df["sla_target_hours"] = df["priority_clean"].apply(get_sla_target)

    df["sla_status"] = np.where(
        (df["status"] == "Closed") &
        (df["resolution_time_hours"] <= df["sla_target_hours"]),
        "SLA Met",
        np.where(
            df["status"] == "Closed",
            "SLA Breached",
            "Open / Not Applicable"
        )
    )

    return df


def combine_tags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combines tag_1 to tag_8 into one field and counts tags.
    """
    tag_columns = [col for col in df.columns if col.startswith("tag_")]

    if len(tag_columns) == 0:
        df["tags_combined"] = ""
        df["tag_count"] = 0
        return df

    def combine_row_tags(row):
        tags = []
        for col in tag_columns:
            value = row.get(col)
            if pd.notna(value) and str(value).strip() != "":
                tags.append(str(value).strip().lower())
        return ", ".join(tags)

    df["tags_combined"] = df.apply(combine_row_tags, axis=1)

    df["tag_count"] = df["tags_combined"].apply(
        lambda x: 0 if x == "" else len(x.split(", "))
    )

    return df


def classify_ticket_category(text: str) -> str:
    """
    Basic rule-based ticket category classification.
    This is a baseline. Advanced NLP categorization will be improved later.
    """
    text = str(text).lower()

    if any(word in text for word in ["payment", "invoice", "billing", "charged", "transaction", "credit card"]):
        return "Payment Issues"
    elif any(word in text for word in ["refund", "return", "money back", "reimbursement"]):
        return "Refund Issues"
    elif any(word in text for word in ["delivery", "shipment", "shipping", "late delivery", "tracking"]):
        return "Delivery Issues"
    elif any(word in text for word in ["login", "password", "sign in", "signin", "account access", "authentication"]):
        return "Login Problems"
    elif any(word in text for word in ["quality", "damaged", "defective", "broken", "poor product"]):
        return "Product Quality"
    elif any(word in text for word in ["account", "profile", "subscription", "email change", "user account"]):
        return "Account Issues"
    elif any(word in text for word in ["bug", "error", "crash", "not working", "technical", "integration", "software"]):
        return "Technical Issues"
    else:
        return "Other"


def create_ticket_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a baseline rule-based ticket category.
    """
    df["ticket_category_rule_based"] = df["combined_text"].apply(classify_ticket_category)
    return df


def create_data_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates useful data quality flags.
    """
    df["has_subject"] = df["subject_clean"].str.len() > 0
    df["has_body"] = df["body_clean"].str.len() > 0
    df["has_answer"] = df["answer_clean"].str.len() > 0

    df["is_operational_data_simulated"] = True

    return df


def create_phase2_summary_report(df: pd.DataFrame) -> None:
    """
    Creates summary report for Phase 2.
    """
    summary = {
        "total_tickets": len(df),
        "total_columns": len(df.columns),
        "closed_tickets": int((df["status"] == "Closed").sum()),
        "open_tickets": int((df["status"] == "Open").sum()),
        "pending_tickets": int((df["status"] == "Pending").sum()),
        "escalated_tickets": int((df["status"] == "Escalated").sum()),
        "avg_resolution_time_hours": round(df["resolution_time_hours"].mean(), 2),
        "sla_met_count": int((df["sla_status"] == "SLA Met").sum()),
        "sla_breached_count": int((df["sla_status"] == "SLA Breached").sum()),
        "open_not_applicable_count": int((df["sla_status"] == "Open / Not Applicable").sum())
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(REPORT_DIR / "phase2_feature_engineering_summary.csv", index=False)

    status_distribution = (
        df["status"]
        .value_counts()
        .reset_index()
    )
    status_distribution.columns = ["status", "ticket_count"]
    status_distribution["ticket_percentage"] = round(
        status_distribution["ticket_count"] / len(df) * 100,
        2
    )
    status_distribution.to_csv(REPORT_DIR / "phase2_status_distribution.csv", index=False)

    sla_distribution = (
        df["sla_status"]
        .value_counts()
        .reset_index()
    )
    sla_distribution.columns = ["sla_status", "ticket_count"]
    sla_distribution["ticket_percentage"] = round(
        sla_distribution["ticket_count"] / len(df) * 100,
        2
    )
    sla_distribution.to_csv(REPORT_DIR / "phase2_sla_distribution.csv", index=False)

    category_distribution = (
        df["ticket_category_rule_based"]
        .value_counts()
        .reset_index()
    )
    category_distribution.columns = ["ticket_category_rule_based", "ticket_count"]
    category_distribution["ticket_percentage"] = round(
        category_distribution["ticket_count"] / len(df) * 100,
        2
    )
    category_distribution.to_csv(REPORT_DIR / "phase2_ticket_category_distribution.csv", index=False)

    markdown_report = f"""
# Phase 2 Feature Engineering Report

## Overview

Phase 2 converts the raw bronze support ticket dataset into a cleaned and business-ready silver dataset.

## Total Records

| Metric | Value |
|---|---:|
| Total Tickets | {summary["total_tickets"]:,} |
| Total Columns After Feature Engineering | {summary["total_columns"]:,} |
| Closed Tickets | {summary["closed_tickets"]:,} |
| Open Tickets | {summary["open_tickets"]:,} |
| Pending Tickets | {summary["pending_tickets"]:,} |
| Escalated Tickets | {summary["escalated_tickets"]:,} |
| Average Resolution Time Hours | {summary["avg_resolution_time_hours"]} |
| SLA Met Count | {summary["sla_met_count"]:,} |
| SLA Breached Count | {summary["sla_breached_count"]:,} |

## Fields Created

- ticket_id
- subject_clean
- body_clean
- answer_clean
- combined_text
- combined_text_length
- type_clean
- queue_clean
- priority_clean
- language_clean
- version_clean
- status
- created_date
- resolved_date
- resolution_time_hours
- agent_name
- sla_target_hours
- sla_status
- tags_combined
- tag_count
- ticket_category_rule_based
- has_subject
- has_body
- has_answer
- is_operational_data_simulated

## Important Note

The original dataset does not contain operational support fields such as ticket status, created date, resolved date, resolution time, agent assignment, and SLA status.

These fields were engineered using reproducible business simulation logic to create a realistic enterprise customer support analytics environment.

## Business Value

The silver dataset is now ready for:

- SQL data modeling
- KPI calculation
- SLA analysis
- Queue workload analysis
- Agent performance analysis
- Ticket category analysis
- Power BI dashboards
- Streamlit application
- Future NLP and AI analysis
"""

    (REPORT_DIR / "phase2_feature_engineering_report.md").write_text(
        markdown_report.strip(),
        encoding="utf-8"
    )


def save_silver_data(df: pd.DataFrame) -> None:
    """
    Saves cleaned and engineered data to silver layer.
    """
    parquet_path = SILVER_DIR / "support_tickets_silver.parquet"
    csv_path = SILVER_DIR / "support_tickets_silver.csv"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"Saved silver parquet file here: {parquet_path}")
    print(f"Saved silver csv file here: {csv_path}")


def main():
    df = load_bronze_data()

    print("Standardizing column names...")
    df = standardize_column_names(df)

    print("Creating ticket IDs...")
    df = create_ticket_id(df)

    print("Cleaning text fields...")
    df = create_clean_text_fields(df)

    print("Cleaning categorical fields...")
    df = clean_categorical_fields(df)

    print("Creating created_date...")
    df = create_created_date(df)

    print("Creating ticket status...")
    df = create_status(df)

    print("Creating resolution fields...")
    df = create_resolution_fields(df)

    print("Assigning agents...")
    df = create_agent_name(df)

    print("Creating SLA fields...")
    df = create_sla_fields(df)

    print("Combining tags...")
    df = combine_tags(df)

    print("Creating rule-based ticket category...")
    df = create_ticket_category(df)

    print("Creating data quality flags...")
    df = create_data_quality_flags(df)

    print("Creating Phase 2 reports...")
    create_phase2_summary_report(df)

    print("Saving silver data...")
    save_silver_data(df)

    print("Phase 2 feature engineering completed successfully.")
    print(f"Final silver dataset shape: {df.shape}")


if __name__ == "__main__":
    main()
