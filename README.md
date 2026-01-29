# Companies House Data Processing Pipeline 🏢🇬🇧

This repository contains a collection of Python scripts used to **clean, filter, and process UK Companies House data**, with a focus on officers, PSCs (Persons with Significant Control), and company-level datasets.

It is designed as a **modular data pipeline**, where each script handles a specific transformation step and can be reused or extended independently.

---

## 📂 Project Structure

```text
.
├── clean_officers.py          # Cleans and normalizes company officer data
├── clean_psc.py               # Cleans and processes PSC (Persons with Significant Control) data
├── items.py                   # Shared items / schemas used across the pipeline
├── keep_selected_columns.py   # Keeps only required columns from large datasets
├── load_company_numbers.py    # Loads and filters target company numbers
├── middlewares.py             # Custom middleware logic
├── pipelines.py               # Data processing pipelines
└── settings.py                # Project-wide configuration and settings

📌 Use Cases

UK company intelligence platforms

M&A sourcing and deal origination

Founder / director discovery

Data enrichment pipelines

Internal analytics on Companies House data
