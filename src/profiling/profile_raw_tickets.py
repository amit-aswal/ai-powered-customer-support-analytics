from pathlib import Path
import pandas as pd


BRONZE_FILE = Path("data/bronze/support_tickets_raw.parquet")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_data() -> pd.DataFrame:
    """
    Loads raw support ticket data from the bronze layer.
    """
    if not BRONZE_FILE.exists():
        raise FileNotFoundError(
            "Bronze file not found. First run: python src/ingestion/load_huggingface_dataset.py"
        )

    df = pd.read_parquet(BRONZE_FILE)
    return df


def generate_column_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a column-level data profile.
    """
    profile_rows = []

    for column in df.columns:
        series = df[column]

        sample_values = (
            series
            .dropna()
            .astype(str)
            .head(3)
            .tolist()
        )

        profile_rows.append({
            "column_name": column,
            "data_type": str(series.dtype),
            "total_rows": len(df),
            "non_null_count": int(series.notna().sum()),
            "null_count": int(series.isna().sum()),
            "null_percentage": round(series.isna().mean() * 100, 2),
            "unique_count": int(series.nunique(dropna=True)),
            "sample_values": sample_values
        })

    return pd.DataFrame(profile_rows)


def generate_missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates missing value report.
    """
    missing_report = pd.DataFrame({
        "column_name": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percentage": (df.isna().mean().values * 100).round(2)
    })

    missing_report = missing_report.sort_values(
        by="missing_percentage",
        ascending=False
    )

    return missing_report


def generate_categorical_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates distribution report for categorical columns.
    """
    possible_categorical_columns = [
        "type",
        "queue",
        "priority",
        "language",
        "version",
        "tag_1",
        "tag_2",
        "tag_3",
        "tag_4",
        "tag_5",
        "tag_6",
        "tag_7",
        "tag_8"
    ]

    available_columns = [
        column for column in possible_categorical_columns
        if column in df.columns
    ]

    distribution_tables = []

    for column in available_columns:
        temp = df[column].value_counts(dropna=False).reset_index()
        temp.columns = ["category_value", "ticket_count"]
        temp["column_name"] = column
        temp["ticket_percentage"] = round(
            temp["ticket_count"] / len(df) * 100,
            2
        )

        distribution_tables.append(temp)

    if len(distribution_tables) > 0:
        final_distribution = pd.concat(distribution_tables, ignore_index=True)
    else:
        final_distribution = pd.DataFrame()

    return final_distribution


def generate_text_length_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Profiles length of text columns.
    """
    possible_text_columns = ["subject", "body", "answer"]

    available_text_columns = [
        column for column in possible_text_columns
        if column in df.columns
    ]

    rows = []

    for column in available_text_columns:
        text_length = df[column].fillna("").astype(str).str.len()

        rows.append({
            "text_column": column,
            "min_length": int(text_length.min()),
            "average_length": round(text_length.mean(), 2),
            "median_length": round(text_length.median(), 2),
            "p90_length": round(text_length.quantile(0.90), 2),
            "p95_length": round(text_length.quantile(0.95), 2),
            "max_length": int(text_length.max())
        })

    return pd.DataFrame(rows)


def generate_duplicate_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Checks possible duplicate tickets using subject and body.
    """
    duplicate_columns = []

    if "subject" in df.columns:
        duplicate_columns.append("subject")

    if "body" in df.columns:
        duplicate_columns.append("body")

    if len(duplicate_columns) == 0:
        duplicate_count = 0
    else:
        duplicate_count = int(df.duplicated(subset=duplicate_columns).sum())

    duplicate_percentage = round(duplicate_count / len(df) * 100, 2)

    duplicate_report = pd.DataFrame({
        "check_name": ["duplicate_subject_body"],
        "duplicate_count": [duplicate_count],
        "duplicate_percentage": [duplicate_percentage]
    })

    return duplicate_report


def generate_business_gap_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies important business fields missing from the raw dataset.
    """
    required_business_fields = {
        "ticket_id": "Unique ticket identifier for fact table and tracking",
        "status": "Open, closed, pending, and escalated ticket reporting",
        "created_date": "Daily, weekly, and monthly ticket trend analysis",
        "resolved_date": "Resolution performance tracking",
        "resolution_time_hours": "Average resolution time KPI",
        "agent_name": "Agent workload and performance analysis",
        "sla_status": "SLA compliance reporting",
        "sentiment": "Customer experience and complaint sentiment tracking",
        "ticket_category": "Root cause and complaint driver analysis"
    }

    rows = []

    for field_name, business_use in required_business_fields.items():
        exists_in_raw_dataset = field_name in df.columns

        if exists_in_raw_dataset:
            action_needed = "Available in raw dataset"
        else:
            action_needed = "Engineer in Phase 2 or later"

        rows.append({
            "field_name": field_name,
            "exists_in_raw_dataset": exists_in_raw_dataset,
            "action_needed": action_needed,
            "business_use": business_use
        })

    return pd.DataFrame(rows)


def save_reports(
    column_profile: pd.DataFrame,
    missing_report: pd.DataFrame,
    categorical_distribution: pd.DataFrame,
    text_length_profile: pd.DataFrame,
    duplicate_report: pd.DataFrame,
    business_gap_report: pd.DataFrame
) -> None:
    """
    Saves profiling outputs inside the reports folder.
    """
    column_profile.to_csv(
        REPORT_DIR / "column_profile.csv",
        index=False,
        encoding="utf-8"
    )

    missing_report.to_csv(
        REPORT_DIR / "missing_values_report.csv",
        index=False,
        encoding="utf-8"
    )

    categorical_distribution.to_csv(
        REPORT_DIR / "categorical_distribution_report.csv",
        index=False,
        encoding="utf-8"
    )

    text_length_profile.to_csv(
        REPORT_DIR / "text_length_profile.csv",
        index=False,
        encoding="utf-8"
    )

    duplicate_report.to_csv(
        REPORT_DIR / "duplicate_report.csv",
        index=False,
        encoding="utf-8"
    )

    business_gap_report.to_csv(
        REPORT_DIR / "business_gap_report.csv",
        index=False,
        encoding="utf-8"
    )


def create_markdown_summary(
    df: pd.DataFrame,
    missing_report: pd.DataFrame,
    duplicate_report: pd.DataFrame,
    business_gap_report: pd.DataFrame
) -> None:
    """
    Creates a markdown report for GitHub documentation.
    """
    total_rows = len(df)
    total_columns = len(df.columns)
    duplicate_count = int(duplicate_report["duplicate_count"].iloc[0])

    top_missing_table = missing_report.head(10).to_markdown(index=False)

    missing_business_fields = business_gap_report[
        business_gap_report["exists_in_raw_dataset"] == False
    ]

    missing_business_fields_table = missing_business_fields.to_markdown(index=False)

    raw_columns = ", ".join(df.columns)

    content = f"""
# Phase 1 Data Profile Report

## Dataset Overview

| Metric | Value |
|---|---:|
| Total Rows | {total_rows:,} |
| Total Columns | {total_columns:,} |
| Possible Duplicate Tickets | {duplicate_count:,} |

## Raw Columns

{raw_columns}

## Top Missing Value Columns

{top_missing_table}

## Missing Business Fields

{missing_business_fields_table}

## Initial Business Understanding

The raw dataset contains customer support ticket text, ticket type, queue, priority, language, version, and tag fields.

These fields are useful for:

- Ticket volume analysis
- Queue workload analysis
- Priority distribution analysis
- Language-based support analysis
- NLP-based ticket classification
- AI-generated summaries
- Root cause analysis

However, the dataset does not contain several operational fields required for enterprise support analytics.

Missing operational fields include:

- ticket_id
- status
- created_date
- resolved_date
- resolution_time_hours
- agent_name
- sla_status
- sentiment
- ticket_category

These fields will be created in the silver layer using documented feature engineering logic.

## Business Risk

If operational fields are not engineered properly, dashboards will not be able to answer important leadership questions such as:

- How many tickets are open?
- How many tickets are closed?
- What is the average resolution time?
- Which teams are overloaded?
- Which tickets breached SLA?
- What are the biggest complaint drivers?

## Next Phase

Phase 2 will clean the raw data and create engineered business fields such as ticket_id, status, created_date, resolved_date, resolution_time_hours, agent_name, and sla_status.
"""

    report_path = REPORT_DIR / "phase1_data_profile_report.md"
    report_path.write_text(content.strip(), encoding="utf-8")

    print(f"Markdown report created here: {report_path}")


if __name__ == "__main__":
    print("Loading raw data from bronze layer...")

    df = load_raw_data()

    print("Raw data loaded successfully.")
    print("Rows and columns:", df.shape)

    print("Creating column profile...")
    column_profile = generate_column_profile(df)

    print("Creating missing value report...")
    missing_report = generate_missing_value_report(df)

    print("Creating categorical distribution report...")
    categorical_distribution = generate_categorical_distribution(df)

    print("Creating text length profile...")
    text_length_profile = generate_text_length_profile(df)

    print("Creating duplicate report...")
    duplicate_report = generate_duplicate_report(df)

    print("Creating business gap report...")
    business_gap_report = generate_business_gap_report(df)

    print("Saving reports...")
    save_reports(
        column_profile,
        missing_report,
        categorical_distribution,
        text_length_profile,
        duplicate_report,
        business_gap_report
    )

    print("Creating markdown summary report...")
    create_markdown_summary(
        df,
        missing_report,
        duplicate_report,
        business_gap_report
    )

    print("Phase 1 profiling completed successfully.")
