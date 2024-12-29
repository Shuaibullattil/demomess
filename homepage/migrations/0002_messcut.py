# Generated by Django 5.1.2 on 2024-10-27 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessCut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromDate', models.DateField()),
                ('toDate', models.DateField()),
                ('mess_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mess_no_messcuts', to='homepage.student')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_messcuts', to='homepage.student')),
            ],
        ),
    ]