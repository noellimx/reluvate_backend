from django.urls import path
from . import views as handlers

urlpatterns = [path("hello/", handlers.say_hello)]
