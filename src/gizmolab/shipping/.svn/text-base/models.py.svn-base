from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from decimal import Decimal

from mooi.models import Location
from shipper import Shipper


class Shipping(models.Model):
    # item as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('content_type', 'object_id') 
    from_location = models.ForeignKey(Location, verbose_name="from", related_name="shipments_from")
    to_location = models.ForeignKey(Location, verbose_name="to", related_name="shipments_to")
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="price")
    type = models.CharField(max_length = 4, choices=settings.SHIPPING_OPTIONS)
    date = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        dest = {'city': self.to_location.city,
                'region': self.to_location.region,
                'country_code': self.to_location.country_code,
                'postal_code': self.to_location.postalcode_set.all()[0].code
                }
        
        if self.from_location.city == self.to_location.city:
            self.type=settings.SHIPPING_OPTIONS[0][0]
            self.price = settings.GIZMOBOOKS_SHIPPING_PRICE
        else:
            self.type=settings.SHIPPING_OPTIONS[1][0]
            try:
                product = self.item
                shipping_calculator = Shipper(dest=dest, product=self.item, service_type=settings.SHIPPING_OPTIONS[1])
                shipping_calculator.calculate()
                self.price = shipping_calculator.cost()
            except:
                self.price = Decimal(settings.DEFAULT_SHIPPING_COST)
        
        super(Shipping, self).save(*args, **kwargs)