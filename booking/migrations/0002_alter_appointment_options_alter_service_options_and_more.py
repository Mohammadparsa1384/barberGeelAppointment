# Generated by Django 4.2.2 on 2024-10-13 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['-created'], 'verbose_name': 'نوبت', 'verbose_name_plural': 'نوبت ها'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'سرویس', 'verbose_name_plural': 'سرویس ها'},
        ),
        migrations.AlterField(
            model_name='appointment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL, verbose_name='مشتری'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='services',
            field=models.ManyToManyField(to='booking.service', verbose_name='خدمات'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(verbose_name='زمان'),
        ),
        migrations.AlterField(
            model_name='service',
            name='desc',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.PositiveBigIntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان'),
        ),
    ]
