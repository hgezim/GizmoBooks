import datetime
from haystack import indexes
from haystack import site
from textbook.models import Book

class BookIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    ISBN = indexes.CharField(model_attr='ISBN')
    
site.register(Book, BookIndex)