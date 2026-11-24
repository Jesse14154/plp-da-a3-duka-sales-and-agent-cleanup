
# PLP Data Analytics Assignment 3
## Duka Electronics Sales Exploration and Mobile-Money Agent Data Cleaning

## Project Overview

This project contains two data analytics engagements completed using Python, Pandas, NumPy, Google Sheets and Excel.

### Engagement 1: Duka Electronics Sales Exploration

The first engagement explores 1,000 sales transactions from five Duka Electronics branches between January and June 2026.

The analysis includes:
- Initial dataset inspection.
- Data exploration and descriptive statistics.
- Revenue calculations.
- Branch performance comparisons.
- Product revenue and sales volume analysis.
- Weekday versus weekend sales analysis.
- Monthly revenue comparisons.
- Filtering and exporting Premium Online orders from Nairobi and Mombasa.
- Spreadsheet analysis using SUMIFS, XLOOKUP and PivotTables.

### Duka Electronics Executive Summary

1. Nairobi was the highest-performing branch, generating KES 26,106,100 from 376 orders.
2. Laptops generated the highest product revenue at KES 41,535,000, while tablets recorded the highest sales volume at 691 units.
3. Weekdays generated KES 51,856,200 from 723 orders, while weekends recorded a higher average order revenue of KES 71,972.20 compared with KES 71,723.65 on weekdays.
4. April was the best month with KES 13,518,300, while June was the weakest with KES 10,903,400. April revenue was 23.98% higher than June.
5. Premium Online orders from Nairobi and Mombasa totalled 83 orders, generating KES 10,218,000.

### Engagement 2: Mobile-Money Agent Data Cleaning

The second engagement focuses on cleaning and validating mobile-money agent transaction records.

The original transaction dataset contained 612 rows and the agent register contained 20 agents.

The cleaning process included:
- Identifying and removing duplicate transaction IDs.
- Standardising transaction types.
- Converting transaction amounts into numeric values.
- Handling missing amounts using transaction-type medians.
- Standardising transaction dates.
- Detecting and flagging potential outliers using the IQR method.
- Merging transactions with the agent register.
- Identifying unknown agent references.
- Producing county and weekly transaction summaries.
- Building a reusable cleaning function in `cleaning_pipeline.py`.

After cleaning, the final transaction dataset contained 600 unique records. Twelve duplicate records were removed.

Seven transactions referenced an unknown agent ID, AG099. These records were retained and flagged for investigation.

Twenty missing transaction amounts were imputed and 53 potential outliers were flagged for review rather than automatically deleted.

## Project Structure

```text
plp-da-a3-duka-sales-and-agent-cleanup/
├── README.md
├── generate_data.py
├── duka_sales_exploration.ipynb
├── cleaning_pipeline.py
├── agent_cleanup.ipynb
├── requirements.txt
├── excel/
│   └── duka_branch_summary.xlsx
└── outputs/
    ├── premium_online_coast_capital.csv
    └── agent_transactions_clean.csv
