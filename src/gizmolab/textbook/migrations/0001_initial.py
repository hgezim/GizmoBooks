# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Book'
        db.create_table('textbook_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('ISBN', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('picture', self.gf('django.db.models.fields.FilePathField')(path='/home/haxhia/book_images', max_length=100, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('published_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discipline', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('textbook', ['Book'])

        # Adding M2M table for field authors on 'Book'
        db.create_table('textbook_book_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['textbook.book'], null=False)),
            ('author', models.ForeignKey(orm['textbook.author'], null=False))
        ))
        db.create_unique('textbook_book_authors', ['book_id', 'author_id'])

        # Adding model 'Book_Copy'
        db.create_table('textbook_book_copy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['textbook.Book'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='book_copies', to=orm['auth.User'])),
            ('condition', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('sponsored', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sold', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('textbook', ['Book_Copy'])

        # Adding model 'Author'
        db.create_table('textbook_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('textbook', ['Author'])


    def backwards(self, orm):
        
        # Deleting model 'Book'
        db.delete_table('textbook_book')

        # Removing M2M table for field authors on 'Book'
        db.delete_table('textbook_book_authors')

        # Deleting model 'Book_Copy'
        db.delete_table('textbook_book_copy')

        # Deleting model 'Author'
        db.delete_table('textbook_author')


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
        'textbook.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'textbook.book': {
            'ISBN': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['textbook.Author']", 'symmetrical': 'False'}),
            'discipline': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.FilePathField', [], {'path': "'/home/haxhia/book_images'", 'max_length': '100', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'textbook.book_copy': {
            'Meta': {'object_name': 'Book_Copy'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['textbook.Book']"}),
            'condition': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_copies'", 'to': "orm['auth.User']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sponsored': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['textbook']
