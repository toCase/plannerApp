from math import ceil
import json
from  .models import mNotes
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

row_count :int = 20

def write_data(data: dict):
    with open('data_engine.json', 'w') as f:
        json.dump(data, f)

def read_data():
    with open('data_engine.json') as f:
        templates = json.load(f)
        return templates
  
def make_notes(user :int, key :str, value :str):
    try:
        note = mNotes.objects.get(Q(user_id=user) & Q(n_query=key))
        note.n_value=value
        note.save()
    except ObjectDoesNotExist:
        note = mNotes()
        note.user_id = user
        note.n_query = key
        note.n_value = value
        note.save(force_insert=True)

def get_notes(user :int, keys :list):
    values = {}
    fA = Q(user_id=user)
    for i in range(len(keys)):
        if i == 0:
            fB = Q(n_query=keys[i])
        else :
            fB = fB | Q(n_query=keys[i])
            
    notes = mNotes.objects.filter(fA & (fB))
    for note in notes:
        values[note.n_query] = note.n_value
     
    return values

def del_notes(user :int, key :str):
    try:
        note = mNotes.objects.get(Q(user_id=user) & Q(n_query=key))
        note.delete()
    except ObjectDoesNotExist:
        pass
    
def page_list(_size :int):
    global row_count
    _pages :int = ceil(_size / row_count)
    _res = []
    for i in range(1, _pages + 1):
        _res.append(str(i))
    return _res

def page_from(_page :int):
    global row_count
    _from :int = (_page - 1) * row_count
    return _from

def page_to(_page :int):
    global row_count
    _to :int = (_page - 1) * row_count + row_count
    return _to

def error_messages(errors:dict):
    messages = []
    for key in errors.keys():            
        l = errors.get(key)
        for x in l:
            messages.append(x.get("message"))
    return messages