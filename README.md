
## Phase 1 - Loan Default Prediction Workflow

![Phase 1 Prediction Architecture](./assets/phase_1_prediction_architecture.png)

### Overview

The prediction workflow serves as the primary entry point of DriftShield. Users submit loan application details through a Streamlit-based interface, which communicates with a FastAPI backend for processing.

The backend validates incoming data using Pydantic schemas before passing it to an XGBoost machine learning model for inference. Once the prediction is generated, the system stores both the input features and prediction results in PostgreSQL. These records later act as production data for drift detection and monitoring.

In parallel, the prediction output is sent to the Loan Advisor Engine, where risk factors and positive factors are analyzed and provided to a Groq-powered Large Language Model (LLM). The LLM generates human-readable loan recommendations and explanations that help users better understand the prediction outcome.

Finally, the backend combines the prediction result and AI-generated recommendation into a single API response and returns it to the frontend for display.

### Workflow

1.  User submits loan application data through the Streamlit interface.
    
2.  FastAPI receives the request and validates the payload using Pydantic schemas.
    
3.  The validated data is passed to the XGBoost model for inference.
    
4.  The model returns the predicted default status and probability score.
    
5.  Input features, prediction results, and timestamps are stored in PostgreSQL as prediction logs.
    
6.  The Loan Advisor Engine analyzes risk indicators and prepares context for the LLM.
    
7.  Groq LLM generates personalized loan recommendations and explanations.
    
8.  The backend combines prediction outputs and AI insights into a JSON response.
    
9.  The Streamlit frontend displays the final prediction result and AI-generated recommendation to the user.

---
---

# Phase 2 – Data Drift Detection & AI-Powered Analysis

![Phase 2 - Drift Detection Architecture](assets/phase_2_drift_detection.png)

## Overview

After the model is deployed, every prediction request is continuously stored as production data inside the PostgreSQL database. These production logs become the primary source for monitoring data quality and identifying distribution changes over time.

When a user generates a drift report from the Streamlit dashboard, the backend invokes the FastAPI Drift Detection API. The API loads two datasets: the original training reference dataset used during model development and the accumulated production prediction logs collected from real-world inference requests.

Both datasets are analyzed using Evidently AI, which performs statistical comparisons across all input features to determine whether the production data distribution has deviated from the original training data. The generated report provides a comprehensive visualization of feature-level drift and the overall health of the deployed model.

Once the drift analysis is completed, Evidently AI produces two outputs. The first is an interactive HTML report rendered directly inside the Streamlit dashboard, allowing users to visually inspect drift statistics and feature comparisons. The second output is a structured JSON file containing detailed drift metrics, which serves as input for the AI-powered analysis stage.

The drift metrics are then processed by the Groq Large Language Model (LLM). Instead of exposing raw statistical values, the LLM interprets the detected drift, identifies the affected features, explains their potential impact on prediction reliability, and generates business-friendly insights that help users understand the current condition of the deployed model.

This pipeline combines statistical drift detection with natural language reasoning, enabling both technical users and non-technical stakeholders to understand model degradation through visual reports as well as AI-generated explanations.

---

## Workflow Summary

1. The user initiates **Generate Report** from the Streamlit interface.
2. The FastAPI Drift Detection API receives the request.
3. Production prediction logs are retrieved from the PostgreSQL database.
4. The original model training reference dataset is loaded.
5. Evidently AI compares both datasets to detect feature-level data drift.
6. An interactive HTML drift report is generated for visualization.
7. Structured drift metrics are exported as a JSON artifact.
8. The JSON drift metrics are processed by the Groq LLM.
9. The LLM analyzes the drifted features and generates AI-powered insights.
10. The frontend displays both the Evidently AI report and the AI-generated drift analysis.

---