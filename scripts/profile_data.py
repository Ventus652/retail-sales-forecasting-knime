"""Profile the raw and cleaned retail datasets used by the KNIME project.

This small portfolio companion does not replace the original KNIME workflow. It
offers a transparent, command-line check of the dataset shapes, missing values,
duplicate store/date keys and date coverage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV and raise a clear error when it is unavailable."""
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path, low_memory=False)


def normalize_store(series: pd.Series) -> pd.Series:
    """Normalize store identifiers without changing missing values."""
    return series.astype("string").str.strip()


def find_date_column(frame: pd.DataFrame) -> str | None:
    """Return the first known date-column name."""
    for candidate in ("Date", "Date (Date&time)"):
        if candidate in frame.columns:
            return candidate
    return None


def profile(frame: pd.DataFrame) -> dict[str, Any]:
    """Build a JSON-serializable quality profile for one dataframe."""
    result: dict[str, Any] = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "missing_values": int(frame.isna().sum().sum()),
    }

    if "Store" in frame.columns:
        stores = normalize_store(frame["Store"])
        result["unique_stores"] = int(stores.nunique(dropna=True))

    date_column = find_date_column(frame)
    if date_column:
        dates = pd.to_datetime(frame[date_column], errors="coerce")
        result["invalid_dates"] = int(dates.isna().sum())
        if dates.notna().any():
            result["date_min"] = dates.min().date().isoformat()
            result["date_max"] = dates.max().date().isoformat()

        if "Store" in frame.columns:
            keys = pd.DataFrame(
                {"Store": normalize_store(frame["Store"]), "Date": dates}
            )
            result["duplicate_store_date_rows"] = int(
                keys.duplicated(subset=["Store", "Date"], keep=False).sum()
            )

    for open_column in ("Open", "Open_clean"):
        if open_column in frame.columns:
            numeric_open = pd.to_numeric(frame[open_column], errors="coerce")
            result["open_store_rows"] = int(numeric_open.eq(1).sum())
            break

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile the retail project's raw and cleaned CSV files."
    )
    parser.add_argument("--stores", type=Path, required=True, help="Store master CSV")
    parser.add_argument("--sales", type=Path, required=True, help="Daily sales CSV")
    parser.add_argument("--clean", type=Path, required=True, help="Clean joined CSV")
    args = parser.parse_args()

    profiles = {
        "store_master": profile(read_csv(args.stores)),
        "daily_sales": profile(read_csv(args.sales)),
        "clean_joined": profile(read_csv(args.clean)),
    }
    print(json.dumps(profiles, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
