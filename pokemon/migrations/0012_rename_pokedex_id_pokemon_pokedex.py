# Generated by Django 4.1rc1 on 2022-07-25 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon", "0011_alter_pokemon_trainer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pokemon",
            old_name="pokedex_id",
            new_name="pokedex",
        ),
    ]
