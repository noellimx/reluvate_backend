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

    try:
        (user, _) = a.authenticate(request)

        print("is acces tk v")

        print(user)
        if user is not None:
            return HttpResponse(status=200)
    except:
        pass

    return HttpResponse(status=401)


def how_many_tries_already(request: HttpRequest) -> HttpResponse:

    try:
        (user, _) = a.authenticate(request)
        if user is not None:
            return HttpResponse(status=200)
    except:
        return HttpResponse(status=401)


    return HttpResponse(status = 400)