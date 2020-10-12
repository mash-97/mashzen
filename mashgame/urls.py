from django.urls import path

from . import views

app_name = "mashgame"
urlpatterns = [
    path("", views.mashgame, name="mashgame"),
    path("joinLoginUser/", views.joinLoginUser, name="join_login_user"),
    path("joinSignupUser/", views.joinSignupUser, name="join_signup_user"),
    path("signup/", views.signup, name="signup"),
    path("ajax/validate_username", views.validate_username, name="validate_username"),
]

STATICFILES_DIRS = [
    
]
