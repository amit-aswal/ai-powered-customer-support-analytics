from pathlib import Path
import pandas as pd


PHASE4_DIR = Path("reports/phase4")
PHASE7_DIR = Path("reports/phase7")
PHASE8_DIR = Path("reports/phase8")

PHASE8_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def safe_int(value):
    if pd.isna(value):
        return 0
    return int(round(float(value)))


def safe_float(value):
    if pd.isna(value):
        return 0.0
    return round(float(value), 2)


def create_recommendations(
    executive,
    queue,
    category,
    priority,
    agent,
    monthly,
    sentiment,
    urgency,
    top_keywords
):
    recommendations = []

    top_queue = queue.iloc[0]
    top_category = category.iloc[0]
    top_priority_breach = priority.sort_values("sla_breached_tickets", ascending=False).iloc[0]
    top_agent = agent.iloc[0]
    highest_month = monthly.sort_values("total_tickets", ascending=False).iloc[0]

    total_tickets = safe_int(executive.loc[0, "total_tickets"])
    sla_breached = safe_int(executive.loc[0, "sla_breached_tickets"])
    sla_compliance = safe_float(executive.loc[0, "sla_compliance_percentage"])

    recommendations.append({
        "recommendation_area": "Queue Workload",
        "finding": f"{top_queue['queue_clean']} has the highest workload with {safe_int(top_queue['total_tickets']):,} tickets.",
        "business_risk": "High queue workload can increase response delays, agent pressure, and SLA breach risk.",
        "recommended_action": "Monitor this queue weekly, rebalance ticket routing, and add support capacity if the volume remains high.",
        "priority_level": "High"
    })

    recommendations.append({
        "recommendation_area": "Top Customer Issue",
        "finding": f"{top_category['ticket_category']} is the largest ticket category with {safe_int(top_category['total_tickets']):,} tickets.",
        "business_risk": "A high-volume issue category increases support cost and may indicate a repeated product or process problem.",
        "recommended_action": "Perform root-cause analysis for this category and create self-service help content to reduce repeated tickets.",
        "priority_level": "High"
    })

    recommendations.append({
        "recommendation_area": "SLA Performance",
        "finding": f"There are {sla_breached:,} SLA breached tickets and SLA compliance is {sla_compliance}%.",
        "business_risk": "SLA breaches can reduce customer trust and increase escalation pressure.",
        "recommended_action": "Review SLA breach drivers by queue, category, and priority. Improve escalation rules for high-risk segments.",
        "priority_level": "High"
    })

    recommendations.append({
        "recommendation_area": "Priority Handling",
        "finding": f"{top_priority_breach['priority_clean']} priority has the highest SLA breach count with {safe_int(top_priority_breach['sla_breached_tickets']):,} breached tickets.",
        "business_risk": "Priority handling gaps may lead to delayed resolution for important customer issues.",
        "recommended_action": "Review routing logic and ensure high-risk priority tickets are assigned faster.",
        "priority_level": "Medium"
    })

    recommendations.append({
        "recommendation_area": "Agent Workload",
        "finding": f"{top_agent['agent_name']} has the highest assigned workload with {safe_int(top_agent['assigned_tickets']):,} tickets.",
        "business_risk": "Uneven workload can cause agent burnout and inconsistent resolution quality.",
        "recommended_action": "Use workload balancing rules and review agent-level open ticket distribution.",
        "priority_level": "Medium"
    })

    recommendations.append({
        "recommendation_area": "Monthly Demand Planning",
        "finding": f"{highest_month['year_month']} had the highest ticket volume with {safe_int(highest_month['total_tickets']):,} tickets.",
        "business_risk": "Peak support periods can create backlog if staffing is not planned early.",
        "recommended_action": "Use monthly trends to plan staffing, shift allocation, and support automation.",
        "priority_level": "Medium"
    })

    if len(sentiment) > 0:
        negative_row = sentiment[sentiment["sentiment_label"] == "Negative"]
        if len(negative_row) > 0:
            negative_count = safe_int(negative_row.iloc[0]["ticket_count"])
            negative_pct = safe_float(negative_row.iloc[0]["ticket_percentage"])

            recommendations.append({
                "recommendation_area": "Negative Sentiment",
                "finding": f"{negative_count:,} tickets are classified as Negative sentiment, representing {negative_pct}% of tickets.",
                "business_risk": "Negative tickets may indicate customer dissatisfaction, repeated failures, or unresolved issues.",
                "recommended_action": "Review negative tickets weekly and prioritize categories with high negative sentiment.",
                "priority_level": "High"
            })

    if len(urgency) > 0:
        high_urgency_row = urgency[urgency["urgency_label"] == "High Urgency"]
        if len(high_urgency_row) > 0:
            high_urgency_count = safe_int(high_urgency_row.iloc[0]["ticket_count"])
            high_urgency_pct = safe_float(high_urgency_row.iloc[0]["ticket_percentage"])

            recommendations.append({
                "recommendation_area": "High Urgency Tickets",
                "finding": f"{high_urgency_count:,} tickets are classified as High Urgency, representing {high_urgency_pct}% of tickets.",
                "business_risk": "High urgency tickets can lead to escalation and poor customer experience if not handled quickly.",
                "recommended_action": "Create a separate high-urgency review queue and monitor it daily.",
                "priority_level": "High"
            })

    if len(top_keywords) > 0:
        top_keyword = top_keywords.iloc[0]["keyword"]
        recommendations.append({
            "recommendation_area": "Keyword Monitoring",
            "finding": f"The most frequent keyword in support tickets is '{top_keyword}'.",
            "business_risk": "Repeated keywords can reveal recurring customer pain points.",
            "recommended_action": "Track top keywords monthly and connect them with issue categories for root-cause analysis.",
            "priority_level": "Low"
        })

    return pd.DataFrame(recommendations)


def create_markdown_summary(
    executive,
    queue,
    category,
    priority,
    agent,
    monthly,
    mom,
    sentiment,
    urgency,
    top_keywords,
    text_quality,
    recommendations
):
    total_tickets = safe_int(executive.loc[0, "total_tickets"])
    open_tickets = safe_int(executive.loc[0, "open_tickets"])
    closed_tickets = safe_int(executive.loc[0, "closed_tickets"])
    pending_tickets = safe_int(executive.loc[0, "pending_tickets"])
    escalated_tickets = safe_int(executive.loc[0, "escalated_tickets"])
    avg_resolution = safe_float(executive.loc[0, "avg_resolution_time_hours"])
    sla_met = safe_int(executive.loc[0, "sla_met_tickets"])
    sla_breached = safe_int(executive.loc[0, "sla_breached_tickets"])
    sla_compliance = safe_float(executive.loc[0, "sla_compliance_percentage"])

    top_queue = queue.iloc[0]
    top_category = category.iloc[0]
    top_priority_breach = priority.sort_values("sla_breached_tickets", ascending=False).iloc[0]
    top_agent = agent.iloc[0]
    highest_month = monthly.sort_values("total_tickets", ascending=False).iloc[0]

    top_sentiment = sentiment.iloc[0]
    top_urgency = urgency.iloc[0]
    top_keyword = top_keywords.iloc[0]["keyword"] if len(top_keywords) > 0 else "Not available"

    negative_row = sentiment[sentiment["sentiment_label"] == "Negative"]
    negative_tickets = safe_int(negative_row.iloc[0]["ticket_count"]) if len(negative_row) > 0 else 0

    high_urgency_row = urgency[urgency["urgency_label"] == "High Urgency"]
    high_urgency_tickets = safe_int(high_urgency_row.iloc[0]["ticket_count"]) if len(high_urgency_row) > 0 else 0

    avg_word_count = safe_float(text_quality.loc[0, "avg_word_count"])

    highest_growth_text = "Not available"
    mom_clean = mom.dropna(subset=["mom_growth_percentage"])
    if len(mom_clean) > 0:
        highest_growth = mom_clean.sort_values("mom_growth_percentage", ascending=False).iloc[0]
        highest_growth_text = (
            f"{highest_growth['year_month']} with {safe_float(highest_growth['mom_growth_percentage'])}% growth"
        )

    top_recommendations_md = ""
    for idx, row in recommendations.head(5).iterrows():
        top_recommendations_md += (
            f"\n{idx + 1}. **{row['recommendation_area']}**: "
            f"{row['recommended_action']}"
        )

    report = f"""
# Phase 8 AI Executive Summary and Business Recommendations

## Objective

Phase 8 creates an AI-style executive summary by combining SQL KPIs, EDA insights, Power BI dashboard findings, and NLP text analytics.

This phase helps convert technical analysis into a management-ready business report.

---

## Executive Summary

The customer support dataset contains **{total_tickets:,} tickets**.

Out of these, **{closed_tickets:,} tickets are closed**, **{open_tickets:,} are open**, **{pending_tickets:,} are pending**, and **{escalated_tickets:,} are escalated**.

The average resolution time is **{avg_resolution} hours**.

SLA performance shows **{sla_met:,} SLA met tickets** and **{sla_breached:,} SLA breached tickets**, with an overall SLA compliance rate of **{sla_compliance}%**.

The highest workload queue is **{top_queue['queue_clean']}**, with **{safe_int(top_queue['total_tickets']):,} tickets**.

The largest ticket category is **{top_category['ticket_category']}**, with **{safe_int(top_category['total_tickets']):,} tickets**.

The highest ticket volume month is **{highest_month['year_month']}**, with **{safe_int(highest_month['total_tickets']):,} tickets**.

---

## Key Business Findings

### 1. Queue Workload

The highest workload queue is **{top_queue['queue_clean']}**.

This queue handled **{safe_int(top_queue['total_tickets']):,} tickets**, making it the most important queue to monitor for backlog, staffing pressure, and SLA risk.

### 2. Ticket Category Demand

The largest ticket category is **{top_category['ticket_category']}**.

This category represents **{safe_float(top_category['ticket_percentage'])}%** of total tickets.

This indicates a recurring customer issue area that should be reviewed for root-cause analysis.

### 3. SLA Risk

The project identified **{sla_breached:,} SLA breached tickets**.

The priority group with the highest SLA breach count is **{top_priority_breach['priority_clean']}**, with **{safe_int(top_priority_breach['sla_breached_tickets']):,} breached tickets**.

This suggests that priority handling and escalation rules should be reviewed.

### 4. Agent Workload

The agent with the highest workload is **{top_agent['agent_name']}**, with **{safe_int(top_agent['assigned_tickets']):,} assigned tickets**.

This insight can help support managers identify workload imbalance and reduce agent burnout.

### 5. Monthly Demand Pattern

The month with the highest ticket volume is **{highest_month['year_month']}**.

The highest month-over-month growth period is **{highest_growth_text}**.

This can help managers plan staffing and support operations before peak demand periods.

---

## NLP and Text Analytics Findings

### Sentiment

The most common sentiment is **{top_sentiment['sentiment_label']}**, with **{safe_int(top_sentiment['ticket_count']):,} tickets**.

The dataset contains **{negative_tickets:,} Negative sentiment tickets**.

Negative tickets should be reviewed because they may indicate poor customer experience, repeated failures, or unresolved complaints.

### Urgency

The most common urgency level is **{top_urgency['urgency_label']}**, with **{safe_int(top_urgency['ticket_count']):,} tickets**.

The dataset contains **{high_urgency_tickets:,} High Urgency tickets**.

High urgency tickets should be monitored through a separate escalation process.

### Keywords

The most frequent keyword is **{top_keyword}**.

Top keywords help identify repeated themes in customer issues and can support root-cause analysis.

### Text Quality

Average cleaned ticket word count is **{avg_word_count}**.

This confirms that the dataset has enough text content for NLP analysis, sentiment scoring, urgency scoring, and future AI summarization.

---

## Final Recommendations

{top_recommendations_md}

---

## Business Impact

This project demonstrates how raw support tickets can be converted into a complete analytics system.

The final solution helps support leaders:

- Monitor ticket volume
- Track SLA performance
- Identify overloaded queues
- Understand agent workload
- Detect recurring issue categories
- Analyze negative and urgent tickets
- Plan staffing using monthly trends
- Build dashboard-ready executive reporting

---

## Recruiter-Friendly Project Value

This project shows end-to-end capability across:

| Skill Area | Demonstrated Through |
|---|---|
| Python | Data ingestion, cleaning, feature engineering, NLP |
| SQL | DuckDB star schema and KPI queries |
| Analytics Engineering | Bronze, silver, and gold layers |
| Business Intelligence | Power BI dashboard |
| Data Analysis | EDA and business insights |
| NLP | Sentiment, urgency, and keyword analysis |
| Reporting | Executive summary and recommendations |
| GitHub Workflow | Version-controlled project phases |

---

## Important Note

Some operational fields such as status, created date, resolved date, agent name, resolution time, and SLA status were simulated in Phase 2 because the original dataset does not include real lifecycle data.

This is clearly documented throughout the project for transparency.

The Phase 8 summary is generated using rule-based logic from project outputs. It is designed to simulate how an AI executive reporting layer can convert analytics outputs into management-ready recommendations.
"""

    output_path = PHASE8_DIR / "phase8_ai_executive_summary.md"
    output_path.write_text(report.strip(), encoding="utf-8")
    print(f"Saved: {output_path}")


def create_business_impact_report():
    report = """
# Final Project Business Impact Report

## Project Name

AI-Powered Customer Support Analytics Platform

---

## Business Problem

Customer support teams handle large volumes of tickets across different queues, priorities, issue categories, and agents.

Without an analytics system, leaders may struggle to answer:

- How many tickets are open?
- Which queues are overloaded?
- Which issues are repeated most often?
- Which tickets breach SLA?
- Which agents have high workload?
- Which categories show negative sentiment?
- What should the business fix first?

---

## Solution Built

This project builds a complete support analytics workflow.

It converts raw customer support ticket data into:

- Cleaned and validated data
- Engineered operational fields
- SQL star schema
- KPI reports
- EDA insights
- Power BI dashboard
- NLP sentiment and urgency analysis
- AI-style executive summary
- Business recommendations

---

## Real-Life Usefulness

In a real company, this project can help support leaders:

- Reduce manual reporting work
- Monitor ticket workload
- Improve SLA compliance
- Identify recurring customer pain points
- Balance agent workload
- Detect negative and urgent tickets
- Prioritize operational improvements
- Communicate insights through dashboards and summaries

---

## Final Outcome

The project demonstrates a full analytics lifecycle from raw data to business decision-making.

It is useful for Data Analyst, BI Analyst, Analytics Engineer, and AI/Data Analyst portfolio positioning.
"""

    output_path = PHASE8_DIR / "final_project_business_impact_report.md"
    output_path.write_text(report.strip(), encoding="utf-8")
    print(f"Saved: {output_path}")


def main():
    print("Loading project outputs...")

    executive = read_csv(PHASE4_DIR / "phase4_executive_kpi.csv")
    queue = read_csv(PHASE4_DIR / "phase4_queue_performance.csv")
    category = read_csv(PHASE4_DIR / "phase4_category_analysis.csv")
    priority = read_csv(PHASE4_DIR / "phase4_priority_sla.csv")
    agent = read_csv(PHASE4_DIR / "phase4_agent_performance.csv")
    monthly = read_csv(PHASE4_DIR / "phase4_monthly_trend.csv")
    mom = read_csv(PHASE4_DIR / "phase4_mom_growth.csv")

    sentiment = read_csv(PHASE7_DIR / "phase7_sentiment_distribution.csv")
    urgency = read_csv(PHASE7_DIR / "phase7_urgency_distribution.csv")
    top_keywords = read_csv(PHASE7_DIR / "phase7_top_keywords_overall.csv")
    text_quality = read_csv(PHASE7_DIR / "phase7_text_quality_summary.csv")

    print("Creating business recommendations...")
    recommendations = create_recommendations(
        executive,
        queue,
        category,
        priority,
        agent,
        monthly,
        sentiment,
        urgency,
        top_keywords
    )

    recommendations_path = PHASE8_DIR / "phase8_business_recommendations.csv"
    recommendations.to_csv(recommendations_path, index=False, encoding="utf-8")
    print(f"Saved: {recommendations_path}")

    print("Creating AI executive summary...")
    create_markdown_summary(
        executive,
        queue,
        category,
        priority,
        agent,
        monthly,
        mom,
        sentiment,
        urgency,
        top_keywords,
        text_quality,
        recommendations
    )

    print("Creating final business impact report...")
    create_business_impact_report()

    print("Phase 8 AI executive summary and recommendations completed successfully.")


if __name__ == "__main__":
    main()
