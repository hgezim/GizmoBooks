from django import forms
from haystack.forms import SearchForm
import re
from pyaws import ecs
import settings

class BookSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.ISBN = None
        self.title = None
    
    def search(self):
        """
        Does actual search.
        
        Returns a two element tuple. First one is the site search results. Second is amazon results.
        """
        
        query = self.cleaned_data['q']
        self.title = query
        
        if self.is_valid():
            local_books_title = self.searchqueryset.auto_query(self.title)
            local_books_query = self.searchqueryset.auto_query(query)
            
            local_books = local_books_query
            # if title query returned more results make that local_books
            if len(local_books_title) > len(local_books_query):
                local_books = local_books_title
            
            return local_books
        else:
            return None
        
    def is_query_ISBN(self):
        """
        Returns True if query is an ISBN number, otherwise False.
        Also sets self.ISBN to be just the plain number.
        """
        query = self.cleaned_data['q']
        
        # ISBN can contain: numbers, spaces, tabs, x or X, dashes, and underscores.
        if re.search(r'[^0-9 \txX\-_]', query):
            return False
        else:
            self.ISBN = re.sub(r'[^0-9xX]', '', query)
            return True
        