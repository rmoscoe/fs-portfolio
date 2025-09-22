from django.core.mail import EmailMessage

def sort_as_linked_list(iterable):
    sorted_list = []
    next_item_map = {}
    current = None
    for obj in iterable:
        if obj.show_after is None:
            current = obj
        else:
            next_item_map[obj.show_after.id] = obj
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