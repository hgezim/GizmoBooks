from django import forms

from models import Location, PostalCode
from utils import set_location

class LocationForm(forms.Form):
    """Form for location.
    
    Form postal code or Location added, set session variables:
        'country_name', 'country_code', 'region_name', 'city', 'postal_code'.
    
    """
    location = forms.ChoiceField(label = "Select your city", choices = Location.objects.city_list())
            
    def clean_location(self):
        """Ensure selection is a Canadian city."""
        
        location_id = self.cleaned_data['location']
        try:
            Location.objects.get(id=location_id)
            return location_id
        except Location.DoesNotExist:
            raise forms.ValidationError(["That's not a Canadian city. Please choose a Canadian city."])
    
    def save(self, request):
        location_id = self.cleaned_data['location']
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return
        
        set_location(request, location.postalcode_set.all()[0])
        return location