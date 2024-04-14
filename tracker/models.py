from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} {self.phone_number}"

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)


class Challenge(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)
    challenge = models.CharField(max_length=200)
    challenge_date = models.DateField()
    def __str__(self):
        return f"{self.profile} {self.challenge} {self.challenge_date}"
    status = models.BooleanField(default=False)
