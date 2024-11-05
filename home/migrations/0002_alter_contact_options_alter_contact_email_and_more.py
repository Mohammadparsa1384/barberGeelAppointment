# Generated by Django 4.2.2 on 2024-10-30 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'تماس', 'verbose_name_plural': 'تماس ها'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='نام و نام خاندوادگی'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='msg',
            field=models.TextField(verbose_name='پیام'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(max_length=20, verbose_name='موضوع'),
        ),
    ]
