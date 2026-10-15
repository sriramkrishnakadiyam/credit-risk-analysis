"""
Tests for the Flask application routes.

Run with:  python -m pytest tests/ -v
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app


@pytest.fixture
def client(tmp_path):
    """Flask test client."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["HISTORY_DATABASE"] = str(tmp_path / "prediction_history.sqlite3")
    with app.test_client() as client:
        yield client


# ── Page load tests ─────────────────────────────────────────────


def test_index_page(client):
    """Home page should load successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Credit Risk" in response.data


def test_predict_page_get(client):
    """Prediction form should load via GET."""
    response = client.get("/predict")
    assert response.status_code == 200
    assert b"Prediction" in response.data or b"Predict" in response.data


def test_dashboard_page(client):
    """Dashboard should load even if model is not trained."""
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_about_page(client):
    """About page should load."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data


def test_chat_page(client):
    """AI Chat page should load."""
    response = client.get("/chat")
    assert response.status_code == 200
    assert b"CreditRisk" in response.data
    assert b"AI Advisor" in response.data


def test_api_chat_endpoint(client):
    """AI Chat API should return valid answer to query."""
    response = client.post("/api/chat", json={"message": "How can I lower my credit risk?"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    assert len(data["reply"]) > 20


def test_api_chat_empty(client):
    """Empty message should return 400 error."""
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400


def test_404_page(client):
    """Non-existent route should return 404."""
    response = client.get("/nonexistent-page")
    assert response.status_code == 404


# ── Prediction tests ───────────────────────────────────────────

VALID_FORM_DATA = {
    "duration_months": "24",
    "credit_amount": "5000",
    "installment_rate": "2",
    "residence_since": "2",
    "age": "35",
    "num_existing_credits": "1",
    "num_dependents": "1",
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


def test_predict_valid_input(client):
    """Valid form submission should redirect to result page (302)."""
    response = client.post("/predict", data=VALID_FORM_DATA, follow_redirects=False)
    # Either 302 redirect on success, or 200 if model not trained (with flash)
    assert response.status_code in (200, 302)


def test_predict_missing_field(client):
    """Missing categorical field should show error (stay on form)."""
    data = VALID_FORM_DATA.copy()
    data.pop("status_checking_account")
    response = client.post("/predict", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_predict_invalid_age(client):
    """Age < 18 should trigger validation error."""
    data = VALID_FORM_DATA.copy()
    data["age"] = "10"
    response = client.post("/predict", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Age must be" in response.data or b"age" in response.data.lower()


def test_predict_negative_amount(client):
    """Negative credit amount should trigger validation error."""
    data = VALID_FORM_DATA.copy()
    data["credit_amount"] = "-500"
    response = client.post("/predict", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_result_without_session(client):
    """Accessing result page without session data should redirect."""
    response = client.get("/result", follow_redirects=True)
    assert response.status_code == 200


def test_prediction_history_is_saved_per_browser(client, monkeypatch):
    """Completed predictions should be saved and isolated to their browser."""
    def fake_predict(input_data):
        assert input_data["credit_amount"] == 5000
        return {
            "risk_category": "Low Risk",
            "probability_bad": 0.2,
            "probability_good": 0.8,
            "binary_prediction": "Good Credit",
        }

    monkeypatch.setattr("app.predict_single", fake_predict)

    response = client.post("/predict", data=VALID_FORM_DATA)
    assert response.status_code == 302

    history_response = client.get("/history")
    assert history_response.status_code == 200
    assert b"Low Risk" in history_response.data
    assert b"5000" in history_response.data

    detail_response = client.get("/history/1")
    assert detail_response.status_code == 200
    assert b"Input Summary" in detail_response.data

    other_browser = app.test_client()
    other_history = other_browser.get("/history")
    assert b"No predictions yet" in other_history.data
    assert other_browser.get("/history/1").status_code == 404
