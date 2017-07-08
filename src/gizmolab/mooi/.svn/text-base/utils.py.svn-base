"""Utility functions for mooi (locatoin and profile based.)"""

from models import Location, PostalCode

def get_location(session):
    """Return a Location or None.
    
    'session' is a dict with:
        'city', 'region_name', 'country_name', 'country_code', 'postal_code' set.
    """
    
    city = session.get('city', None)
    region = session.get('region_name', None)
    country = session.get('country_name', None)
    country_code = session.get('country_code', None)
    postal_code = session.get('postal_code', None)
    
    if not is_not_set(postal_code): #postal code is set
        # remove whitespaces
        postal_code = postal_code.replace(' ','')
        try:
            return PostalCode.objects.get(code=postal_code).location
        except PostalCode.DoesNotExist:
            pass
    
    if is_not_set(city) or is_not_set(region) or is_not_set(country):
        return None
    
    try:
        location = Location.objects.get(city=city, region=region, country=country)
        return location
    except Location.DoesNotExist:
        return None
        
def is_not_set(string):
    """Return true if string is not set or set to '---'."""
    
    NAN_STRING = "---"
    
    return string==NAN_STRING or string=="" or string is None

def set_location(request, postal_code):
    """Set location in the current session.
    
    Sets 'city', 'region_name', 'country_name', 'country_code', and 'postal_code'.
    "postal_code" is an object of PostalCode model.
    """
    
    request.session['city'] = postal_code.location.city
    request.session['region_name'] = postal_code.location.region
    request.session['country_name'] = postal_code.location.country
    request.session['country_code'] = postal_code.location.country_code
    request.session['postal_code'] = postal_code.code
