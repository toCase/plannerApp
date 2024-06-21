from datetime import date, datetime, timezone
from calendar import Calendar
from .models import CalendarModel, mMeet
from django.db.models import Q, F

def calendarMake(year :int, month :int, day :int, params :dict):
    cal_html = '<table border="0" cellpadding="0" cellspacing="0" class="month"><tr>'

    week_head = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    
    saloon = params.get("saloon")
    type = params.get("type")
    target = params.get("target")
    target_page = ""
    target_container = ""
    if target == "CALE":
        target_page = "appcale_date"
        target_container = "#cale-container"
    elif target == "SHED":
        target_page = "appshed_date"
        target_container = "#shed-container"
    
    
    for item in week_head:
        cal_html = cal_html + '<th class="mon">{}</th>'.format(item)
    cal_html = cal_html + '</tr>'

    today = date.today()
    
    cale = Calendar()
    weeks = cale.monthdatescalendar(year, month)
    
    if type == "BASIC":       
        
        # event color
        event_color = "#3B7DDD"
    
    # get events from CalemndarModel
        fDate = weeks[0][0]
        lDate = weeks[len(weeks) - 1][6]
        events = CalendarModel.objects.filter(Q(cl_saloon_id = saloon) & Q(cl_date__gte = fDate) &Q(cl_date__lte = lDate))
        event_list = []
        if len(events) > 0:
            for event in events:
                event_list.append(event.cl_date)
    
        for week in weeks:
            cal_html = cal_html + '<tr>'
            for d in week:
                class_list = ""         
                class_today = "today"
                class_selected = "selected"
                class_event = "event"
                            
                if d == today:
                    class_list = class_list + " " + class_today
                
                if d.day == day and d.month == month:
                    class_list = class_list + " " + class_selected
                
                if d in event_list:
                    class_list = class_list + " " + class_event
                
                cal_html = cal_html + '''<td class="{}" hx-post="/{}/{}/{}/{}" 
                                        hx-trigger="click" 
                                        hx-target="{}"
                                        hx-swap="outerHTML" style="--event-color: {}"><span>{}</span></td>'''.format(
                    class_list,
                    target_page,
                    d.day, 
                    d.month, 
                    d.year,
                    target_container,
                    event_color,                
                    d.day)
            cal_html = cal_html + '</tr>'
            
    elif type == "BASIC_SPEC":
        spec_id = params.get("spec")
        fDate = weeks[0][0]
        lDate = weeks[len(weeks) - 1][6]
        event_color = ""
        
        spec_ann = F("cl_spec__spec_color")
        event_filter = Q(cl_saloon_id = saloon) & Q(cl_spec_id = spec_id) & Q(cl_date__gte = fDate) & Q(cl_date__lte = lDate)
        events = CalendarModel.objects.annotate(spec_color=spec_ann).filter(event_filter)
        
        event_list = []
        if len(events) > 0:
            for event in events:
                event_list.append(event.cl_date)
                event_color = event.spec_color
        
        print(spec_id)
            
        for week in weeks:
            cal_html = cal_html + '<tr>'
            for d in week:
                class_list = ""         
                class_today = "today"
                class_selected = "selected"
                class_event = "event"
                            
                if d == today:
                    class_list = class_list + " " + class_today
                
                if d.day == day and d.month == month:
                    class_list = class_list + " " + class_selected
                
                if d in event_list:
                    class_list = class_list + " " + class_event
                
                cal_html = cal_html + '''<td class="{}" hx-post="/{}/{}/{}/{}" 
                                        hx-trigger="click" 
                                        hx-target="{}"
                                        hx-swap="outerHTML" style="--event-color: {};"><span>{}</span></td>'''.format(
                    class_list,
                    target_page,
                    d.day, 
                    d.month, 
                    d.year,
                    target_container,
                    event_color,             
                    d.day)
            cal_html = cal_html + '</tr>'                    
    cal_html = cal_html + '</table>'
    return cal_html


def htmlShedule(params: dict):
    dt = params.get('date')    
    spec = params.get('spec')
    saloon = params.get('saloon')
    
    model = CalendarModel.objects.annotate(sh_temp = F('cl_shed__st_template')).filter(Q(cl_saloon_id = saloon) & Q(cl_date = dt) &Q(cl_spec = spec))
    template = model[0].sh_temp
    
    # если не привязан template
    if template is None:
        return str()
    
    shedule = sheduleMake(template)
    
     # make dict of datetime with id = 0
    s_dict = {}
    for item in shedule:
        hour = int(item.split(":")[0])
        minute = int(item.split(":")[1])
        d = datetime(dt.year, dt.month, dt.day, hour, minute, 0, tzinfo=timezone.utc)
        
        s_dict[d] = {'id' : 0, "dt" : d}
    
    #get data from mMeet
    s_dt = datetime(dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=timezone.utc)
    f_dt = datetime(dt.year, dt.month, dt.day, 23, 59, 59, tzinfo=timezone.utc)
    meetings = mMeet.objects.annotate(
        clientPhone = F('m_client__phone'),
        ).filter(
            Q(m_dt__gte = s_dt) & Q(m_dt__lt = f_dt) & Q(m_spec = spec) & Q(m_saloon = saloon)
        )   
    
    
        
    for item in meetings:
        clr_status = ""
        if item.m_status == 10 or item.m_status == 20 or item.m_status == 30:
            clr_status = "#ffb641"
        elif item.m_status == 11 or item.m_status == 21 or item.m_status == 31:
            clr_status = "#6fa8dc"
        elif item.m_status == 12 or item.m_status == 22 or item.m_status == 32:
            clr_status = "#fa5456"
        elif item.m_status == 13 or item.m_status == 23 or item.m_status == 33:
            clr_status = "#b3d5a4"
            
        dict_item = {
            'id' : item.id,
            'dt' : item.m_dt,            
            'service' : item.m_service,
            'note' : item.m_note,
            'status' : item.m_status,
            'statusColor' : clr_status,
            'client': item.m_client,
            'clientPhone': item.clientPhone,
            'rating': item.m_rating,
            'report' : item.m_report,
            'review' : item.m_review,
            }
        s_dict[item.m_dt] = dict_item
        
    
    
    #sort data
    main_dict = dict(sorted(s_dict.items()))
    # print(main_dict)
    
    #---
    
    html = '<ul class="list-group mt-3 overflow-scroll" id="meet-list">'
    
    for meeting in main_dict.values():
        url_link = ""
        if meeting.get('id') > 0:
            url_link = "/appmeet_edit/{}/{}/{}/{}/{}/{}".format(
                dt.day,
                dt.month,
                dt.year,
                meeting.get('dt').hour,
                meeting.get('dt').minute,
                meeting.get('id')                
            )
        else:
            url_link = "/appmeet_add/{}/{}/{}/{}/{}/0".format(
                dt.day,
                dt.month,
                dt.year,
                meeting.get('dt').hour,
                meeting.get('dt').minute
            )        
        html = html + '''<li class="list-group-item"  
                    hx-post="{}" hx-trigger="click" 
                     hx-target="#shedule-container" hx-swap="outerHTML" style="cursor:pointer">'''.format(url_link)   
        
        if meeting.get('id') > 0:
            html = html + '<div class="row">'                           
            html = html + '<div class="col-1"><h5>{}</h5></div>'.format(meeting.get('dt').strftime('%H.%M'))
            html = html + '<div class="col-5 text-center fw-medium"><h5>{}</h5></div>'.format(meeting.get('client'))
            html = html + '<div class="col-5 text-center fw-medium"><h5>{}</h5></div>'.format(meeting.get('clientPhone'))
            html = html + '</div>'
            html = html + '<p class="text-start">{}</p>'.format(meeting.get('service'))
            html = html + '<p class="text-end fst-italic">{}</p>'.format(meeting.get('note'))
        else:
            html = html + '<div class="d-flex flex-row justify-content-between">'
            html = html + '<h5>{}</h5><span><i class="bi bi-plus"></i></span>'.format(meeting.get('dt').strftime('%H.%M'))
            html = html + '</div>'
        html = html + '</li>'
        
    html = html + "</ul>"
    return html
    
def get_shedule_free(params:dict):
    dt = params.get('date')    
    spec = params.get('spec')
    saloon = params.get('saloon')
    
    model = CalendarModel.objects.annotate(sh_temp = F('cl_shed__st_template')).filter(Q(cl_saloon_id = saloon) & Q(cl_date = dt) &Q(cl_spec = spec))
    template = model[0].sh_temp
    
    # если не привязан template
    if template is None:
        return str()
    
    shedule = sheduleMake(template)
    
    #get data from mMeet
    s_dt = datetime(dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=timezone.utc)
    f_dt = datetime(dt.year, dt.month, dt.day, 23, 59, 59, tzinfo=timezone.utc)
    meetings = mMeet.objects.filter(
            Q(m_dt__gte = s_dt) & Q(m_dt__lt = f_dt) & Q(m_spec = spec) & Q(m_saloon = saloon)
        ) 
    
    
    for item in meetings:
        if item.m_dt.strftime('%H:%M') in shedule:
            shedule.remove(item.m_dt.strftime('%H:%M'))
            
    return shedule  
    

def sheduleMake(template :str):
    shedule = []
    sessions = template.split("|")
    for session in sessions:
        if len(session) > 0:
            print(len(session.split(":")))
            if len(session.split(":")) == 3:
                s = int(session.split(":")[0])
                f = int(session.split(":")[1])
                d = int(session.split(":")[2]) * 60
                
                ds = int(datetime(year=date.today().year, 
                              month=date.today().month,
                              day=date.today().day,
                              hour=s, 
                              minute=0, 
                              second=0).timestamp())
                df = int(datetime(year=date.today().year, 
                              month=date.today().month,
                              day=date.today().day,
                              hour=f, 
                              minute=0, 
                              second=0).timestamp())
                for x in range(ds, df, d):
                    res = datetime.fromtimestamp(x)
                    shedule.append(res.strftime('%H:%M'))
    return shedule
            
    