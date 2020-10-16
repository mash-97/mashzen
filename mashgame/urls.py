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
    path("<str:user_name>/logout/", views.userLogout, name="user_logout")
]
