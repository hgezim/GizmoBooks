import re

from django import forms
from django.forms import ModelForm
from django.forms import Form
from django.forms.util import ErrorList
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.conf import settings

from accounts.utils import get_or_create_user_from_email

from textbook.models import Book, Book_Copy, Author, Subject, get_book_data
from textbook.models import CONDITION_CHOICES


class PostForm(ModelForm):
    class Meta:
        model = Book_Copy
        fields = ('condition', 'price',)
    
    ISBN = forms.CharField(label = "ISBN", max_length=20, help_text='A 13-digit barcode number at the back of your book. In older books it may just 10 digits long.<br />E.g. 978-0-07-338108-4<br /><br />Got no ISBN? <a href="details/">Click here</a>.')
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['ISBN', 'condition', 'price']
    
    def clean_ISBN(self):
        """Remove any non alphanumeric characters from ISBN."""
        ISBN = self.cleaned_data['ISBN']
        cleanerISBN = re.sub(r'[^a-zA-Z0-9]', '', ISBN)
        
        return ISBN
    
    def save(self, user, commit=True, raw_book=None, inactive=False):
        """Save a book copy and the associated data like Book and Authors.
        
        commit = Whether to actually save or not.
        raw_book = The book object returned from Amazon request.
        inactive = Whether the copy should be inactive initially or not.
        
        If an instance is provided, if ISBN is changed create a new Book_Copy and Book object, if it
            doesn't already exist.
            
        """

        # Get 10-digit ISBN
        if not raw_book:
            raw_book = get_book_data(self.ISBN)
        if hasattr(raw_book, "ISBN"): self.ISBN = raw_book.ISBN
        
        # get Book and Book_Copy objects
        if self.instance.pk is not None:
            book_copy = self.instance
            book = book_copy.book
        else:
            # if we have the book, get it, otherwise download it.
            # get_or_create() cannot be used here because we need to pass save an argument.
            try:
                # raw_book.ISBN is used to search db because that's the ISBN we store
                book = Book.objects.get(ISBN=raw_book.ISBN)
            except Book.DoesNotExist:
                book = Book(ISBN=self.ISBN)
                if commit == True:
                    book.save(raw_book = raw_book)
            book_copy = Book_Copy()
            book_copy.book = book            
            book_copy.condition = self.cleaned_data['condition']
            book_copy.price = self.cleaned_data['price']
            book_copy.owner = user
            if inactive:
                # ensure book_copy.owner is already set
                book_copy.activation_key = book_copy.generate_activation_key() 

            
        
        if commit:
            book_copy.save()
        
        if not self.errors:
            return book_copy
        else:
            raise ValueError
         
class AnonPostForm(PostForm):
    email = forms.EmailField(label = 'E-mail', help_text = 'or  <fb:login-button show-faces="false" width="200" max-rows="1" perms="{% facebook_perms %}">Login with Facebook</fb:login-button>')
        
    def __init__(self, *args, **kwargs):
        super(AnonPostForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'ISBN', 'condition', 'price']

    
    def save(self, commit=True, raw_book=None, user=None):
        """Create user from email and save book."""
        
        user, created = get_or_create_user_from_email(self.cleaned_data['email'])
        if created:
            user.is_active = False
            user.save()
        return super(AnonPostForm, self).save(commit=commit, raw_book=raw_book, user=user, inactive=True)
    
class PostDetailsForm(PostForm):
    title = forms.CharField(label = "Title", max_length=400)
    subjects = forms.CharField(label = "Subjects", help_text="Comma separated list of subjects.<br />E.g. Biology, Molecular Biology, Cell Biology")
    authors = forms.CharField(label = "Authors", widget=forms.Textarea, help_text="One author per line.<br />E.g.<br />Roch Carrier<br />Naomi Klein")
    edition = forms.CharField(label = "Edition", max_length=50, required=False, help_text="Please include an edition to help students determine if this is the right book for them.")
    publisher = forms.CharField(label = "Publisher", max_length=100, required=False)
    picture = forms.ImageField(required=False)
    # details is used for form processing
    details = forms.CharField(required=False, max_length=20, widget=forms.HiddenInput)
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False):
        """Constructor used to remove ISBN field."""
        
        super(PostForm, self).__init__(data, files, auto_id, prefix, initial,
                                       error_class, label_suffix,
                                       empty_permitted)
        del self.fields['ISBN']
        self.fields.keyOrder = ['title', 'subjects', 'authors', 'condition', 'price',
                                'edition', 'publisher', 'picture', 'details']

    def clean_title(self):
        """Make title required."""
        
        title = self.cleaned_data['title']
        if len(title) < 1:
            raise forms.ValidationError("Title is required.")
            
        return title
    
    def clean_authors(self):
        """Ensure authors exist. Return a list of string with author names."""
        
        authors = self.cleaned_data['authors']
        if len(authors) < 1:
            raise forms.ValidationError("You need to specify one or more authors.")
        
        authorsList = authors.split('\n')
        for i, author in enumerate(authorsList):
            authorsList[i] = re.sub(r'[^a-zA-Z0-9 ]', '', author)
        return authorsList
    
    def save(self, user, commit=True, raw_book=None, inactive=False):
        """Save the Book and Book_Copy based on the information given.
        
        commit = Whether to actually save or not.
        raw_book = The book object returned from Amazon request.
        inactive = Whether the copy should be inactive initially or not.
        """
        
        # get Book and Book_Copy objects
        if self.instance.pk is not None:
            book_copy = self.instance
            book = book_copy.book
        else:
            book = Book()
            book.title = self.cleaned_data.get('title')
            book.edition = self.cleaned_data.get('edition')
            book.publisher = self.cleaned_data.get('publisher')
            if commit:
                book.save()
            for author_name in self.cleaned_data.get('authors'):
                author, created = Author.objects.get_or_create(name=author_name)
                book.authors.add(author)
            if self.cleaned_data.get('picture'):
                book.picture = self.cleaned_data.get('picture')
            else:
                book.picture = "%snoimage.png" % settings.BOOK_IMAGE_DIR 
            for subject_string in self.cleaned_data.get('subjects').split(','):
                subject_string = subject_string.strip()
                if Subject.objects.filter(name=subject_string):
                    for subject in Subject.objects.filter(name=subject_string):
                        book.subjects.add(subject)
                else:
                    # create subject
                    new_subject = Subject.objects.create(name=subject_string)
                    try:
                        root_subject = Subject.objects.get(bnid=settings.VALID_ROOT_BNID)
                        new_subject.move_to(root_subject)
                    except Subject.DoesNotExist:
                        pass
                    book.subjects.add(new_subject)
            if commit:
                book.save()
            
            book_copy = Book_Copy()
            book_copy.book = book
            
        book_copy.condition = self.cleaned_data.get('condition')
        book_copy.price = self.cleaned_data.get('price')
        book_copy.owner = user
        if inactive:
            # book_copy.owner needs to be set before calling generate_activation_key()
            book_copy.activation_key = book_copy.generate_activation_key() 

        if commit:
            book_copy.save()
        return book_copy



class AnonPostDetailsForm(PostDetailsForm):
    email = forms.EmailField(label = 'E-mail', help_text = 'or  <fb:login-button show-faces="false" width="200" max-rows="1" perms="{% facebook_perms %}">Login with Facebook</fb:login-button>')
    
    def __init__(self, *args, **kwargs):
        super(AnonPostDetailsForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'title', 'subjects', 'authors', 'condition', 'price',
                                'edition', 'publisher', 'picture', 'details']
    
    def save(self, commit=True, raw_book=None, user=None):
        """Create user, if nonexistent, then save book_copy with user as owner."""
        
        user, created = get_or_create_user_from_email(self.cleaned_data['email'])
        if created:
            user.is_active = False
            user.save()
        return super(AnonPostDetailsForm, self).save(commit=commit, raw_book=raw_book, user=user, inactive=True)