from django.urls import path

from . import views

app_name = "mashgame"
urlpatterns = [
    path("", views.mashgame, name="mashgame"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("ajax/validate_username", views.validate_username, name="validate_username"),
    path("joinLoginUser/", views.joinLoginUser, name="join_login_user"),
    path("joinSignupUser/", views.joinSignupUser, name="join_signup_user"),
    path("<str:user_name>/", views.userProfile, name="user_profile"),
    path("<str:user_name>/preference/", views.userPreference, name="user_preference"),
    path("<str:user_name>/logout/", views.userLogout, name="user_logout"),
    path("<str:user_name>/savePreference/", views.savePreference, name="save_preference"),
    path("<str:user_name>/sent_attacks/", views.sentAttacks, name="sent_attacks"),
    path("<str:user_name>/show_users/", views.showUsers, name="show_users"),
    path("<str:user_name>/sent_attack_details/<int:attack_id>/", views.sentAttackDetails, name="sent_attack_details"),
    path("<str:user_name>/send_attack/<str:reciever_name>", views.sendAttack, name="send_attack"),
    path("<str:user_name>/save_attack/<str:reciever_name>", views.saveAttack, name="save_attack")
]
