# Generated by Django 5.0.6 on 2024-05-28 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0026_patient_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.ImageField(default='faces/default-profile.svg', upload_to='patient_images/'),
        ),
    ]
