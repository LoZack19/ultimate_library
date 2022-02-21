##
# Parsed the messages in the "Biblioteca Statale Leonense" (BSL) format
# into a more readable json data structure containing information
# about each work
#
# Author: Giovanni Zaccaria
#

import json
import re
import links
import config


# Reads the message pool and returns a list of messages (only text information is kept)
def init_messages(filename: str) -> list:
    messages = []

    with open(filename, 'r', encoding='utf-8') as infile:
        record = json.load(infile)["messages"]
        for message in record:
            text = message["text"]
            
            if text != '':
                # Handling broken link
                if type(text) == str and '⏺' in text:
                    text = text.split('⏺')
                    link = {
                        "type": "text_link",
                        "text": "⏺",
                        "href": None
                    }
                    text.insert(1, link)
                
                if len(text) > 3:
                    remove_pretty_formatting(text)
                
                messages.append(text)
    
    return messages


# Initializes directly a list of works from the messages file
def init_works(filename: str, verbose=False) -> list:
    messages = init_messages(filename)
    works = parse_works(messages, verbose)
    links.fix_broken_links(works)
    return works


# Remove bold, italic and other pretty formatting without removing the link
def remove_pretty_formatting(text: list) -> None:
    
    for (i, pretty_dict) in enumerate(text):
        if type(pretty_dict) == dict and "href" not in pretty_dict:
            pretty = pretty_dict["text"]
        
            after = ""
            if i+1 < len(text):
                after = text.pop(i+1)
            
            text[i-1] += pretty + after
            text.pop(i)


# Parses the messages into a list of dictionaries containing major information about each work
def parse_works(messages: list, verbose=False) -> list:
    works = []
    patches = init_patches(config.patches)   # Speeds up the code by loading the patches only once

    for (id, message) in enumerate(messages):
        id += 1

        raw_fields = split_text(message, patches)   # split and patch
        work = format_row_work(raw_fields)          # parse
        works.append(work)                          # append
    
    return works


### PSEUDONYMS ###


# Retrieve currently used name and convert an old pseudonym used by this person
# into its actual name. Useful for spelling correction.
def resolve_pseudonyms(raw: str, pseudonyms: dict) -> str:
    chosen_name = raw

    for name in pseudonyms:
        if chosen_name in pseudonyms[name]:
            chosen_name = name
    
    return chosen_name


# Reads the data structure which links currently used names to a list of old pseudonyms
def init_pseudonyms(filename: str, has_quotes=False) -> dict:
    pseudonyms = {}

    if not has_quotes:
        splits = [':', ';']
    else:
        splits = ['":"', '";"']

    with open(filename, 'r') as infile:
        
        for line in infile:
            (name, raw) = line.strip().split(splits[0])
            pseudonyms_ls = raw.split(splits[1])

            # clean quotes if it has quotes
            if has_quotes:
                name = name.strip('"')
                for i in range(len(pseudonyms_ls)):
                    pseudonyms_ls[i] = pseudonyms_ls[i].strip('"')
            
            pseudonyms[name] = pseudonyms_ls
    
    return pseudonyms


### FORMATTING ###


def format_row_work(raw_work: list) -> dict:
    work = {}
    keys = ["title", "link", "author", "date", "nation", "place"]

    for (i, key) in enumerate(keys):
        work[key] = format_field(raw_work[i], key)
    
    return work


# Refine raw fields
def format_field(raw_field: str, key: str) -> str:
    field = ""
    have_pseudonyms = ["title", "author", "nation"]     # keys which support pseudonyms
    have_quotes = ["title"]     # csv formatting with quotes "
    pseudonyms = None

    if key in have_pseudonyms:
        pseudonym_file = key + "_pseudonyms"
        has_quotes = key in have_quotes
        pseudonyms = init_pseudonyms(config.CONFIG[pseudonym_file], has_quotes)

    if key == "title":
        field = format_title(raw_field, pseudonyms)
    elif key == "link":
        field = format_link(raw_field)
    elif key == "author":
        field = format_author(raw_field, pseudonyms)
    elif key == "date":
        field = format_date(raw_field)
    elif key == "nation":
        field = format_nation(raw_field, pseudonyms)
    elif key == "place":
        field = format_place(raw_field)
    else:
        raise KeyError("Invalid key")
    
    return field


def format_title(raw_field: str, pseudonyms: dict):
    title = resolve_pseudonyms(raw_field.strip(), pseudonyms)
    return title


def format_link(raw_field: str):
    return raw_field["href"]


# Transforms the raw author information into a more readable author
def format_author(raw: str, pseudonyms: dict) -> str:
    author = raw

    # Delete possessive 'di'
    if raw[:2] == "di":
        author = raw[2:].strip()
    
    # Parse each author and resolve its pseudonym
    authors = author.split('&')
    for i in range(len(authors)):
        authors[i] = resolve_pseudonyms(authors[i].strip(), pseudonyms)
    author = '+'.join(authors)
    
    return author


# Initializes a lookup table for months
def init_months(filename: str) -> list:
    lookup = []

    with open(filename, 'r') as infile:
        for line in infile:
            lookup.append(line.strip())
    
    return lookup


# Returns a tuple containing year, month and day
def format_date(date: str) -> tuple:
    lookup = init_months(config.months)

    if date == "None":
        return (0, 0, 0)
    
    date_ls = date.lower().split()
    (day, month, year) = (
        int(date_ls[0]),
        lookup.index(date_ls[1]) + 1,
        int(date_ls[2])
    )

    return (year, month, day)


def format_nation(raw: str, pseudonyms: dict) -> str:
    nation = raw

    nations = nation.split('/')
    for i in range(len(nations)):
        nations[i] = resolve_pseudonyms(nations[i].strip(), pseudonyms)
    nation = '+'.join(nations)

    return nation


def format_place(raw_field: str):
    place = raw_field.strip()
    return place


### SPLIT AND PATCH ###


# Splits the field of the work message coming after the button
def split_text(message: list, patches: dict) -> list:
    for i in range(len(message)):
        if type(message[i]) == str:
            message[i] = patch_text(message[i], patches)

    split_text = re.split(r",|-|\[", message[2])
    raw_fields = [
        message[0],                # title
        message[1],                # link
        split_text[0].strip(),  # author
        split_text[1].strip(),  # date
        split_text[2].strip(),  # nation
        split_text[3].strip("] \n\t")   # place
    ]

    return raw_fields


# Initializes the dictionary of patches
def init_patches(filename: str) -> dict:
    patches = {}

    with open(filename, 'r') as infile:
        for line in infile:
            record = line.strip().split('">"')
            for i in range(len(record)):
                record[i] = record[i].strip('"')
            
            patches[record[0]] = record[1]
    
    return patches


# Corrects text from a dictionary of patches
def patch_text(text: str, patches=None) -> str:
    patch = text

    if patches == None:
        patches = init_patches(config.patches)

    if text in patches:
        patch = patches[text]
    
    return patch


### SELECT BY PATTERN ###


# Select all elements of the list_ which match the pattern
def select_matching__(list_: list, pattern: dict) -> list:
    matches = []

    for element in list_:
        if links.match_pattern(element, pattern):
            matches.append(element)
    
    return matches


# Select all the works which match the pattern
# WARNING: Non pseudonym resolution is performed
def select_matching_works(works: list, pattern: dict) -> list:
    return select_matching__(works, pattern)


### SAVE ###


# Saves the parsed works into a data structure in json
def save_works(filename: str, works: list):
    
    with open(filename, 'w', encoding="utf-8") as outfile:
        json.dump(works, outfile, indent=4)


def test():
    works = init_works(config.pool)
    save_works("temp.json", works)

if __name__ == "__main__":
    test()