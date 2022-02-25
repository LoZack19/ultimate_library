# Itemgetter with case sensitive functionality
from parse import select_matching_works


# Selects an item from all works matching the pattern
def get_item(works: list, key: str, case_sensitive=False, pattern=None, plussplit=False) -> set:
    items = set()

    if pattern != None:
        works = select_matching_works(works, pattern)

    for work in works:
        item_ls = [work[key]]
        if plussplit:
            item_ls = work[key].split('+')
        
        for item in item_ls:
            if not case_sensitive:
                item = item.lower().strip()
            
            items.add(item)
    
    return items


def diff(a_: list, b_: list, key: str, case_sensitive=False) -> set:
    """
        Example of usage:
        diff_works = diff(biblum, ccl, "title", case_sensitive=False)
    """

    a = get_item(a, key, case_sensitive)
    b = get_item(b, key, case_sensitive)

    diff = a - b

    return diff