from django.urls import path

from .views import BooksListView, BookDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, \
    DeleteReviewView


app_name = 'books'

urlpatterns = [
    path('', BooksListView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/reviews', AddReviewView.as_view(), name='reviews'),
    path('<int:book_id>/<int:review_id>/edit/', EditReviewView.as_view(), name='edit_review'),
    path(
        '<int:book_id>/<int:review_id>/confirm_delete_review/',
        ConfirmDeleteReviewView.as_view(),
        name='confirm_delete_review'
    ),
    path(
        '<int:book_id>/<int:review_id>/delete_review/',
        DeleteReviewView.as_view(),
        name='delete_review'
    )
]
