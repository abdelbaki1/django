# Generated by Django 3.1.3 on 2022-11-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20221128_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name_order',
            field=models.CharField(default='unknown', max_length=200),
        ),
    ]