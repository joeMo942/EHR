# Generated by Django 5.0.6 on 2024-05-28 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.ImageField(default='images/faces/default-profile.svg', upload_to='profile_image/'),
        ),
    ]