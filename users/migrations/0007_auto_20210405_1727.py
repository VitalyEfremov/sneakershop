# Generated by Django 3.1.7 on 2021-04-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210405_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='users/profile_pics/default_user_image.png', upload_to='users/profile_pics'),
        ),
    ]
