import math

# -----------------------------
# Utility Functions
# -----------------------------

def normalize_rgb(rgb):
    if not rgb or len(rgb) != 3:
        return [0, 0, 0]
    return [x / 255.0 for x in rgb]


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

    dist = color_distance(normalize_rgb(c1), normalize_rgb(c2))
    base_score = max(0.0, 1.0 - dist)
    
    # Neutral matching means it can go with anything seamlessly
    if is_neutral(c1) or is_neutral(c2):
        base_score += 0.3

    return min(1.0, base_score)


# -----------------------------
# Shoes Selection
# -----------------------------

def select_best_shoes(shoes, outfit, context):
    if not shoes:
        return None

    best_score = -1
    selected = None

    if "full_body" in outfit:
        top_color = outfit["full_body"].get("dominant_color")
    else:
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
            score += 0.5
            
        # Tie breaker against identical score matches (make it dynamic based on preference)
        score += shoe.get("preference_score", 0) * 0.1

        if score > best_score:
            best_score = score
            selected = shoe

    return selected


# -----------------------------
# Accessories Selection
# -----------------------------

def select_accessories(accessories, outfit, context, limit=1):
    if not accessories:
        return []

    if "full_body" in outfit:
        top_color = outfit["full_body"].get("dominant_color")
    else:
        top_color = outfit["top"].get("dominant_color")

    scored_accessories = []
    
    for acc in accessories:
        acc_color = acc.get("dominant_color")
        score = color_match_score(top_color, acc_color)
        
        # Occasion matching bonus
        if acc.get("style") == context.get("occasion"):
            score += 0.5
            
        score += acc.get("preference_score", 0) * 0.1
        scored_accessories.append((score, acc))

    # Sort by score descending
    scored_accessories.sort(key=lambda x: x[0], reverse=True)
    
    selected_items = [item[1] for item in scored_accessories[:limit]]
    return selected_items


# -----------------------------
# Jewellery Selection
# -----------------------------

def select_jewellery(jewellery, outfit, context):
    if not jewellery:
        return None

    occasion = context.get("occasion")
    if occasion not in ["party", "traditional"]:
        return None

    best_score = -1
    selected = None

    if "full_body" in outfit:
        top_color = outfit["full_body"].get("dominant_color")
    else:
        top_color = outfit["top"].get("dominant_color")

    for item in jewellery:
        item_color = item.get("dominant_color")
        score = color_match_score(top_color, item_color)

        if item.get("style") == occasion:
            score += 0.5
            
        score += item.get("preference_score", 0) * 0.1

        if score > best_score:
            best_score = score
            selected = item

    return selected
