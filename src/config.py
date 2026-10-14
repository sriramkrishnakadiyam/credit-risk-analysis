"""
Configuration settings for the Credit Risk Classification project.
"""

import os

# ── Base Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# ── Dataset ─────────────────────────────────────────────────────────────────
DATASET_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "statlog/german/german.data"
)
DATASET_FILENAME = "german_credit.csv"
DATASET_PATH = os.path.join(DATA_DIR, DATASET_FILENAME)

# Column names for the German Credit dataset (UCI)
# Reference: https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)
COLUMN_NAMES = [
    "status_checking_account",   # A1
    "duration_months",           # A2
    "credit_history",            # A3
    "purpose",                   # A4
    "credit_amount",             # A5
    "savings_account",           # A6
    "employment_since",          # A7
    "installment_rate",          # A8
    "personal_status_sex",       # A9
    "other_debtors",             # A10
    "residence_since",           # A11
    "property",                  # A12
    "age",                       # A13
    "other_installment_plans",   # A14
    "housing",                   # A15
    "num_existing_credits",      # A16
    "job",                       # A17
    "num_dependents",            # A18
    "telephone",                 # A19
    "foreign_worker",            # A20
    "credit_risk",               # Target: 1 = Good, 2 = Bad
]

# ── Feature Groups ──────────────────────────────────────────────────────────
CATEGORICAL_FEATURES = [
    "status_checking_account",
    "credit_history",
    "purpose",
    "savings_account",
    "employment_since",
    "personal_status_sex",
    "other_debtors",
    "property",
    "other_installment_plans",
    "housing",
    "job",
    "telephone",
    "foreign_worker",
]

NUMERICAL_FEATURES = [
    "duration_months",
    "credit_amount",
    "installment_rate",
    "residence_since",
    "age",
    "num_existing_credits",
    "num_dependents",
]

TARGET_COLUMN = "credit_risk"

# ── Risk-category mapping ──────────────────────────────────────────────────
# The German Credit dataset has binary labels (1 = Good, 2 = Bad).
# We derive a three-level risk category from the predicted probability:
#   probability of "Bad" <= 0.30  →  Low Risk
#   0.30 < probability <= 0.60   →  Medium Risk
#   probability > 0.60           →  High Risk
RISK_THRESHOLDS = {
    "low": 0.30,
    "medium": 0.60,
}

RISK_LABELS = {
    "low": "Low Risk",
    "medium": "Medium Risk",
    "high": "High Risk",
}

# ── Model Artifacts ─────────────────────────────────────────────────────────
MODEL_FILENAME = "logistic_regression_model.joblib"
PREPROCESSOR_FILENAME = "preprocessor.joblib"
METRICS_FILENAME = "metrics.joblib"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, PREPROCESSOR_FILENAME)
METRICS_PATH = os.path.join(MODEL_DIR, METRICS_FILENAME)

# ── Training Hyper-parameters ───────────────────────────────────────────────
TEST_SIZE = 0.20
RANDOM_STATE = 42
MAX_ITER = 1000

# ── Flask ───────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "credit-risk-dev-key-change-in-prod")
DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
