# Generated by Django 3.2.7 on 2021-11-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarmbutton', '0003_auto_20211025_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caretaker',
            name='fathers_name',
            field=models.CharField(max_length=150, verbose_name='По батькові'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='birth_year',
            field=models.IntegerField(verbose_name='Рік народження'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fathers_name',
            field=models.CharField(max_length=150, verbose_name='По батькові'),
        ),
    ]
