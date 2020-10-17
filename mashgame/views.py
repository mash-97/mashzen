from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .models import User
from .models import Preference
from .models import Home, Spouse, NumChild, Luxury

def mashgame(request):
    request.session["error_message"] = None
    return render(request, "mashgame/mashgame.html", {"error_message": request.session.get("error_message")})



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
    user_name = request.POST["user_name"]
    password = request.POST["password"]

    if not User.objects.filter(user_name__iexact=user_name).exists():
        request.session["error_message"] = "Username doesn't exist!"
        return redirect("mashgame:mashgame")

    #  User.objects.get_authorized_user(user_name, password) will return a dict on success
    authorized_dict = User.objects.get_authorized_user(user_name, password)
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


def userProfile(request, user_name):
    request.session["page_requested"] = "mashgame:user_profile"
    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")

    return render(request, "mashgame/user_profile.html", {"user": user})


def userPreference(request, user_name):
    request.session["page_requested"] = "mashgame:user_preference"
    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")

    class Pref:
        def __init__(self, type_name, type_header, opts, so1i, so2i):
            self.type_name = type_name
            self.type_header = type_header
            self.opts = opts
            self.soptid_1 = so1i
            self.soptid_2 = so2i

    try:
        mash_data = user.preference.mash_data
    except User.preference.RelatedObjectDoesNotExist:
        Preference.objects.createAPreferenceWithDefaultMASHData(user=user)
        mash_data = user.preference.mash_data

    home_pref = Pref("home", "Home", list(Home.objects.all()),
                        mash_data.home_1.id,
                        mash_data.home_2.id)

    spouse_pref = Pref("spouse", "Spouse", list(Spouse.objects.all()),
                        mash_data.spouse_1.id,
                        mash_data.spouse_2.id)

    numchild_pref = Pref("numchild", "Number of Child", list(NumChild.objects.all()),
                        mash_data.numchild_1.id,
                        mash_data.numchild_2.id)

    luxury_pref = Pref("luxury", "Luxury", list(Luxury.objects.all()),
                        mash_data.luxury_1.id,
                        mash_data.luxury_2.id)


    prefs = [home_pref, spouse_pref, numchild_pref, luxury_pref]
    return render(request, "mashgame/user_preference.html", {"user": user, "prefs": prefs})


def savePreference(request, user_name):
    request.session["page_requested"] = "mashgame:user_preference"

    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")

    home_1_id = int(request.POST["selected_home_1"])
    home_2_id = int(request.POST["selected_home_2"])
    spouse_1_id = int(request.POST["selected_spouse_1"])
    spouse_2_id = int(request.POST["selected_spouse_2"])
    numchild_1_id = int(request.POST["selected_numchild_1"])
    numchild_2_id = int(request.POST["selected_numchild_2"])
    luxury_1_id = int(request.POST["selected_luxury_1"])
    luxury_2_id = int(request.POST["selected_luxury_2"])
    lucky_number = int(request.POST["lucky_number"])

    mash_data = user.preference.mash_data
    mash_data.home_1 = Home.objects.get(id=home_1_id)
    mash_data.home_2 = Home.objects.get(id=home_2_id)
    mash_data.spouse_1 = Spouse.objects.get(id=spouse_1_id)
    mash_data.spouse_2 = Spouse.objects.get(id=spouse_2_id)
    mash_data.numchild_1 = NumChild.objects.get(id=numchild_1_id)
    mash_data.numchild_2 = NumChild.objects.get(id=numchild_2_id)
    mash_data.luxury_1 = Luxury.objects.get(id=luxury_1_id)
    mash_data.luxury_2 = Luxury.objects.get(id=luxury_2_id)
    mash_data.save()
    user.lucky_number = lucky_number
    user.save()

    return redirect("mashgame:user_profile", user_name=user_name)

def userLogout(request, user_name):
    request.session["page_requested"] = None
    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")


    user.deauthorizeHash(request.session.get("user_hash"))
    # delete user authentication session data
    request.session["user_hash"] = None
    request.session["user_name"] = None
    request.session["page_requested"] = None
    return redirect("mashgame:login")

def showUsers(request, user_name):
    pass 
