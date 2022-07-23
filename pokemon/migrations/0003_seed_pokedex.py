# Generated by Django 4.0.6 on 2022-07-22 23:22

from django.db import migrations, models

import csv


def seed_pokemon(Pokemon: models.Model):
    pass


def seed_during_migration(apps, _):
    Pokemon = apps.get_model("pokemon", "Pokedex")

    with open("./pokemon.csv") as f:
        reader = csv.reader(f)

        seed_count = 0
        for row in reader:
            p = Pokemon.objects.create(
                pokename=row[0],
                health_point=row[1],
                attack=row[2],
                defense=row[3],
                type=row[4],
            )
            seed_count += 1
        print(f"Seeded pokedex with {seed_count} entries")


def unseed_during_migration(apps, _):
    Pokemon = apps.get_model("pokemon", "Pokedex")
    Pokemon.objects.all().delete()
    print(f"Unseeded pokedex entries")


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon", "0002_pokedex"),
    ]

    operations = [
        migrations.RunPython(seed_during_migration, unseed_during_migration),
    ]