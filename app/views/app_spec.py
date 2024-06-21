import math
from django.db.models import Q, F, Count
from django.shortcuts import render

from ..base import make_notes, get_notes, del_notes, page_list, page_from, page_to, error_messages
from ..forms import SpecForm
from ..models import SpecModel

row_count :int = 20

def get_data(firm_id :int, query :str):    
    calendar_annotation = Count('calendarmodel')
    
    if query is not None:
        data = SpecModel.objects.annotate(call=calendar_annotation).filter(
            Q(firm=firm_id) & (Q(spec_fname__icontains=query) | Q(spec_lname__icontains=query) | Q(spec_phone__icontains=query))
        )
    else:
        data = SpecModel.objects.annotate(call=calendar_annotation).filter(firm=firm_id)
    
    return data
    
def load(request):
    global row_count    
    
    notes :dict = get_notes(request.user.id, ["FRM", "SPE_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SPE_SEARCH")
    data = get_data(firm_id, q)
    
    context = {
        "title": "Spec",
        "page_name": "Співробітники",
        "id":"0",
        "spec_data" : data[0:row_count],  
    }
    
    if q is not None:
        context['query'] = q       
    
    make_notes(request.user.id, "SPE_PAGE", "1")  
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'    
    return render(request, template_name="app_spec.html", context=context)

def filter(request):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "SPE_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SPE_SEARCH")
    
    # filter table 
    if request.method == "GET":
        if request.GET.get("search") != "":        
            q = request.GET.get("search")
            make_notes(request.user.id, "SPE_SEARCH", q)
            
        else:
            q = ""
            del_notes(request.user.id, "SPE_SEARCH")    
    
    data = get_data(firm_id, q)
    
    context = {
        "id":"0",
        "spec_data" : data[0:row_count],
        "query": q,
    }
    
    make_notes(request.user.id, "SPE_PAGE", "1")
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'     
        
    return render(request, template_name="app_spec/app_spec_container.html", context=context)

def add(request):
    form = SpecForm()
    context = {
        "form": form,
        "id": "0",
        "spec_data": "",
    }
    return render(request, template_name="app_spec/app_spec_container.html", context=context)

def edit(request, pk :str):
    id_spec = int(pk)
    model = SpecModel.objects.get(id=id_spec)
    form = SpecForm(instance=model)
    
    context = {
        "form": form,
        "id": pk,
        "spec_data": "",
    }   
    return render(request, template_name="app_spec/app_spec_container.html", context=context)

def close(request):    
    return render(request, template_name="app_spec/app_spec_form.html", context={})

def save(request, pk :str):
    global row_count
    id_spec = int(pk)
    notes :dict = get_notes(request.user.id, ["FRM"])
    firm_id = notes.get("FRM")
    
    form = SpecForm(request.POST)
    if id_spec > 0:
        model = SpecModel.objects.get(id=id_spec)
        form = SpecForm(request.POST, instance=model)
    if form.is_valid():
        data = form.save(commit=False)
        if id_spec == 0:
            data.firm_id = firm_id
        data.user_id = request.user.id
        data.save()
        return page(request, "1")
    else:
        errors = form.errors.get_json_data()
        messages = error_messages(errors)
        context = {
            "form": form,
            "id": pk,
            "spec_data": "",
            "errors": messages,
        }
        return render(request, template_name="app_spec/app_spec_container.html", context=context) 

def delete(request, pk :str):
    id_spec = int(pk) 
    model = SpecModel.objects.get(id=id_spec)
    model.delete()
    return page(request, "1")

def page(request, page :str):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "SPE_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SPE_SEARCH")
    
    make_notes(request.user.id, "spec_page", page)
    data = get_data(firm_id, q)
    
    context = {
        "id":"0",
        "query": q,
        "spec_data": data[page_from(int(page)) : page_to(int(page))],
    }
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
    return render(request, template_name="app_spec/app_spec_container.html", context=context)

