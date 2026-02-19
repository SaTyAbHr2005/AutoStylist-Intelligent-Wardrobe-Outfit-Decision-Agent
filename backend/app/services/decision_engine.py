import math
from itertools import product

# =====================================================
# Utility Functions
# =====================================================

def normalize_rgb(rgb):
    return [x / 255 for x in rgb]


def euclidean_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def is_neutral(rgb):
    if not rgb or len(rgb) != 3:
        return False
    r, g, b = rgb
    return abs(r - g) < 15 and abs(g - b) < 15


# =====================================================
# Color Scoring
# =====================================================

def dominant_color_score(top, bottom):
    top_color = top.get("dominant_color")
    bottom_color = bottom.get("dominant_color")

    if not top_color or not bottom_color:
        return 0.5  # neutral fallback

    if is_neutral(top_color) or is_neutral(bottom_color):
        return 1.0

    c1 = normalize_rgb(top_color)
    c2 = normalize_rgb(bottom_color)

    dist = euclidean_distance(c1, c2)
    return max(0.0, 1 - dist)


def accent_color_score(top, bottom):
    scores = []

    top_colors = top.get("colors", [])
    bottom_colors = bottom.get("colors", [])

    if len(top_colors) >= 2 and len(bottom.get("dominant_color", [])) == 3:
        scores.append(
            1 - euclidean_distance(
                normalize_rgb(top_colors[1]),
                normalize_rgb(bottom["dominant_color"])
            )
        )

    if len(bottom_colors) >= 2 and len(top.get("dominant_color", [])) == 3:
        scores.append(
            1 - euclidean_distance(
                normalize_rgb(bottom_colors[1]),
                normalize_rgb(top["dominant_color"])
            )
        )

    return max(scores) if scores else 0.0


# =====================================================
# Context Scoring
# =====================================================

def occasion_score(item, occasion):
    style_map = {
        "casual": ["casual"],
        "office": ["formal"],
        "party": ["party"],
        "traditional": ["traditional"]
    }

    return 1.0 if item.get("style") in style_map.get(occasion, []) else 0.4


def weather_score(weather_type):
    if weather_type == "rainy":
        return 0.6
    if weather_type == "sunny":
        return 1.0
    return 0.8


def preference_score(item):
    base = item.get("preference_score", 0)
    usage = item.get("usage_count", 0)

    # Schema-aligned preference logic
    return min(1.0, (base + 1) / (usage + 2))


# =====================================================
# FINAL DECISION ENGINE
# =====================================================

def generate_ranked_outfits(tops, bottoms, context):
    """
    Returns best and average outfit combinations based on scoring.
    """

    scored_outfits = []

    for top, bottom in product(tops, bottoms):

        # Color scoring
        dom_score = dominant_color_score(top, bottom)
        acc_score = accent_color_score(top, bottom)
        color_score = (0.7 * dom_score) + (0.3 * acc_score)

        # Occasion scoring
        occ_score = (
            occasion_score(top, context["occasion"]) +
            occasion_score(bottom, context["occasion"])
        ) / 2

        # Preference scoring
        pref_score = (
            preference_score(top) +
            preference_score(bottom)
        ) / 2

        # Final weighted score
        final_score = (
            0.4 * color_score +
            0.3 * occ_score +
            0.2 * weather_score(context["weather_type"]) +
            0.1 * pref_score
        )

        scored_outfits.append({
            "top": top,
            "bottom": bottom,
            "score": round(final_score, 3)
        })

    # Rank outfits
    scored_outfits.sort(key=lambda x: x["score"], reverse=True)

    if not scored_outfits:
        return None

    return {
        "best": scored_outfits[0],
        "average": scored_outfits[-1]
    }
