from django.db import models


class DummyModel(models.Model):

    number = models.IntegerField(null=False)


class Pokedex(models.Model):
    class PokeTypes(models.TextChoices):
        ELECTRIC = "Electric"
        FIGHTING = "Fighting"
        FIRE = "Fire"
        GRASS = "Grass"
        GROUND = "Ground"
        NORMAL = "Normal"
        PSYCHIC = "Psychic"
        WATER = "Water"
        ROCK = "Rock"
        NONE = "None"

    pokename = models.CharField(max_length=255)
    health_point = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(
        choices=PokeTypes.choices, max_length=255, default=PokeTypes.NONE
    )


class GuessGame(models.Model):
    class Tried(models.IntegerChoices):
        NOT_YET = 0
        ONCE = 1
        TWICE = 2

    target = models.IntegerField()
    tried = models.IntegerField(choices=Tried.choices, default=Tried.NOT_YET)
    trainer = models.CharField(max_length=255)


class Pokemon(models.Model):
    trainer = models.CharField(max_length=255)
    pokedex_id = models.IntegerField()