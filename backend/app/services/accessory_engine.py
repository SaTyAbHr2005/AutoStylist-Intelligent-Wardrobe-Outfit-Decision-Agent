import math

# =====================================================
# Utility functions
# =====================================================

def normalize_rgb(rgb):
    return [x / 255 for x in rgb]


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def is_neutral(rgb):
    if not rgb or len(rgb) != 3:
        return False
    r, g, b = rgb
    return abs(r - g) < 15 and abs(g - b) < 15


# =====================================================
# Rules
# =====================================================

ACCESSORY_RULES = {
    "casual": ["watch", "cap", "sunglasses"],
    "office": ["watch", "belt"],
    "party": ["watch", "bracelet"],
    "traditional": []
}

JEWELLERY_RULES = {
    "casual": [],
    "office": [],
    "party": ["ring", "chain"],
    "traditional": ["necklace", "earrings", "bangles"]
}


# =====================================================
# Scoring logic
# =====================================================

def score_item(item, outfit_colors):
    """
    Scores an accessory/jewellery item based on color harmony
    """

    color = item.get("dominant_color")

    # Missing or invalid color
    if not color or len(color) != 3:
        return 0.3

    # Neutral colors always safe
    if is_neutral(color):
        return 1.0

    scores = []

    for c in outfit_colors:
        if not c or len(c) != 3:
            continue

        scores.append(
            1 - color_distance(
                normalize_rgb(color),
                normalize_rgb(c)
            )
        )

    return max(scores) if scores else 0.3


# =====================================================
# Selection engines
# =====================================================

def select_accessories(outfit, accessories, occasion, weather_type):
    allowed_types = ACCESSORY_RULES.get(occasion, [])
    scored = []

    for acc in accessories:
        acc_type = acc.get("type")
        acc_material = acc.get("material")

        # Skip invalid metadata
        if not acc_type or acc_type not in allowed_types:
            continue

        # Weather safety
        if weather_type == "rainy" and acc_material == "leather":
            continue

        score = score_item(
            acc,
            [
                outfit["top"]["dominant_color"],
                outfit["bottom"]["dominant_color"]
            ]
        )

        scored.append((score, acc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:2]]


def select_jewellery(outfit, jewellery, occasion):
    allowed_types = JEWELLERY_RULES.get(occasion, [])
    scored = []

    for item in jewellery:
        jewel_type = item.get("type")

        if not jewel_type or jewel_type not in allowed_types:
            continue

        score = score_item(
            item,
            [
                outfit["top"]["dominant_color"],
                outfit["bottom"]["dominant_color"]
            ]
        )

        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:2]]
