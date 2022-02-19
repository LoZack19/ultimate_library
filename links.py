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


def fix_broken_links(works: list):
    filename = config.fixed_links

    with open(filename, 'r', encoding='utf-8') as infile:
        fixed_ls = json.load(infile)

    for broken in works:
        for fixed in fixed_ls:
            if broken["title"] == fixed["title"]:
                broken["link"] = fixed["link"]
            