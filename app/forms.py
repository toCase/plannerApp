from django.forms import ModelForm, TextInput, NumberInput, Textarea, CheckboxInput, DateInput, ModelChoiceField, Select, DateTimeInput, EmailInput
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from .models import Client, Service, SpecModel, SaloonModel, CalendarModel, mSheduleTemplate, mMeet, mAgent, mProducts
# from .base import get_notes

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['firm', 'user']
        labels = {
            "f_name": "First Name",
            "l_name": "Last Name",
            "phone": "Phone",
            "email": "Email",
            "telegram": "Telegram",
        }
        widgets = {
            "f_name": TextInput(attrs={
                'id':'f_name',
                'class':'form-control',
                'title': "Ім'я",
                'placeholder':'Тарас',
            }),
            "l_name": TextInput(attrs={
                'id':'l_name',
                'class':'form-control',
                'title':'Фамілія',
                'placeholder':'Шевченко',
            }),
            "phone": TextInput(attrs={
                'id':'phone',
                'class':'form-control',
                'title':'Номер телефону',
                'placeholder':'0956662233',
            }),
            "email": EmailInput(attrs={
                'id':'email',
                'class':'form-control',
                'title':'Email',
            }),
            "telegram": TextInput(attrs={
                'id':'telegram',
                'class':'form-control disabled',
                'title':'Telegram',
            }),
        }
        error_messages = {
            'email':{
                'invalid': 'Невірна адреса електронної пошти',
            }            
        }
    
    def __init__(self, *args, **kwargs):       
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['telegram'].disabled = True

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['firm', 'user']
        labels = {
            "name":"Назва послуги",
            "price": "Ціна",
        }
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'id': 'service-name',
                'title': "Назва послуги",
                'placeholder': 'Назва послуги',
            }),
            "price": NumberInput(attrs={
                'class':'form-control',
                'id':'service-price',
                'title': "Ціна",
                'placeholder': "0.00",
                'step' : "0.1",
                'default' : "0.00"
            })
        }
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required': 'Назва не має бути пустою'}
        self.fields['price'].error_messages = {'required': 'Ціна має бути більше 0'}  

class SpecForm(ModelForm):
    class Meta:
        model = SpecModel
        fields = '__all__'
        exclude = ['firm', 'user']
        labels = {
            'spec_fname':"Name",
            'spec_lname':"Fam",
            'spec_phone':"Phone",
            'spec_color':"Color",
            'spec_active':"Active"
        }
        widgets = {
            "spec_fname" : TextInput(attrs={
                'class':'form-control form-control-sm',
                'id': 'spec-fname',
                'placeholder':'First Name'
            }),
            "spec_lname" : TextInput(attrs={
                'class':'form-control form-control-sm',
                'id':'spec-lname',
                'placeholder':'Last name',
            }),
            "spec_phone":TextInput(attrs={
                'class': 'form-control form-control-sm',
                'id':'spec-phone',
                'title': 'Номер телефону',
                'placeholder': '0956662233',
            }),
            "spec_color": TextInput(attrs={
                'class': 'form-control form-control-sm form-control-color',
                'id':'spec-color',
                'type': "color",
                'value': "#FFFFFF",
                'style': "min-height: 30px; max-height: 30px;",
            }),
            "spec_active": CheckboxInput(attrs={
                'class':'form-check-input',
                'id':'spec-active',
            }),
            
        }
    def __init__(self, *args, **kwargs):
        super(SpecForm, self).__init__(*args, **kwargs)
        self.fields['spec_fname'].error_messages = {'required': 'Ім\'я не має бути пустим'}
        self.fields['spec_lname'].error_messages = {'required': 'Прізвище не має бути пустим'}

class SaloonForm(ModelForm):
    class Meta:
        model = SaloonModel
        fields = '__all__'
        exclude = ['firm', 'user']
        labels = {
            'sln_name': "Name",
            'sln_address': "Address",
            'sln_phone': "Phone",
            'sln_note':"Note",
            'sln_color':"Color",
        }
        widgets = {
            "sln_name": TextInput(attrs={
                'class': 'form-control',
                'id': 'sln-name',
            }),
            "sln_address": TextInput(attrs={
                'class': 'form-control',
                'id': 'sln-address',
            }),
            "sln_phone": TextInput(attrs={
                'class': 'form-control',
                'id': 'sln-phone',
            }),
            "sln_note": TextInput(attrs={
                'class': 'form-control',
                'id': 'sln-note',
            }),
            "sln_color": TextInput(attrs={
                'class': 'form-control',
                'id': 'sln-color',
                'type': "color",
                'value': "#FFFFFF",
                'style': "min-height: 38px; max-height: 38px;",
            }),
        }

class CalendarForm(ModelForm):    
    class Meta:
        model = CalendarModel
        fields = '__all__'
        exclude = ['cl_date', 'cl_saloon', 'user']
        labels = {
            'cl_spec':"Spec",
            'cl_shed':"Template",
        }
        widgets = {
            'cl_spec': Select(attrs={
                'class': 'form-control',
                'id': 'cl-spec',
            }),
            'cl_shed': Select(attrs={
                'class': 'form-control',
                'id': 'cl-shed',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        if 'firm' in kwargs:
            firm = kwargs.pop('firm')
            querySpec = SpecModel.objects.filter(firm_id=firm)
            queryShed = mSheduleTemplate.objects.filter(firm_id=firm)
        else:
            querySpec = SpecModel.objects.all()
            queryShed = mSheduleTemplate.objects.all() 
            
        super(CalendarForm, self).__init__(*args, **kwargs)
        self.fields['cl_spec'].queryset=querySpec
        self.fields['cl_spec'].initial = [0]
        self.fields['cl_shed'].queryset=queryShed
        self.fields['cl_shed'].initial = [0]

class ShedTempForm(ModelForm):
    class Meta:
        model = mSheduleTemplate
        fields = '__all__'
        exclude = ['firm', 'user']
        labels = {
            'st_name':"Name",
            'st_template':"Template",
            'st_note':"Notes"
        }
        widgets = {
            "st_name" : TextInput(attrs={
                'class':'form-control',
                'id':'st_name',
            }),
            "st_template" : TextInput(attrs={
                'class':'form-control',
                'id':'st_template',
            }),
            "st_note" : TextInput(attrs={
                'class': 'form-control',
                'id':'st_note',
            })
        }
        
class MeetForm(ModelForm):
    class Meta:
        model = mMeet
        fields = '__all__'
        exclude = ['m_dt', 'm_saloon', 'm_review', 'm_spec', 'm_rating', 'user', 'm_report']
        labels = {
            'm_client':"Client",
            'm_service':"Service",
            'm_note':"Note",      
        }
        widgets = {
            "m_service" : TextInput(attrs={
                'class':'form-control',
                'id':'m_service',
            }),
            "m_note" : TextInput(attrs={
                'class':'form-control',
                'id':'m_note',
            }),
            'm_client': Select(attrs={
                'class': 'form-control',
                'id':'m_client',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        if 'firm' in kwargs:
            firm = kwargs.pop('firm')
            qClients = Client.objects.filter(firm_id=firm)
        else:
            qClients = Client.objects.all()
        
                       
        super(MeetForm, self).__init__(*args, **kwargs)
        self.fields['m_client'].queryset=qClients
        self.fields['m_client'].initial = [0]
        
class AgentForm(ModelForm):
    class Meta:
        model = mAgent
        field = '__all__'
        exclude = ['firm', 'user']
        labels = {
            'a_code':"Code",
            'a_name':"Name",
            'a_note':"Note",
            'a_mail':"Email",
            'a_phone':"Phone",
            'a_person':"Person",
            'a_bank':"Bank",
        }
        widgets = {
            "a_code" : TextInput(attrs={
                'class':'form-control',
                'id':'a_code',
            }),
            "a_name" : TextInput(attrs={
                'class':'form-control',
                'id':'a_name',
            }),
            "a_note" : TextInput(attrs={
                'class':'form-control',
                'id':'a_note',
            }),
            "a_mail" : EmailInput(attrs={
                'class':'form-control',
                'id':'a_mail',
            }),
            "a_phone" : TextInput(attrs={
                'class':'form-control',
                'id':'a_phone',
            }),
            "a_person" : TextInput(attrs={
                'class':'form-control',
                'id':'a_person',
            }),
            "a_bank" : TextInput(attrs={
                'class':'form-control',
                'id':'a_bank',
            }),            
        }
    
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['a_name'].error_messages = {'required': 'Назва контрагента не має бути пустою'} 
        self.fields['a_code'].error_messages = {'required': 'Код ЄДРПОУ не має бути пустим'} 
        
class ProductForm(ModelForm):
    class Meta:
        model = mProducts
        fields = '__all__'
        exclude = ['firm', 'user', 'category']
        labels = {
            'p_code':"Code",
            'p_name':"Name",
            'p_note':"Note",
            'p_unit':"Units",
        }
        widgets = {
            "p_code" : TextInput(attrs={
                'class':'form-control form-control-sm',
                'id':'p-code',
            }),
            "p_name" : TextInput(attrs={
                'class':'form-control form-control-sm',
                'id':'p-name',
            }),
            "p_note" : TextInput(attrs={
                'class':'form-control form-control-sm',
                'id':'p-note',
            }),
            "p_unit" : Select(attrs={
                'class':'form-control form-control-sm',
                'id':'p-unit',
            }),            
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['p_name'].error_messages = {'required': 'Назва не має бути пустою'}    