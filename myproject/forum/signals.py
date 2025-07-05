from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


'''
Django-signals are located in this file.
The profile is created automatically when the user registers (it's signal!).
When someone registers, Django creates a User object.
'''


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  # **kwargs needed for potential additional parameters
    if created:
        UserProfile.objects.create(user=instance)


"""
sender: the model the signal responds to (User)
instance: the User object itself that was just created or updated
created: True if the object has just been created
**kwargs: extra data from Django that you should accept even if i don't use it
"""
