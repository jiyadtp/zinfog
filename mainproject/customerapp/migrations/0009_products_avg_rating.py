# Generated by Django 5.0.1 on 2024-01-19 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0008_productrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='avg_rating',
            field=models.CharField(db_index=True, max_length=10, null=True),
        ),
    ]