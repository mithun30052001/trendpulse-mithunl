import pandas as pd
import numpy as np


def load_data():
    """Load cleaned CSV file"""
    filepath = "data/trends_clean.csv"
    try:
        df = pd.read_csv(filepath)
        #Rows and columns in loaded data
        print(f"Loaded data shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def explore_data(df):
    """Basic exploration"""
   
    #print first 5 rows
    print(f"\nFirst 5 rows:\n {df.head()}")

    # Average scores and comments
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {avg_score:,.2f}")
    print(f"Average comments: {avg_comments:,.2f}")

    return avg_score


def numpy_analysis(df):
    """Analysis using NumPy"""

    #converting dataframe columns to numpy array
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()
    
    print("\n--------------")
    print("\nNumPy Stats")
    print("\n--------------")

    print(f"\nMean score   : {np.mean(scores):,.2f}")
    print(f"Median score : {np.median(scores):,.2f}")
    print(f"Std deviation: {np.std(scores):,.2f}")

    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    # Category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    print(f"\nMost stories in: {top_category} ({category_counts[top_category]} stories)")

    # Story with most comments
    max_comments_idx = np.argmax(comments)
    top_story = df.iloc[max_comments_idx]

    print(f"\nMost commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")


def add_new_columns(df, avg_score):
    """Add engagement and is_popular columns"""

    # Engagement = num_comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = score > average score
    df["is_popular"] = df["score"] > avg_score
    return df


def save_data(df):
    """Save final analysed data"""

    #convert analysed data as a csv file
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved to {output_path}")



df = load_data()
if df is None:
    exit
avg_score = explore_data(df)
numpy_analysis(df)
df = add_new_columns(df, avg_score)
save_data(df)


