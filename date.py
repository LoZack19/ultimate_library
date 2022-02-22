import datetime as dt
import parse
from datetime import datetime
from count import count_frequency
import matplotlib.pyplot as plt

# Returns a list of ordered tuples (year, month, day) from day $start to day $end
def time_range(start_: tuple, end_: tuple) -> list:
    (year, month, day) = start_
    start = datetime(year, month, day)
    
    (year, month, day) = end_
    end = datetime(year, month, day)

    trange = (end - start).days
    time_range = [start + dt.timedelta(days=i) for i in range(trange)]

    return [(date.year, date.month, date.day) for date in time_range]


# Returns a list of string time lables
def time_range_labels(trange: list):
    return ["%d/%d/%d" % i[::-1] for i in trange]


# Find date of the oldes work
def get_oldest(works: list) -> tuple:
    freq = count_frequency(works)
    oldest = min(freq)
    return (oldest.year, oldest.month, oldest.day)


# Find date of the newest workj
def get_newest(works: list) -> tuple:
    freq = count_frequency(works)
    oldest = max(freq)
    return (oldest.year, oldest.month, oldest.day)


def get_datetime_date(work: dict):
    (year, month, day) = work["date"] if work["date"] != (0, 0, 0) else (1999, 1, 1)
    return datetime(year, month, day)


# Returns a list of works written in a certain date
def get_works(works: list, year=None, month=None, day=None, date=()) -> list:
    matches = []

    # At least the year is necessary to be a legitimate value
    if year == None:
        (year, month, day) = date   # could generate ValueError
    

    for work in works:
        if work["date"] != None:
            (wyear, wmonth, wday) = work["date"]
            
            match = wyear == year   # year match
            if month != None:
                match = match and wmonth == month   # month match (if not None)
                if day != None:
                    match = match and wday == day   # day match (if not None)
            
            if match:
                matches.append(work)

    return matches


# Right button to control scaling
# Left button to move the graph
# $start and $end are (year, month, day) tuples
def plot_works(works: list, start=None, end=None, labels_freq=365, pattern=None):
    if start == None:
        start = get_oldest(works)
    if end == None:
        end = get_newest(works)

    # Select works which match this pattern
    if pattern != None:
        works = parse.select_matching_works(works, pattern)

    # prepare labels
    trange = time_range(start, end)
    xticks = time_range_labels(trange)  # custom x labels

    # prepare axes values
    x = [i for i in range(len(trange))]
    y = [0 for i in range(len(x))]
    ## initialize y axis
    for (i, date) in enumerate(trange):
        for work in works:
            if work["date"] == date:
                y[i] += 1
    
    # plot
    plt.axis("auto")
    plt.title("Works from %s to %s" % (xticks[0], xticks[-1]), fontsize=15)
    plt.xticks(x[::labels_freq], xticks[::labels_freq])
    plt.tight_layout()
    plt.plot(x, y,color='orange')
    plt.grid(axis='y')
    plt.show()


def sort_works_by_date(works_: list) -> list:
    works = list(works_)
    works = sorted(works, key=get_datetime_date)
    return works