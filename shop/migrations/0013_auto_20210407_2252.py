# Generated by Django 3.1.7 on 2021-04-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20210407_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='total_sum',
            field=models.FloatField(default=0, verbose_name='Order total sum'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
    ]
