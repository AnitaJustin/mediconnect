# Generated by Django 4.2.4 on 2023-11-14 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dem11app", "0008_req_med_alter_otheraids_current_photo_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="saving_request",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "aid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dem11app.otheraids",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
