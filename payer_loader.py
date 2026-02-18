import argparse
import pandas as pd
from datetime import datetime
from functools import singledispatch
from typing import List, Dict




@singledispatch
def prepare_dataframe(data):
    raise TypeError("Unsupported input type for prepare_dataframe")


@prepare_dataframe.register
def _(data: str) -> pd.DataFrame:
    """
    If input is a string, treat it as file path and read CSV.
    """
    print("Reading data from CSV file...")
    return pd.read_csv(data)


@prepare_dataframe.register
def _(data: list) -> pd.DataFrame:
    """
    If input is a list of dictionaries, convert directly to DataFrame.
    """
    print("Converting manual input to DataFrame...")
    return pd.DataFrame(data)




def transform_data(df: pd.DataFrame, payer: str) -> pd.DataFrame:
    """
    Perform common and payer-specific transformations.
    """

    # Add ingestion timestamp
    df["ingestion_timestamp"] = datetime.now()

    # Convert service_date to datetime
    df["service_date"] = pd.to_datetime(df["service_date"], errors="coerce")

    # Example payer-specific logic
    if payer.lower() == "anthem":
        # Apply 5% processing adjustment
        df["claim_amount"] = df["claim_amount"] * 1.05
        print("Applied Anthem-specific transformation.")

    return df




class BaseLoader:
    """
    Base class defining interface for loaders.
    """

    def __init__(self, payer_name: str):
        self.payer_name = payer_name.lower()

    def load(self, df: pd.DataFrame):
        raise NotImplementedError("Subclasses must implement the load method.")


# ---------------------------------------------------
# 4. CHILD CLASS WITH METHOD OVERRIDING
# ---------------------------------------------------

class PayerLoader(BaseLoader):

    def load(self, df: pd.DataFrame):
        table_name = self._resolve_table_name()

        print(f"\nLoading data into SNOWFLAKE.RAW.{table_name}")
        print(f"Total Records: {len(df)}")
        print("Load completed successfully.\n")

    def _resolve_table_name(self) -> str:
        if self.payer_name == "anthem":
            return "ANTHEM"
        elif self.payer_name == "cigna":
            return "CIGNA"
        else:
            return "GENERIC_CLAIMS"




def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Multi-Source Payer Loader Utility"
    )

    parser.add_argument(
        "--source",
        type=str,
        required=False,
        help="Path to source CSV file"
    )

    parser.add_argument(
        "--payer",
        type=str,
        required=True,
        choices=["anthem", "cigna", "manual"],
        help="Payer name"
    )

    return parser.parse_args()




def main():

    args = parse_arguments()

    # Case A: Manual input
    if args.payer == "manual":
        manual_data: List[Dict] = [
            {
                "member_id": "M1001",
                "claim_id": "C9001",
                "claim_amount": 250.0,
                "service_date": "2024-01-10",
                "payer_name": "manual"
            },
            {
                "member_id": "M1002",
                "claim_id": "C9002",
                "claim_amount": 300.0,
                "service_date": "2024-01-12",
                "payer_name": "manual"
            }
        ]

        df = prepare_dataframe(manual_data)

    # Case B: File input
    else:
        if not args.source:
            raise ValueError("Source file path must be provided for file-based loading.")

        df = prepare_dataframe(args.source)

    # Transform data
    df = transform_data(df, args.payer)

    # Initialize loader
    loader = PayerLoader(args.payer)

    # Load data
    loader.load(df)


if __name__ == "__main__":
    main()
