def get_item(works: list, key: str, case_sensitive=False) -> set:
    items = set()

    for work in works:
        item = item = work[key]
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