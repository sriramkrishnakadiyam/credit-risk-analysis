# Data Directory

This directory stores the German Credit dataset.

## Dataset: Statlog (German Credit Data)

- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))
- **Direct URL:** `https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data`
- **License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)
- **Citation:** Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. Irvine, CA: University of California, School of Information and Computer Science.

## Description

| Property   | Value                                                   |
|------------|---------------------------------------------------------|
| Samples    | 1,000                                                   |
| Features   | 20 (7 numerical, 13 categorical)                       |
| Target     | `credit_risk` — 1 (Good), 2 (Bad)                      |
| Format     | Space-separated values, no header row                   |

The dataset is automatically downloaded when you run `python train_model.py`. It will be saved as `german_credit.csv` in this directory.

## Features

| # | Name                       | Type        | Description                          |
|---|----------------------------|-------------|--------------------------------------|
| 1 | status_checking_account    | Categorical | Status of existing checking account  |
| 2 | duration_months            | Numerical   | Duration in months                   |
| 3 | credit_history             | Categorical | Credit history                       |
| 4 | purpose                    | Categorical | Purpose of the loan                  |
| 5 | credit_amount              | Numerical   | Credit amount                        |
| 6 | savings_account            | Categorical | Savings account / bonds              |
| 7 | employment_since           | Categorical | Present employment since             |
| 8 | installment_rate           | Numerical   | Installment rate (% of income)       |
| 9 | personal_status_sex        | Categorical | Personal status and sex              |
| 10| other_debtors              | Categorical | Other debtors / guarantors           |
| 11| residence_since            | Numerical   | Present residence since              |
| 12| property                   | Categorical | Property                             |
| 13| age                        | Numerical   | Age in years                         |
| 14| other_installment_plans    | Categorical | Other installment plans              |
| 15| housing                    | Categorical | Housing                              |
| 16| num_existing_credits       | Numerical   | Number of existing credits           |
| 17| job                        | Categorical | Job                                  |
| 18| num_dependents             | Numerical   | Number of dependents                 |
| 19| telephone                  | Categorical | Telephone                            |
| 20| foreign_worker             | Categorical | Foreign worker                       |
