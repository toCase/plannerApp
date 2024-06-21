from django.contrib.auth.decorators import login_required

@login_required(login_url="main_login")
def load(request):
    pass