from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator


class Firm(models.Model):
    CURRENCYS = {
        "USD": "$ USD",
        "EUR": "€ EUR",
        "UAH": "₴ UAH",
    }
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40)
    note = models.TextField(null=True, blank=True)
    mail = models.EmailField()
    phone = models.CharField(max_length=15)
    person = models.CharField(max_length=100)
    tested = models.BooleanField(default=False)
    bank = models.CharField(max_length=240, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCYS, default="UAH")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=40, null=False)
    l_name = models.CharField(max_length=40, null=True, blank=True)
    phone = models.CharField(max_length=12, null=False)
    telegram = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['l_name', 'f_name']

    def __str__(self):
        name = self.f_name
        if self.l_name:
            name = name + " " + self.l_name 
        return name

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(limit_value=0.009, message="Ціна має бути більше 0")])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name


class SpecModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    spec_fname = models.CharField(max_length=30, null=False)
    spec_lname = models.CharField(max_length=30, null=False)
    spec_phone = models.CharField(max_length=12, null=True, blank=True)
    spec_color = models.CharField(max_length=10, null=False)
    spec_active = models.BooleanField(null=False, default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['spec_active','spec_fname']

    def __str__(self):
        return self.spec_fname + " " + self.spec_lname
    
    @property
    def full_name(self):
        return self.spec_fname + " " + self.spec_lname
    
    # @property
    # def countCal(self):
    #     return CalendarModel.objects.filter(cl_spec=self.id).count()
    
    

class SaloonModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    sln_name = models.CharField(max_length=50, null=False)
    sln_address = models.CharField(max_length=150, null=True, blank=True)
    sln_phone = models.CharField(max_length=12, null=True, blank=True)
    sln_note = models.TextField(null=True, blank=True)
    sln_color = models.CharField(max_length=10, null=False, default="#FFFFFF")
    sln_main = models.BooleanField(null=False, default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sln_name']

    def __str__(self):
        return self.sln_name
    
class mSheduleTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE, null=False)
    st_name = models.CharField(max_length=40, null=False)
    st_template = models.CharField(max_length=250, null=False)
    st_note = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['st_name']
    
    def __str__(self) -> str:
        return self.st_name

class CalendarModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    cl_date = models.DateField(null=False)
    cl_saloon = models.ForeignKey(SaloonModel, on_delete=models.CASCADE)
    cl_spec = models.ForeignKey(SpecModel, on_delete=models.SET_NULL, null=True)
    cl_shed = models.ForeignKey(mSheduleTemplate, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self) -> str:
        return self.cl_date.isoformat()
    
class mMeet(models.Model):
    class StatusList(models.IntegerChoices):
        REG = 10
        DONE = 11
        CANC = 12
        PAID = 13
        BOT_REG = 20
        BOT_DONE = 21
        BOT_CANC = 22
        BOT_PAID = 23
        API = 30
        API_DONE = 31
        API_CANC = 32
        API_PAID = 33
    
    id = models.BigAutoField(primary_key=True)
    m_dt = models.DateTimeField(null=False)
    m_saloon = models.ForeignKey(SaloonModel, on_delete=models.CASCADE, null=False, related_name='saloon')
    m_spec = models.ForeignKey(SpecModel, on_delete=models.SET_NULL, null=True, related_name='spec')
    m_client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='client')
    m_service = models.CharField(max_length=250, null=True, blank=True)
    m_note = models.TextField(null=True, blank=True)
    # * запасное поле
    m_report = models.TextField(null=True, blank=True)
    
    m_status = models.IntegerField(choices=StatusList, default=StatusList.REG)
    m_rating = models.IntegerField(default=0)
    m_review = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['m_dt']
    
    def __str__(self) -> str:
        return self.m_dt.isoformat()
    
class mProducts(models.Model):
    class CategoryList(models.IntegerChoices):
        Product = 1, ("Товар")
        Material = 2, ("Матеріал")
                
    class UnitsList(models.IntegerChoices):
        Pcs = 1, ("шт")
        Gramm = 2, ("г")
        Liter = 3, ("л")
        Meter = 4, ("м")
    
    id = models.BigAutoField(primary_key=True)
    category = models.IntegerField(choices=CategoryList, default=CategoryList.Product)
    p_code = models.CharField(max_length=40, null=True, blank=True)
    p_name = models.CharField(max_length=40, null=False, validators=[MinLengthValidator(2, "Назва має бути більше 2 символів"),])
    p_note = models.CharField(max_length=250, null=True, blank=True)
    p_unit = models.IntegerField(choices=UnitsList, default=UnitsList.Pcs)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'p_name']
    
    def __str__(self) -> str:
        return self.p_name
    
    


class mCheck(models.Model):
    id = models.BigAutoField(primary_key=True)
    meet = models.ForeignKey(mMeet, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(mProducts, on_delete=models.SET_NULL, null=True)
    c_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self) -> str:
        return str(self.id)
    
class mAgent(models.Model):
    id = models.BigAutoField(primary_key=True)
    a_code = models.CharField(max_length=40)
    a_name = models.CharField(max_length=40)
    a_note = models.TextField(null=True, blank=True)
    a_mail = models.EmailField(null=True, blank=True)
    a_phone = models.CharField(max_length=15, null=True, blank=True)
    a_person = models.CharField(max_length=100, null=True, blank=True)
    a_bank = models.CharField(max_length=240, null=True, blank=True)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['a_name', 'a_code']

    def __str__(self):
        return self.a_name
    
class mDocument(models.Model):
    class DoctypeList(models.IntegerChoices):
        PND = 1, ("Прибуткова накладна")        
        OND = 20, ("Видаткова накладна")
    
    id = models.BigAutoField(primary_key=True)
    d_type = models.IntegerField(choices=DoctypeList, default=DoctypeList.PND)
    d_num = models.CharField(max_length=40, null=True, blank=True)
    d_date = models.DateTimeField(null=False)
    d_note = models.CharField(max_length=150, null=True, blank=True)
    d_file = models.FileField(upload_to='uploads/')
    agent = models.ForeignKey(mAgent, on_delete=models.SET_NULL, null=True)
    saloon = models.ForeignKey(SaloonModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.d_name

class mDocdetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(mDocument, on_delete=models.CASCADE)
    product = models.ForeignKey(mProducts, on_delete=models.SET_NULL, null=True)
    d_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    d_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self) -> str:
        return str(self.id)
    
class mNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    n_query = models.CharField(max_length=250, null=True, blank=True)
    n_value = models.CharField(max_length=250, null=True, blank=True)   
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self) -> str:
        return str(self.id)