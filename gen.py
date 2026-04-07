import numpy as np
import pandas as pd
import os

np.random.seed(42)  # For reproducibility

n_rows = 5000

# 1. Generate Age (Normal dist: mean=42, std=12, range 25-70)
age = np.clip(np.random.normal(42, 12, n_rows), 25, 70).astype(int)

# 2. Generate Income (Lognormal: 20k-200k INR)
income_log = np.random.lognormal(mean=10.9, sigma=0.5, size=n_rows)  # log(50k) ≈ 10.9
income = np.clip((income_log * 1000).astype(int), 20000, 200000)

# 3. Generate Credit Score (Normal: mean=700, std=80, range 300-900)
credit_score = np.clip(np.random.normal(700, 80, n_rows), 300, 900).astype(int)

# 4. Generate Existing Loans (Poisson: mean=2, range 0-5)
existing_loans = np.random.poisson(2, n_rows)
existing_loans = np.clip(existing_loans, 0, 5).astype(int)

# 5. Generate Employment (85% employed)
employed = np.random.choice([1, 0], size=n_rows, p=[0.85, 0.15]).astype(int)

# 6. Calculate Default Probability based on your exact logic
def calculate_default_prob(age, income, credit_score, existing_loans, employed):
    prob = 0.10  # Base probability
    
    # Age adjustments
    if age < 30:
        prob += 0.08
    elif 30 <= age <= 40:
        prob += 0.04
    elif 40 <= age <= 55:
        prob += 0.02
    else:  # >55
        prob += 0.05
    
    # Income adjustments
    if income < 30000:
        prob += 0.12
    elif 30000 <= income < 50000:
        prob += 0.08
    elif 50000 <= income < 100000:
        prob += 0.02
    else:
        prob -= 0.03
    
    # Credit Score adjustments
    if credit_score < 400:
        prob += 0.30
    elif 400 <= credit_score < 550:
        prob += 0.20
    elif 550 <= credit_score < 650:
        prob += 0.10
    elif 650 <= credit_score < 750:
        prob += 0.02
    else:
        prob -= 0.05
    
    # Existing Loans adjustments
    if existing_loans == 0:
        prob += 0.02
    elif existing_loans == 1:
        prob += 0.01
    elif existing_loans in [2, 3]:
        prob += 0.04
    elif existing_loans == 4:
        prob += 0.08
    else:  # 5
        prob += 0.15
    
    # Employment adjustment
    if employed == 1:
        prob -= 0.05
    else:
        prob += 0.25
    
    return np.clip(prob, 0, 1)

# Generate default labels
default_probs = np.array([calculate_default_prob(a, inc, cs, el, emp) 
                         for a, inc, cs, el, emp in zip(age, income, credit_score, existing_loans, employed)])
default = (np.random.random(n_rows) < default_probs).astype(int)

# Create DataFrame
df = pd.DataFrame({
    'age': age,
    'income': income,
    'credit_score': credit_score,
    'existing_loans': existing_loans,
    'employed': employed,
    'default': default
})

# Save to CSV
df.to_csv('synthetic_loan_data.csv', index=False)

# Data Quality Checks
print("=== DATA QUALITY CHECKS ===")
print(f"Rows: {len(df)}")
print(f"Age range: {df['age'].min()}-{df['age'].max()}")
print(f"Income range: ₹{df['income'].min():,} - ₹{df['income'].max():,}")
print(f"Credit Score range: {df['credit_score'].min()}-{df['credit_score'].max()}")
print(f"Existing Loans range: {df['existing_loans'].min()}-{df['existing_loans'].max()}")
print(f"Employed: {df['employed'].value_counts().to_dict()}")
print(f"Default rate: {df['default'].mean():.1%} ({df['default'].sum()} defaults)")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")
print("\nDataset saved as 'synthetic_loan_data.csv'")