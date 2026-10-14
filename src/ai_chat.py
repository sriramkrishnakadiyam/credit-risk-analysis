"""
src/ai_chat.py — Intelligent AI Credit Advisor & Chat Engine.

Provides interactive domain-specific assistance regarding:
- Credit risk classification principles and risk categories
- Logistic Regression model mechanics, evaluation metrics, and thresholds
- Features, impact factors, and improvement recommendations
- Dataset details and lending advisory
- Optional Gemini/OpenAI API integration with built-in comprehensive fallback
"""

import os
from src.config import RISK_THRESHOLDS, RISK_LABELS

# Optional Gemini API integration if API key is provided
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

def generate_ai_response(user_message: str, history: list = None) -> str:
    """Generate an AI response for the user's query.

    Args:
        user_message: The prompt/question submitted by the user.
        history: Optional list of previous chat messages.

    Returns:
        str: Markdown-formatted AI response.
    """
    cleaned = user_message.strip().lower()

    # 1. Check for external LLM API if key is available
    if GEMINI_KEY:
        try:
            import importlib
            genai = importlib.import_module("google.generativeai")
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            system_prompt = (
                "You are 'CreditRisk AI', an expert financial risk analyst and credit advisor. "
                "You assist users in understanding credit risk classification, evaluating loan applications, "
                "explaining machine learning concepts (especially Logistic Regression, 75% accuracy, 80% recall, "
                "balanced class weights, ROC-AUC 80.58%), and giving actionable advice to applicants to improve "
                "their creditworthiness. Use clean markdown formatting, concise paragraphs, and bullet points."
            )
            chat_session = model.start_chat()
            response = chat_session.send_message(f"{system_prompt}\n\nUser Question: {user_message}")
            if response and response.text:
                return response.text
        except Exception:
            pass  # Fall back to built-in domain knowledge engine

    # 2. Intelligent Built-in Credit Risk Domain Engine
    return _rule_based_credit_ai(cleaned, user_message)


def _rule_based_credit_ai(q: str, original_msg: str) -> str:
    """Comprehensive rule-based Credit Risk and ML expert response system."""

    # Greetings & Identity
    if any(k in q for k in ["hello", "hi", "hey", "who are you", "what can you do", "help"]):
        return (
            "👋 **Hello! I'm CreditRisk AI**, your virtual Credit Analyst and Machine Learning Advisor.\n\n"
            "I can assist you with:\n"
            "* 🔍 **Risk Assessment Insights:** Understanding Low, Medium, and High credit risk.\n"
            "* 🤖 **Machine Learning Model:** How our Logistic Regression model works, its 75% accuracy, 80% recall, and ROC-AUC of 80.58%.\n"
            "* 💡 **Improving Creditworthiness:** Specific steps to lower default risk and qualify for better loan terms.\n"
            "* 📋 **Feature Explanations:** Explaining checking account status, installment rates, debt-to-income, and collateral.\n"
            "* 📊 **Dataset Details:** How the German Credit dataset (1,000 applicants, 20 features) is structured.\n\n"
            "Try asking me: *'How can I lower my credit risk?'* or *'Explain how the model classifies risk.'*"
        )

    # Risk Categories & Thresholds
    if any(k in q for k in ["category", "categories", "risk level", "threshold", "low risk", "medium risk", "high risk"]):
        return (
            "🎯 **Credit Risk Categories & Thresholds**\n\n"
            "Our system maps the model's predicted probability of default P(Bad) into 3 operational risk tiers:\n\n"
            "1. 🟢 **Low Risk (P ≤ 30%):**\n"
            "   * High likelihood of timely repayment.\n"
            "   * Typically qualifies for standard or accelerated approval and preferential interest rates.\n\n"
            "2. 🟡 **Medium Risk (30% < P ≤ 60%):**\n"
            "   * Moderate risk of financial distress.\n"
            "   * Often requires secondary underwriting, proof of stable income, or additional collateral/co-applicant.\n\n"
            "3. 🔴 **High Risk (P > 60%):**\n"
            "   * Significant statistical probability of default.\n"
            "   * Requires senior committee sign-off, loan restructuring, or risk-mitigating covenants before consideration."
        )

    # Model Evaluation & Metrics
    if any(k in q for k in ["accuracy", "metric", "precision", "recall", "f1", "roc", "auc", "confusion matrix", "performance"]):
        return (
            "📈 **Model Evaluation & Performance Metrics**\n\n"
            "The Logistic Regression model was rigorously evaluated on an **80/20 stratified split** of the German Credit dataset (200 test cases):\n\n"
            "* **Accuracy (75.0%):** Correctly classifies 3 out of every 4 applicants.\n"
            "* **Recall (80.0%):** **Crucial for banks!** Successfully detects 80% of actual defaulting borrowers (48 out of 60 bad credit risks in the test set).\n"
            "* **ROC-AUC (80.58%):** Demonstrates strong class separability between reliable and risky applicants.\n"
            "* **Precision (55.8%):** Balanced trade-off to ensure few bad debts slip through.\n"
            "* **F1-Score (65.8%):** Harmonic balance between precision and recall.\n\n"
            "💡 *Why High Recall Matters:* In lending, the financial loss from a defaulted loan far exceeds the lost opportunity cost of rejecting a borderline applicant."
        )

    # Why Logistic Regression
    if any(k in q for k in ["logistic regression", "algorithm", "technique", "why logistic"]):
        return (
            "🤖 **Why Logistic Regression for Credit Risk?**\n\n"
            "Logistic Regression is the gold standard baseline in banking and financial credit scoring because:\n\n"
            "1. **Regulatory Interpretability:** Unlike 'black-box' deep learning models, Logistic Regression coefficients directly explain how each variable increases or decreases the log-odds of default (vital for Fair Lending / ECOA compliance).\n"
            "2. **Calibrated Probabilities:** Outputs genuine probabilities P(Bad Credit) between 0 and 1 via the sigmoid function, allowing banks to set dynamic risk thresholds.\n"
            "3. **Balanced Class Weighting:** Handles the natural class imbalance (700 Good vs 300 Bad) by weighting default errors proportionally higher during training.\n"
            "4. **Production Efficiency:** Microsecond prediction latency, zero heavy GPU requirements, and minimal server footprint."
        )

    # How to lower risk / improve credit
    if any(k in q for k in ["improve", "lower risk", "reduce risk", "better score", "tips", "increase chance", "qualify"]):
        return (
            "💡 **Top 5 Ways to Lower Credit Risk & Qualify for a Loan**\n\n"
            "Based on the mathematical coefficients of credit risk models, here is what moves an applicant into the **Low Risk** category:\n\n"
            "1. 🏦 **Maintain a Healthy Checking & Savings Balance:** Having an established account with positive cash flow (≥ 200 DM) is one of the strongest positive indicators.\n"
            "2. ⏱️ **Choose Shorter Loan Durations:** Loans under 18–24 months carry significantly lower default probabilities than 36–60 month commitments.\n"
            "3. 📉 **Keep Installment Rates Low:** Ensure monthly repayments represent less than 20% - 30% of your disposable monthly income (Installment Rate 1 or 2).\n"
            "4. 🏠 **Provide Collateral or Asset Backing:** Owning real estate or life insurance provides recourse and lowers perceived lending risk.\n"
            "5. 🤝 **Add a Creditworthy Guarantor:** If self-employed or with a short employment history, a co-applicant or guarantor dramatically offsets default probability."
        )

    # Feature Importance & Key Predictors
    if any(k in q for k in ["feature", "features", "input", "most important", "factors", "variables"]):
        return (
            "📊 **Key Features Analyzed by the Model**\n\n"
            "The model processes **20 comprehensive financial and demographic features** across 4 categories:\n\n"
            "* 💳 **Account Status:** Checking account balance status and existing savings account reserves.\n"
            "* 📜 **Credit History:** Past repayment track record, delayed payments, or critical existing accounts.\n"
            "* 💰 **Loan Specifications:** Loan amount, duration in months, purpose, and installment rate as % of disposable income.\n"
            "* 👤 **Personal & Employment Profile:** Employment stability, age, housing tenure, property ownership, and guarantor/co-applicant presence.\n\n"
            "⚠️ *Zero Data Leakage:* All numerical scaling and categorical encoding pipelines are fitted strictly on training data."
        )

    # Checking account explanation
    if any(k in q for k in ["checking account", "a11", "a12", "a13", "a14"]):
        return (
            "🏦 **Checking Account Status Breakdown**\n\n"
            "Checking account status is historically the **single strongest predictor** of short-term credit risk:\n\n"
            "* **A11 (< 0 DM / Overdrawn):** Significant risk indicator; indicates negative cash buffer.\n"
            "* **A12 (0 - 200 DM):** Low to moderate liquidity buffer.\n"
            "* **A13 (≥ 200 DM or regular salary account ≥ 1 year):** Strongest positive indicator for Low Risk approval.\n"
            "* **A14 (No checking account at this institution):** Moderate uncertainty due to lack of internal transaction history."
        )

    # Dataset explanation
    if any(k in q for k in ["dataset", "german credit", "uci", "data source", "statlog"]):
        return (
            "📁 **Dataset Overview: Statlog German Credit Data**\n\n"
            "* **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))\n"
            "* **Donated by:** Prof. Dr. Hans Hofmann, University of Hamburg\n"
            "* **Samples:** 1,000 real borrower profiles\n"
            "* **Features:** 20 (7 numerical, 13 categorical)\n"
            "* **Target Class:** Binary (1 = Good Credit, 2 = Bad Credit)\n"
            "* **Distribution:** 700 Good (70%) vs 300 Bad (30%)\n"
            "* **Preprocessing:** Missing value safety net, StandardScaler for numerical variables, and One-Hot Encoding for categorical categories."
        )

    # Human review / advisory disclaimer
    if any(k in q for k in ["guarantee", "decision", "human review", "disclaimer", "legal", "official"]):
        return (
            "⚖️ **Regulatory Disclaimer & Lending Advisory**\n\n"
            "This AI system is an **analytical decision-support tool**, not an automated final underwriter.\n\n"
            "* **Estimates Only:** Predictions represent statistical probabilities based on historical cohort patterns.\n"
            "* **Human Underwriter Required:** A licensed credit committee or loan officer must independently verify physical documentation, credit bureau files (e.g., Schufa, Equifax, Experian), and current debt-to-income before issuing legally binding lending commitments.\n"
            "* **Fair Lending:** Lenders must ensure compliance with anti-discrimination statutes (such as the Equal Credit Opportunity Act)."
        )

    # Default fallback response
    return (
        f"🤔 **I understand your question regarding:** *\"{original_msg}\"*\n\n"
        "Here are key insights related to credit risk classification:\n\n"
        "* **Model Architecture:** We use **Logistic Regression** trained on the German Credit dataset to predict default probability P(Bad).\n"
        "* **Risk Classification:** Applicants are segmented into **Low Risk** (P ≤ 30%), **Medium Risk** (30% - 60%), and **High Risk** (P > 60%).\n"
        "* **Key Drivers:** Checking account balance, loan duration, credit history, and employment stability carry the greatest predictive weight.\n\n"
        "💡 *Would you like to know more about:*\n"
        "1. How to improve a loan applicant's risk rating?\n"
        "2. How our model achieved an **80.0% Recall** rate?\n"
        "3. How to use the Prediction form to test a sample applicant?"
    )
