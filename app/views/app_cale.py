from datetime import date
import calendar

from django.shortcuts import render
from django.db.models import Q, Count

from ..base import make_notes, get_notes, del_notes
from ..forms import CalendarForm
from ..models import CalendarModel, SaloonModel, SpecModel
from ..utils import calendarMake

cale_month = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]

def get_spec_data(dt :date, sln_id :int):
    range = calendar.monthrange(dt.year, dt.month)
    fdate = date(dt.year, dt.month, 1)
    ldate = date(dt.year, dt.month, range[1])
    cale_ann = Count('calendarmodel', filter=Q(calendarmodel__cl_saloon_id=sln_id) & (Q(calendarmodel__cl_date__gte=fdate) & Q(calendarmodel__cl_date__lte=ldate)))
    spec_data = SpecModel.objects.annotate(cale=cale_ann).filter(cale__gt=0)
    return spec_data
    
def load(request):
    global cale_month
    
    _today = date.today() 
    sln_id = get_notes(request.user.id, ["SLN"]).get("SLN")
    
    sln = SaloonModel.objects.get(id=sln_id)
    
    
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_today))
    
    params = {'saloon': sln_id, 'type': 'BASIC', 'target': 'CALE'}    
    app_calendar = calendarMake(_today.year, _today.month, _today.day, params)
    
    spec_data = get_spec_data(_today, sln_id)
    
    make_notes(request.user.id, "CALE", "BASIC")
    
    context = {
        "title": "Загальний розклад" + " | " + sln.sln_name, 
        "page_name": "Загальний розклад", 
        "saloon": sln,
        "cmonth": cale_month[_today.month - 1] + " " + _today.strftime("%Y"),
        "cdate": _today.strftime("%d.%m.%Y"), 
        "day": str(_today.day),
        "month": str(_today.month),
        "year": str(_today.year),
        "calendar": app_calendar,
        "cale_data": cale_data,
        "page_css": "app_cale.css",
        "page_js":'app_calendar.js',
        "spec_data": spec_data,
    }
    # context.update(stateEngine("DASH"))
    return render(request, template_name="app_cale.html", context=context)

def next_month(request, month :str, year :str):
    global cale_month
    _month :int = int(month)
    _year :int = int(year)
    if _month < 12:
        _month += 1
    else:
        _month = 1
        _year = _year + 1
    
    _date = date.today().replace(day=1, month=_month, year=_year)
    sln_id = get_notes(request.user.id, ["SLN"]).get("SLN")
    
    params = {'saloon': sln_id, 'type': 'BASIC', 'target': 'CALE'}
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))
    
    spec_data = get_spec_data(_date, sln_id)
    make_notes(request.user.id, "CALE", "BASIC")
    
    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),         
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year),
        "calendar": app_calendar,
        "cale_data": cale_data,
        "spec_data": spec_data,
    }
    
    return render(request, template_name="app_calendar/app_cale_container.html", context=context)

def prev_month(request, month :str, year :str):
    global cale_month
    _month :int = int(month)
    _year :int = int(year)
    
    if _month > 1:
        _month -= 1
    else:
        _month = 12
        _year = _year - 1
    
    _date = date.today().replace(day=1,month=_month, year=_year)
    sln_id = get_notes(request.user.id, ["SLN"]).get("SLN")
    
    params = {'saloon': sln_id, 'type': 'BASIC', 'target': 'CALE'}
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))
    
    spec_data = get_spec_data(_date, sln_id)
    make_notes(request.user.id, "CALE", "BASIC")
    
    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year),
        "calendar": app_calendar,    
        "cale_data": cale_data,
        "spec_data": spec_data,
    }
    
    return render(request, template_name="app_calendar/app_cale_container.html", context=context)

def add(request, day :str, month :str, year :str):
    firm_id = get_notes(request.user.id, ["FRM"]).get("FRM")
    
    form = CalendarForm(firm=firm_id)
    context = {
        "form": form,
        "id": "0",
        "day": day,
        "month": month,
        "year": year,
    }    
    return render(request, template_name="app_calendar/app_cale_form.html", context=context)

def close(request):
    return render(request, template_name="app_calendar/app_cale_form.html", context={})

def edit(request, pk :str, day :str, month :str, year :str):
    id_cale = int(pk)
    firm_id = get_notes(request.user.id, ["FRM"]).get("FRM")
    model = CalendarModel.objects.get(id=id_cale)
    form = CalendarForm(firm=firm_id, instance=model)
    context = {
        "form": form,
        "id": pk,
        "day": day,
        "month": month,
        "year": year,
    }
    return render(request, template_name="app_calendar/app_cale_form.html", context=context)

def delete(request, pk :str, day :str, month :str, year :str):   
    global cale_month 
    id_cale = int(pk)
    _date = date(year=int(year), month=int(month), day=int(day))
    
    notes :dict = get_notes(request.user.id, ["SLN", "CALE", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    temp_cale = notes.get("CALE")
    spec_id = notes.get("CALE_SPEC")
    
    model = CalendarModel.objects.get(id=id_cale)
    model.delete()
    
    params = {'saloon': sln_id, 'type': temp_cale, 'target': 'CALE'}
    if temp_cale == "BASIC_SPEC":
        params['spec'] = spec_id
        
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))
    
    spec_data = get_spec_data(_date, sln_id)
    
    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year),
        "calendar": app_calendar,    
        "cale_data": cale_data,   
        "spec_data": spec_data,
    }
    
    return render(request, template_name="app_calendar/app_cale_container.html", context=context)

def save(request, pk :str, day :str, month :str, year :str):
    global cale_month
    id_cale = int(pk)
    notes :dict = get_notes(request.user.id, ["SLN", "FRM", "CALE", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    firm_id = notes.get("FRM")
    temp_cale = notes.get("CALE")
    spec_id = notes.get("CALE_SPEC")
    
    _date = date(year=int(year), month=int(month), day=int(day))
    
    if id_cale == 0:
        if request.method == "POST":
            form = CalendarForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.cl_date = _date
                data.cl_saloon_id = sln_id
                data.user_id = request.user.id
                data.save()        
    elif id_cale > 0:
        if request.method == "POST":
            model = CalendarModel.objects.get(id=id_cale)
            form = CalendarForm(request.POST, instance=model)
            if form.is_valid():
                data = form.save(commit=False)
                data.user_id = request.user.id
                data.save()  
    
    params = {'saloon': sln_id, 'type': temp_cale, 'target': 'CALE'}
    if temp_cale == "BASIC_SPEC":
        params['spec'] = spec_id
        
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))
    
    spec_data = get_spec_data(_date, sln_id)

    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year),
        "calendar": app_calendar,    
        "cale_data": cale_data,  
        "spec_data": spec_data,
    }
    
    return render(request, template_name="app_calendar/app_cale_container.html", context=context)

def select_date(request, day :str, month :str, year :str):    
    global cale_month
    notes :dict = get_notes(request.user.id, ["SLN", "CALE", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    temp_cale = notes.get("CALE")
    spec_id = notes.get("CALE_SPEC")
    print("TEMP CALE: ", spec_id)
    
    _date = date(year=int(year), month=int(month), day=int(day))
    
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))
    
    params = {'saloon': sln_id, 'type': temp_cale, 'target': 'CALE'}
    if temp_cale == "BASIC_SPEC":
        params['spec'] = spec_id
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)
    
    spec_data = get_spec_data(_date, sln_id)
    
    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year), 
        "calendar": app_calendar,  
        "cale_data": cale_data,  
        "spec_data": spec_data,
    } 
    
    return render(request, template_name="app_calendar/app_cale_container.html", context=context)

def select_spec(request, day :str, month :str, year :str, spec_id :str):
    global cale_month
    if spec_id == "0":
        temp_cale = "BASIC"
    else:
        temp_cale = "BASIC_SPEC"
    make_notes(request.user.id, "CALE_SPEC", spec_id)
    make_notes(request.user.id, "CALE", temp_cale)
    
    sln_id = get_notes(request.user.id, ["SLN"]).get("SLN")
    _date = date(year=int(year), month=int(month), day=int(day))
    
    params = {'saloon': sln_id, 'spec': spec_id, 'type': temp_cale, 'target': 'CALE'}    
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)    
    
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))    
    
    spec_data = get_spec_data(_date, sln_id)
    
    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year), 
        "cale_data": cale_data,
        "calendar": app_calendar,
        "spec_data": spec_data,
    } 
    
    return render(request, template_name="app_calendar/app_cale_container.html", context=context)