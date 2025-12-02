import pandas as pd
import os

# -----------------------------
# Utility: Safe loader
# -----------------------------
def load_csv(file_path):
    try:
        return pd.read_csv(file_path, on_bad_lines='skip')
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return pd.DataFrame()

# -----------------------------
# Standard schema for watchlists
# -----------------------------
STANDARD_COLS = [
    "name",
    "country",
    "address",
    "list_type",
    "program",
    "risk_level",
    "source",
    "notes"
]

# -----------------------------
# Normalize dataset function
# -----------------------------
def normalize_df(df, list_type, source):
    """Normalize any uploaded dataset into the master schema."""

    # Create empty template
    clean_df = pd.DataFrame(columns=STANDARD_COLS)

    if df.empty:
        return clean_df

    # Map existing columns smartly
    for col in clean_df.columns:
        if col in df.columns:
            clean_df[col] = df[col]
        else:
            clean_df[col] = None

    # Fill missing metadata
    clean_df["list_type"] = list_type
    clean_df["source"] = source

    # Risk level assignment
    if list_type in ["OFAC_SDN", "ENTITY_LIST", "MEU", "MIEU", "UVL", "DPL"]:
        clean_df["risk_level"] = "High"
    else:
        clean_df["risk_level"] = clean_df["risk_level"].fillna("Medium")

    return clean_df

# -----------------------------
# Main integration function
# -----------------------------
def integrate_all_data(input_dir="data", output_dir="data"):

    print("🔵 Starting data integration...")

    # Load raw datasets (using exact filenames you uploaded)
    files_map = {
        "ofac_sdn.csv": ("OFAC_SDN", "OFAC"),
        "bis_entity_list.csv": ("ENTITY_LIST", "BIS"),
        "unverified_list.csv": ("UVL", "BIS"),
        "denied_persons_list.csv": ("DPL", "BIS"),
        "meu_list.csv": ("MEU", "BIS"),
        "military_intelligence_end_user_list.csv": ("MIEU", "BIS"),
        "consolidated_screening_list.csv": ("CSL", "MULTISOURCE"),
        "kyc_red_flags.csv": ("KYC", "INTERNAL")
    }

    all_dfs = []

    # Process each dataset
    for filename, (list_type, source) in files_map.items():

        file_path = os.path.join(input_dir, filename)

        print(f"📄 Loading: {filename}")
        raw_df = load_csv(file_path)

        # Normalize watchlist datasets
        if list_type != "KYC":
            df_norm = normalize_df(raw_df, list_type, source)
            all_dfs.append(df_norm)

    # -----------------------------------------------------
    # Combine into master screening dataset
    # -----------------------------------------------------
    print("🟡 Merging all watchlists...")

    master_df = pd.concat(all_dfs, ignore_index=True).drop_duplicates()

    # Save master dataset
    master_output = os.path.join(output_dir, "master_screening_dataset.csv")
    master_df.to_csv(master_output, index=False)

    print(f"✅ Master screening dataset saved to: {master_output}")

    # -----------------------------------------------------
    # Quick summary
    # -----------------------------------------------------
    summary = master_df["list_type"].value_counts().reset_index()
    summary.columns = ["list_type", "count"]

    summary_output = os.path.join(output_dir, "master_screening_summary.csv")
    summary.to_csv(summary_output, index=False)

    print(f"📊 Summary saved to: {summary_output}")

    return master_df, summary

# -----------------------------------------------------
# Run directly
# -----------------------------------------------------
if __name__ == "__main__":
    integrate_all_data()
