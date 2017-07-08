import re

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile

def get_or_create_user_from_email(email):
    """Create a username with a random password, given an email.
    
    Signal user_registred is not sent.
    The username is generated from the email.
    
    Requires: django-registraion
    """
    
    site = Site.objects.get_current()
    
    try:
        user = User.objects.get(email=email)
        created = False
    except:
        username = generate_username_from_email(email)
        password = User.objects.make_random_password()
        user = RegistrationProfile.objects.create_inactive_user(username=username,
                                                                password=password,
                                                                site=site,
                                                                email=email, send_email=False)
        created = True
        
    return user, created

        
def generate_username_from_email(email):
    """Generate a unique username from the email given. 
    
    For example, with phill@example.com, it will return phill, if not taken,
        otherwise it will append a number starting from 2.
    """
    
    username_guess = re.search("(.+)@", email).group(1)
    username_guess = re.sub(r'[^a-zA-Z0-9_]', '', username_guess)
    postfix = 1
    username = username_guess
    while User.objects.filter(username=username):
        postfix += 1
        username = "%s%d" % (username_guess, postfix)
        
    return username
