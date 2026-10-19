import pandas as pd
from pathlib import Path


def load_and_clean_data(file_path):
    """
    Load and clean the UAC dataset.
    """

    # Convert path to Path object
    file_path = Path(file_path)

    # Check whether file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path.resolve()}"
        )

    # Load CSV
    df = pd.read_csv(file_path)

    # Remove completely empty rows
    df = df.dropna(
        how="all"
    ).copy()

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace(
            "*",
            "",
            regex=False
        )
        .str.strip()
    )

    # Required columns
    required_columns = [
        "Date",
        "Children apprehended and placed in CBP custody",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]

    # Check for missing columns
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Convert Date column
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Remove rows without valid dates
    df = df.dropna(
        subset=["Date"]
    ).copy()

    # Numeric columns
    numeric_columns = [
        "Children apprehended and placed in CBP custody",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]

    # Convert numeric columns
    for column in numeric_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.replace(
                ",",
                "",
                regex=False
            )
            .str.strip()
            .replace(
                {
                    "": pd.NA,
                    "nan": pd.NA,
                    "None": pd.NA
                }
            )
        )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Sort by date
    df = df.sort_values(
        "Date"
    )

    # Remove duplicate dates
    df = df.drop_duplicates(
        subset="Date",
        keep="last"
    )

    # Reset index
    df = df.reset_index(
        drop=True
    )

    return df


def validate_data(df):
    """
    Run basic data-quality checks.
    """

    numeric_columns = df.select_dtypes(
        include="number"
    )

    results = {
        "Rows": len(df),

        "Columns": len(df.columns),

        "Duplicate dates": int(
            df["Date"].duplicated().sum()
        ),

        "Missing values": int(
            df.isna().sum().sum()
        ),

        "Negative numeric values": int(
            (numeric_columns < 0).sum().sum()
        ),

        "Transfer-vs-CBP flags": int(
            (
                df[
                    "Children transferred out of CBP custody"
                ]
                >
                df[
                    "Children in CBP custody"
                ]
            ).sum()
        ),

        "Discharge-vs-HHS flags": int(
            (
                df[
                    "Children discharged from HHS Care"
                ]
                >
                df[
                    "Children in HHS Care"
                ]
            ).sum()
        ),

        "Start date": df["Date"].min(),

        "End date": df["Date"].max(),
    }

    return results


# --------------------------------------------------
# TEST THE FILE DIRECTLY
# --------------------------------------------------

if __name__ == "__main__":

    # Project folder
    project_path = Path(
        __file__
    ).resolve().parent

    # Dataset path
    file_path = (
        project_path
        / "data"
        / "HHS_Unaccompanied_Alien_Children_Program.csv"
    )

    print("\n======================================")
    print("UAC DATA PREPROCESSING")
    print("======================================")

    print("\nLoading dataset...")

    # Load and clean
    df = load_and_clean_data(
        file_path
    )

    print(
        "\nDataset successfully loaded!"
    )

    # Display validation results
    print("\n======================================")
    print("DATA QUALITY CHECK")
    print("======================================")

    results = validate_data(
        df
    )

    for key, value in results.items():

        print(
            f"{key}: {value}"
        )

    # Display columns
    print("\n======================================")
    print("COLUMNS")
    print("======================================")

    for column in df.columns:

        print(
            "-",
            column
        )

    # Display first five rows
    print("\n======================================")
    print("FIRST 5 ROWS")
    print("======================================")

    print(
        df.head()
    )

    print("\n======================================")
    print("PREPROCESSING COMPLETE")
    print("======================================")