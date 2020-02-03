from django.db import models

class Url(models.Model):
	url=models.TextField(max_length=250)
	words = models.TextField(null=True)
	
	def __str__(self):
		return self.url
