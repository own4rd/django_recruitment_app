# Generated by Django 3.2.6 on 2022-06-12 08:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
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
                    "name",
                    models.CharField(max_length=30, unique=True, verbose_name="Nome"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Demissões", "Layoffs"),
                            ("Contratação parada", "Hiring Freeze"),
                            ("Contratando", "Hiring"),
                        ],
                        default="Contratando",
                        max_length=30,
                        verbose_name="Status",
                    ),
                ),
                (
                    "last_update",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Atualização"
                    ),
                ),
                ("application_link", models.URLField(blank=True, max_length=100)),
            ],
        ),
    ]
