from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('features', views.main_features, name="features"),
    path('pricing', views.main_pricing, name="pricing"),
    path('help', views.main_help, name="help"),
    path('about', views.main_about, name="about"),
    path('register', views.main_register, name="register"),
    path('login', views.main_login, name="login"),
    path('logout', views.main_logout, name="logout"),
    path('company', views.main_app, name="company"),
]