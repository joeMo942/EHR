# Generated by Django 5.0.6 on 2024-05-24 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_alter_doctoravailability_doctor'),
        ('patient', '0006_diagnosislu_medicationlu_symptomslu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, max_length=600, null=True)),
                ('crearated_at', models.DateTimeField(auto_now_add=True)),
                ('treatment_type', models.CharField(blank=True, max_length=100, null=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patient.appointment')),
                ('diagnosis', models.ManyToManyField(to='patient.diagnosislu')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
                ('medication', models.ManyToManyField(to='patient.medicationlu')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('symptoms', models.ManyToManyField(to='patient.symptomslu')),
            ],
        ),
    ]
