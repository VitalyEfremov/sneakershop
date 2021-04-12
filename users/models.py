from PIL import Image
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='users/profile_pics/default_user_image.png', upload_to='users/profile_pics')
    phone = models.CharField(max_length=256, blank=True, null=True)
    gender = models.CharField(
        max_length=6,
        choices=(('male', 'Male'), ('female', 'Female')),
        blank=True,
        null=True
    )
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        max_size = 300
        resize_ratio = min(max_size/img.width, max_size/img.height)

        if img.height > max_size or img.width > max_size:
            output_size = (img.height * resize_ratio, img.width * resize_ratio)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(self.image.path, 'JPEG')
