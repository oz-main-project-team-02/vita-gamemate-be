from django.db import migrations


def add_game_data(apps, schema_editor):
    Game = apps.get_model("games", "Game")
    Game.objects.create(name="리그 오브 레전드", image="path/to/lol_image.jpg")
    Game.objects.create(name="오버워치", image="path/to/overwatch_image.jpg")
    Game.objects.create(name="전략적 팀 전투", image="path/to/tft_image.jpg")
    Game.objects.create(name="배틀그라운드", image="path/to/bg_image.jpg")


def remove_game_data(apps, schema_editor):
    Game = apps.get_model("games", "Game")
    Game.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0001_initial"),  # 이전 마이그레이션 파일명으로 변경
    ]

    operations = [
        migrations.RunPython(add_game_data, remove_game_data),
    ]
