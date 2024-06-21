from datetime import date, datetime, timezone
import calendar

from django.shortcuts import render, HttpResponse
from django.db.models import Q, F

from ..base import make_notes, get_notes, del_notes
from ..forms import MeetForm
from ..models import CalendarModel, SaloonModel, SpecModel, mMeet, Client, Service
from ..utils import calendarMake, htmlShedule, get_shedule_free

cale_month = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]

def get_spec_data(dt :date, sln_id :int):    
    spec_data = CalendarModel.objects.annotate(spec_fname = F("cl_spec__spec_fname"), spec_lname = F("cl_spec__spec_lname"), spec_color = F("cl_spec__spec_color")).filter(Q(cl_date=dt) & Q(cl_saloon_id=sln_id))
    return spec_data
    
def load(request):
    global cale_month
    
    _today = date.today() 
    sln_id = get_notes(request.user.id, ["SLN"]).get("SLN")
    
    sln = SaloonModel.objects.get(id=sln_id)
    
    
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_today))
    
    params = {'saloon': sln_id, 'type': 'BASIC', 'target': 'SHED'}
    app_calendar = calendarMake(_today.year, _today.month, _today.day, params)
    
    spec_data = get_spec_data(_today, sln_id)
    
    make_notes(request.user.id, "CALE", "BASIC")
    
    context = {
        "title": "Графік зустрічей" + " | " + sln.sln_name, 
        "page_name": "Графік зустрічей", 
        "saloon": sln,
        "cmonth": cale_month[_today.month - 1] + " " + _today.strftime("%Y"),
        "cdate": _today.strftime("%d.%m.%Y"), 
        "day": str(_today.day),
        "month": str(_today.month),
        "year": str(_today.year),
        "calendar": app_calendar,
        "cale_data": cale_data,
        "page_css": "app_cale.css",
        "spec_data": spec_data,
        "shedule_tab": 1,
        "meet_form":0,
        "meet" : 0,
    }
    # context.update(stateEngine("DASH"))
    return render(request, template_name="app_shed.html", context=context)

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
    
    params = {'saloon': sln_id, 'type': 'BASIC', 'target': 'SHED'}
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
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    }
    
    return render(request, template_name="app_shed/app_shed_container.html", context=context)

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
    params = {'saloon': sln_id, 'type': 'BASIC', 'target': 'SHED'}
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
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    }
    
    return render(request, template_name="app_shed/app_shed_container.html", context=context)

def add(request, day :str, month :str, year :str):
    pass

def close(request, day :str, month :str, year :str):
    notes :dict = get_notes(request.user.id, ["SLN", "CALE", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    spec_id = notes.get("CALE_SPEC")
    
    _date = date(year=int(year), month=int(month), day=int(day))    
    spec_data = get_spec_data(_date, sln_id)
    
    sh_params = {'date': _date, 'spec': spec_id, 'saloon': sln_id}
    app_shedule = htmlShedule(sh_params)
    
    context = {
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year),
        "spec_data": spec_data,
        "shedule_tab": True,
        "shedule":app_shedule,
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    } 
    
    return render(request, template_name="app_shed/app_shed_tab.html", context=context)

def select_date(request, day :str, month :str, year :str):    
    global cale_month
    notes :dict = get_notes(request.user.id, ["SLN", "CALE", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    temp_cale = notes.get("CALE")
    spec_id = notes.get("CALE_SPEC")
    
    _date = date(year=int(year), month=int(month), day=int(day))
    
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))
    
    params = {'saloon': sln_id, 'type': temp_cale, 'target': 'SHED'}
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
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    } 
    
    return render(request, template_name="app_shed/app_shed_container.html", context=context)

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
    
    params = {'saloon': sln_id, 'type': temp_cale, 'target': 'SHED', 'spec': spec_id}  
    app_calendar = calendarMake(_date.year, _date.month, _date.day, params)    
    
    cale_data = CalendarModel.objects.filter(Q(cl_saloon_id=sln_id) & Q(cl_date=_date))    
    
    spec_data = get_spec_data(_date, sln_id)
    app_shedule = ""
    
    if spec_id is not "0":        
        # html shedule
        sh_params = {'date': _date, 'spec': spec_id, 'saloon': sln_id}
        app_shedule = htmlShedule(sh_params)
    
    context = {
        "cmonth": cale_month[_date.month - 1] + " " + _date.strftime("%Y"),
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year), 
        "cale_data": cale_data,
        "calendar": app_calendar,
        "selected_spec": int(spec_id),
        "spec_data": spec_data,
        "shedule": app_shedule,
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    } 
    
    return render(request, template_name="app_shed/app_shed_container.html", context=context)

def meet_add(request, day :str, month :str, year :str, hour :str, minute :str, meet_id :str): 
    dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
    
    firm_id = get_notes(request.user.id, ["FRM"]).get("FRM")
    service_data = Service.objects.filter(Q(firm_id=firm_id))
    
    context = {
        "form_date": dt.strftime("%d.%m.%Y"),
        "form_time": dt.strftime("%H:%M"),
        "id" : meet_id,
        "day": day,
        "month": month,
        "year": year,
        "hour": hour,
        "minute": minute,
        'services' : service_data,
        'meet' : meet_id,
        "shedule_tab": 0,
        "meet_form" : 1,
    }
    
    return render(request, template_name="app_shed/app_shed_tab.html", context=context)
        
    
def meet_edit(request, day :str, month :str, year :str, hour :str, minute :str, meet_id :str):
    
    # dt :date = date(year=int(year), month=int(month), day=int(day))
    
    firm_id = get_notes(request.user.id, ["FRM"]).get("FRM")
    service_data = Service.objects.filter(Q(firm_id=firm_id))
    
    ann_phone = ('m_client__phone')
    
    model = mMeet.objects.get(id=int(meet_id))
    print(model.m_client.phone)
    dt = model.m_dt
    
    context = {
        "form_date": dt.strftime("%d.%m.%Y"),
        "form_time": dt.strftime("%H:%M"),
        "id" : meet_id,
        "day": day,
        "month": month,
        "year": year,
        "hour": hour,
        "minute": minute,
        'services' : service_data,
        'card':model,
        'meet' : meet_id,
        "shedule_tab": 0,
        "meet_form" : 1,
    }
    
    return render(request, template_name="app_shed/app_shed_tab.html", context=context)

def meet_save(request, day :str, month :str, year :str, meet_id :str): 
    # global cale_month
    notes :dict = get_notes(request.user.id, ["FRM", "SLN", "CALE_SPEC"])
    firm_id = notes.get("FRM")
    sln_id = notes.get("SLN")
    spec_id = notes.get("CALE_SPEC")
    
    _date = date(int(year), int(month), int(day))  
    
    
    
    if request.method == "POST":
        time = request.POST.get('dt_time')
        hour = int(str(time).split(":")[0])
        minute = int(str(time).split(":")[1])
        
        dt = datetime(year=int(year), month=int(month), day=int(day), hour=hour, minute=minute, second=0, tzinfo=timezone.utc)
        sln_id = int(get_notes(request.user.id, ["SLN"]).get("SLN"))
        
        #client
        phone = request.POST.get('m-phone')
        client_name = str(request.POST.get('m-client'))
        
        if len(client_name.split(" ")) == 1:
            f = (Q(f_name=client_name) | Q(l_name=client_name))
        elif len(client_name.split(" ")) == 2:
            f = ((Q(f_name=client_name.split(" ")[0]) | Q(l_name=client_name.split(" ")[0])) & (Q(f_name=client_name.split(" ")[1]) | Q(l_name=client_name.split(" ")[1])))
        
        try:
            client = Client.objects.get(Q(phone=phone) & Q(firm_id=firm_id) & f) 
            client_id = client.id
        except:                
            if len(client_name.split(" ")) == 1:
                client_fname = client_name
                client_lname = ""
            elif len(client_name.split(" ")) == 2:
                client_fname = client_name.split(" ")[0]
                client_lname = client_name.split(" ")[1]
            
            client = Client(
                f_name = client_fname,
                l_name = client_lname,
                phone = phone,
                user_id = request.user.id,
                firm_id = firm_id
            )
            client.save()
            client_id = client.id
        
        if meet_id == "0":
            meet = mMeet(
                m_dt = dt,
                m_saloon_id = sln_id,
                m_spec_id = spec_id,
                m_service = request.POST.get('m-service'),
                m_client_id = client_id,
                user_id = request.user.id,
            )
            meet.save()
        else:
            m = mMeet.objects.get(id=int(meet_id))
            m.m_dt = dt
            m.m_service = request.POST.get('m-service')
            m.m_client_id = client_id
            m.user_id = request.user.id
            m.save()
        
    sh_params = {'date': dt, 'spec': spec_id, 'saloon': sln_id}
    app_shedule = htmlShedule(sh_params)
        
    
    context = {
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year), 
        "shedule": app_shedule,
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    } 
    return render(request, template_name="app_shed/app_shed_tab.html", context=context)
            
def meet_del(request, day :str, month :str, year :str, meet_id :str):
    
    _date = date(int(year), int(month), int(day))
    
    notes :dict = get_notes(request.user.id, ["SLN", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    spec_id = notes.get("CALE_SPEC")
    
    m = mMeet.objects.get(id=int(meet_id))
    m.delete()
    
    sh_params = {'date': _date, 'spec': spec_id, 'saloon': sln_id}
    app_shedule = htmlShedule(sh_params)   
    
    
    context = {
        "cdate": _date.strftime("%d.%m.%Y"),
        "day": str(_date.day),
        "month": str(_date.month),
        "year": str(_date.year), 
        "shedule": app_shedule,
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    } 
    return render(request, template_name="app_shed/app_shed_tab.html", context=context)

def meet_receipt(request, day :str, month :str, year :str, meet_id :str):
    
    return render(request, template_name="app_shed/app_meet_receipt.html")

def meet_postpone(request, day :str, month :str, year :str, meet_id :str):
    
    notes :dict = get_notes(request.user.id, ["SLN"])
    sln_id = notes.get("SLN")
    
    _date = date(year=int(year), month=int(month), day=int(day))
    spec_data = get_spec_data(_date, sln_id)
    
    context = {
        "form_date": _date.strftime("%Y-%m-%d"),
        # "form_time": _date.strftime("%H:%M"),
        "day": day,
        "month": month,
        "year": year,
        "meet": meet_id,
        "spec": spec_data,
        "spec_time": []     
    }
        
    return render(request, template_name="app_shed/app_shed_postpone.html", context=context)

def postpone_close(request, day :str, month :str, year :str):
    notes :dict = get_notes(request.user.id, ["CALE_SPEC"])
    spec_id = notes.get("CALE_SPEC")    
    return select_spec(request, day, month, year, spec_id)

def postpone_spec(request):
    notes :dict = get_notes(request.user.id, ["SLN"])
    if request.GET.get("pp-date") != "":
        _date = datetime.strptime(request.GET.get("pp-date"), "%Y-%m-%d").date()
    
    sln_id = notes.get("SLN")
    spec_data = get_spec_data(_date, sln_id)
    
    context = {
        "spec": spec_data,
        "spec_time": []
    }
    return render(request, template_name="app_shed/app_postpone_spec.html", context=context)

def postpone_time(request):
    notes :dict = get_notes(request.user.id, ["SLN"])
    sln_id = notes.get("SLN")
    if request.method == "POST":
        _date = datetime.strptime(request.POST.get("pp-date"), "%Y-%m-%d").date()
        spec_id = request.POST.get("pp-spec")
        
    params = {'date': _date, 'spec': spec_id, 'saloon': sln_id}
    spec_time = get_shedule_free(params)
    print(spec_time)
    context = {
        "spec_time": spec_time
    }    
    return render(request, template_name="app_shed/app_postpone_time.html", context=context)

def postpone_save(request, day :str, month :str, year :str, meet_id:str):
    
    notes :dict = get_notes(request.user.id, ["SLN", "CALE_SPEC"])
    sln_id = notes.get("SLN")
    spec_id = notes.get("CALE_SPEC")
    
    cdate = date(year=int(year), month=int(month), day=int(day))
    
    if request.method == "POST":
        str_dt = request.POST.get("pp-date") + " " + request.POST.get("pp-time") + ":00"
        _date = datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
        # _date.tzinfo = timezone.utc
               
        spec = request.POST.get("pp-spec")
        
        m = mMeet.objects.get(id=int(meet_id))
        m.m_dt = _date
        m.m_spec_id = int(spec)
        m.user_id = request.user.id
        m.save()
        
    sh_params = {'date': cdate, 'spec': spec_id, 'saloon': sln_id}
    app_shedule = htmlShedule(sh_params)
            
    context = {
        "cdate": cdate.strftime("%d.%m.%Y"),
        "day": day,
        "month": month,
        "year": year, 
        "shedule": app_shedule,
        "shedule_tab": 1,
        "meet_form" : 0,
        "meet" : 0,
    } 
    return render(request, template_name="app_shed/app_shed_tab.html", context=context)