from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from mashgame.models import User
from mashgame.models import Preference
from mashgame.models import Home, Spouse, NumChild, Luxury
from .authentication import getAuthenticatedUser

def attackDetails(request, pk):
    pass
