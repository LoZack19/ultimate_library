##
# Automates statistics about works. Counts works per author
# works per date, works per nation and works per publication place.
# Those informations are returned in a form of dictionaries associating
# To each possible key value a number of occurrencies.
#
# Author: Giovanni Zaccaria
#

import datetime as dt
import links
from parse import init_works


def count__(works: list, key: str, plussplit=True) -> dict:
    count = {}

    for work in works:
        record = work[key]

        if plussplit:
            fields = record.split('+')
        else:
            fields = [record]

        for field in fields:
            if field in count:
                count[field] += 1
            else:
                count[field] = 1
    
    return count


def print__(dict_: dict, formatter: str):
    for item in sorted(dict_.items(), key=lambda x: x[1], reverse=True):
        print(formatter % item)


### AUTHORS ###


def count_authors(works: list) -> dict:
    return count__(works, "author")


def print_sorted_authors(authors: dict):
    for author in sorted(authors.items(), key=lambda x: x[1],reverse=True):
        print("%30s:%20s" % author)


### DATE ###
# frequency: works per day

# Create dictionary of works per date
def count_frequency(works: list) -> dict:
    dates = count__(works, "date", plussplit=False)
    frequency = {}

    # Datetime conversion to facilitate sorting
    for date in dates:
        (year, month, day) = date
        if date != (0, 0, 0):
            frequency[dt.datetime(year, month, day)] = dates[date]
    
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


### NATION ###


def count_nations(works: list) -> dict:
    return count__(works, "nation")


def print_nations(nations: dict):
    print__(nations, "%10s:%3d")


### LINK ###


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


def print_hosts(hosts: dict):
    print__(hosts, "%20s:%4d")


def count_channels(works: list) -> dict:
    channels = {}

    for work in works:
        link = links.parse_link(work["link"])
        if link != None and link["domain"] == "t.me":
            channel = link["channel"]
            
            if channel in channels:
                channels[channel] += 1
            else:
                channels[channel] = 1
    
    return channels


def print_channels(channels: dict):
    print__(channels, "%20s:%4d")


### PLACE ###


def count_places(works: list):
    return count__(works, "place", plussplit=False)


def print_places(places: dict):
    print__(places, "%31s:%4d")