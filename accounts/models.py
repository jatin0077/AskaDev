from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from io import BytesIO
from django.core.files import File
import os, uuid


class ProgrammingLanguage(models.Model):
	language = models.CharField(max_length=256)
	bg_color = models.CharField(max_length=50,default='#000000'); 
	def __str__(self):
		return self.language

	class Meta:
		ordering = ['language']

# class UserProfile(models.Model):
# 	id = models.UUIDField(
# 		primary_key=True,
# 		default=uuid.uuid4,
# 		editable=False
# 	)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	bio = models.TextField(max_length=200, help_text='A Short Bio about yourself')
# 	website = models.URLField(blank=True, null=True)
# 	profile_picture = models.ImageField(upload_to='static/images/profile_picture', max_length=255, blank=True, default='')
# 	experience = models.PositiveIntegerField(help_text='Exp. in years')
# 	languages = models.ManyToManyField(ProgrammingLanguage)
# 	follows = models.ManyToManyField('UserProfile',blank=True, related_name='following')
# 	followers = models.ManyToManyField('UserProfile', blank=True)
# 	points = models.PositiveIntegerField(default=0)
# 	def __str__(self):
# 		return str(self.user)
	# def save(self, *args, **kwargs):
		# new_image = compress(self.profile_picture)
		# self.profile_picture = new_image
		# super().save(*args, **kwargs)
class CustomUser(AbstractUser):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	bio = models.TextField(max_length=200, help_text='A Short Bio about yourself')
	website = models.URLField(blank=True, null=True)
	profile_picture = models.ImageField(upload_to='static/images/profile_picture', max_length=255, blank=True, default='')
	experience = models.PositiveIntegerField(help_text='Exp. in years')
	languages = models.ManyToManyField(ProgrammingLanguage)
	follows = models.ManyToManyField('UserProfile',blank=True, related_name='following')
	followers = models.ManyToManyField('UserProfile', blank=True)
	points = models.PositiveIntegerField(default=0)
	
	def __str__(self):
		return str(self.user)
	