from re import U
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


from rest_framework_simplejwt.authentication import authentication, api_settings
from rest_framework_simplejwt import authentication as auth_, tokens


# Request handlers


def say_hello(_: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world from project [poke_project], app [pokemon]")


a = auth_.JWTAuthentication()


def is_access_token_valid(request: HttpRequest) -> HttpResponse:

    (user, _) = a.authenticate(request)

    if user is not None:
        return HttpResponse(status=200)

    return HttpResponse(status=501)
