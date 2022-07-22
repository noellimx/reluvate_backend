from django.urls import path
from . import views as handlers


app_name = "pokemon"
urlpatterns = [path("hello/", handlers.say_hello, name="hello")]
