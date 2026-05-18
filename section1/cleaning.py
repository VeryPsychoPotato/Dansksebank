import pandas as pd

# read data
url = "https://raw.githubusercontent.com/VeryPsychoPotato/Dansksebank/refs/heads/main/data/data.csv"
df = pd.read_csv(url)

print(df)


def clean_agreements(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Fix lower/upper case names
    df["currency"] = df["currency"].str.upper()
    df["status"] = df["status"].str.lower()

    # Fill missing customer_id
    df["customer_id"] = df["customer_id"].fillna("UNKNOWN")

    # Parse dates (coerce invalid -> NaT)
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    # Date error flag
    df["has_date_error"] = (
        df["start_date"].isna() | df["end_date"].isna()
    )

    # check if both datess are valid
    valid = df["start_date"].notna() & df["end_date"].notna()
    
    df["has_date_logic_error"] = False
    
    # checks if date sequence is correct
    df.loc[valid, "has_date_logic_error"] = (df.loc[valid, "end_date"] >= df.loc[valid, "start_date"])
    
    # Payment validation
    df["monthly_payment"] = pd.to_numeric(df["monthly_payment"], errors="coerce")
    df["has_payment_error"] = df["monthly_payment"].isna() | (df["monthly_payment"] <= 0)
    
    # fills missing customer_id as unknown
    df["customer_id"] = df["customer_id"].fillna("UNKNOWN")

    return df

cleaned_data = clean_agreements(df)
print(cleaned_data)


# count already present error flags in cleaned_data
def summarise_errors(df: pd.DataFrame) -> dict:
    return {
        "date_errors": int(df["has_date_error"].sum()),
        "date_logic_errors": int(df["has_date_error"].sum()),
        "payment_errors": int(df["has_payment_error"].sum()),
    }

errors = summarise_errors(cleaned_data)

print(errors)







