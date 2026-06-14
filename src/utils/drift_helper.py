import pandas as pd
from pathlib import Path
from .logs_handler import logger
from src.database.db_ops import get_active_model
from src.database.connection import engine
from evidently import Report
from evidently.presets import DataDriftPreset


def get_current_dataframe():
    query = """
            SELECT
                age,
                income,
                credit_score,
                existing_loans,
                existing_loan_emi,
                employed,
                default,
                loan_amount,
                loan_tenure_months,
                emi_to_income_ratio,
                loan_to_income_ratio,
                employment_type
            FROM predictions
            ORDER BY id DESC
            LIMIT 1000
        """

    current_df = pd.read_sql(query, engine)
    return current_df


def generate_drift_report():

    logger.info("Drift report generation started")

    active_model = get_active_model()

    if active_model is None:
        raise ValueError(
            "No active model found."
        )

    project_root = Path(__file__).resolve().parents[2]

    reference_csv_path = (
        project_root
        / "csv"
        / active_model.reference_csv_name
    )

    if not reference_csv_path.exists():
        raise FileNotFoundError(
            f"Reference CSV not found: {active_model.reference_csv_name}"
        )

    reference_df = pd.read_csv(reference_csv_path)

    current_df = get_current_dataframe()

    if len(current_df) < 50:
        raise ValueError(
            "Minimum 50 prediction records required."
        )

    expected_columns = [
        "age",
        "income",
        "credit_score",
        "existing_loans",
        "existing_loan_emi",
        "employed",
        "default",
        "loan_amount",
        "loan_tenure_months",
        "emi_to_income_ratio",
        "loan_to_income_ratio",
        "employment_type"
    ]

    if list(reference_df.columns) != expected_columns:
        raise ValueError(
            "Reference CSV columns mismatch."
        )

    if list(current_df.columns) != expected_columns:
        raise ValueError(
            "Current dataset columns mismatch."
        )

    reports_dir = project_root / "reports"
    metrics_dir = project_root / "metrics"

    reports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    metrics_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    html_path = reports_dir / "drift_report.html"
    json_path = metrics_dir / "drift_metrics.json"

    if html_path.exists():
        html_path.unlink()

    if json_path.exists():
        json_path.unlink()

    report = Report(
        metrics=[
            DataDriftPreset()
        ]
    )

    snapshot = report.run(
        reference_data=reference_df,
        current_data=current_df
    )

    snapshot.save_html(str(html_path))

    snapshot.save_json(str(json_path))

    logger.info("Drift report generated successfully")

    return {
        "html_file": str(html_path),
        "json_file": str(json_path),
        "reference_csv_file" : str(reference_csv_path)
    }