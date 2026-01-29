import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "csv"
OUTPUT_DIR = BASE_DIR / "cleaned"

OUTPUT_DIR.mkdir(exist_ok=True)

COLUMNS_TO_KEEP = [
    "CompanyName",
    "CompanyNumber",
    "CompanyCategory",
    "CompanyStatus",
    "CountryOfOrigin",
    "DissolutionDate",
    "IncorporationDate",
    "Accounts.AccountCategory",
    "SICCode.SicText_1"
]

for csv_file in INPUT_DIR.glob("*.csv"):
    print(f"Processing {csv_file.name}")

    df = pd.read_csv(csv_file, low_memory=False)

    # IMPORTANT: normalize Companies House headers
    df.columns = df.columns.str.strip()

    keep_cols = [c for c in COLUMNS_TO_KEEP if c in df.columns]
    df = df[keep_cols]

    missing = set(COLUMNS_TO_KEEP) - set(keep_cols)
    if missing:
        print(f"⚠️ Missing columns: {missing}")

    df.to_csv(OUTPUT_DIR / csv_file.name, index=False)
    print("✅ Done\n")


