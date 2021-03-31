from django.urls import path

from notebook.views import notes_list

urlpatterns = [
    path('<username>/', notes_list, name='user_signin')
]
