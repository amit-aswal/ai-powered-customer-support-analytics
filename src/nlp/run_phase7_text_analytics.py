from pathlib import Path
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt


SILVER_FILE = Path("data/silver/support_tickets_silver.parquet")

GOLD_TEXT_DIR = Path("data/gold/text_analytics")
REPORT_DIR = Path("reports/phase7")
CHART_DIR = REPORT_DIR / "charts"

GOLD_TEXT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


POSITIVE_WORDS = {
    "good", "great", "excellent", "thanks", "thank", "helpful", "resolved",
    "fixed", "working", "success", "successful", "appreciate", "perfect",
    "satisfied", "happy", "quick", "fast", "clear", "useful", "supportive"
}

NEGATIVE_WORDS = {
    "bad", "poor", "issue", "problem", "error", "failed", "failure", "fail",
    "angry", "frustrated", "slow", "delay", "delayed", "wrong", "broken",
    "not working", "unable", "refund", "cancel", "complaint", "stuck",
    "bug", "crash", "payment failed", "login failed", "missing", "damaged"
}

URGENCY_WORDS = {
    "urgent", "immediately", "asap", "critical", "emergency", "blocked",
    "not working", "unable", "down", "failed", "failure", "crash",
    "cannot", "can't", "stuck", "priority", "important", "escalate"
}

STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "have", "has",
    "had", "are", "was", "were", "you", "your", "our", "can", "could",
    "would", "should", "will", "shall", "please", "about", "into", "there",
    "their", "they", "them", "then", "than", "also", "been", "being",
    "because", "which", "what", "when", "where", "how", "why", "not",
    "but", "all", "any", "each", "few", "more", "most", "other", "some",
    "such", "only", "own", "same", "too", "very", "just", "now", "get",
    "got", "make", "made", "using", "use", "used", "need", "want", "ticket",
    "support", "customer", "hello", "hi", "dear", "regards", "thanks"
}


def clean_text_for_nlp(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text):
    words = clean_text_for_nlp(text).split()
    return [
        word for word in words
        if word not in STOPWORDS and len(word) > 2
    ]


def calculate_sentiment_score(text):
    text_clean = clean_text_for_nlp(text)
    words = text_clean.split()

    positive_count = 0
    negative_count = 0

    for word in POSITIVE_WORDS:
        if word in words or word in text_clean:
            positive_count += 1

    for word in NEGATIVE_WORDS:
        if word in words or word in text_clean:
            negative_count += 1

    return positive_count - negative_count


def assign_sentiment_label(score):
    if score > 0:
        return "Positive"
    if score < 0:
        return "Negative"
    return "Neutral"


def calculate_urgency_score(row):
    text = clean_text_for_nlp(row.get("combined_text", ""))
    priority = str(row.get("priority_clean", "")).lower()

    score = 0

    if priority in ["critical", "urgent"]:
        score += 5
    elif priority == "high":
        score += 4
    elif priority in ["medium", "normal"]:
        score += 2
    elif priority == "low":
        score += 1

    for word in URGENCY_WORDS:
        if word in text:
            score += 2

    if row.get("sla_status") == "SLA Breached":
        score += 3

    if row.get("status") == "Escalated":
        score += 3

    if len(text) > 1000:
        score += 1

    return score


def assign_urgency_label(score):
    if score >= 9:
        return "High Urgency"
    if score >= 5:
        return "Medium Urgency"
    return "Low Urgency"


def get_top_keywords(text_series, top_n=30):
    counter = Counter()

    for text in text_series.dropna():
        counter.update(tokenize(text))

    return pd.DataFrame(
        counter.most_common(top_n),
        columns=["keyword", "frequency"]
    )


def save_csv(df, filename):
    output_path = REPORT_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved: {output_path}")


def save_bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename, horizontal=False):
    plt.figure(figsize=(10, 6))

    if horizontal:
        plt.barh(df[y_col], df[x_col])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.gca().invert_yaxis()
    else:
        plt.bar(df[x_col], df[y_col])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha="right")

    plt.title(title)
    plt.tight_layout()

    output_path = CHART_DIR / filename
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved chart: {output_path}")


def create_nlp_features(df):
    print("Creating NLP features...")

    df = df.copy()

    if "combined_text" not in df.columns:
        df["combined_text"] = (
            df.get("subject_clean", "").fillna("") + " " +
            df.get("body_clean", "").fillna("")
        )

    df["nlp_clean_text"] = df["combined_text"].fillna("").apply(clean_text_for_nlp)
    df["sentiment_score"] = df["combined_text"].fillna("").apply(calculate_sentiment_score)
    df["sentiment_label"] = df["sentiment_score"].apply(assign_sentiment_label)

    df["urgency_score"] = df.apply(calculate_urgency_score, axis=1)
    df["urgency_label"] = df["urgency_score"].apply(assign_urgency_label)

    df["word_count"] = df["nlp_clean_text"].apply(lambda x: len(x.split()))
    df["has_urgency_keyword"] = df["nlp_clean_text"].apply(
        lambda x: any(word in x for word in URGENCY_WORDS)
    )

    return df


def create_reports(df):
    print("Creating Phase 7 reports...")

    sentiment_distribution = (
        df.groupby("sentiment_label")
        .size()
        .reset_index(name="ticket_count")
        .sort_values("ticket_count", ascending=False)
    )
    sentiment_distribution["ticket_percentage"] = (
        sentiment_distribution["ticket_count"] * 100.0 / len(df)
    ).round(2)

    urgency_distribution = (
        df.groupby("urgency_label")
        .size()
        .reset_index(name="ticket_count")
        .sort_values("ticket_count", ascending=False)
    )
    urgency_distribution["ticket_percentage"] = (
        urgency_distribution["ticket_count"] * 100.0 / len(df)
    ).round(2)

    sentiment_by_category = (
        df.groupby(["ticket_category_rule_based", "sentiment_label"])
        .size()
        .reset_index(name="ticket_count")
        .sort_values(["ticket_category_rule_based", "ticket_count"], ascending=[True, False])
    )

    sentiment_by_queue = (
        df.groupby(["queue_clean", "sentiment_label"])
        .size()
        .reset_index(name="ticket_count")
        .sort_values(["queue_clean", "ticket_count"], ascending=[True, False])
    )

    urgency_by_priority = (
        df.groupby(["priority_clean", "urgency_label"])
        .size()
        .reset_index(name="ticket_count")
        .sort_values(["priority_clean", "ticket_count"], ascending=[True, False])
    )

    top_keywords_overall = get_top_keywords(df["combined_text"], top_n=30)

    keyword_rows = []
    for category, group in df.groupby("ticket_category_rule_based"):
        top_words = get_top_keywords(group["combined_text"], top_n=10)
        for _, row in top_words.iterrows():
            keyword_rows.append({
                "ticket_category": category,
                "keyword": row["keyword"],
                "frequency": row["frequency"]
            })

    top_keywords_by_category = pd.DataFrame(keyword_rows)

    top_negative_tickets = (
        df[df["sentiment_label"] == "Negative"]
        .sort_values(["urgency_score", "sentiment_score"], ascending=[False, True])
        [
            [
                "ticket_id",
                "queue_clean",
                "priority_clean",
                "status",
                "sla_status",
                "ticket_category_rule_based",
                "sentiment_score",
                "urgency_score",
                "combined_text_length",
                "combined_text"
            ]
        ]
        .head(50)
    )

    text_quality_summary = pd.DataFrame([
        {
            "total_tickets": len(df),
            "avg_word_count": round(df["word_count"].mean(), 2),
            "min_word_count": int(df["word_count"].min()),
            "max_word_count": int(df["word_count"].max()),
            "tickets_with_urgency_keywords": int(df["has_urgency_keyword"].sum()),
            "urgency_keyword_percentage": round(df["has_urgency_keyword"].mean() * 100, 2),
            "negative_tickets": int((df["sentiment_label"] == "Negative").sum()),
            "positive_tickets": int((df["sentiment_label"] == "Positive").sum()),
            "neutral_tickets": int((df["sentiment_label"] == "Neutral").sum())
        }
    ])

    save_csv(sentiment_distribution, "phase7_sentiment_distribution.csv")
    save_csv(urgency_distribution, "phase7_urgency_distribution.csv")
    save_csv(sentiment_by_category, "phase7_sentiment_by_category.csv")
    save_csv(sentiment_by_queue, "phase7_sentiment_by_queue.csv")
    save_csv(urgency_by_priority, "phase7_urgency_by_priority.csv")
    save_csv(top_keywords_overall, "phase7_top_keywords_overall.csv")
    save_csv(top_keywords_by_category, "phase7_top_keywords_by_category.csv")
    save_csv(top_negative_tickets, "phase7_top_negative_tickets.csv")
    save_csv(text_quality_summary, "phase7_text_quality_summary.csv")

    create_charts(
        sentiment_distribution,
        urgency_distribution,
        top_keywords_overall,
        sentiment_by_category
    )

    create_markdown_report(
        df,
        sentiment_distribution,
        urgency_distribution,
        top_keywords_overall,
        text_quality_summary
    )


def create_charts(sentiment_distribution, urgency_distribution, top_keywords_overall, sentiment_by_category):
    save_bar_chart(
        sentiment_distribution,
        x_col="sentiment_label",
        y_col="ticket_count",
        title="Ticket Sentiment Distribution",
        xlabel="Sentiment",
        ylabel="Ticket Count",
        filename="sentiment_distribution.png"
    )

    save_bar_chart(
        urgency_distribution,
        x_col="urgency_label",
        y_col="ticket_count",
        title="Ticket Urgency Distribution",
        xlabel="Urgency Level",
        ylabel="Ticket Count",
        filename="urgency_distribution.png"
    )

    save_bar_chart(
        top_keywords_overall.head(15).sort_values("frequency", ascending=True),
        x_col="frequency",
        y_col="keyword",
        title="Top 15 Keywords in Support Tickets",
        xlabel="Frequency",
        ylabel="Keyword",
        filename="top_15_keywords.png",
        horizontal=True
    )

    negative_by_category = (
        sentiment_by_category[sentiment_by_category["sentiment_label"] == "Negative"]
        .sort_values("ticket_count", ascending=False)
        .head(10)
    )

    if len(negative_by_category) > 0:
        save_bar_chart(
            negative_by_category.sort_values("ticket_count", ascending=True),
            x_col="ticket_count",
            y_col="ticket_category_rule_based",
            title="Top Categories by Negative Sentiment",
            xlabel="Negative Ticket Count",
            ylabel="Ticket Category",
            filename="negative_sentiment_by_category.png",
            horizontal=True
        )


def create_markdown_report(df, sentiment_distribution, urgency_distribution, top_keywords, text_quality):
    total_tickets = len(df)

    top_sentiment = sentiment_distribution.iloc[0]
    top_urgency = urgency_distribution.iloc[0]
    top_keyword = top_keywords.iloc[0] if len(top_keywords) > 0 else None
    tq = text_quality.iloc[0]

    negative_count = int((df["sentiment_label"] == "Negative").sum())
    high_urgency_count = int((df["urgency_label"] == "High Urgency").sum())

    report = f"""
# Phase 7 NLP and Text Analytics Report

## Objective

Phase 7 adds a text analytics layer to the AI-Powered Customer Support Analytics Platform.

This phase analyzes customer support ticket text to identify sentiment, urgency, keywords, and text-based operational risks.

---

## Dataset Used

Input dataset:

`data/silver/support_tickets_silver.parquet`

Total tickets analyzed:

**{total_tickets:,}**

---

## NLP Features Created

The following NLP features were created:

| Feature | Description |
|---|---|
| nlp_clean_text | Cleaned text for NLP analysis |
| sentiment_score | Rule-based sentiment score |
| sentiment_label | Positive, Negative, or Neutral |
| urgency_score | Rule-based urgency score |
| urgency_label | Low, Medium, or High Urgency |
| word_count | Number of words in cleaned ticket text |
| has_urgency_keyword | Flag for urgency-related words |

---

## Sentiment Summary

Most common sentiment:

**{top_sentiment["sentiment_label"]}** with **{int(top_sentiment["ticket_count"]):,} tickets**.

Total negative tickets:

**{negative_count:,}**

Sentiment distribution is saved in:

`reports/phase7/phase7_sentiment_distribution.csv`

---

## Urgency Summary

Most common urgency level:

**{top_urgency["urgency_label"]}** with **{int(top_urgency["ticket_count"]):,} tickets**.

High urgency tickets:

**{high_urgency_count:,}**

Urgency distribution is saved in:

`reports/phase7/phase7_urgency_distribution.csv`

---

## Keyword Insights

The most frequent keyword is:

**{top_keyword["keyword"] if top_keyword is not None else "Not available"}**

Top keyword report:

`reports/phase7/phase7_top_keywords_overall.csv`

---

## Text Quality Summary

| Metric | Value |
|---|---:|
| Average Word Count | {tq["avg_word_count"]} |
| Min Word Count | {tq["min_word_count"]} |
| Max Word Count | {tq["max_word_count"]} |
| Tickets With Urgency Keywords | {int(tq["tickets_with_urgency_keywords"]):,} |
| Urgency Keyword Percentage | {tq["urgency_keyword_percentage"]}% |

---

## Business Value

This NLP layer helps support leaders understand:

- Which tickets are negative
- Which tickets are urgent
- Which issue categories contain more negative sentiment
- Which queues receive more negative tickets
- Which words appear most often in support tickets
- Which tickets should be reviewed first

---

## Important Note

This phase uses rule-based NLP for portfolio demonstration.

The sentiment and urgency logic is transparent and reproducible. In a production system, this can be upgraded using machine learning models, transformer-based NLP models, or LLM-based classification.

---

## Phase 7 Outputs

### CSV Reports

- phase7_sentiment_distribution.csv
- phase7_urgency_distribution.csv
- phase7_sentiment_by_category.csv
- phase7_sentiment_by_queue.csv
- phase7_urgency_by_priority.csv
- phase7_top_keywords_overall.csv
- phase7_top_keywords_by_category.csv
- phase7_top_negative_tickets.csv
- phase7_text_quality_summary.csv

### Charts

- sentiment_distribution.png
- urgency_distribution.png
- top_15_keywords.png
- negative_sentiment_by_category.png

### Gold Text Analytics Dataset

- data/gold/text_analytics/support_tickets_text_analytics.parquet
- data/gold/text_analytics/support_tickets_text_analytics.csv
"""

    output_path = REPORT_DIR / "phase7_nlp_text_analytics_report.md"
    output_path.write_text(report.strip(), encoding="utf-8")
    print(f"Saved report: {output_path}")


def main():
    if not SILVER_FILE.exists():
        raise FileNotFoundError(
            "Silver dataset not found. Complete Phase 2 before running Phase 7."
        )

    print("Loading silver dataset...")
    df = pd.read_parquet(SILVER_FILE)

    df_nlp = create_nlp_features(df)

    print("Saving gold text analytics dataset...")
    parquet_path = GOLD_TEXT_DIR / "support_tickets_text_analytics.parquet"
    csv_path = GOLD_TEXT_DIR / "support_tickets_text_analytics.csv"

    df_nlp.to_parquet(parquet_path, index=False)
    df_nlp.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"Saved: {parquet_path}")
    print(f"Saved: {csv_path}")

    create_reports(df_nlp)

    print("Phase 7 NLP and text analytics completed successfully.")


if __name__ == "__main__":
    main()
