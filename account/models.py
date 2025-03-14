from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.conf import settings
from custom_storages import MediaStorage
from recipe.models import Recipe, Ingredient, PreparationStep


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    featured_image = CloudinaryField("image", default="placeholder")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="following", blank=True)
    favorite_recipes = models.ManyToManyField(
        "recipe.Recipe", related_name="favorited_by", blank=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
