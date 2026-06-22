from pathlib import Path
import pandas as pd
from datasets import load_dataset


DATASET_NAME = "Tobi-Bueck/customer-support-tickets"

BRONZE_DIR = Path("data/bronze")
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset_from_huggingface() -> pd.DataFrame:
    print("Loading dataset from Hugging Face...")

    dataset = load_dataset(DATASET_NAME)

    print("Available dataset splits:", list(dataset.keys()))

    if "train" in dataset:
        split_name = "train"
    else:
        split_name = list(dataset.keys())[0]

    print(f"Using split: {split_name}")

    df = dataset[split_name].to_pandas()

    return df


def save_bronze_data(df: pd.DataFrame) -> None:
    parquet_path = BRONZE_DIR / "support_tickets_raw.parquet"
    csv_path = BRONZE_DIR / "support_tickets_raw.csv"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"Saved parquet file here: {parquet_path}")
    print(f"Saved csv file here: {csv_path}")


if __name__ == "__main__":
    df = load_dataset_from_huggingface()

    print("\nDataset loaded successfully.")
    print("Rows and columns:", df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    save_bronze_data(df)

    print("\nBronze data creation completed.")
