# Generated by Django 5.1.2 on 2024-10-19 22:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0001_alter_game_name"),
        ("mates", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="mategameinfo",
            name="game",
            field=models.ForeignKey(db_column="game_id", on_delete=django.db.models.deletion.CASCADE, to="games.game"),
        ),
        migrations.AlterUniqueTogether(
            name="mategameinfo",
            unique_together={("user", "game")},
        ),
    ]
