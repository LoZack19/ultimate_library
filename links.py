import re
import json
import config


def parse_link(link: str) -> dict:
    if link == None:
        return None
    
    (protocol, body) = link.split("://", maxsplit=1)
    (domain, path) = body.split('/', maxsplit=1)
    channel = ""
    
    if domain == "t.me":
        channel += re.split(r"\?|/",path).pop(0)

    parsed_link = {
        "protocol": protocol,
        "domain": domain,
        "path": path,
        "channel": channel
    }

    return parsed_link


# True if all keys in pattern match with the corresponding
# key in the dictionary
def match_pattern(dict_: dict, pattern: dict) -> bool:
    match = True

    for key in pattern:
        if dict_[key] != pattern[key]:  # could generate key error
            match = False

    return match


def get_broken_links(works: list) -> list:
    broken = []
    
    with open(config.broken_patterns, 'r') as infile:
        broken_patterns = json.load(infile)

    for work in works:
        link = parse_link(work["link"])
        
        if link == None:
            broken.append(work)
        else:
            for broken_pattern in broken_patterns:
                if match_pattern(link, broken_pattern):
                    broken.append(work)
    
    return broken       


def save_links(works: list, filename: str):
    infos = []

    for work in works:
        info = {
            "title": work["title"],
            "link": work["link"]
        }
        infos.append(info)
    
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(infos, outfile, indent=4)


def fix_broken_links(works: list):
    filename = config.fixed_links

    with open(filename, 'r', encoding='utf-8') as infile:
        fixed_ls = json.load(infile)

    for broken in works:
        for fixed in fixed_ls:
            if broken["title"] == fixed["title"]:
                broken["link"] = fixed["link"]