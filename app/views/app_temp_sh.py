
from datetime import date
from django.db.models import Q, F, Count
from django.shortcuts import render, redirect

from ..base import get_notes
from ..forms import ShedTempForm
from ..models import mSheduleTemplate

from ..utils import sheduleMake

def load(request):
    firm_id = get_notes(request.user.id, ["FRM"]).get("FRM")    
    
    cale_ann = Count('calendarmodel', filter=Q(calendarmodel__cl_date__gte=date.today()))
    
    if request.GET.get("q") != None:
        q = request.GET.get("q")
        model = mSheduleTemplate.objects.annotate(call=cale_ann).filter(Q(firm=firm_id) & (Q(st_name__icontains=q) | Q(st_note__icontains=q)))
    else:
        model = mSheduleTemplate.objects.annotate(call=cale_ann).filter(firm=firm_id)
        q = ""
    # dt = date.today()
    # # cm = CalendarModel.objects.filter(cl_date__gte=dt)
    
    # call = Count('calendarmodel', filter=Q(calendarmodel__cl_date__gte=dt))
    # mx = mSheduleTemplate.objects.annotate(call=call).filter(firm=firm_id)
    # for i in mx:
    #     print(i.call)
        
    
    if request.GET.get("D") != None:
        idDel = int(request.GET.get("D"))
        item = mSheduleTemplate.objects.get(id=idDel)
        item.delete()
        return redirect("app_sh_template")
    
    context = {
        "data" : model,
        "query" : q,
        "page_name" : "Шаблони робочих розкладів",
        "title": "ST",
    }
    return render(request, template_name="app_sh_temp.html", context=context)

def add(request):
    pk = "0"
    return generator(request, pk)

def update(request, pk :str):
    return generator(request, pk)
    
    
def generator(request, pk :str):
    
    firm_id = get_notes(request.user.id, ["FRM"]).get("FRM")
    key = int(pk)
    q = ""
    sh_temp = []
    if request.GET.get("q") != None:
        q = request.GET.get("q")
        sh_temp = sheduleMake(q)
        
    if key == 0:
        form = ShedTempForm()        
        if request.method == "POST":
            form = ShedTempForm(request.POST)
            data = form.save(commit=False)
            data.firm_id = firm_id
            data.user_id = request.user.id
            data.save()
            return redirect("app_sh_template")
    elif key > 0:
        model = mSheduleTemplate.objects.get(id=key)
        form = ShedTempForm(instance=model)
        if request.method == "POST":
            form = ShedTempForm(request.POST, instance=model)
            if form.is_valid():
                data = form.save(commit=False)
                data.firm_id = firm_id
                data.user_id = request.user.id
                data.save()
                return redirect("app_sh_template")
    context = {
        "form" : form,
        "page_name" : "Шаблони робочих розкладів",
        "title": "ST",
        "page_css": "ap_sh_temp_form.css",
        "page_js" : "ap_sh_temp_form.js",
        "query" : q,
        "sh_temp" : sh_temp,
    }
    
    if key > 0:
        context.update({"update": str(key)})
    
    return render(request, template_name="app_sh_temp_form.html", context=context)