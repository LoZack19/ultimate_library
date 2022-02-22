import json
import parse


# Initializes a works list from a json file
def init_works(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as infile:
        works = json.load(infile)
    
    for work in works:
        work["date"] = tuple(work["date"])
    
    return works


# Merge two works lists
def merge(a: list, b: list) -> list:
    res = list(a)

    for n in b:
        if n not in res:
            res.append(n)
    
    return res


# Checks if the file is a message pool or not
# If it's not, proabily it's a works list
def is_message_pool(filename) -> bool:
    res = False

    with open(filename, 'r', encoding='utf-8') as infile:
            if infile.readline()[0] == '{':
               res = True

    return res 


# Merge works from different works lists
def merge_files(*filenames):
    res = []

    for filename in filenames:
        if is_message_pool(filename):
            works = parse.init_works(filename)
        else:
            works = init_works(filename)
        
        res = merge(res, works)
    
    return res


import config
import main as fn
import date
import links

def main():
    works = merge_files(config.pool, "/home/giovanni/Scaricati/Telegram Desktop/diff.json")
    works = date.sort_works_by_date(works)
    links.fix_file_links(works, backup_path="/home/giovanni/Scaricati/Telegram Desktop/ChatExport_2022-02-22")
    fn.save_works("works.json", works)

main()