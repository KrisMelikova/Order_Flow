# Generated by Django 3.2.4 on 2021-06-11 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_order_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='details',
        ),
    ]