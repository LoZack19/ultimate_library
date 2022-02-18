from parse import *
import count


def show_options(screen="general"):
    options = ""

    if screen == "general":
        options = (
            "--- OPTIONS ---",
            "(s)ave the works",
            "(p)rint",
            "(c)ount",
            "(a)uthor statistics",
            "(n)ation statistics",
            "(d)ate statistics",
            "(l)ink hosts",
            "(h)elp screen",
            "(q)uit [everywhere]",
            "(b)ack [everywhere]"
        )
    elif screen == "author":
        options = (
            "--- AUTHOR ---",
            "(g)eneral statistics",
            "",
            "about a specific author:",
            "(t)itle of works",
            "(c)ountries of activity",
            "(n)umber of works",
            "(l)ist all authors"
        )
    elif screen == "country":
        options = (
            "(g)eneric statistics",
            "",
            "about a specific country:",
            "(n)umber of works for a country",
            "(a)uthors in a country",
            "(t)itles in that country"
        )
    
    print('\n'.join(options))


def main():
    pool = input("pool: ")
    works = init_works(pool)

    show_options()
    done = False
    repeat = False
    option = ""
    while not done:
        if not repeat:
            option = input("> ")
        if option == 'q':
            done = True
        
        if not done:
            repeat = general_screen(option, works)


def clean_option(option: str) -> str:
    if len(option) < 1:
        return ""
    return option[0]


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
    elif option == 'p':
        print_works(works)
    elif option == 'c':
        print(len(works))
    elif option == 'h':
        show_options("general")
    
    return res


def print_works(works: list):
    months = init_months("months.txt")
    for work in works:
        print("%s, %s, %s - %s [%s]" % (work["title"], work["author"],
                                        "%d %s %d" % (work["date"][2], months[work["date"][1] - 1], work["date"][0]),
                                        work["nation"], work["place"]))


### AUTHOR SCREEN ###


# Returns wheather to repeat the screen or not
def author_screen(works: list) -> bool:
    option = clean_option(input("> "))
    authors = count.count_authors(works)
    res = True

    if option == 'h':
        show_options("author")
    elif option == 'g':
        count.print_sorted_authors(authors)
    elif option == 'l':
        list_authors(authors)
    elif option == 't':
        author = get_author()
        print_works_from(works, author)
    elif option == 'n':
        try:
            author = get_author(authors)
            print(authors[author])
        except KeyError as err:
            print(err)
    elif option == 'c':
        try:
            author = get_author(authors)
            author_countries(works, author)
        except KeyError as err:
            print(err)
    elif option == 'b':
        res = False
    elif option == 'q':
        quit()
    
    return res


def get_author(authors=None) -> str:
    buffer = input("author: ")
    pseudonyms = init_pseudonyms("author_pseudonyms.txt")
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

    if option == 'h':
        show_options("country")
    elif option == 'b':
        res = False
    elif option == 'q':
        quit()
    elif option == 'g':
        count.print_nations(nations)
    elif option == 'n':
        try:
            nation = get_nation(nations)
            print(nations[nation])
        except KeyError as err:
            print(err)
    elif option == 'a':
        try:
            nation = get_nation(nations)
            country_authors(works, nation)
        except KeyError as err:
            print(err)
    elif option == 'l':
        try:
            nation = get_nation(nations)
            list_authors(works, nation)
        except KeyError as err:
            print(err)
    
    return res


def get_nation(nations=None) -> str:
    buffer = input("nation: ")
    pseudonyms = init_pseudonyms("nation_pseudonyms.txt")
    nation = resolve_pseudonyms(buffer, pseudonyms)

    if nations != None:
        if nation not in nations:
            raise KeyError("No such nation")

    return nation


def country_authors(works: list, nation: str, verbose=True):
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


def list_authors(works: list, nation: str):
    authors = country_authors(works, nation, False)

    for author in authors:
        print(author)


### DATE SCREEN ###


def date_screen(works: list): pass


### HOSTS SCREEN ###


def hosts_screen(works: list): pass


if __name__ == "__main__":
    main()