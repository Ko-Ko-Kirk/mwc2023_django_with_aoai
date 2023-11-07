from django.urls import path
from first_app import views
from .views import StoryTellerView


urlpatterns = [
    path("", views.home, name="home"),
    path("hello_template/<name>", views.hello_template, name="hello_template"),
    path("hello_model/<id>", views.hello_model, name="hello_model"),
    path("storyteller/", StoryTellerView.as_view(), name="storyteller"),
]
