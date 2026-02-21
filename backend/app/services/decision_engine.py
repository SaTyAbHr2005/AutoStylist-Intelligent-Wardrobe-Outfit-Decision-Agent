import math
from itertools import product
from datetime import datetime


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def normalize_rgb(rgb):
    """
    Convert RGB [0-255] to normalized [0-1]
    Safe fallback if data missing
    """
    if not rgb or len(rgb) != 3:
        return [0, 0, 0]
    return [x / 255 for x in rgb]


def euclidean_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def is_neutral(rgb):
    """
    Detect neutral colors (black, white, grey)
    """
    if not rgb or len(rgb) != 3:
        return True
    r, g, b = rgb
    return abs(r - g) < 15 and abs(g - b) < 15


# -------------------------------------------------
# Color Scoring
# -------------------------------------------------

def dominant_color_score(top, bottom):
    """
    Score based on dominant color harmony
    Neutral colors match everything
    """
    c1 = normalize_rgb(top.get("dominant_color"))
    c2 = normalize_rgb(bottom.get("dominant_color"))

    if is_neutral(top.get("dominant_color")) or is_neutral(bottom.get("dominant_color")):
        return 1.0

    dist = euclidean_distance(c1, c2)
    return max(0.0, 1 - dist)


def accent_color_score(top, bottom):
    """
    Secondary color matching for multi-color clothes
    """
    top_colors = top.get("colors", [])
    bottom_colors = bottom.get("colors", [])

    scores = []

    if len(top_colors) >= 2:
        score = 1 - euclidean_distance(
            normalize_rgb(top_colors[1]),
            normalize_rgb(bottom.get("dominant_color"))
        )
        scores.append(max(0, score))

    if len(bottom_colors) >= 2:
        score = 1 - euclidean_distance(
            normalize_rgb(bottom_colors[1]),
            normalize_rgb(top.get("dominant_color"))
        )
        scores.append(max(0, score))

    return max(scores) if scores else 0.0


# -------------------------------------------------
# Context Scoring
# -------------------------------------------------

def occasion_score(item, occasion):
    style_map = {
        "casual": ["casual"],
        "office": ["formal"],
        "party": ["party"],
        "traditional": ["traditional"]
    }
    return 1.0 if item.get("style") in style_map.get(occasion, []) else 0.4


def weather_score(weather_type):
    """
    Basic weather comfort factor
    """
    if weather_type == "rainy":
        return 0.6
    if weather_type == "sunny":
        return 1.0
    return 0.8


# -------------------------------------------------
# Learning / Preference Scoring
# -------------------------------------------------

def preference_score(item):
    """
    Combines:
    - User like/dislike history
    - Usage frequency (avoid repetition)
    - Recency penalty
    """

    base = item.get("preference_score", 0)
    usage = item.get("usage_count", 0)

    # Normalize preference [-5,5] → [0,1]
    normalized_pref = (base + 5) / 10
    normalized_pref = max(0, min(1, normalized_pref))

    # Light usage penalty (avoid repeating same item daily)
    usage_penalty = min(0.2, usage * 0.02)

    # Recency penalty
    recency_penalty = 0
    last_used = item.get("last_used")
    if last_used:
        days = (datetime.utcnow() - last_used).days
        if days < 2:
            recency_penalty = 0.2

    score = normalized_pref - usage_penalty - recency_penalty
    return max(0, score)


# -------------------------------------------------
# FINAL DECISION ENGINE
# -------------------------------------------------

def generate_ranked_outfits(tops, bottoms, context, limit=3):
    """
    Generates and ranks outfit combinations
    Returns top N outfits
    """

    scored_outfits = []

    for top, bottom in product(tops, bottoms):

        # --- Color harmony ---
        dom_score = dominant_color_score(top, bottom)
        acc_score = accent_color_score(top, bottom)
        color_score = (0.7 * dom_score) + (0.3 * acc_score)

        # --- Occasion relevance ---
        occ_score = (
            occasion_score(top, context["occasion"]) +
            occasion_score(bottom, context["occasion"])
        ) / 2

        # --- User preference learning ---
        pref_score = (
            preference_score(top) +
            preference_score(bottom)
        ) / 2

        # --- Final weighted score ---
        final_score = (
            0.30 * color_score +
            0.20 * occ_score +
            0.15 * weather_score(context["weather_type"]) +
            0.35 * pref_score
        )


        scored_outfits.append({
            "top": top,
            "bottom": bottom,
            "score": round(final_score, 3)
        })

    # Sort by best score
    scored_outfits.sort(key=lambda x: x["score"], reverse=True)

    # Add tiny rank bias to avoid ties
    for i, outfit in enumerate(scored_outfits):
        outfit["score"] = round(outfit["score"] - (i * 0.001), 3)

    return scored_outfits[:limit]

