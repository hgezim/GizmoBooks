from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from cart import Cart
from cart import ItemInAnotherCart
from textbook.models import Book_Copy
from shipping.models import Shipping
from mooi.models import Location
from mooi.forms import LocationForm
from mooi.utils import get_location
from paypal.standard.forms import PayPalPaymentsForm


def add_to_cart(request, product_id, quantity=1):
    book_copy = Book_Copy.objects.get(pk=product_id)
    cart = Cart(request)
    cart.add(product, product.unit_price, quantity)

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)

def get_cart(request, product_id, location_form_class=LocationForm):
    """Clear shopping cart and add new book_copy with product_id to it."""
    
    to_location = get_location(request.session)
    # set location form if no location is detected
    if request.method == "POST":
        location_form = location_form_class(request.POST)
        if location_form.is_valid():
            location_form.save(request)
            return HttpResponseRedirect(request.path)
    elif to_location:
        location_form = location_form_class(initial={'location': to_location.id})
    else:
        location_form = location_form_class()
    
    # get and clear cart, if not clear
    cart_errors = []
    cart = Cart(request)
    cart.clear()
    
    book_copy = Book_Copy.objects.get(pk=product_id)
    try:
        cart.add(product=book_copy, unit_price=str(book_copy.price), quantity=1)
    except ItemInAnotherCart:
        cart_errors.append("Ouch! Someone beat you to this book. Try again in a few minutes; perhaps they won't buy it, afterall.")
    
    from_location = book_copy.owner.profile.postal_code.location
    
    # Get shipping price if we already calculated it for the item
    #    to ship from the specified location to it's destination
    shipping = None
    try:
        shipping = Shipping.objects.get(object_id=book_copy.id,
                                        from_location=from_location,
                                        to_location=to_location)
    except Shipping.DoesNotExist:
        if to_location:
            shipping = Shipping(item=book_copy,
                                from_location=from_location,
                                to_location=to_location)
            shipping.save()
    
    if shipping:
        try:    
            cart.add(shipping, str(shipping.price), 1)
        except ItemInAnotherCart:
            pass
    
    # do paypal form after all the items have been added
    current_site = Site.objects.get_current()
    
    form = None
    if not cart_errors and not shipping:
        cart_errors.append("Please specify your city at the top of the page, so we can calculate your shipping costs.")
    elif not cart_errors and shipping:
        paypal_dict = {
            "cmd": "_cart",
            "currency_code":"CAD",
            "tax":"0.00",
            "amount_1": book_copy.price,
            "shipping_1": shipping.price,
            "no_note": "0",
            "no_shipping": "2",
            "upload": 1,
            "item_number_1": book_copy.id,
            #truncate to 127 chars, papal limit 
            "item_name_1": book_copy.book.title[:126],
            "quantity_1": 1,
            "custom": book_copy.id,
            "return_url": current_site.domain + reverse('paypal_success'),
            "notify_url": current_site.domain + reverse('paypal-ipn'), #defined by paypal module
            "cancel_return": current_site.domain + reverse('paypal_cancel')               
        } 

        form = PayPalPaymentsForm(initial=paypal_dict)    
    
    extra_context = {'form': form,
                    'location_form': location_form,
                    'location': to_location,
                    'book_copy': book_copy,
                    'cart_errors': cart_errors}
    context = RequestContext(request, dict(cart=Cart(request)))
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response('cart/checkout.html', context)

def cancel(request):
    messages.info(request, "Your book order has been canceled.")
    return HttpResponseRedirect(reverse('main'))

def success(request):
    messages.info(request, "Thanks! Your purchase was successful and will be shipped soon.")
    return HttpResponseRedirect(reverse('main'))