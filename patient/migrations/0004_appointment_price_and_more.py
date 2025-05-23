# Generated by Django 5.0.6 on 2024-05-24 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_alter_doctor_user'),
        ('patient', '0003_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='availability_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctoravailability'),
        ),
    ]
