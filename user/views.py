from http.client import HTTPResponse
from django.shortcuts import render,redirect
import requests
import json
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm
from utils import get_client
from django.http import HttpResponse


client = get_client()
db = client.SEProject
userDB  = db.userData

# Home page for PackTravel
def index(request, username=None):
    if request.session.has_key('username'):
         return render(request, 'home/home.html', {"username":request.session["username"]})
    return render(request, 'home/home.html', {"username":None})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            userObj = {
                "username": form.cleaned_data["username"], 
                "unityid": form.cleaned_data["unityid"], 
                "fname": form.cleaned_data["first_name"],
                "lname": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
                "phone": form.cleaned_data["phone_number"]
            }
            userDB.insert_one(userObj)
            request.session['username'] = userObj["username"]
            request.session['unityid'] = userObj["unityid"]
            request.session['fname'] = userObj["fname"]
            request.session['lname'] = userObj["lname"]
            request.session['email'] = userObj["email"]
            request.session['phone'] = userObj["phone"]
            return redirect(index, username=request.session["username"])
        else:
            print(form.errors.as_data()) 
    else:
        if request.session.has_key('username'):
            return index(request,request.session['username'])
        form = RegisterForm()
    return render(request, 'user/register.html', {"form": form})

def logout(request):
   try:
      request.session.clear()
   except:
      pass
   return redirect(index)


# @describe: Existing user login
def login(request):
    if request.session.has_key('username'):
        return redirect(index, {"username": request.session['username']})
    else:
        if request.method=="POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                user = userDB.find_one({"username": username})
                if user["password"] == form.cleaned_data["password"]:
                    request.session["username"] = username
                    request.session['unityid'] = user["unityid"]
                    request.session['fname'] = user["fname"]
                    request.session['lname'] = user["lname"]
                    request.session['email'] = user["email"]
                    request.session["phone"] = user["phone"]
                    return redirect(index, request.session['username'])
            else:
                print(form.errors.as_data()) 
        else:
            form = LoginForm()
        return render(request, 'user/login.html', {"form": form})

