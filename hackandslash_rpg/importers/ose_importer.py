import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
            description_and_stats = monster_string.split("\n\n", 1)

            monster["source_group"] = None
            monster["description"] = description_and_stats[0].strip()
            monster["stats"]["raw"] = description_and_stats[1].strip()

            monster_raw_strings.append(monster)
            
    return monster_raw_strings

def parse_ose_monster_stats(monster_records):
    if monster_records is None:
        return None
    
    for monster in monster_records:
        raw_stats = monster["stats"]["raw"]

        for i in range(len(OSE_STAT_MARKERS) - 1):
            current_marker = OSE_STAT_MARKERS[i]
            next_marker = OSE_STAT_MARKERS[i + 1]

            start = raw_stats.find(current_marker)
            end = raw_stats.find(next_marker)

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

# def normalize_armor_class(ose_ac):

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
# for monster in monster_stats:
#     print(monster["name"], "=", monster["source_group"])
monster_stats_parsed = parse_ose_monster_stats(monster_stats)
validation_results = validate_ose_monster_stats(monster_stats_parsed)
print("done")


