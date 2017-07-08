# encoding: utf-8
import datetime
import os
import subprocess

from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Unzip GeoLiteCity.dat.gz."
        
        CITY_FILE_DIR = 'ip2geo/fixtures/'
        CITY_FILE_TARBALL_NAME = 'GeoLiteCity.tar.gz2'
        CITY_FILENAME = 'GeoLiteCity.dat'
        
        os.chdir(CITY_FILE_DIR)
        if not os.path.isfile(CITY_FILENAME):
            # only uncompress it if csv does not exist
            subprocess.check_call(["tar", "xjvf", CITY_FILE_TARBALL_NAME])
        os.chdir('../..')



    def backwards(self, orm):
        "Can't uncompress the file."
        
        raise RuntimeError("Cannot ununcompress file.")


    models = {
        
    }

    complete_apps = ['ipToGeo']
