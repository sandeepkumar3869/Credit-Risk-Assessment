# Generated by Django 5.0.7 on 2024-07-20 03:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FraudDetectionApp", "0004_creditcardfraud"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoldPricePrediction",
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
                ("open_price", models.FloatField()),
                ("high_price", models.FloatField()),
                ("low_price", models.FloatField()),
                ("volume", models.FloatField()),
                ("change_percent", models.FloatField()),
                ("month", models.IntegerField()),
                ("target_price", models.FloatField()),
            ],
        ),
    ]