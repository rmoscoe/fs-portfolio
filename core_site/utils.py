def sort_as_linked_list(iterable):
    sorted_list = []
    next_item_map = {}
    current = None
    for obj in iterable:
        if obj.show_after is None:
            current = obj
        else:
            next_item_map[obj.show_after] = obj
    while current is not None:
        sorted_list.append(current)
        current = next_item_map.get(current)
    return sorted_list