import os
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    """Load analysed CSV"""
    filepath = "data/trends_analysed.csv"

    try:
        df = pd.read_csv(filepath)
        print(f"Loaded data: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def setup_output_folder():
    """Create outputs folder if not exists"""
    os.makedirs("outputs", exist_ok=True)


def shorten_title(title, max_length=50):
    """Shorten long titles for better visualization"""
    return title if len(title) <= max_length else title[:max_length] + "..."


def chart_top_stories(df):
    """Chart 1: Top 10 stories by score"""
    top10 = df.sort_values(by="score", ascending=False).head(10)

    # Shorten titles
    titles = [shorten_title(t) for t in top10["title"]]
    
    # Top 10 stories horizontal bar chart plotting
    plt.figure()
    plt.barh(titles, top10["score"])
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()

    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()


def chart_categories(df):
    """Chart 2: Stories per category"""
    category_counts = df["category"].value_counts()
    
    #Stories per category bar chart plotting
    plt.figure()
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.savefig("outputs/chart2_categories.png")
    plt.close()


def chart_scatter(df):
    """ Chart 3: Score vs Comments"""
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
   
    #score vs num_comments scatterplot plotting
    plt.figure()
    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.savefig("outputs/chart3_scatter.png")
    plt.close()


def dashboard(df):
    """Bonus: Combine all charts into one dashboard"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Combination of all 3 charts as a dashboard
    # --- Chart 1 ---
    top10 = df.sort_values(by="score", ascending=False).head(10)
    titles = [shorten_title(t) for t in top10["title"]]
    axes[0].barh(titles, top10["score"])
    axes[0].set_title("Top 10 Stories")
    axes[0].set_xlabel("Score")
    axes[0].invert_yaxis()

    # --- Chart 2 ---
    category_counts = df["category"].value_counts()
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Stories per Category")
    axes[1].set_xlabel("Category")

    # --- Chart 3 ---
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Comments")
    axes[2].legend()

    plt.suptitle("TrendPulse Dashboard")
    plt.tight_layout()
    plt.savefig("outputs/dashboard.png")
    plt.close()



df = load_data()
if df is None:
    exit

setup_output_folder()
chart_top_stories(df)
chart_categories(df)
chart_scatter(df)
dashboard(df)

print("\nAll charts saved in outputs/ folder")