# Generated by Django 5.0.1 on 2024-01-19 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0009_products_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='avg_rating',
            field=models.IntegerField(db_index=True, max_length=10, null=True),
        ),
    ]
