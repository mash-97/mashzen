from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User

def mashgame(request):
    if not "password_invalid" in list(request.session.keys()):
        request.session["password_invalid"] = False

    return render(request, "mashgame/mashgame.html", {"password_invalid": request.session["password_invalid"]})


def joinUser(request):
    user_name = request.POST["user_name"]
    password = request.POST["password"]

    if User.objects.check_if_username_exist(user_name):
        user = User.objects.get_authorized_user(user_name, password)
        if user==None:
            request.session["password_invalid"] = True
            return redirect("mashgame:mashgame")
    else:
        user = User.objects.create(user_name=user_name, password=password)
    
    request.session["password_invalid"] = False
    return render(request, "mashgame/user_profile.html", {"user": user})
