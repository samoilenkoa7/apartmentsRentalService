# Generated by Django 4.1.5 on 2023-01-07 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_apartmentpicture_pictures'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Post views count'),
        ),
    ]
