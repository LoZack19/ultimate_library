##
# Automates statistics about works. Counts works per author
# works per date, works per nation and works per publication place
#
# Author: Giovanni Zaccaria
#

import datetime
import links


def count__(works: list, key: str, plussplit=True) -> dict:
    count = {}

    for work in works:
        record = work[key]

        if plussplit:
            fields = record.split('+')
        else:
            fields = [field]

        for field in fields:
            if field in count:
                count[field] += 1
            else:
                count[field] = 1
    
    return count


def count_authors(works: list) -> dict:
    return count__(works, "author")


def print_sorted_authors(authors: dict):
    for author in sorted(authors.items(), key=lambda x: x[1],reverse=True):
        print("%30s:%20s" % author)


# Create dictionary of works per date
def count_frequency(works: list) -> dict:
    frequency = {}

    for work in works:
        (day, month, year) = work["date"]
        date = datetime.datetime(day, month, year)
        if date in frequency:
            frequency[date] += 1
        else:
            frequency[date] = 1
    
    return frequency


# Print works per date
def print_frequency(freq: dict, chron=True):
    if chron:
        # Chronological order (from older to newer)
        for (date, f) in sorted(freq.items(), key=lambda x: x[0]):
            print( "%10s:%3d" % (date.strftime("%d/%m/%Y"), f))
    else:
        # From most to less prolific day
        for (date, f) in sorted(freq.items(), key=lambda x: x[1], reverse=True):
            print( "%10s:%3d" % (date.strftime("%d/%m/%Y"), f))


def count_nations(works: list) -> dict:
    return count__(works, "nation")


def print_nations(nations: dict):
    for (nation, count) in sorted(nations.items(), key=lambda x: x[1], reverse=True):
        print("%10s:%3d" % (nation, count))


def count_hosts(works: list) -> dict:
    hosts = {}

    for work in works:
        link = links.parse_link(work["link"])
        if link != None:
            domain = link["domain"]

            if domain in hosts:
                hosts[domain] += 1
            else:
                hosts[domain] = 1
        
    return hosts


# Wrapper around similar function
def print_hosts(hosts: dict):
    for (host, count) in sorted(hosts.items(), key=lambda x:x[1], reverse=True):
        print("%20s:%4d" % (host, count))