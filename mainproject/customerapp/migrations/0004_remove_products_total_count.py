# Generated by Django 5.0.1 on 2024-01-18 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0003_products_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='total_count',
        ),
    ]
