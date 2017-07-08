import re

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from accounts.utils import generate_username_from_email
from mooi.models import FBProfile, Profile, PostalCode, Location

import facebook

# Authentication back-end (django.contrib.auth)
class EmailModelBackend(ModelBackend):
    """Backend to login with emails only.
    
    We don't provide get_user() as we are inheriting from ModelBackend.
    """
    
    def authenticate(self, username=None, password=None):
        kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
        
class FacebookProfileBackend(ModelBackend):
    """ Authenticate a facebook user and autopopulate facebook data into the users profile. """
    
    def authenticate(self, fb_uid=None, fb_graphtoken=None):
        """ If we receive a facebook uid then the cookie has already been validated."""

        if fb_uid and fb_graphtoken:
            # see if they logged in before with FB, before
            try:
                fb_profile = FBProfile.objects.get(fb_id=fb_uid)
                return fb_profile.user
            except FBProfile.DoesNotExist:
                pass
            
            graph = facebook.GraphAPI(fb_graphtoken)
            if not graph:
                return None
            me = graph.get_object('me')
            if not me or not me.get('email'):
                return None
            email = me['email']
            
            # create user if not already registered with that email
            try:
                # if user is already registered with that email, trust it
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                username = generate_username_from_email(email)
                password = User.objects.make_random_password()
                user = User(username=username, email=email, password=password)
            
            # update other info
            if me.get('first_name'): user.first_name = me['first_name']
            if me.get('last_name'): user.last_name = me['last_name']
            
            user.is_active = True
            user.save()
            
            # create fb_profile info
            fb_profile = FBProfile(user=user, fb_id=fb_uid)
            try:
                if me.get('hometown'): fb_profile.hometown = me.get('hometown')
                if me.get('work'): fb_profile.work = me.get('work')
                if me.get('location'): fb_profile.location = me.get('location').get('name')
                if me.get('gender'): fb_profile.gender = me.get('gender')
                if me.get('education'): fb_profile.education = me.get('education')
                if me.get('link'): fb_profile.link = me.get('link')
            except:
                pass
            fb_profile.save()
            
            # save info to User Profile 
            location_list = [item.strip() for item in fb_profile.location.split(',')]
            try:
                region = Location.objects.get_region_shortname(location_list[1])
                location = Location.objects.get(city=location_list[0], region=region)
                postal_code = PostalCode.objects.filter(location=location)[0]
            except Location.DoesNotExist:
                postal_code = None
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user, postal_code=None)
            profile.postal_code = postal_code
            profile.save()
            
            return user