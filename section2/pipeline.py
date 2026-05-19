import sys
import os
sys.path.append(os.path.abspath(".."))

import pandas as pd
import logging
from sqlalchemy import create_engine
from pathlib import Path
from section1.cleaning import clean_agreements
from section1.sas_migration import calculate_risk_scores
from section1.cleaning import summarise_errors
# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



# ETL Pipeline


class AgreementPipeline:
    def __init__(self, db_path="agreements.db"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.raw_table = "raw_agreements"
        self.processed_table = "processed_agreements"

    # ------------------------
    # Seed DB (part of extract requirement)
    # ------------------------
    def seed_db(self, df: pd.DataFrame):
        logging.info("Seeding database...")
        df.to_sql(self.raw_table, self.engine, if_exists="replace", index=False)

    # ------------------------
    # Extract
    # ------------------------
    def extract(self) -> pd.DataFrame:
        logging.info("Extracting data from DB...")
        query = f"SELECT * FROM {self.raw_table}"
        df = pd.read_sql(query, self.engine)
        logging.info(f"Extracted {len(df)} records")
        return df

    # ------------------------
    # Transform
    # ------------------------
    def transform(self, df: pd.DataFrame):
        logging.info("Transforming data...")

        cleaned = clean_agreements(df)
        risk_scores = calculate_risk_scores(cleaned)

        errors = summarise_errors(cleaned)

        logging.info("Transformation complete")
        return cleaned, risk_scores, errors

    # ------------------------
    # Load
    # ------------------------
    def load(self, cleaned: pd.DataFrame, risk_scores: pd.DataFrame, errors: dict):
        logging.info("Loading data...")

        # --- Load to SQLite (idempotent) ---
        cleaned.to_sql(self.processed_table, self.engine, if_exists="replace", index=False)

        # --- Excel report ---
        excel_path = Path("report.xlsx")
        with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
            for asset, group in cleaned.groupby("asset_type"):
                group.to_excel(writer, sheet_name=str(asset), index=False)

        # --- Text report ---
        txt_path = Path("report.txt")

        summary = f"""
RUN SUMMARY
-----------
Total records: {len(cleaned)}

ERROR COUNTS
------------
Date errors: {errors['date_errors']}
Date logic errors: {errors['date_logic_errors']}
Payment errors: {errors['payment_errors']}

RISK SCORE SUMMARY
------------------
Total customers: {len(risk_scores)}
Total exposure: {risk_scores['total_exposure'].sum():.2f}
Average exposure: {risk_scores['avg_exposure'].mean():.2f}
"""

        txt_path.write_text(summary.strip())

        logging.info("Load complete")

    # ------------------------
    # Run pipeline
    # ------------------------
    def run(self, source_df: pd.DataFrame):
        logging.info("Starting pipeline...")

        self.seed_db(source_df)
        df = self.extract()

        cleaned, risk_scores, errors = self.transform(df)

        self.load(cleaned, risk_scores, errors)

        logging.info("Pipeline finished successfully")


# ----------------------------
# Execute pipeline
# ----------------------------

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/VeryPsychoPotato/Dansksebank/refs/heads/main/data/data.csv"
    df = pd.read_csv(url)

    pipeline = AgreementPipeline()
    pipeline.run(df)



