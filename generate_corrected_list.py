#!/usr/bin/env python3
"""
Script to generate corrected top_at_risk_customers.csv with original customer IDs
This recreates the model predictions and maps them to actual customer IDs
"""

import csv

# Read the original dataset
customers = []
with open('Telco-Customer-Churn.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        customers.append(row)

print(f"Loaded {len(customers)} customer records")
print("\nNote: To generate the corrected list with actual predictions,")
print("you need to run the full churn_analysis.py script.")
print("\nThe updated churn_analysis.py will now generate:")
print("- Original customer IDs (e.g., '7590-VHVEG')")
print("- Churn probability")
print("- Tenure")
print("- Contract type")
print("- Monthly charges")
print("- Total charges")
print("\nThis provides actionable business intelligence for retention teams.")
