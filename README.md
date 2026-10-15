# 🛡️ Credit Risk Classification Using Logistic Regression

A full-stack machine learning web application that classifies credit risk for loan applicants into **Low**, **Medium**, and **High** risk categories using **Logistic Regression**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?logo=scikit-learn&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [Architecture](#-architecture)
- [Dataset](#-dataset)
- [Technologies Used](#-technologies-used)
- [Folder Structure](#-folder-structure)
- [Installation & Setup](#-installation--setup)
- [Model Training](#-model-training)
- [Running the Application](#-running-the-application)
- [Running Tests](#-running-tests)
- [Evaluation Results](#-evaluation-results)
- [Risk Classification Strategy](#-risk-classification-strategy)
- [Screenshots](#-screenshots)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [GitHub Setup](#-github-setup)
- [License](#-license)

---

## 🎯 Project Overview

This project implements an end-to-end credit risk assessment system. Given a loan applicant's financial and personal attributes (20 features), the system:

1. **Preprocesses** data with StandardScaler (numerical) and OneHotEncoder (categorical)
2. **Trains** a Logistic Regression classifier (with balanced class weights)
3. **Predicts** the probability of "Bad Credit"
4. **Classifies** into three risk categories based on probability thresholds
5. **Displays** results through a professional Flask web dashboard

---

## 🏆 Objectives

- Build a reliable credit risk prediction model using Logistic Regression
- Prevent data leakage by fitting the preprocessor on training data only
- Provide an intuitive web interface for making predictions
- Display model evaluation metrics on a performance dashboard
- Implement three-level risk categorization (Low / Medium / High) from binary classification

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Browser    │────▶│  Flask App   │────▶│  ML Pipeline    │
│  (Frontend) │◀────│  (Backend)   │◀────│  (Scikit-learn) │
└─────────────┘     └──────────────┘     └─────────────────┘
                          │                       │
                    ┌─────┴──────┐          ┌─────┴──────┐
                    │ Templates  │          │ Saved Model│
                    │ Static     │          │ Preprocessor│
                    └────────────┘          │ Metrics    │
                                           └────────────┘
```

**Flow:**
1. User fills in the prediction form (20 features)
2. Flask validates input and passes it to the ML pipeline
3. The preprocessor transforms input using the same pipeline fitted during training
4. Logistic Regression outputs `P(Bad Credit)`
5. The probability is mapped to Low / Medium / High risk
6. Results are displayed with probability bars and a risk gauge

---

## 📊 Dataset

| Property   | Value                                                                                          |
|------------|------------------------------------------------------------------------------------------------|
| **Name**   | Statlog (German Credit Data)                                                                  |
| **Source**  | [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)) |
| **License** | CC BY 4.0                                                                                     |
| **Samples** | 1,000                                                                                         |
| **Features**| 20 (7 numerical, 13 categorical)                                                              |
| **Target** | `credit_risk` — 1 (Good), 2 (Bad)                                                             |

The dataset is **automatically downloaded** during training. See [`data/README.md`](data/README.md) for detailed feature descriptions.

---

## 🛠️ Technologies Used

| Category    | Technology                                    |
|-------------|-----------------------------------------------|
| Language    | Python 3.10+                                  |
| ML Library  | Scikit-learn, Pandas, NumPy                   |
| Visualization | Matplotlib, Seaborn                          |
| Backend     | Flask 3.0                                     |
| Frontend    | HTML5, CSS3, JavaScript, Bootstrap 5.3        |
| Serialization | Joblib                                       |
| Testing     | Pytest                                        |
| Deployment  | Gunicorn, Render                              |

---

## 📁 Folder Structure

```
Credit-Risk-Classification/
|-- app.py
|-- train_model.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- render.yaml
|-- data/
|   |-- README.md
|   `-- german_credit.csv
|-- models/
|   |-- logistic_regression_model.joblib
|   |-- preprocessor.joblib
|   `-- metrics.joblib
|-- instance/
|   `-- prediction_history.sqlite3  # Created when predictions are saved
|-- src/
|   |-- __init__.py
|   |-- ai_chat.py
|   |-- config.py
|   |-- model_utils.py
|   `-- preprocessing.py
|-- templates/
|   |-- 404.html
|   |-- 500.html
|   |-- about.html
|   |-- base.html
|   |-- chat.html
|   |-- dashboard.html
|   |-- history.html
|   |-- index.html
|   |-- predict.html
|   `-- result.html
|-- static/
|   |-- css/style.css
|   `-- js/script.js
|-- tests/
|   |-- __init__.py
|   |-- test_app.py
|   `-- test_model.py
`-- screenshots/
```

---

## ⚡ Installation & Setup

### Prerequisites
- **Python 3.10+** installed
- **pip** package manager
- **Git** (for GitHub setup)
- **Windows PowerShell** (commands below are for Windows)

### Step-by-step (Windows PowerShell)

```powershell
# 1. Open PowerShell and go to the project folder
cd "C:\Users\acer\OneDrive\Desktop\Credit Risk Classification"

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 🤖 Model Training

```powershell
# Train the model (downloads dataset automatically)
python train_model.py
```

**What happens:**
1. Downloads the German Credit dataset from UCI (if not present)
2. Loads and cleans the data (maps target: 1→Good, 2→Bad)
3. Splits 80/20 with stratification
4. Fits preprocessor on **training data only** (no data leakage)
5. Trains Logistic Regression (balanced class weights, max_iter=1000)
6. Evaluates on the test set
7. Saves model, preprocessor, and metrics to `models/`

**Expected output:**
```
============================================================
  Credit Risk Classification — Model Training
============================================================

📥  Step 1 / 4 — Downloading dataset …
📂  Step 2 / 4 — Loading dataset …
🧹  Step 3 / 4 — Cleaning dataset …
🤖  Step 4 / 4 — Training Logistic Regression …

✅  Model, preprocessor, and metrics saved to: models/

============================================================
  Evaluation Results
============================================================
  Accuracy : 0.XXXX
  Precision: 0.XXXX
  Recall   : 0.XXXX
  F1 Score : 0.XXXX
  ROC AUC  : 0.XXXX
============================================================
```

---

## Running the Application

```powershell
# Activate the virtual environment if it is not already active
.\venv\Scripts\Activate.ps1

# Start the Flask application
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Keep the PowerShell window open while using the site; press **Ctrl+C** there to stop the server.

Flask prints a red warning that its built-in server is for development. This is expected when running `python app.py` locally; it is not an application error. The Render deployment uses Gunicorn as its production server, as configured in `render.yaml`.

### Using the website step by step

1. **Home:** Review the project introduction and workflow. Select **Start Prediction** or **Predict** to open the form.
2. **Enter application details:** Fill in the loan, financial, personal, employment, and property fields. All required fields must be completed.
3. **Run a prediction:** Select **Classify Risk** at the bottom of the form. The result page displays the risk category and probability scores.
4. **Open prediction history:** Choose **History** in the top navigation. Completed predictions are stored in `instance/prediction_history.sqlite3`; select **View** to reopen a result. Keep this database file to preserve local history.
5. **Review model metrics:** Choose **Dashboard** to view accuracy, precision, recall, ROC AUC, the confusion matrix, and the classification report.
6. **Read project details:** Choose **About** for the dataset, methodology, project structure, limitations, and technology stack.
7. **Use the AI advisor:** Choose **AI Chat** to ask questions about credit-risk concepts and model results.

The prediction form's **Reset** button clears the current form fields; it does not delete saved history.

### Available Pages

| Route | Description |
|---|---|
| `/` | Home page |
| `/predict` | Prediction form |
| `/result` | Prediction result after submission |
| `/history` | Saved predictions |
| `/dashboard` | Model performance dashboard |
| `/about` | Project information |
| `/chat` | AI Credit Advisor chat |
| `/api/chat` | REST API endpoint for chat messages (POST) |

---

## 🧪 Running Tests

```powershell
# Run all tests
python -m pytest tests/ -v

# Run only app tests
python -m pytest tests/test_app.py -v

# Run only model tests
python -m pytest tests/test_model.py -v
```

### Test Coverage

| Test File         | Tests                                                    |
|-------------------|----------------------------------------------------------|
| `test_app.py`     | Home page, predict page, dashboard, about, 404,         |
|                   | valid prediction, missing fields, invalid age/amount,   |
|                   | result without session                                   |
| `test_model.py`   | Artifact existence, model loading, preprocessor loading, |
|                   | metrics loading, predict_single output, risk thresholds, |
|                   | dataset download and cleaning                            |

---

## 📈 Evaluation Results

The model was trained and evaluated on an 80/20 stratified split of the German Credit dataset (800 train samples, 200 test samples) with balanced class weights to compensate for class imbalance (700 Good vs 300 Bad).

### Performance Metrics

| Metric | Description | Value |
|---|---|---|
| **Accuracy** | Overall correct predictions | **75.00%** (0.7500) |
| **Precision** | Of predicted "Bad", how many are truly bad | **55.81%** (0.5581) |
| **Recall** | Of actual "Bad", how many were detected | **80.00%** (0.8000) |
| **F1 Score** | Harmonic mean of precision and recall | **65.75%** (0.6575) |
| **ROC AUC** | Area under the ROC curve | **80.58%** (0.8058) |

### Confusion Matrix (Test Set, N = 200)

| Actual \ Predicted | Predicted Good (Negative) | Predicted Bad (Positive) | Total Actual |
|---|---|---|---|
| **Actual Good Credit** | **102** (True Negative) | **38** (False Positive) | 140 |
| **Actual Bad Credit** | **12** (False Negative) | **48** (True Positive) | 60 |
| **Total Predicted** | **114** | **86** | 200 |

*High Recall (80.0%) ensures that 80% of bad credit risks are successfully flagged, which is crucial in credit risk management to minimize default losses.*

---

## 🎯 Risk Classification Strategy

The Logistic Regression model produces a **binary classification** (Good / Bad credit). We derive three risk categories from the predicted probability of "Bad Credit" ($P(\text{Bad})$):

| Probability $P(\text{Bad})$ | Risk Category | Action / Meaning |
|-----------------------------|---------------|------------------|
| $P \le 0.30$                | 🟢 **Low Risk**    | High likelihood of repayment; standard approval workflow |
| $0.30 < P \le 0.60$         | 🟡 **Medium Risk** | Moderate uncertainty; requires supplementary verification |
| $P > 0.60$                  | 🔴 **High Risk**   | Elevated default probability; senior loan officer sign-off |

This mapping is **empirically grounded, transparent, and configurable** in [`src/config.py`](src/config.py).

---

## ☁️ Live Cloud Deployment (Render)

This application is ready for 1-click or repository deployment on [Render](https://render.com/).

### Deployment Configuration (`render.yaml`)

The repository includes a ready-to-use [`render.yaml`](render.yaml) specification:

- **Environment:** Python 3.12+
- **Build Command:** `pip install -r requirements.txt && python train_model.py`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Environment Variables:**
  - `FLASK_DEBUG`: `False`
  - `SECRET_KEY`: Auto-generated cryptographic key

### Step-by-Step Render Deployment Guide

1. **Sign Up / Log In:** Go to [render.com](https://render.com/) and connect your GitHub account.
2. **New Web Service:** Click **New +** > **Web Service**.
3. **Select Repository:** Choose your `Credit-Risk-Classification` GitHub repository.
4. **Configure Settings:**
   - **Name:** `credit-risk-classification` (or your chosen name)
   - **Region:** Closest to your users (e.g., Frankfurt, Oregon, Singapore)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python train_model.py`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type:** `Free`
5. **Environment Variables:**
   - `FLASK_DEBUG` = `False`
   - `SECRET_KEY` = *any random string or auto-generated*
6. **Deploy:** Click **Create Web Service**.
7. **Verify:** Monitor the build logs. Once deployed, Render provides your live URL (e.g., `https://credit-risk-classification.onrender.com`). Visit the URL, submit a test prediction, and review the live dashboard!

---

## Screenshots

The screenshot images were supplied in chat, but are not yet available as files in this repository. Copy them into `screenshots/` using these names; the markdown links below will then render them.

### Home page

![CreditRiskAI home page](screenshots/home.png)

### How it works

![Home page workflow and model summary](screenshots/how-it-works.png)

### Prediction form

![Loan and financial details form](screenshots/predict-form-loan.png)

![Personal and employment details form](screenshots/predict-form-personal.png)

### Prediction history

![Saved predictions in the History page](screenshots/history.png)

### Model dashboard

![Model performance dashboard](screenshots/dashboard.png)

### About page

![Project overview and methodology](screenshots/about.png)

### AI Chat

![CreditRiskAI advisor chat page](screenshots/ai-chat.png)

---

## ⚠️ Limitations

1. **Small dataset** — 1,000 samples (historical German Credit dataset); production applications require modern, larger-scale portfolios.
2. **Market-specific attributes** — Features (e.g., Deutsche Mark denominations) reflect the original historical study.
3. **Derived 3-class risk** — Risk tiers are derived from calibrated probability thresholds rather than native multi-class labels.
4. **Decision Support Only** — Designed as an assistive tool; lending decisions must adhere to regulatory compliance (e.g., FCRA, ECOA) and human review.

---

## 🚀 Future Enhancements

- [ ] Add SHAP / LIME explainability waterfall charts for individual predictions
- [ ] Implement ensemble comparison (Logistic Regression vs Random Forest vs XGBoost)
- [ ] Add a secure RESTful API (`/api/v1/predict`) with JWT authentication
- [ ] Support batch credit application evaluation via CSV/Excel upload
- [ ] Export PDF decision reports for credit committee audit trails
- [ ] Automated CI/CD pipeline via GitHub Actions

---

## 🔗 GitHub Setup & Execution Commands

### Exact Windows PowerShell Commands in Order

```powershell
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the machine learning model & generate artifacts
python train_model.py

# 4. Run automated test suite
python -m pytest -v

# 5. Run the web application locally
python app.py
# Open your browser at http://127.0.0.1:5000

# 6. Upload project to GitHub
git init
git add .
git commit -m "Build Credit Risk Classification project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

The German Credit dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

<p align="center">
  Built with ❤️ using Python, Flask & Scikit-learn
</p>
