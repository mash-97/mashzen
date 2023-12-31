from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from mashgame.models import User



def getAuthenticatedUser(request, user_name):
    # at the top check if any user session is exist
    if not request.session.get("user_name") or not request.session.get("user_hash"):
        return None

    # if there's user_name in session data, check if it match with the requested user_name
    # else return None
    if request.session["user_name"] != user_name:
        user_name = request.session["user_name"]

    # get filtered QuerySet
    query_set = User.objects.filter(user_name__iexact=user_name)
    # return None if a user with user_name doesn't exist
    if not query_set.exists():
        # delete user_name and user_hash form the session data for future clarification
        request.session["user_name"] = None
        request.session["user_hash"] = None
        return None
    # get the user with user_name
    user = query_set.first()

    # check registered session hash with current session hash
    if request.session.get("user_hash") in user.hashValues():
        return user
    # else means invalid session data
    request.session["user_name"] = None
    request.session["user_hash"] = None
    return None


def login(request):
    # First check if already a session exists
    user = getAuthenticatedUser(request, None)
    if user:
        return redirect("mashgame:user_profile", user_name=user.user_name)
    return render(request, "mashgame/login.html", {"error_message": request.session.get("error_message")})

def signup(request):
    # First check if already a session exists
    user = getAuthenticatedUser(request, None)
    if user:
        return redirect("mashgame:user_profile", user_name=user.user_name)

    return render(request, "mashgame/signup.html", {"error_message": request.session.get("error_message")})


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
            request.session["error_message"] = f"Username already exists: {user_name}"
            return redirect("mashgame:signup")

    user_signup_res = User.objects.signup(user_name=user_name, password=password)
    if not user_signup_res:
        request.session["error_message"] = f"Failed on registering the user: {user_name}"
        return redirect("mashgame:signup")

    user = user_signup_res["user"]
    user_hash = user_signup_res["user_hash"]

    if not user_hash:
        request.session["errror_message"] = f"Failed on authorizing the user: {user_name}"
        return redirect("mashgame:login")

    # keep user_name and user_hash in session data
    request.session["user_name"] = user.user_name
    request.session["user_hash"] = user_hash
    request.session["error_message"] = None

    return redirect("mashgame:user_profile", user_name=user.user_name)


def joinLoginUser(request):
    request.session["error_message"] = None
    user_name = request.POST["user_name"]
    password = request.POST["password"]

    if not User.objects.filter(user_name__iexact=user_name).exists():
        request.session["error_message"] = "Username doesn't exist!"
        return redirect("mashgame:login")

    #  User.objects.get_authorized_user(user_name, password) will return a dict on success
    authorized_dict = User.objects.login(user_name, password)
    if not authorized_dict:
        request.session["error_message"] = f"Failed on authorising the user: {user_name}"
        return redirect("mashgame:login")

    user = authorized_dict.get("user")
    user_hash = authorized_dict.get("user_hash")

    if not user or not user_hash:
        request.session["error_message"] = "Failed on authorizing the user!"
        return redirect("mashgame:mashgame")

    # keep user_name and user_hash in session data
    request.session["user_name"] = user.user_name
    request.session["user_hash"] = user_hash
    request.session["error_message"] = None

    if request.session.get("page_requested"):
        return redirect(request.session.get("page_requested"), user_name=user.user_name)

    return redirect("mashgame:user_profile", user_name=user.user_name)
