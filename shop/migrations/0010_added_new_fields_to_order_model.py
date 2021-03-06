# Generated by Django 3.1.7 on 2021-04-07 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0009_auto_20210405_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+79999999999', max_length=128, region=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='post_code',
            field=models.CharField(default=123456, max_length=6, verbose_name='Post code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='receiver_first_name',
            field=models.CharField(default='John', max_length=50, verbose_name='First name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='receiver_last_name',
            field=models.CharField(default='Doe', max_length=50, verbose_name='Last name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.user'),
            preserve_default=False,
        ),
    ]
