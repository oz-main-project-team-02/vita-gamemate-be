from django.db import migrations


def add_game_data(apps, schema_editor):
    Game = apps.get_model("games", "Game")
    Game.objects.create(name="lol", image="path/to/lol_image.jpg")
    Game.objects.create(name="overwatch", image="path/to/overwatch_image.jpg")
    Game.objects.create(name="tft", image="path/to/tft_image.jpg")
    Game.objects.create(name="bg", image="path/to/bg_image.jpg")


def remove_game_data(apps, schema_editor):
    Game = apps.get_model("games", "Game")
    Game.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0002_alter_game_name"),  # 이전 마이그레이션 파일명으로 변경
    ]

    operations = [
        migrations.RunPython(add_game_data, remove_game_data),
    ]
