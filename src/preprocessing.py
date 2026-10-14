"""
Data loading, cleaning, and preprocessing utilities.

This module downloads the German Credit dataset from the UCI repository,
cleans it, and builds a scikit-learn preprocessing pipeline that is fitted
**only** on training data to prevent data leakage.
"""

import os
import urllib.request

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    CATEGORICAL_FEATURES,
    COLUMN_NAMES,
    DATA_DIR,
    DATASET_PATH,
    DATASET_URL,
    NUMERICAL_FEATURES,
    TARGET_COLUMN,
)


# ── Download / Load ────────────────────────────────────────────────────────

def download_dataset() -> str:
    """Download the German Credit dataset if it does not exist locally.

    Returns:
        str: Path to the downloaded CSV file.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATASET_PATH):
        print(f"Downloading dataset from {DATASET_URL} ...")
        req = urllib.request.Request(
            DATASET_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=30) as response, open(DATASET_PATH, "wb") as out_file:
            out_file.write(response.read())
        print(f"Dataset saved to {DATASET_PATH}")
    else:
        print(f"Dataset already exists at {DATASET_PATH}")
    return DATASET_PATH


def load_dataset(path: str | None = None) -> pd.DataFrame:
    """Load the German Credit dataset into a DataFrame.

    Args:
        path: Optional path override. Defaults to ``DATASET_PATH``.

    Returns:
        pd.DataFrame: Raw dataset with human-readable column names.
    """
    if path is None:
        path = DATASET_PATH
    df = pd.read_csv(path, sep=r"\s+", header=None, names=COLUMN_NAMES)
    return df


# ── Cleaning ────────────────────────────────────────────────────────────────

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Basic data cleaning.

    Steps:
        1. Drop duplicate rows.
        2. Map the target column: 1 → 0 (Good/Low risk), 2 → 1 (Bad/High risk).
        3. Handle missing values (the German Credit data has none, but we
           add a safety net).

    Args:
        df: Raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.copy()

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Map target: 1 (good) → 0, 2 (bad) → 1
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map({1: 0, 2: 1})

    # Fill missing numerics with median, categoricals with mode
    for col in NUMERICAL_FEATURES:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)

    for col in CATEGORICAL_FEATURES:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode()[0], inplace=True)

    return df


# ── Preprocessing Pipeline ─────────────────────────────────────────────────

def build_preprocessor() -> ColumnTransformer:
    """Build a scikit-learn ColumnTransformer for the feature set.

    Numerical features  → StandardScaler
    Categorical features → OneHotEncoder (handle_unknown='ignore')

    Returns:
        ColumnTransformer: Unfitted transformer.
    """
    numerical_pipeline = Pipeline([
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_pipeline, NUMERICAL_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
    return preprocessor


def get_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    """Extract human-readable feature names after fitting.

    Args:
        preprocessor: A **fitted** ColumnTransformer.

    Returns:
        list[str]: Feature names in the transformed feature matrix order.
    """
    return list(preprocessor.get_feature_names_out())
