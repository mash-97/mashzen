from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .models import User

def mashgame(request):
    if not "password_invalid" in list(request.session.keys()):
        request.session["password_invalid"] = False

    return render(request, "mashgame/mashgame.html", {"password_invalid": request.session["password_invalid"]})

def signup(request):
    return render(request, "mashgame/signup.html", {})

def validate_username(request):
    user_name = request.GET.get("user_name", None)
    data = {
        "is_taken": User.objects.filter(user_name__iexact=user_name).exists()
    }
    return JsonResponse(data)


def joinSignupUser(request):
    user_name = request.POST["user_name"]
    password = request.POST["password"]

    if User.objects.filter(user_name__iexact=user_name).exists():
            request.session["error_message"] = "Username already exists!"
            return redirect("mashgame:signup")

    user = User.objects.create(user_name=user_name, password=password)
    if not user:
        request.session["error_message"] = "Failed on authorizing the user!"
        return redirect("mashgame:mashgame")

    user.authorize(password)

    request.session["error_message"] = None
    return render(request, "mashgame/user_profile.html", {"user": user})


def joinLoginUser(request):
    user_name = request.POST["user_name"]
    password = request.POST["password"]

    if not User.objects.filter(user_name__iexact=user_name).exists():
        request.session["error_message"] = "Username doesn't exist!"
        return redirect("mashgame:mashgame")

    user = User.objects.get_authorized_user(user_name, password)

    if not user:
        request.session["error_message"] = "Failed on authorizing the user!"
        return redirect("mashgame:mashgame")

    request.session["error_message"] = None
    return render(request, "mashgame/user_profile.html", {"user": user})
