# Generated by Django 5.1.2 on 2024-12-21 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_alter_messcut_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messcut',
            name='student',
        ),
    ]
