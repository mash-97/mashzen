from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from mashgame.models import User
from mashgame.models import Preference
from mashgame.models import Home, Spouse, NumChild, Luxury
from .authentication import getAuthenticatedUser

def mashgame(request):
    request.session["error_message"] = None
    return render(request, "mashgame/mashgame.html", {"error_message": request.session.get("error_message")})


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
        Preference.objects.assignByDefault(user=user)
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
    return render(request, "mashgame/user_preference.html", {"user": user, "prefs": prefs, "genders": [t[0] for t in User.GENDERS]})


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
    gender = request.POST["gender"]

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
    user.gender = gender
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
    return redirect("mashgame:login")


def showUsers(request, user_name):
    request.session["page_requested"] = "mashgame:show_users"
    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")

    context = {
        "user": user,
        "available_users": User.objects.getUsersAgainst(user)
    }
    return render(request, "mashgame/users_table.html", context)


def sentAttacks(request, user_name):
    request.session["page_requested"] = "mashgame:sent_attacks"
    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")
    return render(request, "mashgame/sent_attacks.html", {"user": user, "sent_attacks": user.sentAttacks()})

def sentAttackDetails(request, user_name, attack_id):
    request.session["page_requested"] = "mashgame:sent_attack_details"
    user = getAuthenticatedUser(request, user_name)
    if not user:
        return redirect("mashgame:login")
    attack = user.sent_attacks.filter(id=attack_id)
    if not attack.exists():
        return redirect("mashgame:sent_attacks", user_name=user.user_name)
    context={
        "user": user,
        "attack": attack.first()
    }
    return render(request, "mashgame/sent_attack_details.html", context)
