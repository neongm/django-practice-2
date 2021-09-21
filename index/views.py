from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.models import auth, User
from django.contrib import messages

# for github gists integration
import requests

def index(req):

    gists_array = []
    response = requests.get(
        "https://api.github.com/users/neongm/gists",
        headers={
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    # checking if the API limit exceeded or any other errors
    if response.status_code == requests.codes.ok:
        json_response = response.json()
        for not_url in json_response:
            gists_array.append(f"https://gist.github.com/{not_url['owner']['login']}/{not_url['url'][not_url['url'].rfind('/')+1::]}.js")


    context = {
        'gists': gists_array,
        'title': 'speedrun page'
    }
    return render(req, 'index/index.html', context)


def about(req):
    context = {
        'title' : 'about page'
    }
    return render(req, 'index/about.html', context)


def register(req):
    context = {
        'title' : 'register page'
    }

    if req.method == "POST":
        username = req.POST.get('username')
        email = req.POST.get('email')
        password1 = req.POST.get('password1')
        password2 = req.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(req, 'email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(req, 'username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username, email, password1)
                user.save()
                return redirect('login')
        else:
            messages.info(req, 'passwords are different')
            return redirect('register')

    else:
        return render(req, 'index/register.html', context)

def login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        print(user)
        print(username)
        print(password)
        if user is not None:
            auth.login(req, user)
            return redirect('index')
        else:
            messages.info(req, "user doesn't exist or password is invalid")
            return redirect('login')
    else:
        return render(req, 'index/login.html')

def logout_user(req):
    auth.logout(req)
    return render(req, 'index/login.html')
