from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
                       
from registration.views import activate
from registration.views import register
from accounts import views as accounts_views
from views import profile, edit_profile

urlpatterns = patterns('',
                       url(r'^login/$',
                           accounts_views.login,
                           {'template_name': 'accounts/login.html'},
                           name='auth_login'),

                       url(r'^fblogin/$',
                           accounts_views.fb_login,
                           name='fb_login'),                       
                           
                       url(r'^logout/$',
                           auth_views.logout,
                           {'next_page': '/',
                            'redirect_field_name': REDIRECT_FIELD_NAME},
                           name='auth_logout'),
                           
                       url(r'^activate/complete/$',
                           direct_to_template,
                           {'template': 'accounts/activation_complete.html'},
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'template_name': 'accounts/activate.html',
                            'backend': 'accounts.backends.reg.EmailRegistrationBackend'},
                           name='registration_activate'),
                           
                       url(r'^register/$',
                           register,
                           {'template_name': 'accounts/registration_form.html',
                            'backend': 'accounts.backends.reg.EmailRegistrationBackend'},
                           name='registration_register'),

                       url(r'^create/$',
                           register,
                           {'template_name': 'accounts/save_password_form.html',
                            'backend': 'accounts.backends.reg.SavePasswordRegistrationBackend'},
                           name='registration_save_password'),
                           
                       url(r'^profile/$',
                           profile,
                           {},
                           name='profile'),
                           
                        url(r'^profile/edit/$',
                            edit_profile,
                            name='edit_profile'
                            ),                        
                           
                       url(r'^register/complete/$',
                           direct_to_template,
                           {'template': 'accounts/registration_complete.html'},
                           name='registration_complete'),
                           
                       url(r'^register/closed/$',
                           direct_to_template,
                           {'template': 'accounts/registration_closed.html'},
                           name='registration_disallowed'),
                           
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           accounts_views.password_reset_confirm,
                           {'template_name': 'accounts/password_reset_confirm.html',
                            'post_reset_redirect': 'profile'},
                           name='password_reset'),
                           
                       url(r'^reset/request/done/$', # ensure to change /reset/request/ if this changes.
                           auth_views.password_reset_done,
                           {'template_name': 'accounts/password_reset_done.html'},
                           name='password_reset_done'),

                       url(r'^reset/request/$',
                           auth_views.password_reset,
                           {'template_name': 'accounts/password_reset_request.html',
                            'email_template_name': 'accounts/password_reset_request_email.txt',
                            'post_reset_redirect':  'done/'}, # change this if /reset/done/ changes
                           name='password_reset_request')
                           
                        )
