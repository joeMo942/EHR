# Generated by Django 5.0.6 on 2024-05-27 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0021_remove_test_resultfileds_testresultfield_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
