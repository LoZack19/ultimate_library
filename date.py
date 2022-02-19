import datetime as dt
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


def time_range_str(trange: list):
    return ["%d/%d/%d" % i[::-1] for i in trange]


def get_oldest(works: list) -> tuple:
    freq = count_frequency(works)
    oldest = min(freq)
    return (oldest.year, oldest.month, oldest.day)


def get_newer(works: list) -> tuple:
    freq = count_frequency(works)
    oldest = max(freq)
    return (oldest.year, oldest.month, oldest.day)


# Right button to control scaling
# Left button to move the graph
# $start and $end are (year, month, day) tuples
def plot_works(works: list, start=None, end=None, labels_freq=365):
    if start == None:
        start = get_oldest(works)
    if end == None:
        end = get_newer(works)

    trange = time_range(start, end)
    xticks = time_range_str(trange)  # custom x labels

    x = [i for i in range(len(trange))]
    y = [0 for i in range(len(x))]

    for (i, date) in enumerate(trange):
        for work in works:
            if work["date"] == date:
                y[i] += 1
    
    plt.axis("auto")
    plt.title("Works from %s to %s" % (xticks[0], xticks[-1]), fontsize=15)
    plt.xticks(x[::labels_freq], xticks[::labels_freq])
    plt.tight_layout()
    plt.plot(x, y)
    plt.grid(axis='y')
    plt.show()


from parse import *
import config
def test():
    works = init_works(config.pool)
    for year in range(2016, 2022):
        plot_works(works, (year, 1, 1), (year + 1, 1, 1), 30)


if __name__ == "__main__":
    test()