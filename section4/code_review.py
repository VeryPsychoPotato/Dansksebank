import pandas as pd
import sqlalchemy

# hardcoded login and plain text login is very bad from security side
engine = sqlalchemy.create_engine("postgresql://admin:password123@prod-db:5432/finance")

def get_customer_data(customer_id):
    # should be validation check for customer_id, query could break simply becausse of
    # invalid string input. Also input without validaion could be used for injection attacks
    query = "SELECT * FROM customers WHERE customer_id = '" + customer_id + "'"
    # reads all table data into dataframe even few columns are needed, could be unnecassary performance/cost issue
    df = pd.read_sql(query, engine)
    data = []
    for i in range(0, len(df)):
        row = df.iloc[i]
        data.append({
            'id': row['customer_id'],
            'name': row['customer_name'],
            
            # issues using flaot on money (balance), could lose presicion, better use decimal for better precision and avoids rounding errors
            'balance': float(row['balance'])
        })
    return data

def process_all_customers():
    all_ids = pd.read_sql("SELECT customer_id FROM customers", engine)
    # loads all ids into the list and then for every id adds another list with customer data
    # results will be list within the list, which probably is not great
    # also similar performance issues with sql like in previous sql task
    # one query for every customer, could be big performance issues
    results = []
    # very generic use of id, better use customer_id
    for id in all_ids['customer_id']:
        results.append(get_customer_data(id))
    return results

# improved code snippet
import os
from decimal import Decimal
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DATABASE_URL")  # e.g. postgresql://user:pass@host:port/db
engine = create_engine(DB_URL)

def get_customer_data(customer_id: str):
    # ✅ Parameterized query (prevents SQL injection)
    query = text("""
        SELECT customer_id, customer_name, balance
        FROM customers
        WHERE customer_id = :customer_id
    """)

    df = pd.read_sql(query, engine, params={"customer_id": customer_id})
    
    data = []
    for i in range(0, len(df)):
     row = df.iloc[i]
     data.append({
         'id': row['customer_id'],
         'name': row['customer_name'],
         'balance': Decimal(row['balance'])
     })
    return data

def process_all_customers():
    query = """
    SELECT customer_id, customer_name, balance
    FROM customers
    """
    
    df = pd.read_sql(query, engine)
    
    results = [
    {
        "id": row.customer_id,
        "name": row.customer_name,
        "balance": Decimal(row.balance) if row.balance is not None else None,
    }
    for row in df.itertuples(index=False)
]
    return results