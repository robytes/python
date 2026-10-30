# Add, remove, search, and count inventory items
# Work with collections of items, such as adding a sword to a character's inventory or finding all wooden items they possess.

def count_items_by_tag(item_registry):
    tag_counts = {}

    for item_name, item_data in item_registry.items():
        tags = item_data["tags"]
        for tag in tags:
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1
    
    return tag_counts

def find_most_common_tags(tag_counts):
    most_common_tags = {}
    highest_count = 0

    for tag, count in tag_counts.items():
        if count > highest_count:
            highest_count = count
            most_common_tags = {tag: count}
        elif count == highest_count:
            most_common_tags[tag] = count
    
    return most_common_tags

def find_top_three_tags(tag_counts):
    top_three = []

    for tag, count in tag_counts.items():
        tag_added = False
        for i in range(len(top_three)):
            if count > top_three[i][1]:
                top_three.insert(i, (tag, count))
                tag_added = True
                break

        if len(top_three) < 3 and not tag_added:
            top_three.append((tag, count))

        if len(top_three) > 3:
            top_three.pop()

    return top_three

tag_counts = {
    "weapon": 12,
    "magic": 8,
    "armor": 15,
    "potion": 5,
    "metal": 10
}

print(find_most_common_tags(tag_counts))
print(find_top_three_tags(tag_counts))