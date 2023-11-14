# Generated by Django 4.2.4 on 2023-11-14 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dem11app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="medicines",
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
                ("name", models.CharField(max_length=256)),
                ("dosage", models.CharField(max_length=50)),
                ("disease", models.CharField(max_length=100)),
                ("quantity", models.PositiveIntegerField()),
                ("expirydate", models.DateField()),
                ("contents", models.CharField(max_length=250)),
                ("manufacturer", models.CharField(max_length=80)),
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