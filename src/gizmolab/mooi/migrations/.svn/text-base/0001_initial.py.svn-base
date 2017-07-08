# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('mooi_user', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('credits', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('transaction_status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.Location'])),
        ))
        db.send_create_signal('mooi', ['User'])

        # Adding model 'Location'
        db.create_table('mooi_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('mooi', ['Location'])

        # Adding model 'Book'
        db.create_table('mooi_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('ISBN', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('picture', self.gf('django.db.models.fields.FilePathField')(path='/home/haxhia/book_images', max_length=100, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('published_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discipline', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('mooi', ['Book'])

        # Adding M2M table for field authors on 'Book'
        db.create_table('mooi_book_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['mooi.book'], null=False)),
            ('author', models.ForeignKey(orm['mooi.author'], null=False))
        ))
        db.create_unique('mooi_book_authors', ['book_id', 'author_id'])

        # Adding model 'Book_Copy'
        db.create_table('mooi_book_copy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.Book'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.User'])),
            ('condition', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('sponsored', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('sold', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('mooi', ['Book_Copy'])

        # Adding model 'Author'
        db.create_table('mooi_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('mooi', ['Author'])

        # Adding model 'Book_Browse'
        db.create_table('mooi_book_browse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.Book'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.User'])),
            ('IP', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mooi', ['Book_Browse'])

        # Adding model 'Book_Copy_Browse'
        db.create_table('mooi_book_copy_browse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book_copy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.Book_Copy'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mooi.User'])),
            ('IP', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mooi', ['Book_Copy_Browse'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('mooi_user')

        # Deleting model 'Location'
        db.delete_table('mooi_location')

        # Deleting model 'Book'
        db.delete_table('mooi_book')

        # Removing M2M table for field authors on 'Book'
        db.delete_table('mooi_book_authors')

        # Deleting model 'Book_Copy'
        db.delete_table('mooi_book_copy')

        # Deleting model 'Author'
        db.delete_table('mooi_author')

        # Deleting model 'Book_Browse'
        db.delete_table('mooi_book_browse')

        # Deleting model 'Book_Copy_Browse'
        db.delete_table('mooi_book_copy_browse')


    models = {
        'mooi.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mooi.book': {
            'ISBN': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mooi.Author']", 'symmetrical': 'False'}),
            'discipline': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.FilePathField', [], {'path': "'/home/haxhia/book_images'", 'max_length': '100', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'mooi.book_browse': {
            'IP': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'Meta': {'object_name': 'Book_Browse'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Book']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.User']"})
        },
        'mooi.book_copy': {
            'Meta': {'object_name': 'Book_Copy'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Book']"}),
            'condition': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.User']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sponsored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'mooi.book_copy_browse': {
            'IP': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'Meta': {'object_name': 'Book_Copy_Browse'},
            'book_copy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Book_Copy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.User']"})
        },
        'mooi.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mooi.user': {
            'Meta': {'object_name': 'User'},
            'browsed_book_copies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mooi.Book_Copy']", 'through': "orm['mooi.Book_Copy_Browse']", 'symmetrical': 'False'}),
            'browsed_books': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mooi.Book']", 'through': "orm['mooi.Book_Browse']", 'symmetrical': 'False'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'transaction_status': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['mooi']
