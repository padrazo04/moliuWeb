# Generated by Django 4.0.2 on 2022-06-02 11:51

from django.db import migrations, models
import moliuWeb.models


class Migration(migrations.Migration):

    dependencies = [
        ("moliuWeb", "0006_patient0_activity0"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="joints",
            field=models.FileField(upload_to=moliuWeb.models.jointsUploadPath),
            preserve_default=False,
        ),
    ]
