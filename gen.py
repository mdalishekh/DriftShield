import numpy as np
import pandas as pd

np.random.seed(42)
n_rows = 5000

# 1. Generate Age first (25-70)
age = np.clip(np.random.normal(42, 12, n_rows), 25, 70).astype(int)

# 2. Generate Income BASED ON AGE (young = low, old = high, realistic spread)
income = np.zeros(n_rows, dtype=int)

for i in range(n_rows):
    if age[i] < 30:        # Young: 20k-80k (mean ~45k)
        income[i] = np.random.randint(20000, 80000)
    elif age[i] < 40:      # 30-39: 30k-120k (mean ~75k)
        income[i] = np.random.randint(30000, 120000)
    elif age[i] < 55:      # 40-54: 50k-160k (mean ~105k)
        income[i] = np.random.randint(50000, 160000)
    else:                  # 55+: 40k-200k (mean ~95k, retirement dip)
        income[i] = np.random.randint(40000, 200000)

# 3. Credit Score
credit_score = np.clip(np.random.normal(700, 80, n_rows), 300, 900).astype(int)

# 4. Existing Loans (Poisson)
existing_loans = np.clip(np.random.poisson(2, n_rows), 0, 5).astype(int)

# 5. Employment (85% employed)
employed = np.random.choice([1, 0], size=n_rows, p=[0.85, 0.15]).astype(int)

# 6. Default probability (your exact logic)
def calculate_default_prob(age, income, credit_score, existing_loans, employed):
    prob = 0.10
    
    # Age adjustments
    if age < 30: prob += 0.08
    elif 30 <= age <= 40: prob += 0.04
    elif 40 <= age <= 55: prob += 0.02
    else: prob += 0.05
    
    # Income adjustments  
    if income < 30000: prob += 0.12
    elif 30000 <= income < 50000: prob += 0.08
    elif 50000 <= income < 100000: prob += 0.02
    else: prob -= 0.03
    
    # Credit Score
    if credit_score < 400: prob += 0.30
    elif 400 <= credit_score < 550: prob += 0.20
    elif 550 <= credit_score < 650: prob += 0.10
    elif 650 <= credit_score < 750: prob += 0.02
    else: prob -= 0.05
    
    # Existing Loans
    if existing_loans == 0: prob += 0.02
    elif existing_loans == 1: prob += 0.01
    elif existing_loans in [2, 3]: prob += 0.04
    elif existing_loans == 4: prob += 0.08
    else: prob += 0.15
    
    # Employment
    if employed == 1: prob -= 0.05
    else: prob += 0.25
    
    return np.clip(prob, 0, 1)

# Generate defaults
default_probs = [calculate_default_prob(a, inc, cs, el, emp) 
                for a, inc, cs, el, emp in zip(age, income, credit_score, existing_loans, employed)]
default = (np.random.random(n_rows) < default_probs).astype(int)

# Create & Save CSV
df = pd.DataFrame({
    'age': age, 'income': income, 'credit_score': credit_score,
    'existing_loans': existing_loans, 'employed': employed, 'default': default
})

df.to_csv('synthetic_loan_data.csv', index=False)

# Quality Check
print("=== REALISTIC DATA GENERATED ===")
print(f"Total rows: {len(df)}")
print(f"Income range: ₹{df['income'].min():,} - ₹{df['income'].max():,}")
print(f"Income by Age groups:")
print(df.groupby('age//5*5')['income'].agg(['min','mean','max']).round(0))
print(f"\nSample incomes: {sorted(df['income'].unique()[:10])}...")
print(f"Default rate: {df['default'].mean():.1%}")
print("File saved: synthetic_loan_data.csv")