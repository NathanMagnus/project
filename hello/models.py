from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

#categories for restaurants
class HICategory(models.Model):
	category = models.CharField(max_length=20, primary_key=True)
	min_value = models.FloatField()
	max_value = models.FloatField()
	def __unicode__(self):
		return "%s: %s - %s" % (self.category, self.min_value, self.max_value)

class Location(models.Model):
	countryChoices = (
		(u'CA', u'Canada'),
		(u'US', u'United States'),
	)
	cityChoices = (
		(u'Regina', u'Regina'),
		(u'Saskatoon', u'Saskatoon'),
	)
	city = models.CharField(max_length=50, choices=cityChoices)
	region = models.CharField(max_length=100)
	province = models.CharField(max_length=2, choices=((u'SK',u'Saskatchewan'),))
	country = models.CharField(max_length=3, choices=countryChoices)
	def __unicode__(self):
		return "%s - %s, %s, %s"%(self.region, self.city, self.province, self.country)



class RegistrationForm(forms.Form):
	query = Location.objects.all()
	username = forms.CharField(max_length=30, label="Username:")
	password = forms.CharField(max_length=100, label="Password:", widget=forms.PasswordInput())
	password_again = forms.CharField(max_length=100, label="Password (again):", widget=forms.PasswordInput())
	first_name = forms.CharField(max_length=30, label="First Name")
	last_name = forms.CharField(max_length=30, label="Last Name")
	email = forms.EmailField(min_length=5, max_length=50)
	street_address = forms.CharField(max_length=75)
	location = forms.ModelChoiceField(queryset=query, empty_label=None)

class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	location = models.ForeignKey(Location)	
	visible = models.BooleanField(default = True)
	street_address = models.CharField(max_length=50)
	health_inspection_status = models.IntegerField(default=0)
	combined = models.FloatField(default=0)
	cleanliness = models.FloatField(default=0)
	food_quality = models.FloatField(default=0)
	atmosphere = models.FloatField(default=0)
	wait_time = models.FloatField(default=0)
	comment_count = models.IntegerField(default=0)
	chain = models.CharField(max_length=50, default="")
	def __unicode__(self):
		return "%s - %s" % (self.name, self.street_address)


class Favourite(models.Model):
	user = models.ForeignKey(User)
	restaurant = models.ForeignKey(Restaurant)
	position = models.IntegerField()


	
class Comment(models.Model):
	comment = models.TextField()
	author = models.ForeignKey(User)
	restaurant = models.ForeignKey(Restaurant)
	combined = models.FloatField(default=0)
	cleanliness = models.FloatField(default=0)
	food_quality = models.FloatField(default=0)
	atmosphere = models.FloatField(default=0)
	wait_time = models.FloatField(default=0)
	id = models.IntegerField(primary_key = True, unique=True)

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('comment', 'food_quality', 'cleanliness', 'atmosphere', 'wait_time')
#	comment = forms.CharField(widget=forms.Textarea(), required=False)
#	food_quality = forms.FloatField(label="Food Quality", required=False)
#	cleanliness = forms.FloatField(required=False)
	#service = forms.FloatField(label="Quality of Service:", required=False)
#	atmosphere = forms.FloatField(required=False)
#	wait_time = forms.FloatField(label="Wait Time", required=False)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'comment', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time')	
	search_fields = ['comment', 'restaurant']


class UserProfile(models.Model):
	street_address = models.CharField(max_length=75)
	location = models.ForeignKey(Location)
	user = models.ForeignKey(User, unique=True)
	def __unicode__(self):
		return "%s" % (self.user.username)

	
	
#health inspection item
class HIItem(models.Model):
	number = models.IntegerField(unique = True, primary_key=True)
	description = models.TextField()
	severity = models.IntegerField()
	def __unicode__(self):
		return "%s"%(self.number)

class HealthReport(models.Model):
	date = models.CharField(max_length=100)#DateTimeField()
	health_inspection_score = models.IntegerField(default=0)
	restaurant = models.ForeignKey(Restaurant)
	priority = models.CharField(max_length=20)
	type = models.CharField(max_length=20)
	items = models.ManyToManyField(HIItem)
	def __unicode__(self):
		return "%s %s %s" % (self.restaurant.name, self.health_inspection_score, self.date)
