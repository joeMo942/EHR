# Generated by Django 5.0.6 on 2024-05-27 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_doctoravailability_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='doctoravailability',
            unique_together={('doctor', 'availability', 'date')},
        ),
    ]
