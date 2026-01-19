# Sales Analytics System

## Overview
A Python-based system designed to process messy sales data, enrich it with external product information using the DummyJSON API, and generate comprehensive business reports. This project demonstrates file handling, data cleaning, API integration, and statistical analysis.

## Repository Structure
```text
sales-analytics-system/
│
├── data/
│   ├── sales_data.txt          # Raw input data
│   └── enriched_sales_data.txt # Processed data with API info
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py         # Handles reading, parsing, and cleaning files
│   ├── data_processor.py       # Handles calculations and report generation
│   └── api_handler.py          # Handles interaction with DummyJSON API
│
├── output/
│   └── sales_report.txt        # Final generated report
│
├── main.py                     # Entry point of the application
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation


# Sales Analytics System

## Overview
A Python-based system to analyze sales data, enrich it with external API data from DummyJSON, and generate comprehensive business reports.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   Round 1: updated documentation
   Round 2: added project details
   Round 3: minor fix