from django.db.models import Q, QuerySet, Count, F
from django.shortcuts import render
from ..base import make_notes, get_notes, del_notes, page_list, page_from, page_to

from ..forms import SaloonForm
from ..models import SaloonModel

row_count :int = 20

def get_data(firm_id :int, query :str):
    if (query is not None):
        data = SaloonModel.objects.filter(
            Q(firm=firm_id) & (Q(sln_name__icontains=query) | Q(sln_phone__icontains=query) | Q(sln_address__icontains=query) | Q(sln_note__icontains=query))
        )
    else:
        data = SaloonModel.objects.filter(firm=firm_id)
    return data

def load(request):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "SLN_SEARCH"])
    
    firm_id = notes.get("FRM")
    q = notes.get("SLN_SEARCH")
    
    context = {
        "title": "Saloon",
        "page_name": "Салони",
    }
    
    if q is not None:
        context['query'] = q
    
    data = get_data(firm_id, q)
    context['sln_data'] = data[0:row_count]
    make_notes(request.user.id, "SLN_PAGE", "1")
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_saloon.html", context=context)

def filter(request):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM"])
    firm_id = notes.get("FRM")
    
    if request.GET.get("search") != "":
        q = request.GET.get("search")
        make_notes(request.user.id, "SLN_SEARCH", q)
    else:
        q = ""
        del_notes(request.user.id, "SLN_SEARCH")
    
    context = {}
    data = get_data(firm_id, q)
    context['sln_data'] = data[0:row_count]
    make_notes(request.user.id, "SLN_PAGE", "1")
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_sln/app_sln_container.html", context=context)

def add(request):
    form = SaloonForm()
    context = {
        "form": form,
        "id": "0",
    }
    return render(request, template_name="app_sln/app_sln_form.html", context=context)

def edit(request, pk):
    id_saloon = int(pk)
    model = SaloonModel.objects.get(id=id_saloon)
    form = SaloonForm(instance=model)
    context = {
        "form": form,
        "id": pk,
    }
    return render(request, template_name="app_sln/app_sln_form.html", context=context)

def active(request, pk :str):
    global row_count
    id_saloon = int(pk)
    
    notes :dict = get_notes(request.user.id, ["FRM", "SLN_SEARCH", "SLN_PAGE"])
    firm_id = notes.get("FRM")
    q = notes.get("SLN_SEARCH")
    page = notes.get("SLN_PAGE")
    
    try:
        model_x = SaloonModel.objects.get(Q(sln_main=1) & Q(firm_id=firm_id))
        model_x.sln_main = 0
        model_x.user_id = request.user.id
        model_x.save()
    except:
        print("NO ACTIVE SALOON")
    
    model = SaloonModel.objects.get(id=id_saloon)
    model.sln_main = 1
    model.user_id = request.user.id
    model.save()
    
    make_notes(request.user.id, "SLN", pk)
    
    context = {}
    data = get_data(firm_id, q)
    context['sln_data'] = data[page_from(int(page)):page_to(int(page))]
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
        
    return render(request, template_name="app_sln/app_sln_container.html", context=context)
    
    

def close(request):
    return render(request, template_name="app_sln/app_sln_form.html")

def save(request, pk :str):
    global row_count
    id_saloon = int(pk)
    notes :dict = get_notes(request.user.id, ["FRM", "SLN_SEARCH", "SLN_PAGE"])
    firm_id = notes.get("FRM")
    q = notes.get("SLN_SEARCH")
    page = notes.get("SLN_PAGE")
    
    if id_saloon == 0:
        form = SaloonForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.firm_id =firm_id
            data.user_id = request.user.id
            data.save()
    elif id_saloon > 0:
        model = SaloonModel.objects.get(id=id_saloon)
        _active = model.sln_main
        form = SaloonForm(request.POST, instance=model)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_id = request.user.id
            data.sln_main = _active
            data.save()
    context = {}
    data = get_data(firm_id, q)
    context['sln_data'] = data[page_from(int(page)):page_to(int(page))]
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
        
    return render(request, template_name="app_sln/app_sln_container.html", context=context)
    
def delete(request, pk :str):
    global row_count
    id_saloon = int(pk)
    
    notes :dict = get_notes(request.user.id, ["FRM", "SLN_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SLN_SEARCH")
    
    model = SaloonModel.objects.get(id=id_saloon)
    model.delete()
    
    context = {}
    data = get_data(firm_id, q)
    context['sln_data'] = data[0:row_count]
    make_notes(request.user.id, "SLN_PAGE", "1")
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_sln/app_sln_container.html", context=context)

def page(request, page :str):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "SLN_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SLN_SEARCH")
    make_notes(request.user.id, "SLN_PAGE", page)
    context = {}
    data = get_data(firm_id, q)
    context['sln_data'] = data[page_from(int(page)):page_to(int(page))]
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
    return render(request, template_name="app_sln/app_sln_container.html", context=context)

