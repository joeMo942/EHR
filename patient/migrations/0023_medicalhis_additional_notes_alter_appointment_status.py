# Generated by Django 5.0.6 on 2024-05-27 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0022_patient_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalhis',
            name='additional_notes',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Declined', 'Declined'), ('Not Paid', 'Not Paid'), ('Completed', 'Completed'), ('cancel_request', 'cancel_request')], default='Pending', max_length=50),
        ),
    ]
