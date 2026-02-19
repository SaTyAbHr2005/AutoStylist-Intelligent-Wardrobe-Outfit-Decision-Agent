from app.config.db import wardrobe_collection
import pprint

print("--- All Items in DB ---")
items = list(wardrobe_collection.find({}))
for item in items:
    # Convert ObjectId to string for printing
    item['_id'] = str(item['_id'])
    pprint.pprint(item)
    print("-" * 20)

print("\n--- Summary ---")
print(f"Total items: {len(items)}")

categories = {}
genders = {}

for i in items:
    cat = i.get('category', 'UNKNOWN')
    gen = i.get('gender', 'UNKNOWN')
    categories[cat] = categories.get(cat, 0) + 1
    genders[gen] = genders.get(gen, 0) + 1

print("\nCategories distribution:")
pprint.pprint(categories)
print("\nGenders distribution:")
pprint.pprint(genders)
