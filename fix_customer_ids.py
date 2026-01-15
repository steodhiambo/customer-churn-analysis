import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif

# Load data
df = pd.read_csv('Telco-Customer-Churn.csv')
original_data = df.copy()

# Handle TotalCharges
df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Encode categorical variables
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
categorical_columns.remove('customerID')

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))

# Prepare features and target
X = df.drop(['Churn', 'customerID'], axis=1)
y = df['Churn']

# Feature selection - top 5
selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)

# Split data
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
    X_selected, y, df.index, test_size=0.2, random_state=42, stratify=y
)

# Train model
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train, y_train)

# Get predictions
churn_probabilities = lr_model.predict_proba(X_test)[:, 1]

# Create results with original customer IDs
results_df = pd.DataFrame({
    'customerID': original_data.iloc[idx_test]['customerID'].values,
    'churn_probability': churn_probabilities,
    'tenure': original_data.iloc[idx_test]['tenure'].values,
    'Contract': original_data.iloc[idx_test]['Contract'].values,
    'MonthlyCharges': original_data.iloc[idx_test]['MonthlyCharges'].values,
    'TotalCharges': original_data.iloc[idx_test]['TotalCharges'].values
})

# Sort by probability
results_df = results_df.sort_values('churn_probability', ascending=False)

# Save top 20
top_20 = results_df.head(20)
top_20.to_csv('top_at_risk_customers.csv', index=False)

print("✅ Updated top_at_risk_customers.csv with original customer IDs")
print("\nTop 20 At-Risk Customers:")
print(top_20.to_string(index=False))
