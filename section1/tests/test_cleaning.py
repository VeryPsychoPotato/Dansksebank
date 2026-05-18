import pandas as pd
from section1.cleaning import clean_agreements, summarise_errors

def test_all_valid_data():
    df = pd.DataFrame({
        "agreement_id": ["A123"],
        "customer_id": ["C321"],
        "asset_type": ["FOND"],
        "start_date": ["2023-01-01"],
        "end_date": ["2024-01-01"],
        "monthly_payment": [100.0],
        "currency": ["EUR"],
        "status": ["ACTIVE"]
    })
    
    cleaned = clean_agreements(df)

    assert len(cleaned) == 1
    row = cleaned.iloc[0]
    
    assert row["currency"] == "EUR"
    assert row["status"] == "ACTIVE"

    assert cleaned["has_date_error"].sum() == 0
    assert cleaned["has_date_logic_error"].sum() == 0
    assert cleaned["has_payment_error"].sum() == 0    
    
def test_missing_customer_id():
    df = pd.DataFrame({
        "agreement_id": ["A123"],
        "customer_id": [],
        "asset_type": ["FUND"],
        "start_date": ["2023-01-01"],
        "end_date": ["2024-01-01"],
        "monthly_payment": [100.0],
        "currency": ["EUR"],
        "status": ["ACTIVE"]
    })
    
    cleaned = clean_agreements(df)    
    
    assert all(cleaned["customer_id"] == "MISSING")
    
def test_missing_payment():
    df = pd.DataFrame({
        "agreement_id": ["A123"],
        "customer_id": ["C321"],
        "asset_type": ["FOND"],
        "start_date": ["2023-01-01"],
        "end_date": ["2024-01-01"],
        "monthly_payment": [],
        "currency": ["EUR"],
        "status": ["ACTIVE"]
    })
    
    cleaned = clean_agreements(df)  
    
    assert cleaned["has_payment_error"].sum() == 1
    
def test_wrong_payment_date_order():
    df = pd.DataFrame({
        "agreement_id": ["A123"],
        "customer_id": ["C321"],
        "asset_type": ["FOND"],
        "start_date": ["2025-01-01"],
        "end_date": ["2024-01-01"],
        "monthly_payment": [100.0],
        "currency": ["EUR"],
        "status": ["ACTIVE"]
    })
    
    cleaned = clean_agreements(df)  
    errors = summarise_errors(cleaned)  
    
    assert errors["date_logic_errors"] > 0