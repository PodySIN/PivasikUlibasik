# Generated by Django 5.0.6 on 2024-05-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_beer_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="beer",
            name="Strength",
            field=models.FloatField(default=9.9),
        ),
    ]