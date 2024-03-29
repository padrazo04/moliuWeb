# Generated by Django 4.0.2 on 2022-04-19 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("moliuWeb", "0002_alter_game_video_frame"),
    ]

    operations = [
        migrations.CreateModel(
            name="Posture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (-1, "Non Scored"),
                            (0, "Very Bad"),
                            (25, "Bad"),
                            (50, "Regular"),
                            (75, "Good"),
                            (100, "Very Good"),
                        ],
                        default=-1,
                        null=True,
                    ),
                ),
                ("image", models.CharField(max_length=250)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="moliuWeb.game"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Frame",
        ),
    ]
