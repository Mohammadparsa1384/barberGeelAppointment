# Generated by Django 4.2.2 on 2024-10-17 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_appointment_phone_number_alter_appointment_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['created'], 'verbose_name': 'نوبت', 'verbose_name_plural': 'نوبت ها'},
        ),
        migrations.AddField(
            model_name='appointment',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(verbose_name='تاریخ رزرو'),
        ),
    ]
