from django.db.models import Q, QuerySet, Count, F
from django.shortcuts import render
from ..base import make_notes, get_notes, del_notes, page_list, page_from, page_to, error_messages
from ..forms import ServiceForm
from ..models import Service

row_count :int = 20

def get_data(firm_id :int, query :str):
    if (query is not None):
        data = Service.objects.filter(
            Q(firm=firm_id) & (Q(name__icontains=query) | Q(price__icontains=query))
        )
    else:
        data = Service.objects.filter(firm=firm_id)
    return data

def load(request):
    global row_count
    
    notes :dict = get_notes(request.user.id, ["FRM", "SER_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SER_SEARCH")
    
    context = {
        "title": "Service",
        "page_name": "Послуги",
        "id":"0"
    }
    
    if q is not None:
        context['query'] = q
    
    data = get_data(firm_id, q)
    
    context['service_data'] = data[0:row_count]
    make_notes(request.user.id, "SER_PAGE", "1")
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'    
    return render(request, template_name="app_service.html", context=context)

def filter(request):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM"])
    firm_id = notes.get("FRM")
    
    if request.GET.get("search") != "":        
        q = request.GET.get("search")
        make_notes(request.user.id, "SER_SEARCH", q)
    else:
        q = ""
        del_notes(request.user.id, "SER_SEARCH")
    
    data = get_data(firm_id, q)
    context = {
        "id":"0",
        "service_data":data[0:row_count],
    }
    
    make_notes(request.user.id, "SER_PAGE", "1")    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_service/app_service_container.html", context=context)

def add(request):
    form = ServiceForm()
    context = {
        "form": form,
        "id": "0",
        "service_data": "",
    }
    return render(request, template_name="app_service/app_service_container.html", context=context)

def edit(request, pk :str):
    id_service = int(pk)
    
    model = Service.objects.get(id=id_service)
    form = ServiceForm(instance=model)
    context = {
        "form": form,
        "id": pk,
        "service_data": "",
    }
    return render(request, template_name="app_service/app_service_container.html", context=context)
    
def save(request, pk :str):
    global row_count
    id_service = int(pk)
    notes :dict = get_notes(request.user.id, ["FRM"])
    firm_id = notes.get("FRM")
    
    form = ServiceForm(request.POST)
    if id_service > 0:
        model = Service.objects.get(id=id_service)
        form = ServiceForm(request.POST, instance=model)
    
    if form.is_valid():
        data = form.save(commit=False)
        if id_service == 0:
            data.firm_id = firm_id
        data.user_id = request.user.id
        data.save()
        return page(request, "1")
    else:
        errors = error_messages(form.errors.get_json_data())
        context = {
            "form": form,
            "id": pk,
            "errors": errors,
            "service_data": "",
        }
        return render(request, template_name="app_service/app_service_container.html", context=context)
            

def delete(request, pk :str):
    id_service = int(pk) 
    model = Service.objects.get(id=id_service)
    model.delete()
    return page(request, "1")

def page(request, page :str):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "SER_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("SER_SEARCH")
    
    make_notes(request.user.id, "SER_PAGE", page)
    
    data = get_data(firm_id, q)
    context = {
        "id":"0",
        "query":q,
        "service_data":data[page_from(int(page)):page_to(int(page))],
    }
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
    return render(request, template_name="app_service/app_service_container.html", context=context)