import pandas as pd

# read data
df = pd.read_csv('C:/Users/Kernius/Danskebank/data/data.csv')

print(df)

def calculate_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize status just in case (similaar to previous task)
    df["status"] = df["status"].str.lower()
    
    # All unique customers (includes inactive-only ones)
    customers = pd.DataFrame({"customer_id": df["customer_id"].unique()})


    # Filter only active agreements (matches SAS IF status = 'active')
    active = df[df["status"] == "active"]

    # Aggregate per customer
    grouped = active.groupby("customer_id", as_index=False).agg(
        total_exposure=("monthly_payment", "sum"),
        agreement_count=("monthly_payment", "count")
    )

    # Merge to keep ALL customers
    result = customers.merge(grouped, on="customer_id", how="left")

    # Fill missing values for inactive-only customers
    result["total_exposure"] = result["total_exposure"].fillna(0)
    result["agreement_count"] = result["agreement_count"].fillna(0)

    # Compute average safely
    result["avg_exposure"] = (
        result["total_exposure"] /
        result["agreement_count"].replace(0, pd.NA)
    )

    # Replace NaN/inf with 0 (matches SAS logic)
    result["avg_exposure"] = result["avg_exposure"].fillna(0)

    return result

calculated_risk_scores = calculate_risk_scores(df)

print(calculated_risk_scores)