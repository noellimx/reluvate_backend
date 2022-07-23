from random import randint
from re import U
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework_simplejwt import authentication as auth_
from pokemon.models import GuessGame


low = 0
high = 10


def random_guessing_number_target():
    return randint(low, high)


# Request handlers


def say_hello(_: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world from project [poke_project], app [pokemon]")


a = auth_.JWTAuthentication()


def is_access_token_valid(request: HttpRequest) -> HttpResponse:

    try:
        (user, _) = a.authenticate(request)

        if user is not None:
            return HttpResponse(status=200)
    except:
        pass

    return HttpResponse(status=401)


def how_many_tries_already(request: HttpRequest) -> HttpResponse:
    print("how_many_tries_already")
    try:
        (user, _) = a.authenticate(request)

        GuessGame.objects.create(trainer=user, target=random_guessing_number_target())

        game = GuessGame.objects.get(trainer=user)

        data = {"tried": game.tried}

        return JsonResponse(data)

    except Exception as err:
        print(err)
        return HttpResponse(status=400)
