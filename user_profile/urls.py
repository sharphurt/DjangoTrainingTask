from django.urls import path
from . import views

urlpatterns = [
    path('/', views.user_signin),
    path('signin/', views.user_signin, name="signin"),
    path('logout/', views.user_logout),
    path('signup/', views.user_signup, name="signup")
]
