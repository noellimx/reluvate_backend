from django.urls import path
from . import views as handlers


app_name = "pokemon"
urlpatterns = [
    path("hello/", handlers.say_hello, name="hello"),
    path(
        "is-my-access-token-valid/",
        handlers.is_access_token_valid,
        name="is-my-access-token-valid",
    ),
    path(
        "how-many-tries-already/",
        handlers.how_many_tries_already,
        name="how-many-tries-already",
    ),
    path("guess/", handlers.guess, name="guess"),
    path("owned-pokemon/", handlers.owned_pokemon, name="owned-pokemon"),
    path("unowned-pokedex/", handlers.unowned_pokedex, name="unowned-pokedex"),
]
