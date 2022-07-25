
from rest_framework import serializers


from pokemon.models import GuessGame, Pokedex, Pokemon




class PokedexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokedex
        fields = ["pokename"]
class PokemonSerializer(serializers.ModelSerializer):
    pokedex = PokedexSerializer( read_only = True)
    class Meta:
        model = Pokemon
        fields = ["id","pokedex"]
