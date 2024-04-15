from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Book, BookReview
from .forms import BookReviewForm


# class BooksListView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 3

class BooksListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')

        search_query = request.GET.get('q', '')
        if search_query:
            books = Book.objects.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 3)
        paginator = Paginator(books, page_size)

        # default bo'yicha page_num birinchi pageni olib beradi
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(request,
                      'books/list.html',
                      {
                          'page_obj': page_obj,
                          'search_query': search_query
                       }
                      )



# class BookDetailView(DetailView):
#     template_name = 'books/detail.html'
#     pk_url_kwarg = 'id'
#     model = Book

class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        review_form = BookReviewForm()
        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})



class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        context = {
            'book': book,
            'review': review,
            'review_form': review_form
        }
        return render(request, 'books/edit_review.html', context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        context = {
            'book': book,
            'review': review,
            'review_form': review_form
        }

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/edit_review.html', context)



class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        context = {
            'book': book,
            'review': review
        }
        return render(request, 'books/confirm_delete_review.html', context)



class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)

        review.delete()
        messages.success(request, 'You have successfully deleted this review.')

        return redirect(reverse('books:detail', kwargs={'id': book.id}))
