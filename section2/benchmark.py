import pandas as pd
import numpy as np
import time
from optimisation import calculate_total_cost_vectorized
from optimisation import calculate_total_cost_polars
from optimisation import calculate_total_cost

def create_dataset(n=5000000):
    return pd.DataFrame({
        "status": np.random.choice(["active", "inactive"], n),
        "currency": np.random.choice(["EUR", "USD"], n),
        "monthly_payment": np.random.rand(n) * 1000,
        "asset_type": np.random.choice(["CAR", "FLEET", "OTHER"], n)
    })



def benchmark():
    df = create_dataset()
    
    # original
    start = time.time()
    calculate_total_cost(df.copy())
    t1 = time.time() - start

    # Pandas vectorised
    start = time.time()
    calculate_total_cost_vectorized(df.copy())
    t2 = time.time() - start

    # Polars
    start = time.time()
    calculate_total_cost_polars(df.copy())
    t3 = time.time() - start

    print({
        "original": t1,
        "pandas_vectorised": t2,
        "polars": t3
    })

benchmark()