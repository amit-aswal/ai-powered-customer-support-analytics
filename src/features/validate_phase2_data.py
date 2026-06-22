from pathlib import Path
import pandas as pd
import numpy as np


BRONZE_FILE = Path("data/bronze/support_tickets_raw.parquet")
SILVER_FILE = Path("data/silver/support_tickets_silver.parquet")
REPORT_DIR = Path("reports/phase2")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    bronze_df = pd.read_parquet(BRONZE_FILE)
    silver_df = pd.read_parquet(SILVER_FILE)

    return bronze_df, silver_df


def add_check(results, check_name, status, details):
    results.append({
        "check_name": check_name,
        "status": status,
        "details": details
    })


def validate_phase2():
    bronze_df, silver_df = load_data()

    results = []

    # 1. Row count check
    if len(bronze_df) == len(silver_df):
        add_check(
            results,
            "Row Count Check",
            "PASS",
            f"Bronze and silver both have {len(silver_df)} rows."
        )
    else:
        add_check(
            results,
            "Row Count Check",
            "FAIL",
            f"Bronze rows: {len(bronze_df)}, Silver rows: {len(silver_df)}"
        )

    # 2. Original columns exist in silver
    original_columns = list(bronze_df.columns)
    missing_original_columns = [
        col for col in original_columns
        if col not in silver_df.columns
    ]

    if len(missing_original_columns) == 0:
        add_check(
            results,
            "Original Columns Presence Check",
            "PASS",
            "All original bronze columns are present in silver data."
        )
    else:
        add_check(
            results,
            "Original Columns Presence Check",
            "FAIL",
            f"Missing original columns in silver: {missing_original_columns}"
        )

    # 3. Original data unchanged check
    common_original_columns = [
        col for col in original_columns
        if col in silver_df.columns
    ]

    bronze_original = bronze_df[common_original_columns].fillna("__NULL__").astype(str)
    silver_original = silver_df[common_original_columns].fillna("__NULL__").astype(str)

    original_data_same = bronze_original.equals(silver_original)

    if original_data_same:
        add_check(
            results,
            "Original Data Unchanged Check",
            "PASS",
            "Original raw columns match exactly between bronze and silver."
        )
    else:
        add_check(
            results,
            "Original Data Unchanged Check",
            "FAIL",
            "Some original raw column values changed between bronze and silver."
        )

    # 4. Ticket ID uniqueness
    duplicate_ticket_ids = silver_df["ticket_id"].duplicated().sum()

    if duplicate_ticket_ids == 0:
        add_check(
            results,
            "Ticket ID Uniqueness Check",
            "PASS",
            "All ticket_id values are unique."
        )
    else:
        add_check(
            results,
            "Ticket ID Uniqueness Check",
            "FAIL",
            f"Duplicate ticket_id count: {duplicate_ticket_ids}"
        )

    # 5. Ticket ID missing check
    missing_ticket_ids = silver_df["ticket_id"].isna().sum()

    if missing_ticket_ids == 0:
        add_check(
            results,
            "Ticket ID Missing Check",
            "PASS",
            "No missing ticket_id values."
        )
    else:
        add_check(
            results,
            "Ticket ID Missing Check",
            "FAIL",
            f"Missing ticket_id count: {missing_ticket_ids}"
        )

    # 6. Created date missing check
    missing_created_dates = silver_df["created_date"].isna().sum()

    if missing_created_dates == 0:
        add_check(
            results,
            "Created Date Missing Check",
            "PASS",
            "No missing created_date values."
        )
    else:
        add_check(
            results,
            "Created Date Missing Check",
            "FAIL",
            f"Missing created_date count: {missing_created_dates}"
        )

    # 7. Closed tickets should have resolved date
    closed_missing_resolved = silver_df[
        (silver_df["status"] == "Closed") &
        (silver_df["resolved_date"].isna())
    ]

    if len(closed_missing_resolved) == 0:
        add_check(
            results,
            "Closed Tickets Resolved Date Check",
            "PASS",
            "All closed tickets have resolved_date."
        )
    else:
        add_check(
            results,
            "Closed Tickets Resolved Date Check",
            "FAIL",
            f"Closed tickets missing resolved_date: {len(closed_missing_resolved)}"
        )

    # 8. Non-closed tickets should not have resolved date
    non_closed_with_resolved = silver_df[
        (silver_df["status"] != "Closed") &
        (silver_df["resolved_date"].notna())
    ]

    if len(non_closed_with_resolved) == 0:
        add_check(
            results,
            "Open/Pending/Escalated Resolved Date Check",
            "PASS",
            "Non-closed tickets do not have resolved_date."
        )
    else:
        add_check(
            results,
            "Open/Pending/Escalated Resolved Date Check",
            "FAIL",
            f"Non-closed tickets with resolved_date: {len(non_closed_with_resolved)}"
        )

    # 9. Resolution time should not be negative
    negative_resolution_time = silver_df[
        silver_df["resolution_time_hours"].fillna(0) < 0
    ]

    if len(negative_resolution_time) == 0:
        add_check(
            results,
            "Negative Resolution Time Check",
            "PASS",
            "No negative resolution_time_hours found."
        )
    else:
        add_check(
            results,
            "Negative Resolution Time Check",
            "FAIL",
            f"Negative resolution time records: {len(negative_resolution_time)}"
        )

    # 10. Resolved date should be after created date
    invalid_resolved_dates = silver_df[
        (silver_df["resolved_date"].notna()) &
        (silver_df["resolved_date"] < silver_df["created_date"])
    ]

    if len(invalid_resolved_dates) == 0:
        add_check(
            results,
            "Resolved Date After Created Date Check",
            "PASS",
            "All resolved_date values are after created_date."
        )
    else:
        add_check(
            results,
            "Resolved Date After Created Date Check",
            "FAIL",
            f"Invalid resolved_date records: {len(invalid_resolved_dates)}"
        )

    # 11. SLA status valid values
    valid_sla_values = {
        "SLA Met",
        "SLA Breached",
        "Open / Not Applicable"
    }

    invalid_sla_values = silver_df[
        ~silver_df["sla_status"].isin(valid_sla_values)
    ]

    if len(invalid_sla_values) == 0:
        add_check(
            results,
            "SLA Status Value Check",
            "PASS",
            "All SLA status values are valid."
        )
    else:
        add_check(
            results,
            "SLA Status Value Check",
            "FAIL",
            f"Invalid SLA status records: {len(invalid_sla_values)}"
        )

    # 12. SLA logic check
    closed_df = silver_df[silver_df["status"] == "Closed"].copy()

    wrong_sla_met = closed_df[
        (closed_df["sla_status"] == "SLA Met") &
        (closed_df["resolution_time_hours"] > closed_df["sla_target_hours"])
    ]

    wrong_sla_breached = closed_df[
        (closed_df["sla_status"] == "SLA Breached") &
        (closed_df["resolution_time_hours"] <= closed_df["sla_target_hours"])
    ]

    if len(wrong_sla_met) == 0 and len(wrong_sla_breached) == 0:
        add_check(
            results,
            "SLA Logic Check",
            "PASS",
            "SLA status correctly matches resolution time and SLA target."
        )
    else:
        add_check(
            results,
            "SLA Logic Check",
            "FAIL",
            f"Wrong SLA Met: {len(wrong_sla_met)}, Wrong SLA Breached: {len(wrong_sla_breached)}"
        )

    # 13. Synthetic data flag check
    if "is_operational_data_simulated" in silver_df.columns:
        flag_values = silver_df["is_operational_data_simulated"].unique().tolist()

        if flag_values == [True] or set(flag_values) == {True}:
            add_check(
                results,
                "Synthetic Data Flag Check",
                "PASS",
                "All records are clearly flagged as having simulated operational fields."
            )
        else:
            add_check(
                results,
                "Synthetic Data Flag Check",
                "FAIL",
                f"Unexpected simulated flag values: {flag_values}"
            )
    else:
        add_check(
            results,
            "Synthetic Data Flag Check",
            "FAIL",
            "is_operational_data_simulated column is missing."
        )

    # 14. Ticket category valid values
    valid_categories = {
        "Payment Issues",
        "Refund Issues",
        "Delivery Issues",
        "Login Problems",
        "Product Quality",
        "Account Issues",
        "Technical Issues",
        "Other"
    }

    invalid_categories = silver_df[
        ~silver_df["ticket_category_rule_based"].isin(valid_categories)
    ]

    if len(invalid_categories) == 0:
        add_check(
            results,
            "Ticket Category Value Check",
            "PASS",
            "All ticket category values are valid."
        )
    else:
        add_check(
            results,
            "Ticket Category Value Check",
            "FAIL",
            f"Invalid ticket category records: {len(invalid_categories)}"
        )

    # 15. Tag count should not be negative
    invalid_tag_count = silver_df[silver_df["tag_count"] < 0]

    if len(invalid_tag_count) == 0:
        add_check(
            results,
            "Tag Count Check",
            "PASS",
            "No negative tag_count values."
        )
    else:
        add_check(
            results,
            "Tag Count Check",
            "FAIL",
            f"Invalid tag_count records: {len(invalid_tag_count)}"
        )

    validation_df = pd.DataFrame(results)
    validation_df.to_csv(
        REPORT_DIR / "phase2_data_validation_report.csv",
        index=False,
        encoding="utf-8"
    )

    failed_checks = validation_df[validation_df["status"] == "FAIL"]

    markdown_content = f"""
# Phase 2 Data Validation Report

## Validation Summary

| Metric | Value |
|---|---:|
| Total Validation Checks | {len(validation_df)} |
| Passed Checks | {(validation_df["status"] == "PASS").sum()} |
| Failed Checks | {(validation_df["status"] == "FAIL").sum()} |

## Validation Purpose

This validation confirms that Phase 2 feature engineering did not damage the original dataset and that all engineered fields follow logical business rules.

## Important Note

Some operational fields such as status, created_date, resolved_date, resolution_time_hours, agent_name, sla_target_hours, and sla_status are synthetic fields created for portfolio and analytics simulation purposes.

These fields should not be interpreted as real company operational history.

## Validation Results

{validation_df.to_markdown(index=False)}
"""

    if len(failed_checks) == 0:
        markdown_content += """

## Final Result

All Phase 2 validation checks passed.

The silver dataset is technically consistent, original raw columns were preserved, row count remained unchanged, and engineered fields follow the expected business logic.
"""
    else:
        markdown_content += f"""

## Failed Checks

{failed_checks.to_markdown(index=False)}

## Final Result

Some validation checks failed. Review the failed checks before moving to the next phase.
"""

    (REPORT_DIR / "phase2_data_validation_report.md").write_text(
        markdown_content.strip(),
        encoding="utf-8"
    )

    print(validation_df)
    print("\nValidation report saved to reports/phase2/phase2_data_validation_report.csv")
    print("Markdown report saved to reports/phase2/phase2_data_validation_report.md")

    if len(failed_checks) == 0:
        print("\nAll validation checks passed.")
    else:
        print(f"\nValidation failed. Failed checks: {len(failed_checks)}")


if __name__ == "__main__":
    validate_phase2()
