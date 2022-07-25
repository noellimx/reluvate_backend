# Generated by Django 4.1rc1 on 2022-07-25 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pokemon", "0006_alter_guessgame_trainer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemon",
            name="trainer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
