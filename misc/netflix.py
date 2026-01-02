# We're analyzing user engagement patterns across different content.
#

# A user's engagement with a piece of content is defined by:
# - "Abandoned" if they watched less than 25% of the content
# - "Sampled" if they watched 25% to 75% of the content
# - "Completed" if they watched more than 75% of the content
#

# Given a list of viewing sessions where each session contains:
# - account_id
# - title_id
# - title_runtime_secs (total length of the content in seconds)
# - watched_secs (how much the user watched in seconds)
# - day_nbr (an integer representing the day of viewing, where consecutive numbers are consecutive days)

#
# Write a function that:
# 1. Classifies each session as "Abandoned", "Sampled", or "Completed"
# 2. For each user, finds their most common engagement pattern across all their sessions
# 3. Returns a dictionary with the count of users for each dominant engagement pattern

viewing_data = [
    {"account_id": "U1", "title_id": "T1", "title_runtime_secs": 3600, "watched_secs": 3500, "day_nbr": 1},
    {"account_id": "U1", "title_id": "T2", "title_runtime_secs": 5400, "watched_secs": 5000, "day_nbr": 3},
    {"account_id": "U1", "title_id": "T3", "title_runtime_secs": 7200, "watched_secs": 6800, "day_nbr": 6},
    {"account_id": "U2", "title_id": "T1", "title_runtime_secs": 3600, "watched_secs": 3500, "day_nbr": 5},
    {"account_id": "U2", "title_id": "T4", "title_runtime_secs": 2700, "watched_secs": 2600, "day_nbr": 9},
    {"account_id": "U2", "title_id": "T5", "title_runtime_secs": 4500, "watched_secs": 4300, "day_nbr": 10},
    {"account_id": "U3", "title_id": "T2", "title_runtime_secs": 5400, "watched_secs": 5200, "day_nbr": 2},
    {"account_id": "U3", "title_id": "T3", "title_runtime_secs": 7200, "watched_secs": 6500, "day_nbr": 3},
    {"account_id": "U3", "title_id": "T4", "title_runtime_secs": 2700, "watched_secs": 2000, "day_nbr": 4},
    {"account_id": "U4", "title_id": "T1", "title_runtime_secs": 3600, "watched_secs": 2000, "day_nbr": 1},
]

def analyze_engagement_patterns(viewing_data):
    # abandoned_df = viewing_data.filter("watched_secs / title_runtime_secs <= 0.25")
    abandonded = []
    sampled = []
    complted = []
    pattern = {}
    viewing_category = None
    for d in viewing_data:
        if d["watched_secs"] <= d["title_runtime_secs"] * 0.25:
            viewing_category = "abandonded"
        elif d["watched_secs"] <= d["title_runtime_secs"] * 0.75:
            viewing_category = "sampled"
        else:
            viewing_category = "complted"

        if d["account_id"] not in pattern.keys():
            pattern[d["account_id"]] = {viewing_category: 1}
        else:
            if viewing_category not in pattern[d["account_id"]].keys():
                pattern[d["account_id"]][viewing_category] = 1
            else:
                pattern[d["account_id"]][viewing_category] = pattern[d["account_id"]][viewing_category] + 1

    engagement = {}
    for d in pattern.keys():
        max_count = 0
        dominant_pattern = None
        for p in pattern[d].keys():
            if pattern[d][p] > max_count:
                max_count = pattern[d][p]
                dominant_pattern = p
    
        # if dominant_pattern not in engagement.keys():
        #     engagement[dominant_pattern] = 1
        # else:
        #     engagement[dominant_pattern] = engagement[dominant_pattern] + 1
    
        if d not in engagement.keys():
            engagement[d] =  dominant_pattern
            
    return engagement


if __name__ == "__main__":
    result = analyze_engagement_patterns(viewing_data)
    print(result)
