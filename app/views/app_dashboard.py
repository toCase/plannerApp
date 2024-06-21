from django.shortcuts import render, redirect

def load(request):
    context = {"title": "Dashboard", "name": "Dashboard here"}
    # context.update(stateEngine("DASH"))
    return render(request, template_name="app_dashboard.html", context=context)