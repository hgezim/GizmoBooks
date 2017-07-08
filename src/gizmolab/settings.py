# Django settings for gizmolab project.

DEBUG = False
TEMPLATE_DEBUG = False
SEND_BROKEN_LINK_EMAILS = True

ADMINS = (('Gezim', 'hgezim@gmail.com'),)

#EMAIL SERVER SETTING
EMAIL_HOST = 'mail.gizmobooks.com'
EMAIL_HOST_USER = 'help@gizmobooks.com'
EMAIL_HOST_PASSWORD = 'mypass'
EMAIL_PORT = '587'
DEFAULT_FROM_EMAIL = 'GizmoBooks.com <help@gizmobooks.com>'
CONFIRM_FROM_EMAIL = 'GizmoBooks.com <post@gizmobooks.com>'
SERVER_EMAIL = 'help@gizmobooks.com'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': 'gizmobooks',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'gezim',
        'PASSWORD': 'mypass',
        'HOST': 'mysql.gizmobooks.com',
    }
}

AUTHENTICATION_BACKENDS = (
                           'accounts.backends.authentication.FacebookProfileBackend',
                           'accounts.backends.authentication.EmailModelBackend',
                           'django.contrib.auth.backends.ModelBackend'
                           )

#CACHE_BACKEND = 'db://mooi_cache'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Edmonton'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

#FORCE_SCRIPT_NAME = '/test'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/haxhia/domains/media.gizmobooks.com'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.gizmobooks.com/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://media.gizmobooks.com/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'long secret key'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    #'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_facebook.middleware.FacebookMiddleware',
    'ip2geo.middleware.CityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
                               "django.core.context_processors.request",
                               "django.core.context_processors.auth",
                               "django.core.context_processors.debug",
                               "ip2geo.context_processors.add_session",
                               "django.core.context_processors.media",
                               "django.contrib.messages.context_processors.messages",
                               )

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/haxhia/django/templates/gizmobooks',
)

INSTALLED_APPS = (
    'haystack',
    'sorl.thumbnail',
    'ip2geo',
    'checkout',
    'shipping',
    'redis',
    'uni_form',
    'south',
    'paypal.standard.ipn',
    'registration',
    'PIL',
    'mooi',
    'django_facebook',
    'textbook',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'search',
    'mailer',
    'mptt',
    'django.contrib.comments',
)


# How long the cart will be valid for (minutes)
CART_LIFESPAN = 5

#PAYPAL SETTINGS
PAYPAL_RECEIVER_EMAIL = "myemail@example.com"

#shipping settings
CPCID = "MY canada post ID" #Canada Post ID
TURN_AROUND_TIME = "24"
CONNECTION = "http://sellonline.canadapost.ca:30000"
GIZMOBOOKS_SHIPPING_PRICE = 3
SHIPPING_OPTIONS = (
                    ('0500', 'GizmoBooks.com' ),
                    ('1010', 'CanadaPost: Domestic - Regular'),
                    )
# default dimensions of book, if non exist
DEFAULT_WEIGHT = 2
DEFAULT_LENGTH = 30
DEFAULT_WIDTH = 22
DEFAULT_HEIGHT = 5
DEFAULT_SHIPPING_COST = 15

#ip2geo
GEOIP_DATA = '/home/haxhia/django/projects/gizmobooks/ip2geo/fixtures/GeoLiteCity.dat'
#GEOIP_SESSION_FIELDS = ['country_name', 'country_code', 'country_code3', 'region_name', 'city', 'latitude', 'longitude', 'postal_code']
GEOIP_SESSION_FIELDS = ['country_name', 'country_code', 'region_name', 'city', 'postal_code']


#textbook settings
VALID_ROOT_BNID = "1000"
BOOK_IMAGE_DIR = "books/"
BOOK_DEFUALT_IMAGE = "noimage.png"

#django-registration
ACCOUNT_ACTIVATION_DAYS = 365

#profile
AUTH_PROFILE_MODULE = 'mooi.Profile'

# Facebook settings
FACEBOOK_API_KEY = 'fb api key'
FACEBOOK_SECRET_KEY = 'much secret'

# haystack
HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_XAPIAN_PATH = '/home/haxhia/django/projects/gizmobooks/search/haystack_book_index'

# AWS
AWS_LICENSE_KEY = "aws license key"
AWS_SECRET_ACCESS_KEY = "very hush hush"
AWS_ACCESS_KEY_ID = "key id"

# Facebook
FACEBOOK_APP_ID = 'fb app id'
FACEBOOK_API_KEY = 'fb ai key'
FACEBOOK_SECRET_KEY = 'secret key'

# Optionally set default permissions to request, e.g: ['email', 'user_about_me']
FACEBOOK_PERMS = ['email', 'user_location', 'publish_stream']

#override with local settings, if local:
try:
   from local_settings import *
except ImportError, e:
   pass
