# Generated by Django 4.2.2 on 2024-10-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_service_slug_alter_service_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
