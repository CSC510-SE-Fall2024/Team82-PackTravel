from http.client import HTTPResponse
from django.shortcuts import render,redirect
from numpy import True_, dtype
import requests
import json
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from publish.forms import RideForm
from utils import get_client

client = get_client()
db = client.SEProject
ridesDB  = db.rides
routesDB  = db.routes

def search_index(request):
    all_rides = list(ridesDB.find())
    processed = list()
    for ride in all_rides:
        ride['id'] = ride.pop('_id')
        processed.append(ride)
    return render(request, 'search/search.html', {"username": request.session['username'], "rides":processed})
    