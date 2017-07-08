#encoding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class FBProfile(models.Model):
	"""Store information for users loggining in with Facebook."""
	
	user = models.OneToOneField(User) #django user
	fb_id = models.CharField(max_length=25, unique=True)
	hometown = models.CharField(max_length=300, blank=True)
	work = models.TextField(blank=True)
	location = models.CharField(max_length=300, blank=True)
	gender = models.CharField(max_length=10, blank=True)
	education = models.TextField(blank=True)
	link = models.CharField(max_length=60, blank=True)

class Profile(models.Model):
	"""Store profile data for the user.
	
	If 'postal_code' is set to None, it means postal_code.location is confirmed
	If 'confirmed_postal_code' is set to True, postal_code.code is also confirmed
	"""
	
	user = models.OneToOneField(User)
	phone = models.CharField(max_length = 20, blank = True)
	credits = models.IntegerField(default=1)
	transaction_status = models.CharField(max_length = 20, blank=True)
	address = models.CharField(max_length=100, blank=True)
	postal_code = models.ForeignKey('PostalCode', null=True) # if this is set, city is confirmed
	confirmed_postal_code = models.BooleanField(default=False) # if this is set, postal_code is also confirmed

class PostalCode(models.Model):
	"""Store postal code and location.
	
	"confirmed_code" indicates whether postal code has been confirmed by user.
	"confimed_location" indicates whether location has been confirmed by user. 
	"""
	
	code = models.CharField(max_length=6)
	location = models.ForeignKey('Location')
	
	class Meta:
		unique_together = ('code','location') 
	
class LocationManager(models.Manager):
	def city_list(self):
		"""Return a list of tuples of cities.
		
		It looks like this: [(1, "Lethbridge, AB"), (2, "Calgary, AB")]
		"""
		city_list = [(location.id, "%s, %s" % (location.city, location.region)) for location in self.model.objects.all().order_by('city')] 
		city_list.insert(0, ('0','---'))
		return city_list
	
	def get_region_shortname(self, region):
		"""Return the shortname for a region, if we know it. Otherwise return what's passed."""
		region_dict = {"Alberta": "AB",
					   "British Columbia": "BC",
					   "Manitoba": "MB",
					   "New Brunswick": "NB",
					   "Newfoundland and Labrador": "NL",
					   "Newfoundland": "NL",
					   "Northwest Territories": "NT",
					   "Nova Scotia": "NS",
					   "Nunavut": "NU",
					   "Ontario": "ON",
					   "Prince Edward Island": "PE",
					   "Quebec": "QC",
					   "Qu�bec": "QC",
					   "Saskatchewan": "SK",
					   "Yukon": "YT" };
					   
		return region_dict.get(region) or region
	 

class Location(models.Model):
	"""Store locations."""
	
	city = models.CharField(max_length = 50)
	region = models.CharField(max_length = 2)
	country = models.CharField(max_length = 50)
	country_code = models.CharField(max_length = 2)
	
	#managers
	objects = LocationManager()
	
	def __unicode__(self):
		if self.region is not None:
			return self.city + ", " + self.region
		
		return self.city + ", " + self.country
	
	def clean(self):
		"""Ensure fields have appropriate data."""
		
				

def create_profile(sender, **kwargs):
	#sender -- model class
	#kwargs['instance'] -- actual instance being saved
	#kwargs['created'] -- A boolean; True if a new record was created.
	instance = kwargs['instance']
	created = kwargs['created']
	if created:
		try:
			Profile.objects.get(user=instance)
			return None # if profile already exits, do nothing
		except Profile.DoesNotExist:
			newProfile = Profile(user=instance, postal_code=None)
			newProfile.save()

post_save.connect(create_profile, sender=User)