
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import unicodedata

OSE_STAT_MARKERS = [
        "AC",
        "HD",
        "Att",
        "THAC0",
        "MV",
        "SV",
        "ML",
        "AL",
        "XP",
        "NA",
        "TT"
    ]

def parse_ose_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_ose_page(url):
    response = requests.get(url)
    if response.status_code >= 400:
        return None
    return response

def get_parsed_html(response):
    if response is None:
        return None

    parsed_html = parse_ose_html(response.text)
    return parsed_html

def get_html_links(parsed_html):
    if parsed_html is None:
        return None

    links = []
    for link in parsed_html.find_all("a"):
        links.append(link)
    return links

def get_ose_monster_links(links):
    if links is None:
        return None

    found_monster_list = False
    monster_links = []
    for link in links:        
        wiki_id = link.get("data-wiki-id")
        if wiki_id == "monsters:monster_list":
            found_monster_list = True
            continue
        if wiki_id and wiki_id.startswith("monsters:") and found_monster_list:
            monster_links.append(link)
    return monster_links

def build_ose_monster_records(monster_links):
    if monster_links is None:
        return None

    monster_records = []
    base_url = "https://oldschoolessentials.necroticgnome.com"
    for link in monster_links:
        monster_record = {}
        monster_record["name"] = link.get_text()
        monster_record["wiki_id"] = link.get("data-wiki-id")
        monster_record["relative_url"] = link.get("href")
        monster_record["full_url"] = urljoin(base_url, monster_record["relative_url"])
        monster_record["description"] = None
        monster_record["stats"] = {
            "raw": None,
            "formatted": {}
        }
        monster_records.append(monster_record)
    return monster_records

def get_ose_monster_page(monster_records):
    if monster_records is None:
        return None
    ose_monster_page = []

    for monster in monster_records:
        response = get_ose_page(monster["full_url"])
        ose_monster_page.append(response)

    return ose_monster_page

def get_ose_monster_stats_string(monster_pages, monster_records):
    if monster_pages is None:
        return None

    monster_raw_strings = []
    for response, monster in zip(monster_pages, monster_records):
        parsed_html = get_parsed_html(response)
        subheadings = parsed_html.find_all("h4")

        if subheadings:
            related_monsters = []
            for heading in subheadings:
                section = heading.find_next_sibling()
                monster_string = section.find("p").get_text()

                related_monster = {}
                related_monster["stats"] = {
                    "raw": None,
                    "formatted": {}
                }
                related_monster["name"] = heading.get_text().strip()
                related_monster["source_group"] = monster["name"]

                description_and_stats = monster_string.split("\n\n", 1)
                if len(description_and_stats) == 1:
                    related_monster["description"] = None
                    related_monster["stats"]["raw"] = description_and_stats[0].strip()
                else:
                    related_monster["description"] = description_and_stats[0].strip()
                    related_monster["stats"]["raw"] = description_and_stats[1].strip()   

                related_monsters.append(related_monster)

            monster_raw_strings.extend(related_monsters)

        else:
            paragraphs = parsed_html.find_all("p")

            monster_string = paragraphs[1].get_text()
            # description_and_stats = monster_string.split("\n\n", 1)
            stats_start = monster_string.find("\nAC ")
            if stats_start == -1:
                raise ValueError(f"Stats boundary not found for: {monster['name']}")

            monster["source_group"] = None
            monster["description"] = monster_string[:stats_start].strip()
            monster["stats"]["raw"] = monster_string[stats_start + 1:].strip()

            monster_raw_strings.append(monster)
            
    return monster_raw_strings

def parse_ose_monster_stats(monster_records):
    if monster_records is None:
        return None
    
    for monster in monster_records:
        raw_stats = monster["stats"]["raw"]
        search_position = raw_stats.find(OSE_STAT_MARKERS[0])
        if search_position == -1:
            raise ValueError(f"Stats boundary not found for: {monster['name']}")
        
        for i in range(len(OSE_STAT_MARKERS) - 1):
            current_marker = OSE_STAT_MARKERS[i]
            next_marker = OSE_STAT_MARKERS[i + 1]

            start = raw_stats.find(current_marker, search_position)
            end = raw_stats.find(next_marker, start + len(current_marker))

            stat_value = raw_stats[start + len(current_marker):end].strip()
            monster["stats"]["formatted"][current_marker] = stat_value
        last_marker = OSE_STAT_MARKERS[-1]
        start = raw_stats.find(last_marker) + len(last_marker)
        monster["stats"]["formatted"][last_marker] = raw_stats[start:].strip()
    
    return monster_records

def validate_ose_monster_stats(monster_records):
    if monster_records is None:
        return None

    validated_monster_records = []
    for monster in monster_records:
        validated_monster = {
            "name": monster["name"],
            "ose_stats_validated": {},
        }
        raw_stats = monster["stats"]["raw"]
        for marker in OSE_STAT_MARKERS:
            marker_position = raw_stats.find(marker)
            validated_monster["ose_stats_validated"][marker] = "Valid"
            if marker_position == -1:
                validated_monster["ose_stats_validated"][marker] = "Missing"
        validated_monster_records.append(validated_monster)
    return validated_monster_records

def normalize_armor_class(ose_ac):
    armor_class = {
        "base_ac": 10,
        "secondary_ac": None,
    }
    ac_string_begin = ose_ac.find("[")
    ac_string_end = ose_ac.find("]")
    armor_class["base_ac"] = int(ose_ac[ac_string_begin + 1:ac_string_end])

    secondary_ac_string_begin = ose_ac.find("[", ac_string_end + 1)
    if secondary_ac_string_begin != -1:
        secondary_ac_string_end = ose_ac.find("]", ac_string_end + 1)

        if secondary_ac_string_end == -1:
            raise ValueError(f"Secondary AC boundary not found for: {ose_ac}")
        armor_class["secondary_ac"] = int(ose_ac[secondary_ac_string_begin + 1:secondary_ac_string_end])

    return armor_class

def normalize_hit_dice(ose_hd):
    hit_dice = {
        "number_of_dice": 0,
        "die": "d8",
        "hp_modifier": 0,
        "requires_enrichment": False
    }
    clean_hd = ose_hd.replace("*", "")
    first_parenthesis = clean_hd.find("(")
    if "+" in clean_hd:        
        modifier = clean_hd.find("+")
        hit_dice["number_of_dice"] = int(clean_hd[:modifier])
        hit_dice["hp_modifier"] = int(clean_hd[modifier + 1:first_parenthesis])
    elif "-" in clean_hd:
        modifier = clean_hd.find("-")
        hit_dice["number_of_dice"] = int(clean_hd[:modifier])
        hit_dice["hp_modifier"] = -int(clean_hd[modifier + 1:first_parenthesis])
    elif "½" in clean_hd:
        hit_dice["number_of_dice"] = unicodedata.numeric("½")
    elif "to" in clean_hd:
        to_begin = clean_hd.find("to")
        hit_dice["number_of_dice"] = int(clean_hd[:to_begin])
        hit_dice["requires_enrichment"] = True
        # These monsters' hd are expressed ranges. Will have to build variants for each.
    else:
        hit_dice["number_of_dice"] = int(clean_hd[:first_parenthesis])

    return hit_dice

def normalize_single_attack(single_attack_string):
    attack = {
        "attack_name": None,
        "number_of_attacks": 1,
        "damage_dice": None,
        "damage_modifier": 0,
        "effects": []        
    }

    if single_attack_string.strip().lower() == "none":
        attack["number_of_attacks"] = 0
        return attack
    
    first_parenthesis = single_attack_string.find("(")
    closing_parenthesis = single_attack_string.find(")")

    if first_parenthesis == -1 and closing_parenthesis == -1:
        attack["attack_name"] = single_attack_string.strip().lower()
        return attack
    
    if (
        first_parenthesis == -1
        or closing_parenthesis == -1
        or closing_parenthesis < first_parenthesis
    ):
        raise ValueError(
            f"Invalid single attack format: {single_attack_string!r}"
        )

    base_number_attacks = single_attack_string.find("×", 0, first_parenthesis)
    
    if base_number_attacks != -1:
        count_string = single_attack_string[:base_number_attacks].strip()
        if "to" in count_string:
            attack["number_of_attacks"] = None
            attack["requires_enrichment"] = True
            attack["source_attack_string"] = count_string
        else:    
            attack["number_of_attacks"] = int(count_string)
        
        attack["attack_name"] = single_attack_string[base_number_attacks + 1:first_parenthesis].strip().lower()
    else:
        attack["attack_name"] = single_attack_string[:first_parenthesis].strip().lower()

    damage_string = single_attack_string[first_parenthesis + 1:closing_parenthesis]
    damage_string = damage_string.replace("–", "-")

    if "/" in damage_string:
        weapon_expression = damage_string.split("/", 1)[1].strip()

        if weapon_expression == "weapon damage die" or weapon_expression.startswith(
            ("weapon damage die +", "weapon damage die -")
        ):
            damage_string = weapon_expression

    damage_string = damage_string.replace(" - ", " + -")  
    damage_parts = damage_string.split("+")
    first_damage_part = damage_parts[0].strip()
    first_has_numeral = any(char.isdigit() for char in first_damage_part)

    if first_damage_part == "weapon damage die":
        attack["damage_dice"] = first_damage_part
        effects = damage_parts[1:]
    elif first_has_numeral:
        attack["damage_dice"] = first_damage_part
        effects = damage_parts[1:]
    else:
        effects = damage_parts

    for effect in effects:
        part = effect.strip()

        try:
            modifier = int(part)
        except ValueError:
            attack["effects"].append(part)
        else:
            attack["damage_modifier"] += modifier

    return attack

def split_outside_parentheses(ose_attacks, separator):
    attack_strings = []
    current_attack = ""
    inside_parentheses = False
    index = 0

    while index < len(ose_attacks):
        character = ose_attacks[index]
        if character == "(":
            inside_parentheses = True
        elif character == ")":
            inside_parentheses = False
        
        if not inside_parentheses and ose_attacks[index:index + len(separator)] == separator:
            attack_strings.append(current_attack.strip())
            current_attack = ""
            index += len(separator)
        else:
            current_attack += character
            index += 1

    attack_strings.append(current_attack.strip())
    return attack_strings

def normalize_attacks(ose_attacks):
    attack_options = []
    routines = split_outside_parentheses(ose_attacks, " or ")
    if len(routines) == 2 and "(" not in routines[0] and "(" in routines[1]:
        first_parenthesis = routines[1].find("(")
        closing_parenthesis = routines[1].find(")")
        shared_damage_dice = routines[1][first_parenthesis:closing_parenthesis + 1].strip()
        routines[0] = routines[0] + " " + shared_damage_dice

    for routine in routines:
        routine = routine.strip()

        if routine.startswith("[") and routine.endswith("]"):
            routine = routine[1:-1].strip()

        attack_option = {}
        
        for attack_string in split_outside_parentheses(routine, "+"):
            attack = normalize_single_attack(attack_string)
            attack_option[attack["attack_name"]] = attack

        attack_options.append(attack_option)

    return attack_options


url = "https://oldschoolessentials.necroticgnome.com/rules/doku.php?id=monsters:monster_list"
response = get_ose_page(url)
parsed_html = get_parsed_html(response)
links = get_html_links(parsed_html)
monster_links = get_ose_monster_links(links)

test_monster_links = monster_links[50:92]
test_monster_links.append(monster_links[0])
test_monster_links.append(monster_links[21])
test_monster_links.append(monster_links[32])
test_monster_links.append(monster_links[43])

monster_records = build_ose_monster_records(test_monster_links)
monster_pages = get_ose_monster_page(monster_records)
monster_stats = get_ose_monster_stats_string(monster_pages, monster_records)

monster_stats_parsed = parse_ose_monster_stats(monster_stats)
# validation_results = validate_ose_monster_stats(monster_stats_parsed)
# for monster in monster_stats:
#     print(monster["name"], "=", monster["source_group"])
# for monster in monster_stats_parsed:
#     if "to" in monster["stats"]["formatted"]["HD"]:
#         print(monster["name"], "=", monster["stats"]["formatted"]["HD"])
# for monster in monster_stats_parsed:
#     monster_armor_class = normalize_armor_class(monster["stats"]["formatted"]["AC"])
#     print(monster["name"], ":", monster_armor_class)

# for monster in monster_stats_parsed:
#     print(monster["name"], ":", monster["stats"]["formatted"]["Att"])
#     monster_attack = normalize_attacks(monster["stats"]["formatted"]["Att"])

#     if monster_attack:
#         print(monster["name"], ":", "Attacks normalized")

# for monster in monster_stats_parsed:
#     monster_attack = normalize_attacks(monster["stats"]["formatted"]["Att"])
#     print(monster["name"], ":", monster_attack)

# print(normalize_single_attack("Butt (1d8)"))
# print(normalize_single_attack("2 × claw (1d4)"))
# print(normalize_single_attack("Sting (1d3 + poison + lodged stinger)"))

# print(normalize_attacks("2 × claw (1d4) + bite (2d8)"))
# print(normalize_attacks("Sting (1d3 + poison + lodged stinger)"))
# print(normalize_attacks("2 × claw (1d4) + bite (2d8) + tail (1d6 + poison)"))
# print(normalize_attacks("Bite (1d6) or breath (1d6 per Hit Die)"))
# print(normalize_attacks("Talons or beak (1d6)"))
# print(normalize_attacks("Touch (1d10 + energy drain) or gaze (charm)"))
# print(normalize_attacks("Weapon (1d8 / weapon damage die)"))
# print(normalize_attacks("Weapon (1d6 + 2 / weapon damage die + 2)"))

print(normalize_single_attack("Weapon (1d6 + 2 / weapon damage die + 2)"))
print(normalize_single_attack("Weapon (1d4 / weapon damage die – 1)"))
print(normalize_single_attack("Fist (3d10 + 1d10 heat)"))


monster_armor_class = normalize_armor_class()
print("done")


