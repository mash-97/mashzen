from django.urls import path

from . import views

app_name = "mashgame"
urlpatterns = [
    path("", views.mashgame, name="mashgame"),
    path("join/", views.joinUser, name="join_user")
]
