# Generated by Django 3.1.7 on 2021-04-04 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('title', 'brand')},
        ),
    ]
