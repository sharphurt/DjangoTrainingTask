from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout),
    path('signup/', views.user_registration, name="registration")
]
