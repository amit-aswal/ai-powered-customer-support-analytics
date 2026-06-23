# Phase 7 NLP and Text Analytics Report

## Objective

Phase 7 adds a text analytics layer to the AI-Powered Customer Support Analytics Platform.

This phase analyzes customer support ticket text to identify sentiment, urgency, keywords, and text-based operational risks.

---

## Dataset Used

Input dataset:

`data/silver/support_tickets_silver.parquet`

Total tickets analyzed:

**61,765**

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

**Negative** with **29,204 tickets**.

Total negative tickets:

**29,204**

Sentiment distribution is saved in:

`reports/phase7/phase7_sentiment_distribution.csv`

---

## Urgency Summary

Most common urgency level:

**Low Urgency** with **46,450 tickets**.

High urgency tickets:

**893**

Urgency distribution is saved in:

`reports/phase7/phase7_urgency_distribution.csv`

---

## Keyword Insights

The most frequent keyword is:

**die**

Top keyword report:

`reports/phase7/phase7_top_keywords_overall.csv`

---

## Text Quality Summary

| Metric | Value |
|---|---:|
| Average Word Count | 68.17 |
| Min Word Count | 1.0 |
| Max Word Count | 342.0 |
| Tickets With Urgency Keywords | 7,219 |
| Urgency Keyword Percentage | 11.69% |

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