# Generated by Django 4.2.4 on 2023-11-14 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dem11app", "0007_alter_otheraids_current_photo_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="req_med",
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
                ("medicine", models.CharField(max_length=250)),
                ("quantity", models.PositiveIntegerField()),
                ("disease", models.CharField(max_length=150)),
                (
                    "prescription_photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="media/prescriptions/"
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
        migrations.AlterField(
            model_name="otheraids",
            name="current_photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/otheraids/"
            ),
        ),
        migrations.DeleteModel(
            name="receiver",
        ),
    ]
