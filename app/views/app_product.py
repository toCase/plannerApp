from django.db.models import Q, Count, F
from django.shortcuts import render

from ..base import make_notes, get_notes, del_notes, page_list, page_from, page_to

from ..forms import ProductForm
from ..models import mProducts

row_count = 20
def get_data(firm_id :int, cat :int, query :str = None):  
    
    if (query is not None):
        data = mProducts.objects.filter(
            Q(firm=firm_id) & Q(category=cat) & (Q(p_name__icontains=query) | Q(p_code__icontains=query))
        )
    else:
        data = mProducts.objects.filter(Q(firm=firm_id) & Q(category=cat))        
        
    return data

def load(request, category:str):    
    global row_count
    
    cat_id = int(category)    
    notes :dict = get_notes(request.user.id, ["FRM", "PRD_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("PRD_SEARCH")
    
    context = {
        "title": "Products",
        "page_name": "Товари" if cat_id == 1 else "Матеріали",
        "id":"0",
        "category": category
    }
    
    if q is not None:
        context['query'] = q
    
    data = get_data(firm_id, cat_id, q)
    
    context['product_data'] = data[0:row_count]
    make_notes(request.user.id, "PRD_PAGE", "1")
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_product.html", context=context)

def filter(request, category:str):
    global row_count
    cat_id = int(category)
    
    notes :dict = get_notes(request.user.id, ["FRM", "PRD_SEARCH"])
    firm_id = notes.get("FRM")
    q = notes.get("PRD_SEARCH")
    
    if request.method == "GET":
        if request.GET.get("search") != "":        
            q = request.GET.get("search")
            make_notes(request.user.id, "PRD_SEARCH", q)
        else:
            q = ""
            del_notes(request.user.id, "PRD_SEARCH")
    
    data = get_data(firm_id, cat_id, q)
    
    context = {
        "id":"0",
        "category": category,
        "product_data": data[0:row_count]
    }
    
    make_notes(request.user.id, "PRD_PAGE", "1")
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = '1'
    
    return render(request, template_name="app_product/app_product_container.html", context=context)

def add(request, category:str):
    form = ProductForm()
    context = {
        "form": form,
        "id": "0",
        "category": category,
        "product_data":""
    }
    return render(request, template_name="app_product/app_product_container.html", context=context)

def edit(request, pk :str, category:str):
    id_prod = int(pk)
    model = mProducts.objects.get(id=id_prod)
    form = ProductForm(instance=model)
    context = {
        "form": form,
        "id": pk,
        "category": category,
        "product_data":"",        
    }
    return render(request, template_name="app_product/app_product_container.html", context=context)

def save(request, pk :str, category:str):
    global row_count
    id_product = int(pk)
    id_cat = int(category)
    notes :dict = get_notes(request.user.id, ["FRM"])
    firm_id = notes.get("FRM")
    
    form = ProductForm(request.POST)
    if id_product > 0:
        model = mProducts.objects.get(id=id_product)
        form = ProductForm(request.POST, instance=model)
    if form.is_valid():
        data = form.save(commit=False)
        if id_product == 0:
            data.category = mProducts.CategoryList.Product if id_cat == 1 else mProducts.CategoryList.Material
            data.firm_id = firm_id
        data.user_id = request.user.id
        data.save()
        return page(request, "1", category)
    else:
        errors = form.errors.get_json_data()
        messages = []
        for key in errors.keys():            
            l = errors.get(key)
            for x in l:
                messages.append(x.get("message"))
        
        context = {
            "form": form,
            "id": pk,
            "category": category,
            "product_data":"",
            "errors": messages,  
        }
        return render(request, template_name="app_product/app_product_container.html", context=context)
        
        
    

def delete(request, pk:str, category:str):
    id_prod = int(pk)
    model = mProducts.objects.get(id=id_prod)
    model.delete()
    return page(request, "1", category)

def page(request, page:str, category:str):
    global row_count
    notes :dict = get_notes(request.user.id, ["FRM", "PRD_SEARCH", "PRD_PAGE"])
    firm_id = notes.get("FRM")
    q = notes.get("PRD_SEARCH")
    cat_id = int(category)
    
    make_notes(request.user.id, "PRD_PAGE", page)
    
    data = get_data(firm_id, cat_id, q)
    
    context = {
        "id": "0",
        "category": category,
        "product_data": data[page_from(int(page)):page_to(int(page))]
    }
    
    if len(data) > row_count:
        context['pag'] = page_list(len(data))
        context['apage'] = page
    
    return render(request, template_name="app_product/app_product_container.html", context=context)