#!/usr/bin/env python
"""
train_model.py — Download data, preprocess, train Logistic Regression,
                  evaluate, and save artifacts.

Usage:
    python train_model.py
"""

import sys
import os

# Ensure the project root is on sys.path so `src` is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing import download_dataset, load_dataset, clean_dataset
from src.model_utils import train_model


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 60)
    print("  Credit Risk Classification - Model Training")
    print("=" * 60)

    # Step 1: Download
    print("\n[+] Step 1 / 4 - Downloading dataset ...")
    download_dataset()

    # Step 2: Load
    print("\n[+] Step 2 / 4 - Loading dataset ...")
    df = load_dataset()
    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
    print(f"   Target distribution (raw):\n{df['credit_risk'].value_counts().to_string()}")

    # Step 3: Clean
    print("\n[+] Step 3 / 4 - Cleaning dataset ...")
    df = clean_dataset(df)
    print(f"   Rows after cleaning: {len(df)}")
    print(f"   Target distribution (mapped 0=Good, 1=Bad):\n{df['credit_risk'].value_counts().to_string()}")

    # Step 4: Train & evaluate
    print("\n[+] Step 4 / 4 - Training Logistic Regression ...")
    metrics = train_model(df)

    print("\n" + "=" * 60)
    print("  Evaluation Results")
    print("=" * 60)
    print(f"  Accuracy : {metrics['accuracy']}")
    print(f"  Precision: {metrics['precision']}")
    print(f"  Recall   : {metrics['recall']}")
    print(f"  F1 Score : {metrics['f1_score']}")
    print(f"  ROC AUC  : {metrics['roc_auc']}")
    print(f"\n  Confusion Matrix:")
    for row in metrics["confusion_matrix"]:
        print(f"    {row}")
    print("\n  Train size:", metrics["train_size"])
    print("  Test size :", metrics["test_size"])
    print("=" * 60)
    print("[SUCCESS] Training complete. Artifacts saved in models/ directory.\n")


if __name__ == "__main__":
    main()
