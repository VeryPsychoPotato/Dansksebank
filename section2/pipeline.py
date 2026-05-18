import pandas as pd
import logging
from sqlalchemy import create_engine, text

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