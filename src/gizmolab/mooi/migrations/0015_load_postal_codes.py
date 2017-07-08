# encoding: utf-8
import datetime
import os
import subprocess

from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

class Migration(DataMigration):

    def forwards(self, orm):
        """Load sql dump of Locaions and PostalCodes.
        
        Nuke mooi_location too because otherwise we won't be able to use mysql load.
        """
                
        # save location data in memory
        locations = {}
        for location in orm.Location.objects.all():
            city = location.city 
            if city not in locations:
                locations[city] = [id_list[0] for id_list in location.profile_set.values_list('id')]

        print locations
            
	    # nuke mooi_location as any data will corrupt our mysql load command below
        db.clear_table('mooi_location')

        dbhostname = settings.DATABASES['default']['HOST']
        dbusername = settings.DATABASES['default']['USER']
        dbpassword = settings.DATABASES['default']['PASSWORD']
        dbname = settings.DATABASES['default']['NAME']
        dumpfiletarball = 'locations_with_postalcodes.tar.bz2'
        dumpfilepath = 'mooi/fixtures/'
        dumpfilename = 'locations_with_postalcodes.sql'
	
        os.chdir(dumpfilepath)
        if not os.path.isfile(dumpfilename):
            subprocess.check_call(["tar", "xjvf", dumpfiletarball])
        
        dumpfile = open(dumpfilename)
                
        ret = subprocess.check_call(["mysql", "-h", dbhostname, "-u", dbusername, "--password=%s" % (dbpassword,), dbname], stdin=dumpfile)
        dumpfile.close()
        os.chdir('../..')
        
        # restore location data
        for city, user_id_list in locations.items():
            new_locations = orm.Location.objects.filter(city=city)
            if len(new_locations) == 1:
                location_to_set = new_locations[0]
            elif len(new_locations) > 1:
                print ["%s, %s" % (j.city, j.region ) for j in new_locations ]
                choice = int(raw_input("Which city is correct (0 is first): "))
                location_to_set = new_locations[choice]
            else:
                print "Couldn't find city matching '%s' for these user ids:" % city
                print user_id_list
                continue
            
            for user_id in user_id_list:
                user_model = orm['auth.User']
                try:
                    user = user_model.objects.get(pk=user_id)
                except:
                    print "Couldn't fix loation of uid:%d\n" % user_id
                    continue
                try:
                    user.profile.postal_code = location_to_set.postalcode_set.all()[0]
                    user.profile.save()
                except:
                    print "Couldn't change location for uid:%d to loc id: %d" % (user_id, location_to_set.id)
                

    def backwards(self, orm):
        """Don't remove data as it could corrupt database."""
        
        raise RuntimeError("Cannot safely remove location and postal code data.")


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mooi.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'mooi.postalcode': {
            'Meta': {'object_name': 'PostalCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Location']"})
        },
        'mooi.profile': {
            'Meta': {'object_name': 'Profile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Location']", 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.PostalCode']", 'null': 'True'}),
            'transaction_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['mooi']
