# 🛡️ Sanctions & Compliance Screening Automation  
### End-to-End OFAC • BIS • MEU/MIEU • CSL Screening & Risk Assessment System

This project is a complete, production-style **Sanctions & Compliance Screening Automation System** built using Python.  
It replicates real-world screening workflows used by **Global Trade Compliance, AML/KYC, and Regulatory Risk** teams at major organizations.

It includes:

- Multi-source sanctions data ingestion  
- Fuzzy matching sanctions screening engine  
- Risk scoring model (match score + geo risk + KYC)  
- Automated PDF screening report generator  
- Dashboard-ready analytics outputs  

---

## Features

### ✔ 1. **Data Integration Module**
Ingests and normalizes multiple global watchlists:

- OFAC SDN List  
- BIS Entity List  
- BIS UVL / DPL  
- BIS MEU  
- MIEU (synthetic sample)  
- Consolidated Screening List (CSL)  
- KYC Red Flags Dataset  

Produces:

```
master_screening_dataset.csv
master_screening_summary.csv
```

---

### ✔ 2. **Sanctions Screening Engine**
A fuzzy-matching system that evaluates:

- Name similarity (token set ratio)  
- Country similarity  
- Address similarity  
- Weighted match score  
- Threshold-based “Potential Match” classification  

Uses:  
`fuzzywuzzy`, Levenshtein distance, phonetic normalization.

---

### ✔ 3. **Risk Scoring Engine**
Weighted compliance risk model:

| Component          | Weight |
|-------------------|--------|
| Fuzzy Match Score | 50%    |
| Geographic Risk   | 30%    |
| KYC Flags         | 20%    |

Outputs:

- Final Risk Score  
- Risk Level (LOW / MEDIUM / HIGH)  
- Matched Watchlist Type  

---

### ✔ 4. **PDF Screening Report Generator**
Automatically creates a clean, professional 1-page PDF:

- Entity name & country  
- Screening results  
- Watchlist hit details  
- Risk level  
- Risk score breakdown  
- Timestamp  

Saved in:
```
/reports
```

---

### ✔ 5. **Dashboard-Ready Summaries**
Script + notebooks generate:

- List distribution chart  
- Summary tables  
- Entities per watchlist type  

Saved in:
```
/dashboard
```

---

## Project Structure

```
.
├── data/
│   ├── ofac_sdn.csv
│   ├── bis_entity_list.csv
│   ├── unverified_list.csv
│   ├── denied_persons_list.csv
│   ├── meu_list.csv
│   ├── military_intelligence_end_user_list.csv
│   ├── consolidated_screening_list.csv
│   ├── kyc_red_flags.csv
│   ├── master_screening_dataset.csv        <-- generated
│   └── master_screening_summary.csv        <-- generated
│
├── src/
│   ├── data_integration.py
│   ├── screening_engine.py
│   ├── risk_scoring.py
│   └── report_generator.py
│
├── reports/
│   └── <entity>_screening_report.pdf
│
├── dashboard/
│   └── list_distribution.png
│
├── notebooks/
│   ├── 01_data_integration.ipynb
│   ├── 02_screening_engine_demo.ipynb
│   └── 03_risk_scoring_demo.ipynb
│
└── README.md
```

---

## How to Run

### Install requirements
```bash
pip install pandas fuzzywuzzy python-Levenshtein reportlab matplotlib seaborn
```

### 1. Generate master dataset
```bash
python src/data_integration.py
```

### 2. Run screening
```python
from screening_engine import ScreeningEngine
engine = ScreeningEngine("data/master_screening_dataset.csv")
engine.screen("Mohammed Ali", country="Pakistan")
```

### 3. Risk scoring
```python
from risk_scoring import RiskScoringEngine
risk = RiskScoringEngine("data/master_screening_dataset.csv")
risk.score_entity("Mohammed Ali", country="Pakistan")
```

### 4. Generate PDF report
```python
from report_generator import ReportGenerator
report = ReportGenerator("reports")
report.generate_report("Mohammed Ali", screen_result, risk_result)
```

---

## Disclaimer  
All data used in this project is either:  
- publicly available (OFAC, BIS),  
- or synthetic (training/demo datasets).  

This project is for educational and analytical purposes only.

---


