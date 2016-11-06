from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
	summary = models.CharField(max_length=250)
	description = models.TextField()
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	likes = models.IntegerField()
	deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.summary

class Answer(models.Model):
	description	= models.TextField()
	user = models.ForeignKey(User)
	question = models.ForeignKey('Question')
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	likes = models.IntegerField()
	deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.description

class Category(models.Model):
	name = models.CharField(max_length=80)
	sort_id = models.IntegerField()

	def __str__(self):
		return self.name 

class SubCategory(models.Model):
	name = models.CharField(max_length=80)
	sort_id = models.IntegerField()
	category = models.ForeignKey('Category')

	def __str__(self):
		return self.name 

class QLike(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey('Question')
	created_date = models.DateTimeField(auto_now_add=True)
	like = models.BooleanField()

	class Meta:
		unique_together = (('user', 'question'),)

class ALike(models.Model):
	user = models.ForeignKey(User)
	answer = models.ForeignKey('Answer')
	created_date = models.DateTimeField(auto_now_add=True)
	like = models.NullBooleanField()

	class Meta:
		unique_together = (('user', 'answer'),)			

class Tag(models.Model):	
	subcat = models.ForeignKey('SubCategory')
	question = models.ForeignKey('Question')

