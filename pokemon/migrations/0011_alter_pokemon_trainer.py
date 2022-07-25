# Generated by Django 4.1rc1 on 2022-07-25 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pokemon", "0010_alter_guessgame_prize"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemon",
            name="trainer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
