# Checkout_flow_friction_Audit
Automated pipeline tracking why shoppers abandon checkout — GA4 events → Databricks medallion (Bronze/Silver/Gold) → live dashboard → daily auto-emailed report. Found 76.97% drop-off at View→Cart, the biggest funnel leak. End-to-end data engineering, zero manual steps.

# 🛒 GA4 Checkout Friction Analytics

An end-to-end, automated analytics pipeline that identifies exactly where and why online shoppers abandon the checkout process — from raw event tracking to a scheduled, stakeholder-ready email report.

> 7 out of 10 shoppers add something to their cart and vanish. This project finds out exactly where — and tells the right person, automatically, every single day.

---

## 📌 Overview

This project simulates a realistic e-commerce checkout funnel using **Google Analytics 4 (GA4)**, processes the event data through a **Bronze → Silver → Gold medallion pipeline** in **Databricks**, and surfaces the results in a live **Databricks SQL Dashboard** that is automatically emailed to stakeholders on a daily schedule — with zero manual intervention once deployed.

**Funnel stages tracked:**
`session_start → view_item → add_to_cart → begin_checkout → add_payment_info → purchase`

---

## 🏗️ Architecture

```
GA4 Measurement Protocol (simulated events)
        │
        ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Bronze Layer │ ──▶ │  Silver Layer │ ──▶ │  Gold Layer   │
│  Raw events   │     │  Cleaned +    │     │  Drop-off %   │
│  (as-is)      │     │  deduplicated │     │  + conversion │
└───────────────┘     └───────────────┘     └───────────────┘
                                                     │
                                                     ▼
                                      Databricks SQL Dashboard
                                                     │
                                                     ▼
                                      Scheduled Email Report → Manager Inbox
```

| Layer | Purpose |
|---|---|
| **Bronze** | Raw GA4 events, ingested exactly as received (append-only, full history) |
| **Silver** | Deduplicated, typed, and cleaned — one row per `(event_date, event_name)` |
| **Gold** | Pivoted daily funnel metrics — stage-to-stage drop-off % and overall conversion % |

---

## ⚙️ Tech Stack

- **Google Analytics 4** — Measurement Protocol (event simulation) + Data API (event retrieval)
- **Databricks** — Lakehouse platform, PySpark, Delta Lake
- **Databricks Jobs** — scheduled nightly pipeline orchestration
- **Databricks SQL Dashboards** — visualization + scheduled email reporting
- **Python** — `requests`, `google-analytics-data`, `pyspark`

---

## 📂 Repository Structure

```
├── ga4_event_simulator.py              # Simulates realistic funnel sessions via GA4 Measurement Protocol
├── Checkout_Friction_Medallion_Pipeline.py   # Databricks notebook: Bronze → Silver → Gold pipeline
├── README.md
└── docs/
    └── screenshots/                    # Dashboard, GA4, and email report screenshots
```

---

## 🚀 How It Works

1. **Event Simulation** (`ga4_event_simulator.py`)
   Generates realistic funnel sessions with randomized drop-off at each stage (mirroring real-world abandonment behavior), and sends them to a GA4 property via the Measurement Protocol.

2. **Bronze Layer — Raw Ingestion**
   Pulls raw event counts from the GA4 Data API and appends them to a Bronze Delta table, preserving full history.

3. **Silver Layer — Cleaning**
   Deduplicates using a `ROW_NUMBER()` window function (keeping the most recently ingested row per date/event) and casts types correctly.

4. **Gold Layer — Business Metrics**
   Pivots the funnel into daily stage counts and calculates drop-off percentages using `try_divide()` for safe handling of zero-traffic days.

5. **Automation**
   A scheduled Databricks Job (`Checkout_flow_audit`) re-runs the full pipeline nightly — no manual reruns required.

6. **Dashboard + Reporting**
   A Databricks SQL Dashboard visualizes conversion trends, KPIs, and stage-by-stage drop-off, and is scheduled to email a snapshot directly to stakeholders every day.

---

## 📊 Key Finding

The largest and most consistent friction point is between **product view and add-to-cart**, with an average **76.97% drop-off** at that single stage — meaning roughly 3 out of every 4 interested visitors are lost before they even engage with the cart.

| Metric | Value |
|---|---|
| Avg. Conversion Rate | 3.47% |
| Total Purchases | 32 |
| Total Views | 682 |
| Avg. Drop-off (View → Cart) | 76.97% |

---

## 🖼️ Screenshots



- `dashboard_trends.png` — Conversion & Funnel Trends + KPIs
- `dashboard_dropoff.png` — Stage-by-Stage Drop-off Analysis
- `dashboard_insights.png` — Automated Key Insights panel
- `job_runs.png` — Scheduled Databricks Job run history
- `email_report.png` — Automated daily email report

---

## ⚠️ Notes on Data & Credentials

- Traffic in this project is **simulated**, not real user data — it was generated specifically to build and demonstrate the pipeline.
- `SERVICE_ACCOUNT_PATH`, `PROPERTY_ID`, and other credentials in the code are placeholders — **replace with your own GA4 service account and property ID**, and never commit real credentials or `.json` key files to this repo (add them to `.gitignore`).

---

## 🔮 Future Scope

- Replace simulated traffic with a real, live storefront
- Add cohort/segment-level funnel analysis (device, source, geography)
- Introduce a predictive model to flag at-risk sessions before they abandon
- Integrate with A/B testing to measure the impact of funnel fixes directly
- Expand alerting beyond email (e.g. Slack/Teams) for faster response

---

## 🙋 About This Project

Built as part of a Summer Internship Project (SIP) — a working demonstration of end-to-end data engineering: event tracking, Lakehouse architecture, automated orchestration, and stakeholder-facing reporting, mirroring how real analytics teams operate in production.
