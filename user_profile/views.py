from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from user_profile.forms import SignUpForm, SignInForm


def index(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        return render(request, 'index.html', {'user': user[0]})
    else:
        return redirect('login')


def user_signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username, _, password = get_form_inputs(form)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html', {'user': user})
            else:
                return render(request, 'signin.html', {'invalid': True, 'form': form})
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'invalid': False, 'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username, email, password = get_form_inputs(form)
            if is_email_free(email) and is_username_free(username):
                user = register_user(request, (username, email, password))
                return render(request, 'index.html', {'user': user})
            else:
                return render(request, 'signup.html', {'error': 'A user with this data already exists', 'form': form})
        else:
            return render(request, 'signup.html', {'error': 'Invalid input data', 'form': form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'error': None, 'form': form})


def register_user(request, user_data):
    username, email, password = user_data
    user = User.objects.create_user(username, email, password)
    user.save()
    user = authenticate(request, username=username, email=email, password=password)
    login(request, user)
    return user


def get_form_inputs(form):
    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    return username, email, password


def is_username_free(username):
    existing_user = User.objects.filter(username=username)
    return len(existing_user) == 0


def is_email_free(email):
    existing_user = User.objects.filter(email=email)
    return len(existing_user) == 0
