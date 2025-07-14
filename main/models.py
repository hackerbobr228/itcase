from django.contrib.auth.models import User
from django.db import models

class AppItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    apk_file = models.FileField(upload_to='apk_files/', blank=True, null=True)
    image = models.ImageField(upload_to='app_images/', blank=True, null=True)  # <== добавлено поле

    def __str__(self):
        return self.title
