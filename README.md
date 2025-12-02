# 🛡️ Sanctions & Compliance Screening Automation

This project is a work-in-progress system for automating global sanctions and compliance screening.  
It integrates multiple regulatory datasets (OFAC, BIS, UN, MEU/MIEU) and builds a unified master list for further screening, risk scoring, and analytics.

### ✔ Current Features
- Data integration from multiple sanctions lists  
- Schema normalization and merging  
- Generation of a master screening dataset  
- Initial summary analytics via Jupyter notebooks  

### ✔ Datasets Included
- OFAC SDN List (`ofac_sdn.csv`)
- BIS Entity List (`bis_entity_list.csv`)
- BIS UVL / DPL / MEU Lists  
- MIEU List (synthetic)
- Consolidated Screening List
- KYC Red Flags (synthetic)

### ✔ Auto-Generated Outputs
- `master_screening_dataset.csv`
- `master_screening_summary.csv`


### ✔ How to Run Integration
```bash
python src/data_integration.py




