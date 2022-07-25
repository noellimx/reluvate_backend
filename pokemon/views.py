from random import randint
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework_simplejwt import authentication as auth_
from pokemon.models import GuessGame, Pokedex, Pokemon
from django.core import serializers
from django.db.models import Q

import json

from django.conf import settings

from integration_tests.helpers import ORACLE_TARGET

# TODO New class for game logic

low = 0
high = 10


def random_guessing_number_target_in_prod():
    return randint(low, high)


def random_guessing_number_target_in_test():
    return ORACLE_TARGET


random_guessing_number_target = (
    random_guessing_number_target_in_test
    if settings.IN_TEST_ENVIRONMENT
    else random_guessing_number_target_in_prod
)


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
    try:
        (user, _) = a.authenticate(request)

        game, _ = GuessGame.objects.get_or_create(
            trainer=user, defaults={"target": random_guessing_number_target()}
        )

        data = {"tried": game.tried}

        return JsonResponse(data)

    except Exception as err:
        print(err)
        return HttpResponse(status=400)


# guess a number
# if valid number:
#   1. accept and compare with target
#       1.1 If correct:
#           - reset tried
#           - reward prize pokemon
#           - reset prize pokemon
#       1.2 If wrong:
#           - tried++
#           If tried == 3
#           - reset tried
#           - reset prize pokemon
#
# else:
#   -
#
# Returns end state of tried and award, if any
#
def guess(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            (user, _) = a.authenticate(request)

            body_in_json = json.loads(request.body)

            game, _ = GuessGame.objects.get_or_create(
                trainer=user, defaults={"target": random_guessing_number_target()}
            )

            reply = ""
            if "guess" in body_in_json:
                guess = body_in_json["guess"]
                if type(guess) != int:
                    pass
                elif game.target == guess:
                    game.tried = 0
                    reply = "hit"
                    # TODO reward service
                else:
                    game.tried += 1
                    if game.tried == 3:
                        game.tried = 0
                        # TODO reward service
                game.save()

            data = {"tried": game.tried, "reply" : reply}

            return JsonResponse(data)

        except Exception as err:
            print("[guess] Error")
            print(err)
            return JsonResponse({"err": str(err)}, status=400)
    else:
        return JsonResponse({}, status=501)


def owned_pokemon(request: HttpRequest) -> HttpResponse:
    print("[owned_pokemon]")
    if request.method == "GET":
        try:
            (user, _) = a.authenticate(request)

            trained_pokemons = Pokemon.objects.filter(trainer=user)

            data = {"pokemons": serializers.serialize("json", trained_pokemons)}
            print(len(data["pokemons"]))
            print("len(data)")
            return JsonResponse(data, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({},status=400)
    return JsonResponse(status=500)



def unowned_pokemon(request: HttpRequest) -> HttpResponse:
    print("[unowned_pokemon]")
    if request.method == "GET":
        try:
            (user, _) = a.authenticate(request)

            trained_pokemons = Pokemon.objects.filter(~Q(trainer=user))

            data = {"pokemons": serializers.serialize("json", trained_pokemons)}

            return JsonResponse(data, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({},status=400)
    return JsonResponse(status=500)

