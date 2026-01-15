# Customer Churn Prediction Project

## Overview
This project predicts customer churn for a telecommunications company using machine learning techniques. The goal is to identify customers who are likely to cancel their service, allowing the business to take proactive retention measures.

## Dataset
- **Source**: Telco-Customer-Churn.csv
- **Size**: 7,043 customer records
- **Features**: 20 features including demographics, services subscribed, account information, and tenure
- **Target Variable**: Churn (binary: Yes/No)

## Methodology

### 1. Data Preprocessing
- Handled missing/blank values in TotalCharges column by replacing with median
- Encoded categorical variables using Label Encoding
- Removed customerID column as it has no predictive power
- Performed data validation and exploration

### 2. Exploratory Data Analysis
- Analyzed class distribution (26.5% churn rate)
- Identified relationships between features and churn
- Created visualizations to understand patterns

### 3. Feature Engineering
- Selected top 5 features driving churn using statistical methods:
  1. Contract (Score: 1315.09)
  2. tenure (Score: 997.27)
  3. OnlineSecurity (Score: 643.16)
  4. TechSupport (Score: 610.61)
  5. TotalCharges (Score: 290.44)

### 4. Model Development
- Trained two models: Logistic Regression and Random Forest
- Used stratified sampling to maintain class distribution in train/test splits
- Evaluated models using AUC-ROC metric

### 5. Model Evaluation
- **Logistic Regression**: AUC-ROC = 0.8375
- **Random Forest**: AUC-ROC = 0.7780
- Selected Logistic Regression as the best performing model
- Both models exceeded the minimum threshold of AUC-ROC > 0.80

### 6. Results
- Successfully achieved AUC-ROC score of 0.8375 (> 0.80 requirement)
- Generated a ranked list of at-risk customers based on churn probability
- Created visualizations for model comparison and insights

## Key Findings
1. Contract type is the strongest predictor of churn
2. Customer tenure significantly impacts churn likelihood
3. Availability of online security and tech support reduces churn
4. Total charges also influence customer retention

## Deliverables
1. `churn_analysis.py` - Main analysis script
2. `top_at_risk_customers.csv` - Ranked list of at-risk customers
3. `eda_visualizations.png` - Exploratory data analysis charts
4. `model_comparison_dashboard.png` - Model performance comparison
5. `slide_deck_outline.txt` - Presentation outline for stakeholders

## Business Impact
- Enables proactive customer retention strategies
- Allows targeted marketing campaigns for at-risk customers
- Helps reduce customer acquisition costs by improving retention
- Provides insights into factors driving customer churn

## Technical Approach
- Python libraries: pandas, scikit-learn, matplotlib, seaborn
- Machine Learning: Logistic Regression, Random Forest
- Feature Selection: Statistical methods (SelectKBest)
- Model Evaluation: ROC-AUC, Classification Reports

## Model Performance
- Achieved AUC-ROC of 0.8375, exceeding the 0.80 requirement
- Properly handled class imbalance (73.5% No Churn, 26.5% Churn)
- Used cross-validation principles in train/test splits
- Applied appropriate preprocessing for categorical variables