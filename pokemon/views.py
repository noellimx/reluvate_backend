from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Request handlers

def say_hello(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world from project [poke_project], app [pokemon]")