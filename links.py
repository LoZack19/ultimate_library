import re


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