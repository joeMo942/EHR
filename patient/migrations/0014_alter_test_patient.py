# Generated by Django 5.0.6 on 2024-05-26 00:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_remove_testlu_shortname_testfiled_shortname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient'),
        ),
    ]
