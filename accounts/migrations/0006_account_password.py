# Generated by Django 5.0.6 on 2024-05-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_account_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
