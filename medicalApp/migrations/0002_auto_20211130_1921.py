# Generated by Django 3.1.7 on 2021-11-30 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaldetails',
            name='medicine_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_detailss', to='medicalApp.medicine'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='medicalApp.company'),
        ),
    ]
