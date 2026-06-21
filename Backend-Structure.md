

##  Drifshield Backend Structure

> **Note:** The `csv/`, `logs/`, `metrics/`, `models/`, and `reports/` directories are mounted from an AWS EBS (Elastic Block Store) volume. These folders are not version-controlled and are excluded from GitHub.
>
> **EBS (Elastic Block Store)** is used as persistent storage for model artifacts, drift reports, metrics, logs, and datasets.
---
```
driftshield/
│
├── .github/                 # CI/CD via Github Actions
│	└── workflows/
│		└── ci_cd.yml
│
├── csv/						# Mounted with AWS EBS Volume
│	└── train_V1_reference.csv  # Used for Model training
│	└── train_V2_reference.csv
│
├── logs/                     # Mounted with AWS EBS Volume
│	└── 2026-05-25.log        # Daily logs
│	└── 2026-05-26.log
│
├── metrics/				  # Mounted with AWS EBS Volume
│	└── drift_metrics.json    # Generated from Evidently AI
│	└── train_V1_metrics.json # Model accuracy & Scores at training 
│	└── train_V2_metrics.json
│ 
├── models/                   # Mounted with AWS EBS Volume
│	 └── xgboost_V1_model.pkl
│	 └── xgboost_V2_model.pkl 
│	 └── xgboost_V1_scaler.pkl
│	 └── xgboost_V2_scaler.pkl
│
├── reports/   				 # Mounted with AWS EBS Volume
│	 └── drift_report.html   # Generated from Evidently AI
│
├── notebooks/
│   └── model_training.ipynb
│
├── src/
│	├── api/
│	│	├── routers/      # FastAPI APIRouters
│	│	│	└── prediction_route.py
│	│	│	└── drift_route.py
│	│	│	└── model_registry_route.py
│	│	│
│	│	├── schemas/     # Pydantic Model Schema 
│	│	│	└── __init__.py
│	│	│	└── schemas.py
│	│
│	├── config/
│	│	└── config.py
│	│
│	├── database/
│	│	└── connection.py
│	│	└── db_ops.py
│	│	└── models.py    # Table structure
│	│
│	├── llm/
│	│	└── __init__.py
│	│	└── groq_client.py
│	│	└── llm_services.py
│	│	└── prompts.py
│	│
│	├── models/             # Loading models & use into application
│	│	└── evaluate.py
│	│	└── load_models.py  # Loading models from AWS EBS Volume
│	│	└── prediction.py   # Making prediction 
│	│
│	├── utils/               # Utility files for application
│	│	└── drift_helper.py  # Helper file for generating Data drift
│	│	└── loan_advisor.py  # Smart loan suggestion and risk calculation
│	│	└── logs_handler.py
│
├── app.py              # FastAPI main controller & All APIRouters registered here
├── Dockerfile
├── README.md           # Detailed Architecture
├── Backend-Structure.md  
├── requirements.txt    # All necessary packages for this application
├── .dockerignore 
├── .gitignore
├── .env                # (excluded from GitHub)
```
---
### AWS EBS Mounted Directories

| Directory | Purpose |
|------------|----------|
| models/ | Store trained models and scalers |
| reports/ | Store generated Evidently reports |
| metrics/ | Store drift and training metrics |
| logs/ | Store Application logs |
| csv/ | Store reference datasets and uploaded training data |
---
### Database Tables

1. predictions
    - Stores incoming prediction requests and model outputs.
    - Used as production data for drift detection and Evidently AI reporting.

2. model_registry
    - Stores metadata for uploaded model artifacts.
    - Tracks model versions, datasets, metrics, and deployment status.
    - Maps artifacts stored in `csv/`, `metrics/`, and `models/`.
    - Maintains active and historical model versions.
---

### Model Registry Upload Requirements

Each new model version must include the following artifacts:

| Artifact | Naming Convention |
|-----------|------------------|
| Model File | `<version>_model.pkl` |
| Scaler File | `<version>_scaler.pkl` |
| Reference Dataset | `<version>_reference.csv` |
| Training Metrics | `<version>_metrics.json` |

Example:

- `xgboost_V1_model.pkl`
- `xgboost_V1_scaler.pkl`
- `train_V1_reference.csv`
- `train_V1_metrics.json`
or
- `xgboost_V2_model.pkl`
- `xgboost_V2_scaler.pkl`
- `train_V2_reference.csv`
- `train_V2_metrics.json`

> **Important:** All four artifacts must be uploaded together during every model upgrade. The application validates file naming conventions to ensure version consistency and prevent accidental deployment of mismatched model artifacts.