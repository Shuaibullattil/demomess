# Generated by Django 5.1.2 on 2024-12-23 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_messbill'),
    ]

    operations = [
        migrations.AddField(
            model_name='messbill',
            name='totalFee',
            field=models.IntegerField(default=0),
        ),
    ]
