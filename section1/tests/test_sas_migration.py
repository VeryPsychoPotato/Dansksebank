import pandas as pd
from cleaning import calculate_risk_scores

def test_active_customers_are_aggregated_correctly():
    df = pd.DataFrame({
        "customer_id": ["C123", "C123", "C234"],
        "status": ["ACTIVE", "ACTIVE", "ACTIVE"],
        "monthly_payment": [100, 200, 300]
    })

    result = calculate_risk_scores(df)

    c123 = result[result["customer_id"] == "C123"].iloc[0]

    assert c123["total_exposure"] == 300
    assert c123["agreement_count"] == 2
    assert c123["avg_exposure"] == 150
    
    c234 = result[result["customer_id"] == "C234"].iloc[0]

    assert c234["total_exposure"] == 300
    assert c234["agreement_count"] == 1
    assert c234["avg_exposure"] == 300
    
def test_inactive_customer_is_kept_with_zero_exposure():
    df = pd.DataFrame({
        "customer_id": ["C123", "C234"],
        "status": ["ACTIVE", "INACTIVE"],
        "monthly_payment": [100, 500]
    })

    result = calculate_risk_scores(df)

    c234 = result[result["customer_id"] == "C234"].iloc[0]

    assert c234["total_exposure"] == 0
    assert c234["agreement_count"] == 0
    assert c234["avg_exposure"] == 0    
    
def test_no_active_agreements_returns_zero_exposure():
    df = pd.DataFrame({
        "customer_id": ["C123", "C234"],
        "status": ["INACTIVE", "INACTIVE"],
        "monthly_payment": [100, 200]
    })

    result = calculate_risk_scores(df)

    assert result["total_exposure"].sum() == 0
    assert result["agreement_count"].sum() == 0
    assert result["avg_exposure"].sum() == 0    