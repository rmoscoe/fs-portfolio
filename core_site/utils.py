from django.core.mail import EmailMessage

def sort_as_linked_list(iterable):
    sorted_list = []
    iterable_list = list(iterable)
    if not iterable_list:
        return sorted_list

    model = iterable_list[0]._meta.model
    iterable_dict = {obj.id: obj for obj in iterable_list}
    
    # 1. Fetch missing ancestors in a single bulk query
    all_show_after_ids = {obj.show_after_id for obj in iterable_list if obj.show_after_id}
    missing_ids = all_show_after_ids - set(iterable_dict.keys())
    
    chain_cache = {}
    if missing_ids:
        # Single database round-trip for ALL missing historical nodes
        missing_objs = model.objects.filter(pk__in=missing_ids)
        chain_cache = {obj.id: obj for obj in missing_objs}

    next_item_map = {}
    current = None

    # 2. Use ID suffix (_id) to avoid invoking lazy-loading queries on relations
    for obj in iterable_list:
        if obj.show_after_id is None:
            if current is not None:
                raise Exception('Multiple instances in iterable with show_after == None')
            current = obj
        elif obj.show_after_id in iterable_dict:
            next_item_map[obj.show_after_id] = obj
        else:
            # Walk back through chain_cache to find connection point
            prev = chain_cache.get(obj.show_after_id)
            while prev and prev.id not in iterable_dict:
                if prev.show_after_id is None:
                    if current is not None:
                        raise Exception('Multiple instances with show_after == None')
                    current = obj
                    break
                prev = chain_cache.get(prev.show_after_id)
            else:
                if prev and prev.id in iterable_dict:
                    next_item_map[prev.id] = obj
    
    # Traverse the linked list
    while current is not None:
        sorted_list.append(current)
        current = next_item_map.get(current.id)

    return sorted_list

def send_email(subject, body, to=('ryan@ryanmoscoe.com',), from_email=None, reply_to=None, content_subtype='plain'):
    kwargs = {
        'subject': subject,
        'body': body,
        'to': to
    }
    if from_email:
        kwargs['from_email'] = from_email
    if reply_to:
        kwargs['reply_to'] = reply_to
    email = EmailMessage(**kwargs)
    if content_subtype != 'plain':
        email.content_subtype = content_subtype
    success = email.send()
    return bool(success)