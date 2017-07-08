from django.db.models import Min, Count
from django.template import RequestContext
from django.conf import settings

from haystack.views import SearchView
from haystack.forms import ModelSearchForm
from haystack.query import EmptySearchQuerySet

from textbook.models import Subject

class BookSearchView(SearchView):
    def __init__(self, template=None, load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext):
        super(BookSearchView, self).__init__(template, load_all, form_class, searchqueryset, context_class)
        self.sponsored_books = None
    
    def __name__(self):
        return "BookSearchView"
    
    def get_results(self):
        if self.query:
            
            search_results = self.form.search()
            self.subjects = Subject.objects.filter(hidden=False, parent__parent__bnid=settings.VALID_ROOT_BNID).order_by('name')
            
            # add count, min price data
            search_results_list = []
            for result_obj in search_results:
                try:
                    search_results_list.append((result_obj.object, result_obj.object.copies.aggregate(Min('price'), Count('id')).values()))
                except AttributeError:
                    continue
             
            return search_results_list
        
        return EmptySearchQuerySet()

    def extra_context(self):
        return {'q': self.query,
                'subjects' : self.subjects}