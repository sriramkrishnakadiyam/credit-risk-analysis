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
- Implement three-level risk categorisation (Low / Medium / High) from binary classification

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
| Serialisation | Joblib                                       |
| Testing     | Pytest                                        |
| Deployment  | Gunicorn, Render                              |

---

## 📁 Folder Structure

```
Credit-Risk-Classification/
│
├── app.py                      # Flask application (routes, form handling)
├── train_model.py              # Training script (download → clean → train → save)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── render.yaml                 # Render deployment config
│
├── data/
│   ├── .gitkeep
│   ├── README.md               # Dataset documentation
│   └── german_credit.csv       # Downloaded at training time
│
├── models/
│   ├── .gitkeep
│   ├── logistic_regression_model.joblib  # Trained model
│   ├── preprocessor.joblib              # Fitted ColumnTransformer
│   └── metrics.joblib                   # Evaluation metrics dict
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Paths, feature lists, thresholds
│   ├── preprocessing.py        # Download, load, clean, build pipeline
│   └── model_utils.py          # Train, evaluate, predict, classify
│
├── templates/
│   ├── base.html               # Base template (navbar, footer)
│   ├── index.html              # Home page
│   ├── predict.html            # Prediction form
│   ├── result.html             # Prediction result display
│   ├── dashboard.html          # Model performance dashboard
│   ├── about.html              # Project information
│   ├── 404.html                # Custom 404 page
│   └── 500.html                # Custom 500 page
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom dark glassmorphism theme
│   ├── js/
│   │   └── script.js           # Form validation & UI enhancements
│   └── images/
│       └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py             # Flask route tests
│   └── test_model.py           # Model & prediction tests
│
└── screenshots/
    └── .gitkeep
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
# 1. Clone or navigate to the project directory
cd "Credit-Risk-Classification"

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate

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

## 🚀 Running the Application

```powershell
# Start the Flask development server
python app.py
```

Open your browser and navigate to: **http://localhost:5000**

### Available Pages

| Route          | Description                                    |
|----------------|------------------------------------------------|
| `/`            | Home page                                      |
| `/predict`     | Prediction form                                |
| `/result`      | Prediction result (after submit)               |
| `/dashboard`   | Model performance dashboard                    |
| `/about`       | Project information                            |
| `/chat`        | Dedicated AI Credit Advisor interactive chat   |
| `/api/chat`    | REST API endpoint for chat messages (POST)     |

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

## 📸 Screenshots

> Place screenshots in the `screenshots/` directory after running the application.

- Home Page (`screenshots/home.png`)
- Prediction Form (`screenshots/predict_form.png`)
- Prediction Result with Risk Gauge & Advisory (`screenshots/prediction_result.png`)
- Model Analytics Dashboard with Confusion Matrix (`screenshots/dashboard.png`)
- About Page with Methodology (`screenshots/about.png`)

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
