from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Note


def notes_list(request, username=None):
    if request.user.is_authenticated and request.user.username == username:
        notes = Note.objects.filter(user=request.user)
        return render(request, 'notebook.html', {'user': request.user, 'notes_list': notes})
    return redirect('signin.html')
# Create your views here.
