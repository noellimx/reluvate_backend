# Generated by Django 4.1rc1 on 2022-07-25 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon", "0007_alter_pokemon_trainer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemon",
            name="pokedex_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pokemon.pokedex"
            ),
        ),
    ]