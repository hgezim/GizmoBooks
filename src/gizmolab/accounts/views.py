from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site, RequestSite
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.core.urlresolvers import reverse
from django.utils.http import base36_to_int
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from forms import EditProfileForm, LoginForm
from textbook.models import Book_Copy

def login(request, form_class=LoginForm, template_name='accounts/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """Displays the login form and handles the login action.
    
    Code is borrowed from django.contrib.auth.views and modified to allow for custom form.
    """
    
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = form_class(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login = never_cache(login)

def fb_login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Authenticate/register a user using their Facebook credentials.
    """
    
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    try:
        user = authenticate(fb_uid=request.facebook.uid, fb_graphtoken=request.facebook.graph.access_token)
        if user:
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
                
            from django.contrib.auth import login
            login(request, user)
    except:
        pass
        
    return HttpResponseRedirect(redirect_to)


def password_reset_confirm(request, uidb36=None, token=None, template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator, set_password_form=SetPasswordForm,
                           post_reset_redirect=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password. Once the new password is set, a message
    to notify the user is created, user is logged in and redirected.
    
    Initial code taken from django.auth.contrib.views.
    """

    assert uidb36 is not None and token is not None # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                
                authed_user = authenticate(username=user.email, password=form.cleaned_data['new_password1'])
                if authed_user is not None:
                    if authed_user.is_active:
                        auth_login(request, authed_user)
                
                messages.info(request, message="Your new password has been saved. Welcome back!")
                return HttpResponseRedirect(reverse(post_reset_redirect))
        else:
            form = set_password_form(None)
    else:
        context_instance['validlink'] = False
        form = None
    context_instance['form'] = form
    return render_to_response(template_name, context_instance=context_instance)

@login_required
def profile(request, template_name='accounts/profile.html'):
    """User profile."""
    
    book_copies = request.user.book_copies.filter(activation_key="")
    
    return render_to_response(template_name, 
                              {'book_copies': book_copies},
                              context_instance=RequestContext(request))

@login_required
def edit_profile(request, form_class=EditProfileForm, template_name='accounts/edit_profile.html'):
    """View that allows user to edit profile."""
    
    import pdb
    pdb.set_trace()
    
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = form_class()
        
    return render_to_response(template_name, {'form': form},
                              context_instance=RequestContext(request))
        
        
        
        