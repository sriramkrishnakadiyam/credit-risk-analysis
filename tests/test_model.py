"""
Tests for model training, loading, and prediction utilities.

Run with:  python -m pytest tests/ -v
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.config import MODEL_PATH, PREPROCESSOR_PATH, METRICS_PATH


# ── Model artifact tests ───────────────────────────────────────


def test_model_file_exists():
    """Model artifact should exist after training."""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model not trained yet — run train_model.py first.")
    assert os.path.exists(MODEL_PATH)


def test_preprocessor_file_exists():
    """Preprocessor artifact should exist after training."""
    if not os.path.exists(PREPROCESSOR_PATH):
        pytest.skip("Model not trained yet — run train_model.py first.")
    assert os.path.exists(PREPROCESSOR_PATH)


def test_metrics_file_exists():
    """Metrics artifact should exist after training."""
    if not os.path.exists(METRICS_PATH):
        pytest.skip("Model not trained yet — run train_model.py first.")
    assert os.path.exists(METRICS_PATH)


# ── Model loading tests ────────────────────────────────────────


def test_load_model():
    """Model should load without error."""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model not trained yet.")
    from src.model_utils import load_model
    model = load_model()
    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")


def test_load_preprocessor():
    """Preprocessor should load without error."""
    if not os.path.exists(PREPROCESSOR_PATH):
        pytest.skip("Model not trained yet.")
    from src.model_utils import load_preprocessor
    preprocessor = load_preprocessor()
    assert hasattr(preprocessor, "transform")


def test_load_metrics():
    """Metrics should be a dict with expected keys."""
    if not os.path.exists(METRICS_PATH):
        pytest.skip("Model not trained yet.")
    from src.model_utils import load_metrics
    metrics = load_metrics()
    assert isinstance(metrics, dict)
    for key in ["accuracy", "precision", "recall", "f1_score", "roc_auc"]:
        assert key in metrics
        assert 0 <= metrics[key] <= 1


# ── Prediction tests ───────────────────────────────────────────


def test_predict_single_valid():
    """predict_single should return expected keys."""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model not trained yet.")
    from src.model_utils import predict_single

    input_data = {
        "duration_months": 24,
        "credit_amount": 5000,
        "installment_rate": 2,
        "residence_since": 2,
        "age": 35,
        "num_existing_credits": 1,
        "num_dependents": 1,
        "status_checking_account": "A12",
        "credit_history": "A32",
        "purpose": "A43",
        "savings_account": "A62",
        "employment_since": "A73",
        "personal_status_sex": "A93",
        "other_debtors": "A101",
        "property": "A121",
        "other_installment_plans": "A143",
        "housing": "A152",
        "job": "A173",
        "telephone": "A192",
        "foreign_worker": "A201",
    }

    result = predict_single(input_data)

    assert "risk_category" in result
    assert result["risk_category"] in ["Low Risk", "Medium Risk", "High Risk"]
    assert "probability_bad" in result
    assert "probability_good" in result
    assert 0 <= result["probability_bad"] <= 1
    assert 0 <= result["probability_good"] <= 1
    assert abs(result["probability_bad"] + result["probability_good"] - 1.0) < 0.01


def test_classify_risk_boundaries():
    """Risk classification thresholds should work correctly."""
    from src.model_utils import classify_risk

    assert classify_risk(0.0) == "Low Risk"
    assert classify_risk(0.15) == "Low Risk"
    assert classify_risk(0.30) == "Low Risk"
    assert classify_risk(0.31) == "Medium Risk"
    assert classify_risk(0.50) == "Medium Risk"
    assert classify_risk(0.60) == "Medium Risk"
    assert classify_risk(0.61) == "High Risk"
    assert classify_risk(1.0) == "High Risk"


# ── Data loading tests ─────────────────────────────────────────


def test_load_and_clean_dataset():
    """Dataset download, load, and clean should work."""
    from src.preprocessing import download_dataset, load_dataset, clean_dataset

    download_dataset()
    df = load_dataset()
    assert len(df) > 0
    assert "credit_risk" in df.columns

    df_clean = clean_dataset(df)
    # After mapping: target should be 0 or 1
    assert set(df_clean["credit_risk"].unique()).issubset({0, 1})
