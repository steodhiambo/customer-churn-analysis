import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """
    Load the customer churn dataset from the CSV file.
    """
    df = pd.read_csv('Telco-Customer-Churn.csv')
    return df

def explore_dataset(df):
    """Explore the dataset structure"""
    print("Dataset Shape:", df.shape)
    print("\nColumn Names:")
    print(df.columns.tolist())
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 5 Rows:")
    print(df.head())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nBasic Statistics:")
    print(df.describe())

    # Check for any blank strings in TotalCharges specifically
    total_charges_blank = df[df['TotalCharges'].str.strip() == '']
    print(f"\nRows with blank TotalCharges: {len(total_charges_blank)}")

    return df

def handle_missing_values(df):
    """Handle missing values in TotalCharges column"""
    print(f"\nBefore handling missing/blank values in TotalCharges: {df['TotalCharges'].isnull().sum()} null values")

    # Replace blank strings with NaN
    df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)

    # Convert TotalCharges to numeric, handling any non-numeric values
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Fill missing values with median
    median_total_charges = df['TotalCharges'].median()
    df['TotalCharges'].fillna(median_total_charges, inplace=True)

    print(f"After handling missing values in TotalCharges: {df['TotalCharges'].isnull().sum()} missing values")

    return df

def encode_categorical_variables(df):
    """Encode categorical variables"""
    # Identify categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    categorical_columns.remove('customerID')  # Remove customerID from encoding

    # Encode categorical variables using Label Encoding
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    print(f"Encoded categorical columns: {categorical_columns}")

    return df, label_encoders

def remove_customer_id(df):
    """Remove customerID column as it has no predictive power"""
    df = df.drop(columns=['customerID'])
    print("Removed customerID column")
    return df

def perform_eda(df):
    """Perform exploratory data analysis"""
    print("\nPerforming Exploratory Data Analysis...")

    # Distribution of target variable
    churn_counts = df['Churn'].value_counts()
    print(f"\nChurn Distribution:\n{churn_counts}")

    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Churn distribution
    axes[0, 0].bar(['No Churn', 'Churn'], [churn_counts.iloc[0], churn_counts.iloc[1]])
    axes[0, 0].set_title('Distribution of Churn')
    axes[0, 0].set_ylabel('Count')

    # Tenure vs Churn
    df_temp = df.copy()
    df_temp['Churn'] = df_temp['Churn'].map({0: 'No', 1: 'Yes'})  # Map back for visualization
    churn_by_tenure = df.groupby('Churn')['tenure'].mean()
    axes[0, 1].bar(['No Churn', 'Churn'], churn_by_tenure.values)
    axes[0, 1].set_title('Average Tenure by Churn Status')
    axes[0, 1].set_ylabel('Average Tenure')

    # Monthly Charges vs Churn
    churn_by_monthly = df.groupby('Churn')['MonthlyCharges'].mean()
    axes[1, 0].bar(['No Churn', 'Churn'], churn_by_monthly.values)
    axes[1, 0].set_title('Average Monthly Charges by Churn Status')
    axes[1, 0].set_ylabel('Average Monthly Charges')

    # Contract vs Churn
    contract_churn = pd.crosstab(df['Contract'], df['Churn'], normalize='index')
    contract_churn.plot(kind='bar', ax=axes[1, 1])
    axes[1, 1].set_title('Churn Rate by Contract Type')
    axes[1, 1].set_ylabel('Proportion')
    axes[1, 1].legend(title='Churn')

    plt.tight_layout()
    plt.savefig('eda_visualizations.png')
    plt.show()

def handle_class_imbalance(X, y):
    """Identify and handle class imbalance"""
    print(f"\nClass distribution in target variable:")
    print(y.value_counts(normalize=True))

    # For now, we'll proceed with the original distribution
    # In a real scenario, we might use techniques like SMOTE or class weights
    return X, y

def feature_selection(X, y, k=5):
    """Perform feature selection to find top 5 drivers of churn"""
    selector = SelectKBest(score_func=f_classif, k=k)
    X_selected = selector.fit_transform(X, y)

    # Get selected feature indices
    selected_features_idx = selector.get_support(indices=True)
    selected_features = X.columns[selected_features_idx]

    print(f"\nTop {k} features selected:")
    for i, feature in enumerate(selected_features):
        print(f"{i+1}. {feature} (Score: {selector.scores_[selected_features_idx[i]]:.2f})")

    return X_selected, selected_features, selector

def train_logistic_regression(X_train, y_train):
    """Train Logistic Regression model"""
    print("\nTraining Logistic Regression model...")
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train, y_train)
    print("Logistic Regression model trained successfully!")

    return lr_model

def train_random_forest(X_train, y_train):
    """Train Random Forest model"""
    print("\nTraining Random Forest model...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    print("Random Forest model trained successfully!")

    return rf_model

def evaluate_models(models, X_test, y_test):
    """Evaluate models and select best performer based on AUC-ROC"""
    results = {}

    for name, model in models.items():
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred_proba)

        results[name] = {
            'model': model,
            'auc_score': auc_score
        }

        print(f"\n{name} AUC-ROC Score: {auc_score:.4f}")

    # Find the best model
    best_model_name = max(results, key=lambda x: results[x]['auc_score'])
    best_model = results[best_model_name]['model']

    print(f"\nBest performing model: {best_model_name} with AUC-ROC: {results[best_model_name]['auc_score']:.4f}")

    return best_model, best_model_name, results

def fine_tune_model(model, model_name, X_train, y_train, X_test, y_test):
    """Fine-tune selected model if needed"""
    print(f"\nFine-tuning {model_name} model...")

    # For demonstration, I'll adjust hyperparameters for Random Forest if it's the best model
    if model_name == "Random Forest":
        # Try different hyperparameters
        rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        rf_model.fit(X_train, y_train)

        # Evaluate the fine-tuned model
        y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred_proba)

        print(f"Fine-tuned Random Forest AUC-ROC Score: {auc_score:.4f}")

        if auc_score > 0.80:
            print("Model meets AUC-ROC > 0.80 requirement!")
            return rf_model
        else:
            print("Fine-tuned model does not meet AUC-ROC > 0.80 requirement.")
            return model

    # For Logistic Regression, we could try different regularization parameters
    elif model_name == "Logistic Regression":
        lr_model = LogisticRegression(C=0.1, random_state=42, max_iter=1000)
        lr_model.fit(X_train, y_train)

        # Evaluate the fine-tuned model
        y_pred_proba = lr_model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred_proba)

        print(f"Fine-tuned Logistic Regression AUC-ROC Score: {auc_score:.4f}")

        if auc_score > 0.80:
            print("Model meets AUC-ROC > 0.80 requirement!")
            return lr_model
        else:
            print("Fine-tuned model does not meet AUC-ROC > 0.80 requirement.")
            return model

    return model

def generate_at_risk_customers(best_model, X_test, original_test_df, model_name):
    """Generate list of at-risk customers sorted by probability"""
    print(f"\nGenerating list of at-risk customers using {model_name}...")

    # Get churn probabilities
    churn_probabilities = best_model.predict_proba(X_test)[:, 1]

    # Create a dataframe with customer IDs and their churn probabilities
    risk_df = pd.DataFrame({
        'customerID': original_test_df['customerID'].values,
        'churn_probability': churn_probabilities,
        'tenure': original_test_df['tenure'].values,
        'Contract': original_test_df['Contract'].values,
        'MonthlyCharges': original_test_df['MonthlyCharges'].values,
        'TotalCharges': original_test_df['TotalCharges'].values
    })

    # Sort by churn probability in descending order
    risk_df = risk_df.sort_values(by='churn_probability', ascending=False)

    # Get top 20 at-risk customers
    top_at_risk = risk_df.head(20)

    print(f"\nTop 20 At-Risk Customers:")
    print(top_at_risk)

    # Save to CSV
    top_at_risk.to_csv('top_at_risk_customers.csv', index=False)
    print("\nAt-risk customer list saved to 'top_at_risk_customers.csv'")

    return top_at_risk

def create_dashboard_visualization(results, X_test, y_test, best_model, best_model_name):
    """Create dashboard/visualization"""
    print("\nCreating dashboard visualizations...")

    # Plot AUC-ROC curves for all models
    from sklearn.metrics import roc_curve

    plt.figure(figsize=(12, 5))

    # Subplot 1: Model Comparison
    plt.subplot(1, 2, 1)
    for name, result in results.items():
        model = result['model']
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        plt.plot(fpr, tpr, label=f'{name} (AUC = {result["auc_score"]:.3f})')

    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves Comparison')
    plt.legend()

    # Subplot 2: Feature Importance (for Random Forest)
    if best_model_name == "Random Forest":
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]  # Top 10 features

        plt.subplot(1, 2, 2)
        plt.bar(range(len(indices)), importances[indices])
        plt.title('Top 10 Feature Importances (Random Forest)')
        plt.xticks(range(len(indices)), [f'Feature_{i}' for i in indices], rotation=45)

    plt.tight_layout()
    plt.savefig('model_comparison_dashboard.png')
    plt.show()

def prepare_slide_deck():
    """Prepare slide deck with findings and recommendations"""
    print("\nPreparing slide deck outline...")

    slides = [
        "Customer Churn Prediction - Executive Summary",
        "Business Problem & Objectives",
        "Data Overview & Quality",
        "Exploratory Data Analysis",
        "Feature Engineering & Selection",
        "Model Development & Training",
        "Model Evaluation & Selection",
        "Key Findings & Insights",
        "At-Risk Customer List",
        "Recommendations & Next Steps"
    ]

    print("Slide deck outline:")
    for i, slide in enumerate(slides, 1):
        print(f"{i}. {slide}")

    # Create a simple text file with the outline
    with open('slide_deck_outline.txt', 'w') as f:
        f.write("Customer Churn Prediction - Slide Deck Outline\n")
        f.write("="*50 + "\n\n")
        for i, slide in enumerate(slides, 1):
            f.write(f"{i}. {slide}\n")

    print("\nSlide deck outline saved to 'slide_deck_outline.txt'")

def main():
    """Main function to execute the churn prediction pipeline"""
    print("Starting Customer Churn Prediction Pipeline...")

    # Step 1: Load data
    df = load_data()
    original_data = df.copy()  # Keep original data for customer IDs
    print("Data loaded successfully!")

    # Step 2: Explore dataset
    df = explore_dataset(df)

    # Step 3: Handle missing values
    df = handle_missing_values(df)

    # Step 4: Encode categorical variables
    df, label_encoders = encode_categorical_variables(df)

    # Step 5: Remove customerID
    df = remove_customer_id(df)

    # Step 6: Perform EDA
    perform_eda(df.copy())  # Pass a copy to preserve original for later use

    # Prepare features and target
    X = df.drop('Churn', axis=1)
    y = df['Churn']

    # Step 7: Handle class imbalance
    X, y = handle_class_imbalance(X, y)

    # Step 8: Feature selection
    X_selected, selected_features, selector = feature_selection(X, y, k=5)

    # Step 9: Split data
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X_selected, y, df.index, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    # Step 10: Train Logistic Regression
    lr_model = train_logistic_regression(X_train, y_train)

    # Step 11: Train Random Forest
    rf_model = train_random_forest(X_train, y_train)

    # Step 12: Evaluate models
    models = {
        "Logistic Regression": lr_model,
        "Random Forest": rf_model
    }
    best_model, best_model_name, results = evaluate_models(models, X_test, y_test)

    # Step 13: Fine-tune model if needed
    best_model = fine_tune_model(best_model, best_model_name, X_train, y_train, X_test, y_test)

    # Step 14: Generate at-risk customers list
    original_test_df = original_data.iloc[idx_test].copy()
    top_at_risk = generate_at_risk_customers(best_model, X_test, original_test_df, best_model_name)

    # Step 15: Create dashboard
    create_dashboard_visualization(results, X_test, y_test, best_model, best_model_name)

    # Step 16: Prepare slide deck
    prepare_slide_deck()

    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    main()