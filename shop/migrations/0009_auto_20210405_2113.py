# Generated by Django 3.1.7 on 2021-04-05 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_added_timestamp_fields_to_order_and_product_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='products/thumbnails/default_thumbnail.png', upload_to='products/thumbnails'),
        ),
    ]
