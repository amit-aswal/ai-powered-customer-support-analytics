from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]

PHASE4_DIR = BASE_DIR / "reports" / "phase4"
PHASE7_DIR = BASE_DIR / "reports" / "phase7"
PHASE8_DIR = BASE_DIR / "reports" / "phase8"


st.set_page_config(
    page_title="Customer Support Analytics Platform",
    page_icon="📊",
    layout="wide"
)


def read_csv_file(file_path):
    if file_path.exists():
        return pd.read_csv(file_path)
    st.warning(f"Missing file: {file_path}")
    return pd.DataFrame()


def read_markdown_file(file_path):
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return "Report file not found."


@st.cache_data
def load_data():
    data = {
        "executive_kpi": read_csv_file(PHASE4_DIR / "phase4_executive_kpi.csv"),
        "status_distribution": read_csv_file(PHASE4_DIR / "phase4_status_distribution.csv"),
        "queue_performance": read_csv_file(PHASE4_DIR / "phase4_queue_performance.csv"),
        "priority_sla": read_csv_file(PHASE4_DIR / "phase4_priority_sla.csv"),
        "agent_performance": read_csv_file(PHASE4_DIR / "phase4_agent_performance.csv"),
        "category_analysis": read_csv_file(PHASE4_DIR / "phase4_category_analysis.csv"),
        "monthly_trend": read_csv_file(PHASE4_DIR / "phase4_monthly_trend.csv"),
        "sentiment_distribution": read_csv_file(PHASE7_DIR / "phase7_sentiment_distribution.csv"),
        "urgency_distribution": read_csv_file(PHASE7_DIR / "phase7_urgency_distribution.csv"),
        "top_keywords": read_csv_file(PHASE7_DIR / "phase7_top_keywords_overall.csv"),
        "business_recommendations": read_csv_file(PHASE8_DIR / "phase8_business_recommendations.csv"),
    }
    return data


def show_header():
    st.title("AI-Powered Customer Support Analytics Platform")
    st.markdown(
        """
        This Streamlit app presents the final analytics outputs from the customer support analytics project.

        It includes executive KPIs, queue workload, SLA performance, agent workload, ticket categories,
        NLP sentiment analysis, urgency analysis, keywords, and business recommendations.
        """
    )


def show_metric(label, value):
    st.metric(label=label, value=value)


def format_number(value):
    try:
        return f"{int(round(float(value))):,}"
    except Exception:
        return "0"


def format_float(value):
    try:
        return f"{float(value):.2f}"
    except Exception:
        return "0.00"


def executive_overview(data):
    st.header("Executive Overview")

    executive = data["executive_kpi"]

    if executive.empty:
        st.error("Executive KPI file is missing.")
        return

    row = executive.iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_metric("Total Tickets", format_number(row.get("total_tickets", 0)))
    with col2:
        show_metric("Open Tickets", format_number(row.get("open_tickets", 0)))
    with col3:
        show_metric("Closed Tickets", format_number(row.get("closed_tickets", 0)))
    with col4:
        show_metric("Escalated Tickets", format_number(row.get("escalated_tickets", 0)))

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        show_metric("Average Resolution Hours", format_float(row.get("avg_resolution_time_hours", 0)))
    with col6:
        show_metric("SLA Met Tickets", format_number(row.get("sla_met_tickets", 0)))
    with col7:
        show_metric("SLA Breached Tickets", format_number(row.get("sla_breached_tickets", 0)))
    with col8:
        show_metric("SLA Compliance %", format_float(row.get("sla_compliance_percentage", 0)))

    st.subheader("Ticket Status Summary")
    status_df = data["status_distribution"]
    if not status_df.empty:
        st.dataframe(status_df, use_container_width=True)

        if "status" in status_df.columns and "total_tickets" in status_df.columns:
            chart_df = status_df.set_index("status")["total_tickets"]
            st.bar_chart(chart_df)


def queue_performance(data):
    st.header("Queue Performance")

    queue_df = data["queue_performance"]

    if queue_df.empty:
        st.error("Queue performance file is missing.")
        return

    st.subheader("Queue Performance Table")
    st.dataframe(queue_df, use_container_width=True)

    if "queue_clean" in queue_df.columns and "total_tickets" in queue_df.columns:
        st.subheader("Top Queues by Ticket Volume")
        chart_df = queue_df.sort_values("total_tickets", ascending=False).head(10)
        chart_df = chart_df.set_index("queue_clean")["total_tickets"]
        st.bar_chart(chart_df)

    if "queue_clean" in queue_df.columns and "sla_breached_tickets" in queue_df.columns:
        st.subheader("Top Queues by SLA Breached Tickets")
        chart_df = queue_df.sort_values("sla_breached_tickets", ascending=False).head(10)
        chart_df = chart_df.set_index("queue_clean")["sla_breached_tickets"]
        st.bar_chart(chart_df)


def sla_performance(data):
    st.header("SLA Performance")

    priority_df = data["priority_sla"]

    if priority_df.empty:
        st.error("Priority SLA file is missing.")
        return

    st.subheader("Priority-Level SLA Performance")
    st.dataframe(priority_df, use_container_width=True)

    if "priority_clean" in priority_df.columns and "sla_breached_tickets" in priority_df.columns:
        st.subheader("SLA Breaches by Priority")
        chart_df = priority_df.sort_values("sla_breached_tickets", ascending=False)
        chart_df = chart_df.set_index("priority_clean")["sla_breached_tickets"]
        st.bar_chart(chart_df)

    if "priority_clean" in priority_df.columns and "sla_compliance_percentage" in priority_df.columns:
        st.subheader("SLA Compliance Percentage by Priority")
        chart_df = priority_df.set_index("priority_clean")["sla_compliance_percentage"]
        st.bar_chart(chart_df)


def agent_workload(data):
    st.header("Agent Workload")

    agent_df = data["agent_performance"]

    if agent_df.empty:
        st.error("Agent performance file is missing.")
        return

    st.subheader("Agent Performance Table")
    st.dataframe(agent_df, use_container_width=True)

    if "agent_name" in agent_df.columns and "assigned_tickets" in agent_df.columns:
        st.subheader("Top 10 Agents by Assigned Tickets")
        chart_df = agent_df.sort_values("assigned_tickets", ascending=False).head(10)
        chart_df = chart_df.set_index("agent_name")["assigned_tickets"]
        st.bar_chart(chart_df)


def category_analysis(data):
    st.header("Ticket Category Analysis")

    category_df = data["category_analysis"]

    if category_df.empty:
        st.error("Category analysis file is missing.")
        return

    st.subheader("Category Analysis Table")
    st.dataframe(category_df, use_container_width=True)

    if "ticket_category" in category_df.columns and "total_tickets" in category_df.columns:
        st.subheader("Ticket Volume by Category")
        chart_df = category_df.sort_values("total_tickets", ascending=False)
        chart_df = chart_df.set_index("ticket_category")["total_tickets"]
        st.bar_chart(chart_df)


def monthly_trends(data):
    st.header("Monthly Trend Analysis")

    monthly_df = data["monthly_trend"]

    if monthly_df.empty:
        st.error("Monthly trend file is missing.")
        return

    st.subheader("Monthly Ticket Trend Table")
    st.dataframe(monthly_df, use_container_width=True)

    if "year_month" in monthly_df.columns and "total_tickets" in monthly_df.columns:
        st.subheader("Monthly Ticket Volume Trend")
        chart_df = monthly_df.set_index("year_month")["total_tickets"]
        st.line_chart(chart_df)


def nlp_insights(data):
    st.header("NLP Text Analytics")

    sentiment_df = data["sentiment_distribution"]
    urgency_df = data["urgency_distribution"]
    keywords_df = data["top_keywords"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment Distribution")
        if not sentiment_df.empty:
            st.dataframe(sentiment_df, use_container_width=True)

            if "sentiment_label" in sentiment_df.columns and "ticket_count" in sentiment_df.columns:
                chart_df = sentiment_df.set_index("sentiment_label")["ticket_count"]
                st.bar_chart(chart_df)
        else:
            st.warning("Sentiment distribution file is missing.")

    with col2:
        st.subheader("Urgency Distribution")
        if not urgency_df.empty:
            st.dataframe(urgency_df, use_container_width=True)

            if "urgency_label" in urgency_df.columns and "ticket_count" in urgency_df.columns:
                chart_df = urgency_df.set_index("urgency_label")["ticket_count"]
                st.bar_chart(chart_df)
        else:
            st.warning("Urgency distribution file is missing.")

    st.subheader("Top Keywords")
    if not keywords_df.empty:
        st.dataframe(keywords_df.head(20), use_container_width=True)

        if "keyword" in keywords_df.columns and "frequency" in keywords_df.columns:
            chart_df = keywords_df.sort_values("frequency", ascending=False).head(15)
            chart_df = chart_df.set_index("keyword")["frequency"]
            st.bar_chart(chart_df)
    else:
        st.warning("Top keywords file is missing.")


def recommendations(data):
    st.header("Business Recommendations")

    recommendations_df = data["business_recommendations"]

    if recommendations_df.empty:
        st.error("Business recommendations file is missing.")
        return

    st.subheader("Recommendation Table")
    st.dataframe(recommendations_df, use_container_width=True)

    st.subheader("Top Recommendations")

    for _, row in recommendations_df.iterrows():
        area = row.get("recommendation_area", "Recommendation")
        finding = row.get("finding", "")
        risk = row.get("business_risk", "")
        action = row.get("recommended_action", "")
        priority = row.get("priority_level", "")

        with st.expander(f"{area} | Priority: {priority}"):
            st.markdown(f"**Finding:** {finding}")
            st.markdown(f"**Business Risk:** {risk}")
            st.markdown(f"**Recommended Action:** {action}")


def executive_summary_report():
    st.header("AI Executive Summary Report")

    summary_text = read_markdown_file(PHASE8_DIR / "phase8_ai_executive_summary.md")
    st.markdown(summary_text)


def project_about():
    st.header("About This Project")

    st.markdown(
        """
        ## Project Summary

        This project is an end-to-end customer support analytics platform.

        It uses Python, SQL, DuckDB, Power BI, and NLP to convert raw customer support tickets into
        business-ready insights and recommendations.

        ## Main Capabilities

        - Data ingestion
        - Data profiling
        - Data cleaning
        - Feature engineering
        - SQL data modeling
        - KPI reporting
        - EDA and business insights
        - Power BI dashboard
        - NLP sentiment analysis
        - Urgency scoring
        - Keyword extraction
        - Executive summary generation

        ## Business Value

        The project helps support leaders monitor ticket workload, SLA performance, queue bottlenecks,
        agent workload, customer issue categories, negative sentiment, and high urgency tickets.

        ## Important Note

        Some operational lifecycle fields were simulated because the original dataset does not include
        ticket status, created date, resolved date, agent name, resolution time, and SLA status.
        This is clearly documented in the project.
        """
    )


def main():
    data = load_data()
    show_header()

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Select Page",
        [
            "Executive Overview",
            "Queue Performance",
            "SLA Performance",
            "Agent Workload",
            "Ticket Category Analysis",
            "Monthly Trend Analysis",
            "NLP Insights",
            "Business Recommendations",
            "AI Executive Summary",
            "About Project",
        ]
    )

    if page == "Executive Overview":
        executive_overview(data)
    elif page == "Queue Performance":
        queue_performance(data)
    elif page == "SLA Performance":
        sla_performance(data)
    elif page == "Agent Workload":
        agent_workload(data)
    elif page == "Ticket Category Analysis":
        category_analysis(data)
    elif page == "Monthly Trend Analysis":
        monthly_trends(data)
    elif page == "NLP Insights":
        nlp_insights(data)
    elif page == "Business Recommendations":
        recommendations(data)
    elif page == "AI Executive Summary":
        executive_summary_report()
    elif page == "About Project":
        project_about()


if __name__ == "__main__":
    main()