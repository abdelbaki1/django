# Generated by Django 3.1.3 on 2022-11-28 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_name_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name_order',
            field=models.CharField(default='unknown', max_length=200),
        ),
    ]
