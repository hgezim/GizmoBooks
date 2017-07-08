# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    # ensure textbook models are created
    depends_on = (
                  ("textbook", "0001_initial"),
                  )


    def forwards(self, orm):
        "Copy the Book, Book_Copy, Author data from mooi to textbook."
        
        mooi_book_type = orm.Book
        mooi_book_copy_type = orm.Book_Copy
        mooi_author_type = orm.Author
        textbook_book_type = orm['textbook.Book']
        textbook_book_copy_type = orm['textbook.Book_Copy']
        textbook_author_type = orm['textbook.Author']
        
        # copy authors over
        mooiauthors = mooi_author_type.objects.all()
        for mooiauthor in mooiauthors:
            new_author = textbook_author_type(id=mooiauthor.id, name=mooiauthor.name)
            new_author.save()
        
        # copy books over
        mooibooks = mooi_book_type.objects.all()
        for mooibook in mooibooks:
            new_book = textbook_book_type(
                                          id=mooibook.id,
                                          title=mooibook.title,
                                          ISBN=mooibook.ISBN,
                                          picture=mooibook.picture,
                                          publisher=mooibook.publisher,
                                          edition=mooibook.edition,
                                          published_date=mooibook.published_date,
                                          discipline=mooibook.discipline
                                          )
            new_book.save()
            for book_author in mooibook.authors.all():
                textbook_author = textbook_author_type.objects.get(pk=book_author.id)
                new_book.authors.add(textbook_author)
            
        # copy book copies over
        mooibookcopies = mooi_book_copy_type.objects.all()
        for mooibookcopy in mooibookcopies:
            textbook_book = textbook_book_type.objects.get(pk=mooibookcopy.book.id)
            new_copy = textbook_book_copy_type(
                                               id=mooibookcopy.id,
                                               book=textbook_book,
                                               owner=mooibookcopy.owner,
                                               condition=mooibookcopy.condition,
                                               price=mooibookcopy.price,
                                               sponsored=mooibookcopy.sponsored,
                                               sold=mooibookcopy.sold
                                               )
            new_copy.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot copy Book, Book_Copy, Author data from textbook to mooi.")
#        "Copy Book, Book_Copy, Author data from textbook to mooi."
                        
#        mooi_book_type = orm.Book
#        mooi_book_copy_type = orm.Book_Copy
#        mooi_author_type = orm.Author
#        textbook_book_type = orm['textbook.Book']
#        textbook_book_copy_type = orm['textbook.Book_Copy']
#        textbook_author_type = orm['textbook.Author']
#
#        # copy authors over
#        textbookauthors = textbook_author_type.objects.all()
#        for textbookauthor in textbookauthors:
#            new_author = mooi_author_type(id=textbookauthor.id, name=textbookauthor.name)
#            new_author.save()
#        
#        # copy books over
#        textbookbooks = mooi_book_type.objects.all()
#        for textbookbook in textbookbooks:
#            new_book = mooi_book_type(
#                                          id=textbookbook.id,
#                                          title=textbookbook.title,
#                                          ISBN=textbookbook.ISBN,
#                                          picture=textbookbook.picture,
#                                          publisher=textbookbook.publisher,
#                                          edition=textbookbook.edition,
#                                          published_date=textbookbook.published_date,
#                                          discipline=textbookbook.discipline
#                                          )
#            new_book.save()
#            for book_author in textbookbook.authors.all():
#                mooi_author = mooi_author_type.objects.get(pk=book_author.id)
#                new_book.authors.add(mooi_author)
#            
#        # copy book copies over
#        textbookbookcopies =  textbook_book_copy_type.objects.all()
#        for textbookbookcopy in textbookbookcopies:
#            mooi_book = mooi_book_type.objects.get(pk=textbookbookcopy.book.id)
#            new_copy = mooi_book_copy_type(
#                                               id=textbookbookcopy.id,
#                                               book=mooi_book,
#                                               owner=textbookbookcopy.owner,
#                                               condition=textbookbookcopy.condition,
#                                               price=textbookbookcopy.price,
#                                               sponsored=textbookbookcopy.sponsored,
#                                               sold=textbookbookcopy.sold
#                                               )
#            new_copy.save()


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
        'mooi.book_copy': {
            'Meta': {'object_name': 'Book_Copy'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Book']"}),
            'condition': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sponsored': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mooi.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mooi.profile': {
            'Meta': {'object_name': 'Profile'},
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mooi.Location']", 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'transaction_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
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

    complete_apps = ['textbook', 'mooi']
