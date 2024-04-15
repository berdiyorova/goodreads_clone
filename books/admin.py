from django.contrib import admin

from .models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn', 'description')
    # list_filter = ('genre', )

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    list_display = (Author.full_name, 'email')

class BookAuthorAdmin(admin.ModelAdmin):
    list_filter = ('author', )
    search_fields = ('book', 'author')
    list_display = ('book', 'author')

class BookReviewAdmin(admin.ModelAdmin):
    list_filter = ('book', 'user')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
