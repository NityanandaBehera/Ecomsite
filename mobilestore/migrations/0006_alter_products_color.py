# Generated by Django 4.0.3 on 2022-07-01 19:18

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobilestore', '0005_alter_products_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default='', image_field='image', max_length=18, samples=None),
        ),
    ]
