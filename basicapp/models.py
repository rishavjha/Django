from django.db import models
from django.contrib.auth.models import User
# call user model
# Create your models here.

class UserProfileInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    #additional information
    profile_pic=models.ImageField(upload_to='profilepics',blank=True)
    # if user doesnot want to upload photo


    def __str__(self):
        return self.user.username
