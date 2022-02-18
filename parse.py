##
# Parsed the messages in the "Biblioteca Statale Leonense" (BSL) format
# into a more readable json data structure containing information
# about each work
#
# Author: Giovanni Zaccaria
#

import json
import re


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
    patches = init_patches("patches.txt")   # Speeds up the code by loading the patches only once
    author_pseudonyms = init_pseudonyms("author_pseudonyms.txt")
    nation_pseudonyms = init_pseudonyms("nation_pseudonyms.txt")

    for (id, message) in enumerate(messages):
        id += 1

        # Handle format errors
        try:
            split_text = parse_text(message[2], patches)
        except:
            raise RuntimeError("Bad Format")
        
        # Handle broken link
        link = message[1]["href"]
        
        # Handle broken author
        try:
            author = format_author(split_text[0], author_pseudonyms)
        except:
            raise RuntimeError("Bad author")

        # Handle broken date
        try:
            date = format_date(split_text[1])
        except (IndexError):
            raise RuntimeError("Broken date")
        
        # Handle broken nation
        try:
            nation = format_nation(split_text[2], nation_pseudonyms)
        except:
            raise RuntimeError("Bad nation")

        work = {
            "title": patch_text(message[0]).strip(),
            "link": link,
            "author": author,
            "date": date,
            "nation": nation,
            "place": split_text[3]
        }

        works.append(work)
    
    return works


# Initializes directly a list of works from the messages file
def init_works(filename: str, verbose=False) -> list:
    messages = init_messages(filename)
    works = parse_works(messages, verbose)
    return works


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


def format_nation(raw: str, pseudonyms: dict) -> str:
    nation = raw

    nations = nation.split('/')
    for i in range(len(nations)):
        nations[i] = resolve_pseudonyms(nations[i].strip(), pseudonyms)
    nation = '+'.join(nations)

    return nation


# Retrieve currently used name and convert an old pseudonym used by this person
# into its actual name. Useful for spelling correction.
def resolve_pseudonyms(raw: str, pseudonyms: dict) -> str:
    chosen_name = raw

    for name in pseudonyms:
        if chosen_name in pseudonyms[name]:
            chosen_name = name
    
    return chosen_name


# Reads the data structure which links currently used names to a list of old pseudonyms
def init_pseudonyms(filename: str) -> dict:
    pseudonyms = {}

    with open(filename, 'r') as infile:
        for line in infile:
            (name, raw) = line.strip().split(':')
            pseudonyms_ls = raw.split(';')
            pseudonyms[name] = pseudonyms_ls
    
    return pseudonyms


# Splits the field of the work message oming after the button
def parse_text(text: str, patches: dict) -> list:
    text = patch_text(text, patches)

    split_text = re.split(r",|-|\[", text)
    parsed = [
        split_text[0].strip(),  # author
        split_text[1].strip(),  # raw date
        split_text[2].strip(),  # nation
        split_text[3].strip("] \n\t")   # place
    ]

    return parsed


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
        patches = init_patches("patches.txt")

    if text in patches:
        patch = patches[text]
    
    return patch


# Initializes a lookup table for months
def init_months(filename: str) -> list:
    lookup = []

    with open("months.txt", 'r') as infile:
        for line in infile:
            lookup.append(line.strip())
    
    return lookup


# Returns a tuple containing year, month and day
def format_date(date: str) -> tuple:
    lookup = init_months("months.txt")

    if date == "None":
        return (0, 0, 0)
    
    date_ls = date.lower().split()
    (day, month, year) = (
        int(date_ls[0]),
        lookup.index(date_ls[1]) + 1,
        int(date_ls[2])
    )

    return (year, month, day)


# Saves the parsed works into a data structure in json
def save_works(filename: str, works: list):
    
    with open(filename, 'w', encoding="utf-8") as outfile:
        json.dump(works, outfile, indent=4)