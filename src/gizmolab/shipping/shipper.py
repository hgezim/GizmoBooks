"""Taken from Satchmo."""

# Note, make sure you use decimal math everywhere!
from decimal import Decimal
from django.core.cache import cache
from django.template import loader, Context
from django.utils.safestring import mark_safe
from django.conf import settings 
import datetime
import logging
import urllib2

try:
    from xml.etree.ElementTree import fromstring, tostring
except ImportError:
    from elementtree.ElementTree import fromstring, tostring

log = logging.getLogger('canadapost.shipper')

class BaseShipper(object):
    def __init__(self, cart=None, contact=None):
        self._calculated = False
        self.cart = cart
        self.contact = contact 
        self._calculated = False
        
        if cart or contact:
            self.calculate(cart, contact)
        
    def calculate(self, cart, contact):
        """
        Perform shipping calculations, separated from __init__ so that the object can be 
        used for keys and labels more easily.
        """
        self.cart = cart
        self.contact = contact
        self._calculated = True

class Shipper(BaseShipper):
    
    def __init__(self, dest, product, cart=None, contact=None, service_type=None):

        self._calculated = False
        self.cart = cart
        self.product = product
        self.dest = dest
        self.contact = contact
        if service_type:    
            self.service_type_code = service_type[0]
            self.service_type_text = service_type[1]
        else:
            self.service_type_code = '99'
            self.service_type_text = 'Uninitialized'

        self.id = u'canadapost-%s' % (self.service_type_code)
  
    def __str__(self):
        '''
          This is mainly helpful for debugging purposes
        '''

        return 'Canada Post'

    def __unicode__(self):
        '''
          As is this.
        '''

        return 'Canada Post'
    
    def description(self):
        '''
          A basic description that will be displayed to the user when 
          selecting their shipping options
        '''

        return _('Canada Post - %s' % self.service_type_text)

    def cost(self):
        '''
          Complex calculations can be done here as long as the return 
          value is a decimal figure
        '''

        assert(self._calculated)
        return(Decimal(self.charges))

    def method(self):
        '''
          Describes the actual delivery service (Mail, FedEx, DHL, UPS, etc)
        '''

        return _('Canada Post')

    def expectedDelivery(self):
        '''
          Can be a plain string or complex calcuation 
          returning an actual date
        '''

        if str(self.delivery_days) <> '1':
            return _('%s business days' % self.delivery_days)
        else:
            return _('%s business day' % self.delivery_days)
    
    def valid(self, order=None):
        '''
        Can do complex validation about whether or not this
        option is valid. For example, may check to see if the 
        recipient is in an allowed country or location.
        '''

        return self.is_valid

    def _process_request(self, connection, request):
        '''
          Post the data and return the XML response
        '''
        conn = urllib2.Request(url=connection, data=request.encode("utf-8"))
        f = urllib2.urlopen(conn, timeout=3)
        all_results = f.read()
        self.raw = all_results
        print all_results
        return(fromstring(all_results))
    
    def calculate(self):
        '''
          Based on the chosen Canada Post method, we will do our call(s) 
          to Canada Post and see how much it will cost. We will also need 
          to store the results for further parsing and return via the
          methods above.
        '''
        log.debug("Starting Canada Post calculations")
            
        self.delivery_days = '3 - 4' #Default setting for ground delivery
        seller = self.product.owner
        self.is_valid = False
        error = False
        self.charges = 0

        if not settings.CPCID:
            log.warn("No CPCID found in settings")
            return
        connection = settings.CONNECTION
        
        configuration = {
            'cpcid': settings.CPCID,
            'turn_around_time': settings.TURN_AROUND_TIME,
            'default_weight': settings.DEFAULT_WEIGHT,
            'default_length': settings.DEFAULT_LENGTH,
            'default_width': settings.DEFAULT_WIDTH,
            'default_height': settings.DEFAULT_HEIGHT
        }
        c = Context({
                'config': configuration,
                'product': self.product,
                'destination': self.dest,
                'seller': seller,
            })
        
        t = loader.get_template('shipping/canadapost.xml')
        request = t.render(c)
        print request
        self.is_valid = False
        
        
        self.verbose_log("Requesting from Canada Post [%s]", request)
        tree = self._process_request(connection, request)
        self.verbose_log("Got from Canada Post [%s]", self.raw)
            
        try:
            status_code = tree.getiterator('statusCode')
            status_val = status_code[0].text
            self.verbose_log("Canada Post Status Code for product #%s = %s", int(self.product.id), status_val)
        except AttributeError:
            status_val = "-1"
            
        if status_val == '1':
            self.is_valid = False
            self._calculated = False
            all_rates = tree.getiterator('product')

            for rate in all_rates:
                self.verbose_log("Got product id from cp: %s", rate.attrib['id'])
                if self.service_type_code == rate.attrib['id']:
                    self.charges = Decimal(rate.find('.//rate').text)
                    #YYYY-MM-DD
                    delivery_date = rate.find('.//deliveryDate').text
                    shipping_date = rate.find('.//shippingDate').text
                    self.delivery_days = datetime.date(
                                            int(delivery_date[:4]),
                                            int(delivery_date[5:7]),
                                            int(delivery_date[8:])) - \
                                         datetime.date(
                                            int(shipping_date[:4]),
                                            int(shipping_date[5:7]),
                                            int(shipping_date[8:]))
                    self.delivery_days = self.delivery_days.days
                    self.is_valid = True
                    self._calculated = True

            if not self.is_valid:
                self.verbose_log("Canada Post Cannot find rate for code: %s [%s]", self.service_type_code, self.service_type_text)
              
    def verbose_log(self, *args, **kwargs):
            log.debug(*args, **kwargs)
