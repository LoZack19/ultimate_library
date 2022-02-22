import json
import parse


def init_works(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as infile:
        works = json.load(infile)
    
    for work in works:
        work["date"] = tuple(work["date"])
    
    return works


def merge(a: list, b: list) -> list:
    res = list(a)

    for n in b:
        if n not in res:
            res.append(n)
    
    return res


def is_message_pool(filename) -> bool:
    res = False

    with open(filename, 'r', encoding='utf-8') as infile:
            if infile.readline()[0] == '{':
               res = True

    return res 


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

def main():
    works = merge_files(config.pool, "/home/giovanni/Scaricati/Telegram Desktop/diff.json")
    works = date.sort_works_by_date(works)
    fn.print_works(works)

main()