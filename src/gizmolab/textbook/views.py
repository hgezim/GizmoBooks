from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import QueryDict, HttpResponseRedirect
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import int_to_base36
from django.utils.html import escape

from textbook.models import Book, Book_Copy, Author, CONDITION_TYPES, CONDITION_CHOICES, get_book_data
from textbook.models import Subject
from textbook.forms import PostForm, AnonPostForm, PostDetailsForm, AnonPostDetailsForm
from registration.models import RegistrationProfile
from mooi.models import PostalCode
from mooi.utils import get_location, set_location
from mooi.forms import LocationForm

def activate_copy(request, activation_key,  location_form_class=LocationForm, template_name="textbook/activate.html"):
    """Activate the book copy with activation_key.
    
    It only removes the activation_key as that is if it's present it indicates book is
        inactive.
    """
        
    # fetch book with correct activation key
    book_copy = get_object_or_404(Book_Copy, activation_key=activation_key)
    
    if book_copy.owner.profile.postal_code is None:
        location = get_location(request.session)
        if request.method == "POST":
            location_form = location_form_class(data=request.POST)
            if location_form.is_valid():
                # save location and confirmation
                saved_location = location_form.save(request=request)
                saved_postal_code = saved_location.postalcode_set.all()[0] 
                owner_profile = book_copy.owner.profile
                owner_profile.postal_code = saved_postal_code
                owner_profile.save()
            else:
                return render_to_response(template_name,
                                          {'location_form': location_form,
                                           'copy': book_copy,},
                                           context_instance=RequestContext(request))
        else:
            if hasattr(location, "id"):
                location_id = location.id
            else:
                location_id = None
            location_form = location_form_class(initial={'location': location_id})
            return render_to_response(template_name,
                                      {'location_form': location_form,
                                       'copy': book_copy,},
                                       context_instance=RequestContext(request))
    
    # set location of book_copy owner
    set_location(request=request, postal_code=book_copy.owner.profile.postal_code)
           
    # make book "active"
    book_copy.activation_key = ""
    book_copy.save()
        
    messages.success(request, "Awesome! \"%s\" is now active." % escape(book_copy.book))
    return HttpResponseRedirect(reverse('book', kwargs={"book_id": book_copy.book.id }))
    

def book(request, book_id, condition_type="", template_name="textbook/book.html", location_form_class=LocationForm):
    """Show details and seller list of a book."""
    
    location = get_location(request.session)
    # set location form if no location is detected
    if request.method == "POST":
        location_form = location_form_class(request.POST)
        if location_form.is_valid():
            location_form.save(request)
            return HttpResponseRedirect(request.path)
    else:
        if hasattr(location, "id"):
            location_id = location.id
        else:
            location_id = None
        location_form = location_form_class(initial={'location': location_id})

    book = get_object_or_404(Book, id=book_id)
    
    subjects = Subject.objects.filter(hidden=False, parent__parent__bnid=settings.VALID_ROOT_BNID).order_by('name')
    
    # if activation_key=="", then the book is active
    copies = book.copies.filter(activation_key="", sold=False)
    if condition_type == CONDITION_TYPES[0]: #new
        copies = book.copies.filter(activation_key="", condition=CONDITION_CHOICES[0][0], sold=False)
    elif condition_type == CONDITION_TYPES[1]: #used
        copies = book.copies.filter(activation_key="", condition__lt=CONDITION_CHOICES[0][0], sold=False)
    
    copy_set = []
    for copy in copies:
        copy_set.append((copy, copy.get_price_with_shipping(dest_location=location)))
    
    copy_set = sorted(copy_set, key=lambda book_copy: book_copy[1])
    return render_to_response(template_name,
                              {
                               'location_form': location_form,
                               'location': location,
                               'subjects' : subjects,
                               'book' : book,
                               'copy_set': copy_set,
                               'condition_type': condition_type,
                               },
                              context_instance=RequestContext(request))

def buy(request, template_name="textbook/buy.html"):
    """Show a list of popular textbooks."""
    
    # subjects, direct grand-children of valid root
    subjects = Subject.objects.filter(book__copies__activation_key="", book__copies__sold=False, hidden=False, parent__parent__bnid=settings.VALID_ROOT_BNID).distinct().order_by('name')
    
    # get a list of top subject (direct children of valid root)
    top_subjects = Subject.objects.filter(book__copies__activation_key="", book__copies__sold=False, hidden=False, parent__bnid=settings.VALID_ROOT_BNID).distinct().order_by('name')
    
    # for each top_subject:
    #    get it's children
    #        for child subject in children
    #            add the books under that subject (wchi are not sold and inactive)
    
    
    #list of Books with most Book_Copies in each category
    top_books_list = []
    for subject in top_subjects:
        # show books with highest number of copies that have at least 1 of them unsold
        top_books_list.append({'subject': subject, 'books': Book.objects.filter(subjects__name=subject, copies__sold=False).annotate(number_of_copies=Count('copies')).filter(copies__sold=False, copies__activation_key="").order_by('-number_of_copies')[:5]})

    return render_to_response(template_name,
                              {
                               'subjects' : subjects,
                               'top_books' : top_books_list,
                               },
                              context_instance=RequestContext(request))


def main(request, template_name="textbook/main.html"):
    """Show main selling page."""
    
    if request.user.is_authenticated():
        post_form = PostForm()
    else:
        post_form = AnonPostForm()

    return render_to_response(template_name,
                              {
                               'post_form': post_form,
                               },
                              context_instance=RequestContext(request))
    
def post(request, form_class=PostForm, no_ISBN=False, template_name="textbook/post.html"):
    """Post book for sale."""
    
    form_data = form_initial = form_files = None
    
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
        
    if request.method == 'POST':
        rawBook = get_book_data(request.POST.get('ISBN'))
        if rawBook:
            form_data = request.POST
            if user:
                form_class = PostForm
            else:
                form_class = AnonPostForm 
        else:
            if not no_ISBN:
                # show message indicating ISBN didn't work.
                # only show this if ISBN wasn't disabled.
                messages.error(request, "Sorry! We couldn't find the ISBN you entered. Please enter your book details manually.")
            
            if 'details' in request.POST:
                form_data = request.POST
                form_files = request.FILES
            else:
                # this is volatile as it doesn't accept more than one value for key
                # it just uses the first one in the list
                form_initial = {}
                for key, value in request.POST.items():
                    form_initial[key] = value
            if user:
                form_class = PostDetailsForm
            else:
                form_class = AnonPostDetailsForm
    else:
        if no_ISBN:
            form_class = PostDetailsForm
        if not user:
            if no_ISBN:
                form_class = AnonPostDetailsForm
            else:
                form_class = AnonPostForm
    
    post_form = form_class(data=form_data, files=form_files, initial=form_initial)
    
    if post_form.is_valid():
        new_copy = post_form.save(user=user, raw_book=rawBook)
        
        # get site
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        # setup email context
        emailContext = {'book_copy': new_copy,
                        'site': site}
        
        # setup subject
        subject = render_to_string('textbook/copy_activation_email_subject.txt',
                                   emailContext)
        subject = ''.join(subject.splitlines())
        
        if request.user.is_authenticated():
            messages.success(request, message=render_to_string('textbook/authenticated_user_success_message.html', {'book_copy': new_copy}, context_instance=RequestContext(request)))
            
            if request.facebook:
                graph = request.facebook.graph
                title = ""
                link = "http://www.gizmobooks.com/"
                caption = "{*actor*} posted a new review"
                description = "This is a longer description of the attachment"
                picture = "http://www.google.com/logos/2011/shinichi_hoshi-2011-hp.jpg"
                wall_post_attachment = {"name": title ,"link": link, "caption": caption, "description": description, "picture": picture}
                graph.put_wall_post("message", wall_post_attachment)

            # if user has fbprofile:
            #    post a pretty message to his/her wall
            
            return HttpResponseRedirect(reverse('post'))
        elif new_copy.owner.is_active:
            emailContext['uid'] = int_to_base36(new_copy.owner.id)
            emailContext['user'] = new_copy.owner
            emailContext['reset_token'] = token_generator.make_token(new_copy.owner)
            
            message = render_to_string('textbook/active_user_copy_activation_email.txt',
                                   emailContext)
            new_copy.owner.email_user(subject, message, settings.CONFIRM_FROM_EMAIL)
            messages.warning(request, message=render_to_string('textbook/active_user_success_message.html', {'book_copy': new_copy}, context_instance=RequestContext(request)))
            return HttpResponseRedirect(reverse('post'))
        else:
            # TODO: Ideally, this email would be in a queue and we'd be able to cancel it
            #     if the user chooses to register (i.e. create a password in the next step.
            message = render_to_string('textbook/inactive_user_copy_activation_email.txt',
                                       emailContext)
             
            new_copy.owner.email_user(subject, message, settings.CONFIRM_FROM_EMAIL)
            request.session['user_hash'] = RegistrationProfile.objects.get(user=new_copy.owner).creation_hash
            request.session['user_email'] = new_copy.owner.email

            return HttpResponseRedirect(reverse('registration_save_password'))
        
        #TODO : redirect them somewhere smart, maybe the book page where they just posted?!
        return HttpResponseRedirect(reverse('main'))
        
    return render_to_response(template_name,
                              {
                               'post_form' : post_form,
                               },
                              context_instance=RequestContext(request))


def subject(request, id, name, template_name="textbook/subject.html"):
    """Show all unsold books for a category."""
    
    books_per_page = 25
    subject = get_object_or_404(Subject, pk=id)
    children = subject.get_children()
    
    try:
        books_list = subject.book_set.filter(copies__activation_key="", copies__sold=False).distinct()
    except Subject.DoesNotExist:
        books_list = None
    
    paginator = Paginator(books_list, books_per_page)
    
    subjects = Subject.objects.filter(book__copies__activation_key="", hidden=False, parent__parent__bnid=settings.VALID_ROOT_BNID).distinct().order_by('name')
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        pages = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pages = paginator.page(paginator.num_pages)
        
    
    return render_to_response(template_name,
                              {
                               'current_subject': subject,
                               'subjects': subjects,
                               'children': children,
                               'pages' : pages,
                               },
                              context_instance=RequestContext(request))
