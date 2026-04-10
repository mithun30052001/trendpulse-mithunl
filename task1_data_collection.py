import requests
import time
import os
import json
from datetime import datetime

# Base URLs for both entire list and details of each story
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header as mentioned in the task
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Max stories per category
MAX_PER_CATEGORY = 25


def fetch_top_story_ids():
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    """Fetch a single story by ID"""
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


def assign_category(title):
    """Assign category based on keywords"""
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        if any(keyword in title_lower for keyword in keywords):
            return category

    return None



# Step 1: Fetch all top story IDs
story_ids = fetch_top_story_ids()

if not story_ids:
    print("No stories fetched. Exiting.")
    exit

collected_stories = []
category_counts = {cat: 0 for cat in CATEGORIES.keys()}

# Step 2: Loop through categories
for category in CATEGORIES.keys():
    print(f"\nProcessing category: {category}")

    for story_id in story_ids:
        # Stop when category limit reached
        if category_counts[category] >= MAX_PER_CATEGORY:
            break
        
        #Fetching each story details
        story = fetch_story(story_id)
        if not story:
            continue
        
        #Assigning categories by matching keywords in title
        title = story.get("title", "")
        assigned_category = assign_category(title)

        # Only keep stories matching current category
        if assigned_category != category:
            continue

        # Extract required fields
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_stories.append(story_data)
        category_counts[category] += 1

    # Wait 2 seconds between each category 
    time.sleep(2)

# Step 3: Save to JSON file
os.makedirs("data", exist_ok=True)

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

#saving stories in the created file
with open(filename, "w") as f:
    json.dump(collected_stories, f, indent=4)

print(f"\nCollected {len(collected_stories)} stories and Saved to {filename}")