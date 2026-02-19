import math


# -----------------------------
# Utility Functions
# -----------------------------

def normalize_rgb(rgb):
    if not rgb or len(rgb) != 3:
        return [0, 0, 0]
    return [x / 255 for x in rgb]


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def is_neutral(rgb):
    if not rgb or len(rgb) != 3:
        return True
    r, g, b = rgb
    return abs(r - g) < 15 and abs(g - b) < 15


def color_match_score(c1, c2):
    """
    Returns value between 0 and 1
    """
    if not c1 or not c2:
        return 0

    if is_neutral(c1) or is_neutral(c2):
        return 1.0

    dist = color_distance(normalize_rgb(c1), normalize_rgb(c2))
    return max(0, 1 - dist)


# -----------------------------
# Shoes Selection
# -----------------------------

def select_best_shoes(shoes, outfit, context):
    if not shoes:
        return None

    best_score = -1
    selected = None

    top_color = outfit["top"].get("dominant_color")

    for shoe in shoes:

        shoe_color = shoe.get("dominant_color")
        score = color_match_score(top_color, shoe_color)

        # Neutral shoes bonus
        if is_neutral(shoe_color):
            score += 0.2

        # Weather rule (fixed)
        # Skip open footwear in rain
        if context.get("weather_type") == "rainy" and shoe.get("shoe_type") == "open":
            continue

        # Occasion matching bonus
        if shoe.get("style") == context.get("occasion"):
            score += 0.2

        if score > best_score:
            best_score = score
            selected = shoe

    return selected


# -----------------------------
# Accessories Selection
# -----------------------------

def select_accessories(accessories, occasion, limit=2):
    if not accessories:
        return []

    # Prefer occasion-matched accessories
    matched = [a for a in accessories if a.get("style") == occasion]

    if matched:
        return matched[:limit]

    # Fallback
    return accessories[:limit]


# -----------------------------
# Jewellery Selection
# -----------------------------

def select_jewellery(jewellery, occasion):
    if not jewellery:
        return None

    # Jewellery only for specific occasions
    if occasion not in ["party", "traditional"]:
        return None

    for item in jewellery:
        if item.get("style") == occasion:
            return item

    # fallback
    return jewellery[0]
