from ast import Num
from random import randint
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework_simplejwt import authentication as auth_
from pokemon.models import GuessGame, Pokedex, Pokemon
from django.core import serializers
from django.db.models import Q
from django.conf import settings
from pokemon.serializer import PokemonSerializer

import json

from django.conf import settings

from integration_tests.helpers import ORACLE_TARGET

# TODO New class for game logic

low = 1
high = 2


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


def new_prize_pokemon():
    pokedex = Pokedex.objects.order_by("?").first()
    prize = Pokemon.objects.create(pokedex=pokedex)

    return prize


def get_game_of_user(user: settings.AUTH_USER_MODEL):

    game = None
    try:
        game = GuessGame.objects.get(trainer=user)
    except:
        target = random_guessing_number_target()
        prize = new_prize_pokemon()
        game = GuessGame.objects.create(trainer=user, prize=prize, target=target)
    return game


def how_many_tries_already(request: HttpRequest) -> HttpResponse:
    try:
        (user, _) = a.authenticate(request)

        game = get_game_of_user(user)
        prize = json.dumps(PokemonSerializer(game.prize).data)
        data = {"tried": game.tried, "prize": prize}

        return JsonResponse(data)

    except Exception as err:
        print(err)
        return HttpResponse(status=400)



def processGuess(guess:str or int) -> int or None:
    try:
        if type(guess) != int:
            return int(guess)
        return guess
    except:
        return None
    
# guess a number
# if valid number:
#   1. accept and compare with target
#       1.1 If correct:
#           - reset tried
#           - reward prize pokemon
#           - reset prize pokemon and guess
#       1.2 If wrong:
#           - tried++
#           If tried == 3
#           - reset tried
#           - reset prize pokemon and guess
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

            game = get_game_of_user(user)
            reply = ""
            rewarded_prize = None
            next_prize = None
            if "guess" in body_in_json:
                guess = processGuess(body_in_json["guess"])
                if guess is None:
                    pass
                elif game.target == guess:
                    game.tried = 0
                    reply = "hit"
                    # TODO reward service

                    # set trainer of prize to owner
                    game.prize.trainer = user
                    game.prize.save()

                    rewarded_prize = json.dumps(PokemonSerializer(game.prize).data)

                    # update with new random pokemon and guess target
                    prize = new_prize_pokemon()
                    game.prize = prize
                    game.target = random_guessing_number_target()

                    game.save()
                    next_prize = json.dumps(PokemonSerializer(game.prize).data)
                else:
                    game.tried += 1
                    if game.tried == 3:
                        game.tried = 0


                        prize = new_prize_pokemon()
                        game.prize = prize
                        game.target = random_guessing_number_target()
                        game.save()

                        next_prize = json.dumps(PokemonSerializer(game.prize).data)
                game.save()

            data = {
                "tried": game.tried,
                "reply": reply,
                "prize_next": next_prize,
                "prize_rewarded": rewarded_prize,
            }

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

            trained_pokemons_serialized = PokemonSerializer(
                trained_pokemons, many=True
            ).data
            trained_pokemons_serialized_json = json.dumps(trained_pokemons_serialized)

            data = {"pokemons": trained_pokemons_serialized_json}
            return JsonResponse(data, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({}, status=400)
    return JsonResponse(status=500)


def unowned_pokedex(request: HttpRequest) -> HttpResponse:
    print("[unowned_pokedex]")
    if request.method == "GET":
        try:
            (user, _) = a.authenticate(request)

            pokemons = Pokemon.objects.filter(Q(trainer=user)).select_related("pokedex")

            pokedex_ids = set()

            [pokedex_ids.add(pokemon.pokedex.id) for pokemon in pokemons]

            pokedex_not = [
                pokedex.pokename
                for pokedex in Pokedex.objects.exclude(id__in=pokedex_ids)
            ]

            return JsonResponse({"pokedex": pokedex_not}, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({}, status=400)
    return JsonResponse(status=500)
