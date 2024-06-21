from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from app.models import Firm

def index(request):
    return render(request, 'main_index.html')

def main_features(request):
    return render(request, 'main_features.html')

def main_pricing(request):
    return render(request, 'main_pricing.html')    

def main_help(request):
    return render(request, 'main_help.html')

def main_about(request):
    return render(request, 'main_about.html')

def main_register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    print(context)
    return render(request, "main_register.html", context=context)

def main_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')
    context = {'form':form}
    return render(request, template_name="main_login.html", context=context)

def main_logout(request):
    auth.logout(request)
    return redirect('login')

def main_app(request):

    firm_test = Firm.objects.filter(tested=1)[0]
    firms = Firm.objects.filter(user=request.user.id)
    has_firms = len(firms)

    context = {'firm_test': firm_test, 'has_firms': has_firms, 'firms': firms}
    print(context)

    return render(request, template_name="main_app.html", context=context)