from django.conf.urls.defaults import * 
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                        url(r'^review/(?P<product_id>\d+)/$',
                            'checkout.views.get_cart',
                            name='cart_review'),
                        url(r'^checkout/success/$',
                            'checkout.views.success',
                            name='paypal_success'),
                        url(r'checkout/cancel/$',
                            'checkout.views.cancel',
                            name='paypal_cancel'),
                        (r'^checkout/ipn48710/',
                            include('paypal.standard.ipn.urls')),
                       )
