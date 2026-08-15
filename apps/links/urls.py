from django.urls import path

from . import views

app_name = "links"

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("create-short-link/", views.create_short_link_view, name="create_short_link"),
]
