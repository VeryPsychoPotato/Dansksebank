import numpy as np
import polars as pl

#------------------------------------
# original loop from the task
#------------------------------------

def calculate_total_cost(df):
    results = []
    for _, row in df.iterrows():
        if row['status'] == 'active' and row['currency'] == 'EUR':
            cost = row['monthly_payment'] * 12
            if row['asset_type'] == 'CAR':
                cost *= 0.95  # 5% discount
            elif row['asset_type'] == 'FLEET':
                cost *= 0.90  # 10% discount
        else:
            cost = 0
        results.append(cost)
    df['annual_cost'] = results
    return df

#------------------------------------
# vectorized loop 
#------------------------------------

def calculate_total_cost_vectorized(df):
    df = df.copy()

    # Base condition mask
    mask = (df["status"] == "active") & (df["currency"] == "EUR")

    # Base cost (vectorised)
    cost = np.where(mask, df["monthly_payment"] * 12, 0)

    # Apply discounts (vectorised)
    cost = np.where(mask & (df["asset_type"] == "CAR"), cost * 0.95, cost)
    cost = np.where(mask & (df["asset_type"] == "FLEET"), cost * 0.90, cost)

    df["annual_cost"] = cost
    return df

#------------------------------------
# lazy Polars evaluation 
#------------------------------------

def calculate_total_cost_polars(df):
    lf = pl.from_pandas(df).lazy()

    result = (
        lf.with_columns(
            pl.when((pl.col("status") == "active") & (pl.col("currency") == "EUR"))
            .then(pl.col("monthly_payment") * 12)
            .otherwise(0)
            .alias("annual_cost")
        )
        .with_columns(
            pl.when(pl.col("asset_type") == "CAR")
            .then(pl.col("annual_cost") * 0.95)
            .when(pl.col("asset_type") == "FLEET")
            .then(pl.col("annual_cost") * 0.90)
            .otherwise(pl.col("annual_cost"))
            .alias("annual_cost")
        )
        .collect()
    )

    return result.to_pandas()