from django.contrib import admin
from models import Book, Book_Copy, Subject, Author

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)

class BookCopyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book_Copy, BookCopyAdmin)

class SubjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject, SubjectAdmin)