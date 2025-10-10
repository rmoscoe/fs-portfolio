from django.core.mail import EmailMessage

def sort_as_linked_list(iterable):
    sorted_list = []
    next_item_map = {}
    current = None
    
    # Convert to list and get model
    iterable_list = list(iterable)
    if not iterable_list:
        return sorted_list
    
    model = iterable_list[0]._meta.model
    iterable_dict = {obj.id: obj for obj in iterable_list}
    
    # Find all missing show_after IDs
    missing_ids = set()
    for obj in iterable_list:
        if obj.show_after_id is not None and obj.show_after_id not in iterable_dict:
            missing_ids.add(obj.show_after_id)
    
    # Fetch all missing objects at once and build a chain cache
    chain_cache = {}
    if missing_ids:
        missing_objs = model.objects.filter(pk__in=missing_ids)
        for obj in missing_objs:
            chain_cache[obj.id] = obj
        
        # Now walk back through chains to find where they connect
        for obj_id in list(missing_ids):
            current_obj = chain_cache.get(obj_id)
            while current_obj and current_obj.id not in iterable_dict:
                if current_obj.show_after_id and current_obj.show_after_id not in chain_cache:
                    # Need to fetch more ancestors
                    ancestor = model.objects.get(pk=current_obj.show_after_id)
                    chain_cache[ancestor.id] = ancestor
                    current_obj = ancestor
                elif current_obj.show_after_id:
                    current_obj = chain_cache[current_obj.show_after_id]
                else:
                    break
    
    # Build next_item_map
    for obj in iterable_list:
        if obj.show_after is None:
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