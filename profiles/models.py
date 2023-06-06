from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from music.models import Audio


# Create your models here.


# When user signup, create one profile for each user using - OneToOneField
class UserProfile(models.Model):
    """ A user profile model for capturing summary of user activity.
    models.cascade deletes user profile when user is deleted
    """

    # Get each user who registers using the imported User model above
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Create variable to get audio saved by registered users
    fav_audio = models.ManyToManyField("music.Audio")

    # At login, return user's username on designated page -eg- profile.html
    def __str__(self):
        return self.user.username


# Attach quick receiver for post-save events from user model above
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    As user registers/saves, automatically create or update user profile
    if already existed. All users created b4 creating the UserProfile model
    won't able to login again. Comment out d lines below to allow them login.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
