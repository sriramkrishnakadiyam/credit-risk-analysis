"""
app.py — Flask application for Credit Risk Classification.

Routes:
    /                → Home page
    /predict         → Prediction form (GET) / Run prediction (POST)
    /result          → Prediction result display
    /dashboard       → Model performance dashboard
    /about           → Project information
"""

import sys
import os
import json
import secrets
import sqlite3
from datetime import datetime

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from src.config import (
    SECRET_KEY,
    DEBUG,
    TEMPLATE_DIR,
    STATIC_DIR,
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
)
from src.model_utils import predict_single, load_metrics, load_model, load_preprocessor
from src.ai_chat import generate_ai_response

# ── App factory ─────────────────────────────────────────────────────────────

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)
app.secret_key = SECRET_KEY
app.config["HISTORY_DATABASE"] = os.path.join(
    app.instance_path, "prediction_history.sqlite3"
)

# ── Dropdown options for the prediction form ────────────────────────────────
# These mirror the raw German Credit encoding values.

FORM_OPTIONS = {
    "status_checking_account": [
        ("A11", "< 0 DM"),
        ("A12", "0 – 200 DM"),
        ("A13", "≥ 200 DM / salary for ≥ 1 year"),
        ("A14", "No checking account"),
    ],
    "credit_history": [
        ("A30", "No credits taken / all paid back duly"),
        ("A31", "All credits at this bank paid back duly"),
        ("A32", "Existing credits paid back duly till now"),
        ("A33", "Delay in paying off in the past"),
        ("A34", "Critical account / other credits existing"),
    ],
    "purpose": [
        ("A40", "Car (new)"),
        ("A41", "Car (used)"),
        ("A42", "Furniture / equipment"),
        ("A43", "Radio / television"),
        ("A44", "Domestic appliances"),
        ("A45", "Repairs"),
        ("A46", "Education"),
        ("A47", "Vacation"),
        ("A48", "Retraining"),
        ("A49", "Business"),
        ("A410", "Others"),
    ],
    "savings_account": [
        ("A61", "< 100 DM"),
        ("A62", "100 – 500 DM"),
        ("A63", "500 – 1000 DM"),
        ("A64", "≥ 1000 DM"),
        ("A65", "Unknown / no savings account"),
    ],
    "employment_since": [
        ("A71", "Unemployed"),
        ("A72", "< 1 year"),
        ("A73", "1 – 4 years"),
        ("A74", "4 – 7 years"),
        ("A75", "≥ 7 years"),
    ],
    "personal_status_sex": [
        ("A91", "Male – divorced / separated"),
        ("A92", "Female – divorced / separated / married"),
        ("A93", "Male – single"),
        ("A94", "Male – married / widowed"),
        ("A95", "Female – single"),
    ],
    "other_debtors": [
        ("A101", "None"),
        ("A102", "Co-applicant"),
        ("A103", "Guarantor"),
    ],
    "property": [
        ("A121", "Real estate"),
        ("A122", "Building society savings / life insurance"),
        ("A123", "Car or other"),
        ("A124", "Unknown / no property"),
    ],
    "other_installment_plans": [
        ("A141", "Bank"),
        ("A142", "Stores"),
        ("A143", "None"),
    ],
    "housing": [
        ("A151", "Rent"),
        ("A152", "Own"),
        ("A153", "For free"),
    ],
    "job": [
        ("A171", "Unemployed / unskilled – non-resident"),
        ("A172", "Unskilled – resident"),
        ("A173", "Skilled employee / official"),
        ("A174", "Management / self-employed / highly qualified"),
    ],
    "telephone": [
        ("A191", "None"),
        ("A192", "Yes, registered"),
    ],
    "foreign_worker": [
        ("A201", "Yes"),
        ("A202", "No"),
    ],
}


def _save_prediction_history(browser_id, input_data, result):
    """Persist a prediction for the current browser."""
    database_path = app.config["HISTORY_DATABASE"]
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS prediction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    browser_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    input_data TEXT NOT NULL,
                    result TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_prediction_history_browser
                ON prediction_history (browser_id, id DESC)
                """
            )
            connection.execute(
                """
                INSERT INTO prediction_history
                    (browser_id, created_at, input_data, result)
                VALUES (?, ?, ?, ?)
                """,
                (
                    browser_id,
                    datetime.now().astimezone().replace(microsecond=0).isoformat(),
                    json.dumps(input_data),
                    json.dumps(result),
                ),
            )
    finally:
        connection.close()


def _get_browser_prediction_history():
    """Load saved predictions, newest first.

    History is intentionally available from the shared history database even
    when the browser identifier cookie is missing or was cleared. This keeps
    records visible on the History page after browser data resets.
    """
    browser_id = request.cookies.get("prediction_history_id")
    database_path = app.config["HISTORY_DATABASE"]
    if not os.path.exists(database_path):
        return []

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        if browser_id:
            rows = connection.execute(
                """
                SELECT id, created_at, input_data, result
                FROM prediction_history
                WHERE browser_id = ?
                ORDER BY id DESC
                """,
                (browser_id,),
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT id, created_at, input_data, result
                FROM prediction_history
                ORDER BY id DESC
                """
            ).fetchall()
    finally:
        connection.close()

    return [
        {
            "id": row["id"],
            "created_at": row["created_at"],
            "input_data": json.loads(row["input_data"]),
            "result": json.loads(row["result"]),
        }
        for row in rows
    ]


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """Prediction form (GET) and handler (POST)."""
    if request.method == "GET":
        return render_template("predict.html", form_options=FORM_OPTIONS)

    # ── Collect form data ───────────────────────────────────────────────
    try:
        input_data = {}

        # Numerical
        input_data["duration_months"] = float(request.form.get("duration_months", 0))
        input_data["credit_amount"] = float(request.form.get("credit_amount", 0))
        input_data["installment_rate"] = float(request.form.get("installment_rate", 1))
        input_data["residence_since"] = float(request.form.get("residence_since", 1))
        input_data["age"] = float(request.form.get("age", 18))
        input_data["num_existing_credits"] = float(request.form.get("num_existing_credits", 1))
        input_data["num_dependents"] = float(request.form.get("num_dependents", 1))

        # Categorical
        for feat in CATEGORICAL_FEATURES:
            value = request.form.get(feat, "")
            if not value:
                flash(f"Please select a value for {feat.replace('_', ' ').title()}.", "danger")
                return render_template("predict.html", form_options=FORM_OPTIONS)
            input_data[feat] = value

        # Validation
        if input_data["age"] < 18 or input_data["age"] > 120:
            flash("Age must be between 18 and 120.", "danger")
            return render_template("predict.html", form_options=FORM_OPTIONS)
        if input_data["duration_months"] <= 0:
            flash("Loan duration must be positive.", "danger")
            return render_template("predict.html", form_options=FORM_OPTIONS)
        if input_data["credit_amount"] <= 0:
            flash("Credit amount must be positive.", "danger")
            return render_template("predict.html", form_options=FORM_OPTIONS)

        result = predict_single(input_data)

        # Store result in session for the result page
        session["prediction_result"] = result
        session["input_data"] = {k: str(v) for k, v in input_data.items()}
        history_browser_id = (
            request.cookies.get("prediction_history_id") or secrets.token_urlsafe(32)
        )
        _save_prediction_history(history_browser_id, session["input_data"], result)

        response = redirect(url_for("result"))
        response.set_cookie(
            "prediction_history_id",
            history_browser_id,
            # Keep the browser identifier across restarts and deployments.
            # Without an expiry, this is a persistent browser cookie; the
            # prediction rows themselves live in the SQLite database.
            httponly=True,
            secure=request.is_secure,
            samesite="Lax",
        )
        return response

    except FileNotFoundError as e:
        flash(str(e), "danger")
        return render_template("predict.html", form_options=FORM_OPTIONS)
    except Exception as e:
        flash(f"Prediction error: {e}", "danger")
        return render_template("predict.html", form_options=FORM_OPTIONS)


@app.route("/result")
def result():
    """Display prediction result."""
    prediction_result = session.get("prediction_result")
    input_data = session.get("input_data")
    if not prediction_result:
        flash("No prediction result found. Please submit the form first.", "warning")
        return redirect(url_for("predict"))
    return render_template(
        "result.html",
        result=prediction_result,
        input_data=input_data,
        form_options=FORM_OPTIONS,
    )


@app.route("/history")
def history():
    """Display this browser's saved prediction history."""
    return render_template(
        "history.html",
        predictions=_get_browser_prediction_history(),
        form_options=FORM_OPTIONS,
    )


@app.route("/history/<int:prediction_id>")
def history_detail(prediction_id):
    """Display a saved prediction from the history database."""
    browser_id = request.cookies.get("prediction_history_id")
    database_path = app.config["HISTORY_DATABASE"]
    if not os.path.exists(database_path):
        return render_template("404.html"), 404

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        if browser_id:
            prediction = connection.execute(
                """
                SELECT input_data, result
                FROM prediction_history
                WHERE id = ? AND browser_id = ?
                """,
                (prediction_id, browser_id),
            ).fetchone()
        else:
            prediction = connection.execute(
                """
                SELECT input_data, result
                FROM prediction_history
                WHERE id = ?
                """,
                (prediction_id,),
            ).fetchone()
    finally:
        connection.close()

    if prediction is None:
        return render_template("404.html"), 404

    return render_template(
        "result.html",
        result=json.loads(prediction["result"]),
        input_data=json.loads(prediction["input_data"]),
        form_options=FORM_OPTIONS,
    )


@app.route("/dashboard")
def dashboard():
    """Model performance dashboard."""
    try:
        metrics = load_metrics()
        return render_template("dashboard.html", metrics=metrics)
    except FileNotFoundError as e:
        flash(str(e), "danger")
        return render_template("dashboard.html", metrics=None)


@app.route("/about")
def about():
    """Project information page."""
    return render_template("about.html")


@app.route("/chat")
def chat():
    """Dedicated AI Credit Advisor Chat page."""
    return render_template("chat.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """AI Chat API endpoint for interactive conversation."""
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    reply = generate_ai_response(user_message, history=history)
    return jsonify({"reply": reply})


# ── Error handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# ── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=5000)
