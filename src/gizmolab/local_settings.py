DEBUG = True

DATABASES = {
    'default': {
        'NAME': 'gizmobooks',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'gizmo',
        'PASSWORD': 'mypass',
        'HOST': 'localhost',
    }
}

MEDIA_ROOT = '/Users/gezimhoxha/Sites/gizmobooks'

MEDIA_URL = 'http://localhost/~gezimhoxha/gizmobooks/'

TEMPLATE_DIRS = (
                 '/Users/gezimhoxha/projects/gizmobooks/trunk/UI',
)

GEOIP_DATA = '/Users/gezimhoxha/projects/gizmobooks/trunk/src/gizmolab/ip2geo/fixtures/GeoLiteCity.dat'

HAYSTACK_XAPIAN_PATH = '/Users/gezimhoxha/Sites/gizmobooks_beta/index'

# And for local debugging, use one of the debug middlewares and set:
FACEBOOK_DEBUG_TOKEN = 'lonnngtext'
FACEBOOK_DEBUG_UID = 'somenumber'
FACEBOOK_DEBUG_COOKIE = ''
FACEBOOK_DEBUG_SIGNEDREQ = ''
