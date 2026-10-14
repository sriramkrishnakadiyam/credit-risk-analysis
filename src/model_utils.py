"""
Model training, evaluation, prediction, and persistence utilities.
"""

import os

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

from src.config import (
    MAX_ITER,
    METRICS_PATH,
    MODEL_DIR,
    MODEL_PATH,
    PREPROCESSOR_PATH,
    RANDOM_STATE,
    RISK_LABELS,
    RISK_THRESHOLDS,
    TARGET_COLUMN,
    TEST_SIZE,
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
)
from src.preprocessing import build_preprocessor


# ── Training ────────────────────────────────────────────────────────────────

def train_model(df: pd.DataFrame) -> dict:
    """End-to-end training pipeline.

    1. Split data (stratified).
    2. Fit preprocessor on **train only** (no data leakage).
    3. Train Logistic Regression.
    4. Evaluate on test set.
    5. Save model, preprocessor, and metrics to disk.

    Args:
        df: Cleaned DataFrame (target already mapped to 0/1).

    Returns:
        dict: Evaluation metrics.
    """
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    # Fit preprocessor on training data only
    preprocessor = build_preprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Train logistic regression
    model = LogisticRegression(
        max_iter=MAX_ITER,
        random_state=RANDOM_STATE,
        solver="lbfgs",
        class_weight="balanced",
    )
    model.fit(X_train_processed, y_train)

    # Evaluate
    y_pred = model.predict(X_test_processed)
    y_proba = model.predict_proba(X_test_processed)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(
            y_test, y_pred, target_names=["Good Credit", "Bad Credit"], output_dict=True
        ),
        "test_size": len(y_test),
        "train_size": len(y_train),
    }

    # Persist artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    joblib.dump(metrics, METRICS_PATH)

    print("\n[+] Model, preprocessor, and metrics saved to:", MODEL_DIR)
    return metrics


# ── Loading ─────────────────────────────────────────────────────────────────

def load_model():
    """Load the trained model from disk.

    Returns:
        LogisticRegression: Fitted model.

    Raises:
        FileNotFoundError: If the model artifact is missing.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run train_model.py first."
        )
    return joblib.load(MODEL_PATH)


def load_preprocessor():
    """Load the fitted preprocessor from disk.

    Returns:
        ColumnTransformer: Fitted preprocessor.

    Raises:
        FileNotFoundError: If the preprocessor artifact is missing.
    """
    if not os.path.exists(PREPROCESSOR_PATH):
        raise FileNotFoundError(
            f"Preprocessor not found at {PREPROCESSOR_PATH}. Run train_model.py first."
        )
    return joblib.load(PREPROCESSOR_PATH)


def load_metrics() -> dict:
    """Load saved evaluation metrics.

    Returns:
        dict: Metrics dictionary.

    Raises:
        FileNotFoundError: If the metrics artifact is missing.
    """
    if not os.path.exists(METRICS_PATH):
        raise FileNotFoundError(
            f"Metrics not found at {METRICS_PATH}. Run train_model.py first."
        )
    return joblib.load(METRICS_PATH)


# ── Prediction ──────────────────────────────────────────────────────────────

def classify_risk(probability: float) -> str:
    """Map the predicted probability of *Bad Credit* to a risk category.

    Thresholds (configurable in config.py):
        P(Bad) ≤ 0.30  →  Low Risk
        0.30 < P(Bad) ≤ 0.60  →  Medium Risk
        P(Bad) > 0.60  →  High Risk

    Args:
        probability: Predicted probability of the positive class (Bad Credit).

    Returns:
        str: Human-readable risk label.
    """
    if probability <= RISK_THRESHOLDS["low"]:
        return RISK_LABELS["low"]
    elif probability <= RISK_THRESHOLDS["medium"]:
        return RISK_LABELS["medium"]
    else:
        return RISK_LABELS["high"]


def predict_single(input_data: dict) -> dict:
    """Run prediction for a single customer.

    Args:
        input_data: Dictionary whose keys match the feature column names
                    expected by the preprocessor.

    Returns:
        dict: {
            "risk_category": str,
            "probability_bad": float,
            "probability_good": float,
            "binary_prediction": str,
        }
    """
    model = load_model()
    preprocessor = load_preprocessor()

    # Build a DataFrame with the correct column order
    all_features = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    df_input = pd.DataFrame([input_data], columns=all_features)

    # Cast numerical columns to float
    for col in NUMERICAL_FEATURES:
        df_input[col] = pd.to_numeric(df_input[col], errors="coerce")

    X_processed = preprocessor.transform(df_input)
    proba = model.predict_proba(X_processed)[0]  # [P(Good), P(Bad)]
    prob_bad = float(proba[1])
    prob_good = float(proba[0])

    return {
        "risk_category": classify_risk(prob_bad),
        "probability_bad": round(prob_bad, 4),
        "probability_good": round(prob_good, 4),
        "binary_prediction": "Bad Credit" if prob_bad > 0.5 else "Good Credit",
    }
