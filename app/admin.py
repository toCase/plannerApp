from django.contrib import admin

from .models import Firm, Client, Service, SaloonModel, SpecModel, CalendarModel, mSheduleTemplate, mMeet, mProducts

admin.site.register(Firm)
admin.site.register(Client)
admin.site.register(SpecModel)
admin.site.register(CalendarModel)
admin.site.register(SaloonModel)
admin.site.register(Service)
admin.site.register(mSheduleTemplate)
admin.site.register(mMeet)
admin.site.register(mProducts)
