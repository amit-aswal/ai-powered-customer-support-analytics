# Phase 2 Data Dictionary

## Dataset

Silver Layer Dataset:

`data/silver/support_tickets_silver.parquet`

This dataset is created from the raw bronze customer support tickets dataset after cleaning and feature engineering.

## Important Note

The original Hugging Face dataset does not contain operational ticket lifecycle fields such as ticket status, created date, resolved date, resolution time, assigned agent, or SLA status.

These fields were engineered using documented simulation logic for analytics and portfolio demonstration purposes.

Synthetic operational fields should not be interpreted as real company historical data.

---

## Original Raw Columns

| Column | Description | Source |
|---|---|---|
| subject | Original ticket subject | Raw dataset |
| body | Original customer message | Raw dataset |
| answer | Original support response | Raw dataset |
| type | Ticket type | Raw dataset |
| queue | Support queue | Raw dataset |
| priority | Ticket priority | Raw dataset |
| language | Ticket language | Raw dataset |
| version | Dataset/product version field | Raw dataset |
| tag_1 to tag_8 | Ticket tags | Raw dataset |

---

## Cleaned and Engineered Fields

| Column | Description | Field Type |
|---|---|---|
| ticket_id | Unique ticket identifier generated sequentially | Engineered |
| subject_clean | Cleaned subject text | Cleaned |
| body_clean | Cleaned body text | Cleaned |
| answer_clean | Cleaned answer text | Cleaned |
| combined_text | Combined subject and body text | Engineered |
| combined_text_length | Character length of combined_text | Engineered |
| type_clean | Standardized lowercase ticket type | Cleaned |
| queue_clean | Standardized lowercase support queue | Cleaned |
| priority_clean | Standardized lowercase priority | Cleaned |
| language_clean | Standardized lowercase language | Cleaned |
| version_clean | Standardized lowercase version field | Cleaned |
| status | Simulated ticket status | Simulated |
| created_date | Simulated ticket creation timestamp | Simulated |
| resolved_date | Simulated resolved timestamp for closed tickets | Simulated |
| resolution_time_hours | Resolution time for closed tickets | Simulated / Derived |
| agent_name | Simulated support agent assigned based on queue | Simulated |
| sla_target_hours | SLA threshold based on priority | Derived |
| sla_status | SLA Met, SLA Breached, or Open / Not Applicable | Derived |
| tags_combined | Combined tag values | Engineered |
| tag_count | Number of tags per ticket | Engineered |
| ticket_category_rule_based | Basic keyword-based ticket category | Engineered |
| has_subject | True if subject_clean is available | Data Quality Flag |
| has_body | True if body_clean is available | Data Quality Flag |
| has_answer | True if answer_clean is available | Data Quality Flag |
| is_operational_data_simulated | Shows operational fields are simulated | Documentation Flag |

---

## Ticket Category Values

- Payment Issues
- Refund Issues
- Delivery Issues
- Login Problems
- Product Quality
- Account Issues
- Technical Issues
- Other

---

## Validation Checks Completed

Phase 2 validation checks confirmed:

- Row count was preserved
- Original raw columns were preserved
- Original raw values were unchanged
- ticket_id values are unique
- created_date values are present
- Closed tickets have resolved_date
- Non-closed tickets do not have resolved_date
- resolved_date is after created_date
- resolution_time_hours is not negative
- SLA status values are valid
- SLA logic is correct
- Synthetic data flag is present
- Ticket category values are valid
- tag_count is valid

Validation report:

`reports/phase2/phase2_data_validation_report.md`
