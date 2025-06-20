from django.db import models

# My models here.

class User(models.Model):
    nickname = models.CharField(max_length=40, unique=True)  # Be sure to specify the field type in objects in Django ('models.CharField' - or other)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # The folder is created automatically on first boot.
    sex_choice = [
        ('Ж', 'Женский'),
        ('М', 'Мужской'),
    ]
    sex = models.CharField(max_length=1, choices=sex_choice)

    def __str__(self):
        return self.nickname

