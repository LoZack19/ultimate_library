from parse import *
import count
import config
import json
import date
import diff


# Show help for a particular screen
def show_options(screen="general"):
    with open(config.help_screen) as infile:
        help_screen = json.load(infile)

    options = help_screen[screen]
    print('\n'.join(options))


def main():
    # If no file is specified read from stdin
    pool = input("pool: ") if config.pool == "" else config.pool
    works = init_works(pool)

    show_options()
    done = False
    keep_screen = False     # Don't go back to general screen
    option = ""
    while not done:
        if not keep_screen:
            option = input("> ")
        if option == 'q':
            done = True
        
        if not done:
            keep_screen = general_screen(option, works)


def clean_option(option: str) -> str:
    if len(option) < 1:
        return ""
    return option[0]


### GENERAL SCREEN ###

"""
    A screen is a function which controls the flow of the program through
    user input.
    It returns a keep_screen boolean value to determine wheatehr to go back to the
    general screen (False) or stay in the current screen (True)

    The general screen is the main screen
    It can directly perform actions or redirect to other screens
"""

def general_screen(option: str, works: list) -> bool:
    res = False
    option = clean_option(option)
    
    # execute actions or goto other screen
    if option == 's':
        filename = input("filename: ")
        save_works(filename, works)
    elif option == 'a':
        res = author_screen(works)
    elif option == 'n':
        res = nation_screen(works)
    elif option == 'd':
        res = date_screen(works)
    elif option == 'l':
        res = hosts_screen(works)
    elif option == 'u':
        res = places_screen(works)
    elif option == 'p':
        print_works(works)
    elif option == 'c':
        print(len(works))
    elif option == 'h':
        show_options("general")
    
    return res


# Print all works in BSL format
def print_works(works: list):
    months = init_months(config.months)
    for work in works:
        if work["date"] != (0, 0, 0):
            date = "%d %s %d" % (work["date"][2], months[work["date"][1] - 1], work["date"][0])
        else:
            date = str(None)
        print("%s, %s, %s - %s [%s]" % (work["title"], work["author"],
                                        date,
                                        work["nation"], work["place"]))


### AUTHOR SCREEN ###

"""
    A screen can both have options that don't require further
    user input or options that do require it.
    The input should be asked once, and not repeatedly in more parts
    of the code if it's used by more than 1 or at most 2 options, to make the
    code more readable and the error handling more managable.
"""

def author_screen(works: list) -> bool:
    option = clean_option(input("> "))
    authors = count.count_authors(works)
    specific = list("tnc")  # options for a specific author
    res = True

    if option == 'h':
        show_options("author")
    elif option == 'b':
        res = False
    elif option == 'q':
        quit()
    elif option == 'g':
        count.print_sorted_authors(authors)
    elif option == 'l':
        list_authors(authors)
    elif option in specific:
        try:
            author = get_author(authors)

            if option == 't':
                print_works_from(works, author)
            elif option == 'n':
                print(authors[author])
            elif option == 'c':
                author_countries(works, author)
            
        except KeyError as err:
            print(err)
    
    return res


def get_author(authors=None) -> str:
    buffer = input("author: ")
    pseudonyms = init_pseudonyms(config.author_pseudonyms)
    author = resolve_pseudonyms(buffer, pseudonyms)

    if authors != None:
        if author not in authors:
            raise KeyError("No such author")
    
    return author


def list_authors(authors: dict):
    for author in authors:
        print(author)


def print_works_from(works: list, author: str):
    for work in works:
        if work["author"] == author:
            print(work["title"])


def author_countries(works: list, author: str):
    countries = {}

    for work in works:
        if work["author"] == author:
            country_ls = work["nation"].split('+')

            for country in country_ls:
                if country in countries:
                    countries[country] += 1
                else:
                    countries[country] = 1
    
    for (country, count_) in sorted(countries.items(), key=lambda x:x[1], reverse=True):
        print("%10s: %4d" % (country, count_))


### NATION SCREEN ###


def nation_screen(works: list):
    option = clean_option(input("> "))
    nations = count.count_nations(works)
    res = True  # remain in the screen
    specific = list("nalt")     # options for a specific country

    if option == 'h':
        show_options("country")
    elif option == 'b':
        res = False
    elif option == 'q':
        quit()
    elif option == 'g':
        count.print_nations(nations)
    if option in specific:
        try:
            nation = get_nation(nations)

            if option == 'n':
                print(nations[nation])
            elif option == 'a':
                country_authors(works, nation, verbose=True)
            elif option == 'l':
                authors = country_authors(works, nation)
                list_authors(authors)
            elif option == 't':
                country_titles(works, nation, verbose=True)
        
        except KeyError as err:
            print(err)
    
    return res


def get_nation(nations=None) -> str:
    buffer = input("nation: ")
    pseudonyms = init_pseudonyms(config.nation_pseudonyms)
    nation = resolve_pseudonyms(buffer, pseudonyms)

    if nations != None:
        if nation not in nations:
            raise KeyError("No such nation")

    return nation


def country_authors(works: list, nation: str, verbose=False) -> dict:
    authors = {}
    
    for work in works:
        if nation == work["nation"]:
            authors_str = work["author"]
            author_ls = authors_str.split('+')

            for author in author_ls:
                if author in authors:
                    authors[author] += 1
                else:
                    authors[author] = 1
    
    if verbose:
        for (author, count_) in sorted(authors.items(), key=lambda x:x[1], reverse=True):
            print("%30s: %4s" % (author, count_))
    
    return authors


def country_titles(works: list, nation: str, verbose=False) -> list:
    titles = []

    for work in works:
        if work["nation"] == nation:
            titles.append(work["title"])
    
    if verbose:
        for title in titles:
            print(title)
    
    return titles


### DATE SCREEN ###


def date_screen(works: list):
    option = clean_option(input("> "))
    freq = count.count_frequency(works)
    res = True

    if option == 'q':
        quit()
    elif option == 'b':
        res = False
    elif option == 'h':
        show_options("date")
    elif option == 'c':
        count.print_frequency(freq)
    elif option == 'a':
        count.print_frequency(freq, chron=False)
    elif option == 'p':
        date.plot_works(works)
    elif option == 'd':
        try:
            date_ = get_date()
            matches = date.get_works(works, date=date_)
            print_works(matches)
        except (IndexError, ValueError) as err:
            print(err)
    
    return res


def get_date() -> tuple:
    year = int(input("year [mandatory]: "))
    month = None
    day = None
    
    print("%s[Press enter to stop]" % (" " * len("year ")))
    buffer = input("month: ")

    # parse month
    if buffer.isnumeric():
        month = int(buffer)
        if not 1 <= month <= 12:
            raise ValueError("Invalid month (%d)" % (month))    # ValueError
    elif buffer.isalpha():
        months = init_months(config.months)
        month = months.index(buffer.strip().lower()) + 1    # can raise IndexError
    
    if month != None:
        buffer = input("day: ")
        
        if buffer != "":
            day = int(buffer)   # can raise ValueError
            if not 1 <= day <= 31:
                raise ValueError("Invalid day (%d)" % (day))
    
    return (year, month, day)


### HOSTS SCREEN ###


def hosts_screen(works: list) -> bool:
    option = clean_option(input("> "))
    hosts = count.count_hosts(works)
    channels = count.count_channels(works)
    res = True

    if option == 'q':
        quit()
    elif option == 'b':
        res = False
    elif option == 'h':
        show_options("hosts")
    elif option == 'o':
        count.print_hosts(hosts)
    elif option == 'c':
        count.print_channels(channels)
    elif option == 'r':
        broken = links.get_broken_links(works)
        print_works(broken)
        print("TOT: %d" % (len(broken)))
    
    return res


### PLACE SCREEN ###


def places_screen(works: list) -> bool:
    option = clean_option(input("> "))
    places = count.count_places(works)
    res = True

    if option == 'q':
        quit()
    elif option == 'b':
        res = False
    elif option == 'h':
        show_options("place")
    elif option == 'g':
        count.print_places(places)
    elif option == 'a':
        places = diff.get_item(works, "place", case_sensitive=True)
        for place in sorted(places):
            print(place)
    
    return res


if __name__ == "__main__":
    main()