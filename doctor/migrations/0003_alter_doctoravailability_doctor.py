# Generated by Django 5.0.6 on 2024-05-24 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoravailability',
            name='doctor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor'),
        ),
    ]
