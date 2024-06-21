from django.db.models import Q, F, Count
from django.shortcuts import render

from ..base import make_notes, get_notes, del_notes, page_list, page_from, page_to, error_messages
from ..forms import AgentForm
from ..models import mAgent

row_count:int = 20

def get_data(firm_id:int, query:str = None):
    
    doc_annotation = Count('mdocument')
    
    if query is not None:
        data = mAgent.objects.annotate(docs=doc_annotation).filter(
            Q(firm=firm_id) & (Q(a_name__icontains=query) | Q(a_code__icontains=query) | Q(a_phone__icontains=query))
        )
    else:
        data = mAgent.objects.annotate(docs=doc_annotation).filter(firm=firm_id)
    return data

def load(request):
    global row_count
    
    notes:dict = get_notes(request.user.id, ["FRM", "AGT_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("AGT_SEARCH")
        
    data = get_data(firm_id, q)
    
    context = {
        'title': "Agent",
        'page_name': "Контрагенти",
        'agent_data' : data[0:row_count],
        'id':"0"
    }
    if q is not None:
        context['query'] = q
    
    make_notes(request.user.id, "AGT_PAGE", "1")
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_agent.html", context=context)

def filter(request):
    global row_count
    notes:dict = get_notes(request.user.id, ["FRM", "AGT_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("AGT_SEARCH")
    
    if request.method == "GET":
        if request.GET.get("search") != "":
            q = request.GET.get("search")
            make_notes(request.user.id, "AGT_SEARCH", q)
        else:
            q = ""
            del_notes(request.user.id, "AGT_SEARCH")
    
    context = {}
    data = get_data(firm_id, q)
    
    context = {
        'agent_data' : data[0:row_count],
        'id':"0"
    }
    
    make_notes(request.user.id, "AGT_PAGE", "1")
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_agent/app_agent_container.html", context=context)

def add(request):
    form = AgentForm()
    context = {
        "agent_data":"",
        "form": form,
        "id": "0",
    }
    return render(request, template_name="app_agent/app_agent_container.html", context=context)

def edit(request, pk :str):
    id_agent = int(pk)
    model = mAgent.objects.get(id=id_agent)
    form = AgentForm(instance=model)
    context = {
        "agent_data":"",
        "form": form,
        "id": pk,
    }
    return render(request, template_name="app_agent/app_agent_container.html", context=context)

def save(request, pk :str):
    id_agent = int(pk)
    notes:dict = get_notes(request.user.id, ["FRM"])
    firm_id = notes.get("FRM")
    
    form = AgentForm(request.POST)
    if id_agent > 0:
        model = mAgent.objects.get(id=id_agent)
        form = AgentForm(request.POST, instance=model)
    if form.is_valid():
        data = form.save(commit=False)
        if id_agent == 0:
            data.firm_id = firm_id
        data.user_id = request.user.id
        data.save()
        return page(request, "1")
    else:
        messages = error_messages(form.errors.get_json_data())
        context = {
            "form": form,
            "id": pk,
            "errors": messages,
            "agent_data": "",
        }
        # print(context)
        return render(request, template_name="app_agent/app_agent_container.html", context=context)

def delete(request, pk :str):
    id_agent = int(pk)
    model = mAgent.objects.get(id=id_agent)
    model.delete()
    return page(request, "1")

def page(request, page:str):
    global row_count
    notes:dict = get_notes(request.user.id, ["FRM", "AGT_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("AGT_SEARCH")
    
    make_notes(request.user.id, "AGT_PAGE", page)
    
    data = get_data(firm_id, q)
    
    context = {
        "id": "0",
        'agent_data' : data[page_from(int(page)):page_to(int(page))],
    }
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
    
    return render(request, template_name="app_agent/app_agent_container.html", context=context)
    