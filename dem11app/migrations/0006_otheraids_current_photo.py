# Generated by Django 4.2.4 on 2023-11-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dem11app", "0005_rename_medcicine_receiver_medicine"),
    ]

    operations = [
        migrations.AddField(
            model_name="otheraids",
            name="current_photo",
            field=models.ImageField(blank=True, null=True, upload_to="otheraids/"),
        ),
    ]
