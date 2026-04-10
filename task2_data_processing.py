import os
import json
import pandas as pd


def load_latest_json():
    """Load the latest trends_YYYYMMDD.json file from data/ folder"""

    data_folder = "data"
    # Get all trend files
    files = [f for f in os.listdir(data_folder) if f.startswith("trends_") and f.endswith(".json")]
    
    #No file present check works in case no data after first step
    if not files:
        print("No JSON files found in data/ folder.")
        return None

    # Pick the latest file (sorted by name)
    latest_file = sorted(files)[-1]
    filepath = os.path.join(data_folder, latest_file)

    # Load JSON
    with open(filepath, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print(f"Loaded {len(df)} stories from {filepath}")
    return df

def clean_data(df):
    """Perform all cleaning steps"""

    # 1. Remove duplicates
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # 2. Remove missing values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # 3. Fix data types
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # 4. Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 5. Strip whitespace from title
    df["title"] = df["title"].str.strip()
    print(f"Title after removing space:\n {df["title"]}")

    return df

def save_to_csv(df):
    """Save cleaned data to CSV and print summary"""
    
    #Converting the attained dataframe to csv file
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} rows to {output_path}")

    # Results as Stories per category
    print("\nStories per category:")
    print(df["category"].value_counts())

df = load_latest_json()
if df is None:
    exit
df_clean = clean_data(df)
save_to_csv(df_clean)