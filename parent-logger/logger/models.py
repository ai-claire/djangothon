from django.db import models

# Create your models here.
class Insight(models.Model):
	dimensionX = models.IntegerField(default=0)
	dimensionY = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)
	# user_token = models.CharField(max_length=200,default="none",primary_key=True)
	insights = models.TextField(default="[]")
	url = models.CharField(max_length=200)
	file_name = models.CharField(max_length=200)
	html_filename = models.CharField(max_length=200)
	height = models.IntegerField(default=0)
