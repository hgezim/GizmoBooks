import random
import re
import urllib2
import tempfile
from decimal import Decimal

from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.hashcompat import sha_constructor
from django.db.models import Min, Count
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import mail_managers

from pyaws import ecs
from mptt.models import MPTTModel
from shipping.models import Shipping
from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged

CONDITION_CHOICES = (
                    ('5.0','New'),
                    ('4.0','Used - Like New'),
                    ('3.0','Used - Very Good'),
                    ('2.0','Used - Good'),
                    ('1.0','Used - Acceptable'),
                    )

CONDITION_TYPES = ("new", "used",)

class BookManager(models.Manager):
    def with_data(self):
        pass

class Book(models.Model):    
    title = models.CharField(max_length = 400)
    ISBN = models.CharField(max_length = 20, blank = True)
    picture = models.ImageField(upload_to=settings.BOOK_IMAGE_DIR,
                            default="%s%s" % (settings.BOOK_IMAGE_DIR, settings.BOOK_DEFUALT_IMAGE))
    publisher = models.CharField(max_length = 100, blank = True)
    edition = models.CharField(max_length = 50, blank = True)
    published_date = models.DateField(blank = True, null = True)
    list_price = models.FloatField(null = True)
    subjects = models.ManyToManyField('Subject')    
    authors = models.ManyToManyField('Author')
    # these are all metric units (centimeters and kilograms)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    def get_authors(self):
        return ", ".join(["%s" % (k[0],) for k in self.authors.values_list('name')])
    
    def min_price(self):
        min_price = self.copies.filter(sold=False, activation_key="").aggregate(Min('price')).values()[0]
        return "%.2f" % (min_price)
    
    def used_count(self):
        # CONDITION_CHOICES[0][0] is the new condition
        used_count = self.copies.filter(sold=False, activation_key="", condition__lt=CONDITION_CHOICES[0][0]).count()
        return used_count
    
    def min_used_price(self):
        # CONDITION_CHOICES[0][0] is the new condition
        min_used_price = self.copies.filter(sold=False, activation_key="", condition__lt=CONDITION_CHOICES[0][0]).aggregate(Min('price')).values()[0]
        return min_used_price 
    
    def new_count(self):
        # CONDITION_CHOICES[0][0] is the new condition
        new_count = self.copies.filter(sold=False, activation_key="", condition=CONDITION_CHOICES[0][0]).count()
        return new_count
        
    def min_new_price(self):
        # CONDITION_CHOICES[0][0] is the new condition
        min_new_price = self.copies.filter(sold=False, activation_key="", condition=CONDITION_CHOICES[0][0]).aggregate(Min('price')).values()[0]
        return min_new_price
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book", args=(self.id,))
    
    def save(self, raw_book=None, *args, **kwargs):
        """Fetch data from Amazon if we have ISBN. Otherwise do a normal save."""

        if self.ISBN:
            
            # get book data
            if raw_book:
                book = raw_book
            else:            
                book = get_book_data(self.ISBN)
                
            if not book:
                raise LookupError('Amazon lookup couldn\'t be performed.')
                
            # assign data
            if hasattr(book, "ISBN"): self.ISBN = book.ISBN
            if hasattr(book, "Title"): self.title = book.Title
            if hasattr(book, "Publisher"): self.publisher = book.Publisher
            if hasattr(book, "Edition"): self.edition = book.Edition
            super(Book, self).save(*args, **kwargs) # save before adding many2many relationships
            if hasattr(book, "Author"):
                authors = book.Author
                if type(authors) == type(u''):
                    authors = [authors]
                for author_name in authors:
                    author = Author.objects.get_or_create(name=author_name)
                    # reference 0 because get_or_create returns a tuple: (object, created)
                    self.authors.add(author[0])
                    
            if hasattr(book, "PackageDimensions"):
                # these are divided by 100 because the units are:
                # hundredths-inches and hundreths-pounds
                if hasattr(book.PackageDimensions, "Height"):
                    self.height = inches_to_centimeters(Decimal(book.PackageDimensions.Height)/100)
                if hasattr(book.PackageDimensions, "Length"):
                    self.length = inches_to_centimeters(Decimal(book.PackageDimensions.Length)/100)
                if hasattr(book.PackageDimensions, "Width"):
                    self.width = inches_to_centimeters(Decimal(book.PackageDimensions.Width)/100)
                                    
                if hasattr(book.PackageDimensions, "Weight"):
                    self.weight = lbs_to_kgs(Decimal(book.PackageDimensions.Weight)/100)
                

            
            # published date
            try:
                self.published_date = fixDate(book.PublicationDate)
            except:
                self.published_date = "2099-12-31"
            #save pic
            try:
                image = book.MediumImage.URL
                imageExt = image.split('.')[-1]
                saveImageName = "%s.%s" % (self.ISBN, imageExt)
                f = urllib2.urlopen(image)
                fh = open("%s/%s%s" % (settings.MEDIA_ROOT, settings.BOOK_IMAGE_DIR, saveImageName), 'wb')
                fh.write(f.read())
                fh.close()
                self.picture = "%s%s" % (settings.BOOK_IMAGE_DIR, saveImageName,)
                super(Book, self).save(*args, **kwargs)
            except:
                # add default image path 
                pass
            #list price
            try:
                self.list_price = float(book.ListPrice.Amount)/100.0 # convert from pennies to dollars
            except:
                pass
            # subjects
            if hasattr(book, "BrowseNodes"):
                for node in book.BrowseNodes:
                    # ensure node has "Book" as an ancestor, else don't add it
                    if not has_ancestor(node, settings.VALID_ROOT_BNID):
                        continue
                    
                    # deal with node first
                    try:
                        subject, created = Subject.objects.get_or_create(name=node.Name, bnid=node.BrowseNodeId)
                    except:
                        continue
                    self.subjects.add(subject)
                    
                    # deal with ancestors only if subject was created
                    if created:
                        add_ancestors(self, node, subject)
                    
                    # deal with children
                    if hasattr(node, "Children"):
                        for child in node.Children:
                            try:
                                child_subject, created = Subject.objects.get_or_create(name=child.Name, bnid=child.BrowseNodeId)
                            except:
                                continue
                            self.subjects.add(child_subject)
                            if created:
                                child_subject.move_to(subject)                    
            else:
                # 0 is references because get_or_create returns a tuple
                self.subjects.add(Subject.objects.get_or_create(name="Other")[0])

        # save
        super(Book, self).save(*args, **kwargs)

def inches_to_centimeters(inches):
    return inches * Decimal("2.54")

def lbs_to_kgs(lbs):
    return lbs * Decimal("0.45359237")

def add_ancestors(book, node, subject):
    """Recursive function that adds subjects.
    
    book = Book object being dealt with.
    node = New node that was just added as Subject
    subject = The Subject just created from new node.
    
    Assume that if a subject is added, it has right ancestory.
    """
    
    if hasattr(node, "Ancestors"):
        ancestor = node.Ancestors[0] # 0 is referenced because nodes have only one ancestor
        try:
            ancestor_subject, created = Subject.objects.get_or_create(name=ancestor.Name, bnid=ancestor.BrowseNodeId)
            subject.move_to(ancestor_subject) # move subject to ancestor tree as it's new
        except:
            return
        # add subject to book because we want it to show up even
        #    if lowest level of subject hasn't been chosen.
        book.subjects.add(ancestor_subject)
        if created:
            add_ancestors(book, ancestor, ancestor_subject)

def has_ancestor(node, bnid):
    """Return True if node has an ancestor with bnid as the BrowseNodeId.
    
    node = the node that is being inspected.
    bnid = The ancestor BrowseNodeId which we're checking against. 
    """
    
    if hasattr(node, "Ancestors"):
        ancestor = node.Ancestors[0] # 0 is referenced because nodes have only one ancestor
        if hasattr(ancestor, "BrowseNodeId"):
            if ancestor.BrowseNodeId == bnid:
                return True
        return has_ancestor(ancestor, bnid)
            

def fixDate(pub_date):
    if re.search(r'^\d{4}-[01][0-9]-[0-3][0-9]$', pub_date):
        return pub_date
    elif re.search(r'^\d{4}-[01][0-9]$', pub_date):
        return pub_date + "-01"
    elif re.search(r'^\d{4}$', pub_date):
        return pub_date + "-01-01"
    else:
        raise "Date not found" 

class BookCopyManager(models.Manager):
    use_for_related_fields = True
    
    def sold(self):
        return self.model.objects.filter(sold=True)
    
    def unsold(self):
        return self.model.objects.filter(sold=False)

class Book_Copy(models.Model):
    book = models.ForeignKey(Book, related_name='copies')
    owner = models.ForeignKey(User, related_name='book_copies')
    condition = models.CharField(max_length = 3,
                                    choices=CONDITION_CHOICES, null=True)
    price = models.FloatField(help_text="Price you're charging for the book.<br />We keep 15% of this when the books sells.")
    sponsored = models.BooleanField(default = False)
    sold = models.BooleanField(default = False)
    date_added = models.DateField(auto_now_add=True)
    activation_key = models.CharField(max_length=40, blank=True) # If None, book is active
    
    # managers
    objects = BookCopyManager()
    def __unicode__(self):
        return self.book.title

    def generate_activation_key(self):
        """Generate activation_key for the book_copy."""
        
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(salt+self.owner.email).hexdigest()
        return activation_key
        
    def get_price(self):
        """Return a formatted string of the price."""
        return "$%.2f" % (self.price,)
    
    def get_price_with_shipping(self, dest_location):
        """Return a formatted string of the price with shipping."""
        
        return "$%.2f" % (self.price_with_shipping(dest_location))
    
    def is_active(self):
        """Return True if copy is active, other wise false.
        
        "Activity" is determined by presence of absence of an activation key.
        If one is present, then it's not active, otherwise, it is.
        """
        
        return self.activation_key is None
    
    def price_with_shipping(self, dest_location):
        """Return total price of book, including shipping.
        
        If no dest_location is specified, it will just return price.
        
        dest_location: a Location object where the book is being shipped to.
        """
        
        if dest_location is None:
            return self.price

        try:
            shipping = Shipping.objects.get(object_id=self.id,
                                            from_location=self.owner.profile.postal_code.location,
                                            to_location=dest_location)
        except Shipping.DoesNotExist:
            shipping = Shipping(item=self,
                                from_location=self.owner.profile.postal_code.location,
                                to_location=dest_location)
        shipping.save()

        return Decimal(str(self.price)) + shipping.price    

def book_copy_just_sold(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    
    try:
        book_copy = Book_Copy.objects.get(pk=ipn_obj.custom)
        book_copy.sold=True
        book_copy.save()
    except Book_Copy.DoesNotExist:
        pass
    
    mail_managers("Book sold", "Book copy with id: %d has sold.\n IPN id: %d" % (book_copy.id, ipn_obj.id))        
payment_was_successful.connect(book_copy_just_sold)

def book_copy_sale_flagged(sender, **kwargs):
    ipn_obj = sender
    mail_managers("Book payment flagged.", "A book payment has been flagged.\n IPN id: %d." % ipn_obj.id)
payment_was_flagged.connect(book_copy_sale_flagged)

class Author(models.Model):
    name = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.name

class Subject(MPTTModel):
    name = models.CharField(max_length = 50)
    bnid = models.CharField(max_length = 50, blank=True)
    hidden = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("subject", kwargs={'id':self.id, 'name':self.name})

    
def get_book_data(ISBN):
    """Returns an Amazon API book object if ISBN is valid, otherwise returns False.
    
    All non-alpha-num characters are removed from ISBN.
    """
    
    if not ISBN:
        return False
    
    # clean ISBN -- remove all non alpha-num chars
    ISBN = re.sub(r'[^a-zA-Z0-9]', '', ISBN)
        
    # setup connection
    ecs.setLicenseKey(settings.AWS_LICENSE_KEY);
    ecs.setSecretAccessKey(settings.AWS_SECRET_ACCESS_KEY)
    Service = 'AWSECommerceService'
    AWSAccessKeyId = settings.AWS_ACCESS_KEY_ID
    ItemId = ISBN
    
    # run lookup
    try:
        books = ecs.ItemLookup(
                               ItemId,
                               IdType='ISBN',
                               SearchIndex='Books',
                               ResponseGroup='Images,ItemAttributes,BrowseNodes')
        book = books[0]
        return book
    except ecs.InvalidParameterValue:
        return False
