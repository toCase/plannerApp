from math import ceil
from django.db.models import Q, QuerySet, Count, F
from django.shortcuts import render
from ..base import make_notes, get_notes, del_notes, page_from, page_to, page_list, error_messages
from ..forms import ClientForm
from ..models import Client

row_count :int = 20

def get_data(firm_id :int, query :str):
    if (query is not None):
        data = Client.objects.filter(
            Q(firm=firm_id) & (Q(phone__icontains=query) | Q(f_name__icontains=query) | Q(l_name__icontains=query))
        )
    else:
        data = Client.objects.filter(firm=firm_id)
    return data
    
def load(request):
    global row_count    
    notes :dict = get_notes(request.user.id, ["FRM", "CLI_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("CLI_SEARCH")
    
    data = get_data(firm_id, q)
    make_notes(request.user.id, "CLI_PAGE", "1")
    
    context = {
        "title": "Clients",
        "page_name": "Клієнти",
        "id": "0",
        "client_data": data[0:row_count],
        "query": q,
    }    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'    
    return render(request, template_name="app_clients.html", context=context)
    
def filter(request):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "CLI_SEARCH"])
    firm_id = notes.get("FRM")  
    q = notes.get("CLI_SEARCH")
    if request.method == "GET":
        if request.GET.get("search") != "":
            q = request.GET.get("search")
            make_notes(request.user.id, "CLI_SEARCH", q)
        else:
            q = ""
            del_notes(request.user.id, "CLI_SEARCH")    
    
    data = get_data(firm_id, q)
    
    context = {
        "id":"0",
        "client_data": data[0:row_count],
        "query":q,
    }
    
    # make_notes(request.user.id, "CLI_PAGE", "1")
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_client/app_client_container.html", context=context)  

def add(request):
    form = ClientForm()
    context = {
        'form' : form,
        'id' : '0',
        "client_data": "",
    }
    return render(request, template_name="app_client/app_client_container.html", context=context)

def edit(request, pk :str):
    id_client = int(pk)
    model = Client.objects.get(id=id_client)
    form = ClientForm(instance=model)
    context = {
        'form' : form,
        'id' : pk,
        "client_data": "",
    }
    return render(request, template_name="app_client/app_client_container.html", context=context)   


def save(request, pk :str):
    global row_count
    id_client = int(pk)    
    notes :dict = get_notes(request.user.id, ["FRM", "CLI_SEARCH", "CLI_PAGE"])
    firm_id = notes.get("FRM")
    q = notes.get("CLI_SEARCH")
    page = notes.get("CLI_PAGE")
    
    form = ClientForm(request.POST)
    if id_client > 0:
        model = Client.objects.get(id=id_client)
        form = ClientForm(request.POST, instance=model)
        
    if form.is_valid():
        data = form.save(commit=False)
        if id_client == 0:
            data.firm_id = firm_id
        data.user_id = request.user.id
        data.save()
        return page(request, "1")
    else:
        errors = error_messages(form.errors.get_json_data())
        context = {
            "id" : pk,
            "form": form,
            "client_data": "",
            "errors": errors
        }
        return render(request, template_name="app_client/app_client_container.html", context=context)
    
def delete(request, pk :str):
    id_client = int(pk) 
    model = Client.objects.get(id=id_client)
    model.delete()
    return page(request, "1")

def page(request, page:str):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "CLI_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("CLI_SEARCH")
    
    make_notes(request.user.id, "CLI_PAGE", page)
    data = get_data(firm_id, q)
    
    context = {
        "id": "0",
        "client_data" : data[page_from(int(page)):page_to(int(page))],
        "query": q,
    }
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
    return render(request, template_name="app_client/app_client_container.html", context=context)
