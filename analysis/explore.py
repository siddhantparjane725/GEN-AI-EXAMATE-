
"""Explore MatdarMitra records using pandas."""

import pandas as pd
from app.records import load_records


def explore():

    records = load_records()

    df = pd.DataFrame(records)

    print("\n========== MATDARMITRA DATA EXPLORATION ==========\n")

    # Fact 1: Total records
    print("FACT 1: Total records")
    print("Total:", len(df))

    # Fact 2: Record types
    print("\nFACT 2: Records by type")
    print(df["record_type"].value_counts().to_string())

    # Fact 3: Categories
    print("\nFACT 3: Records by category")
    print(
        df["category"]
        .fillna("uncategorized")
        .value_counts()
        .to_string()
    )

    print("\n===============================================\n")


if __name__ == "__main__":
    explore()
