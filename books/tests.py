from django.contrib import messages
from django.test import TestCase, RequestFactory
from django.urls import reverse

from books.forms import BookReviewForm
from books.models import Book, Author, BookAuthor, BookReview
from users.models import CustomUser


class BooksTestCase(TestCase):

    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response, 'Books Not Found.')

    def test_books_list(self):
        book1 = Book.objects.create(title='book1', description='description1', isbn='123123')
        book2 = Book.objects.create(title='book2', description='description2', isbn='111111')
        book3 = Book.objects.create(title='book3', description='description3', isbn='222222')
        book4 = Book.objects.create(title='book4', description='description4', isbn='333333')

        response = self.client.get(reverse('books:list') + "?page_size=3")

        for book in [book1, book2, book3]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('books:list') + "?page=2&page_size=3")

        self.assertContains(response, book4.title)


    def test_book_detail(self):
        book = Book.objects.create(title='book1', description='description1', isbn='123123')
        author1 = Author.objects.create(first_name='James', last_name="Collins", email='collins@gmail.com')
        author2 = Author.objects.create(first_name='Lisa', last_name="Braun", email='braun@gmail.com')
        BookAuthor.objects.create(book=book, author=author1)
        BookAuthor.objects.create(book=book, author=author2)

        book_authors = book.bookauthor_set.all()
        print(book_authors)

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        for book_author in book_authors:
            self.assertContains(response, book_author.author.full_name())



    def test_search_books(self):
        book1 = Book.objects.create(title='Sport', description='description1', isbn='123123')
        book2 = Book.objects.create(title='Guide', description='description2', isbn='111111')
        book3 = Book.objects.create(title='Shoe Dog', description='description3', isbn='222222')

        response = self.client.get(reverse('books:list') + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?q=guide")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?q=shoe")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)





class BookReviewsTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        self.user = CustomUser.objects.create(first_name='Rano', last_name='Berdiyorova', username='baxromovna',
                                         email='berdiyorova@gmail.com')
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='baxromovna', password='somepass')


    def test_book_reviews(self):
        response = self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                                    data={
                                        'stars_given': 3,
                                        'comment': 'Nice book'
                                    }
                                    )
        book_reviews = self.book.reviews.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, self.book)
        self.assertEqual(book_reviews[0].user, self.user)


    def test_stars_greater_than_5(self):
        response = self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                                    data={'stars_given': 6,
                                          'comment': 'Nice book'
                                          }
                                    )
        self.assertFormError(
            response,
            'review_form',
            'stars_given',
            'Ensure this value is less than or equal to 5.'
        )


    def test_stars_less_than_1(self):
        response = self.client.post(reverse('books:reviews', kwargs={'id': self.book.id}),
                                    data={'stars_given': 0,
                                          'comment': 'Nice book'
                                          }
                                    )
        self.assertFormError(
            response,
            'review_form',
            'stars_given',
            'Ensure this value is greater than or equal to 1.'
        )


    def test_edit_review_get(self):
        review = BookReview.objects.create(book=self.book, user=self.user, stars_given=5, comment='Nice book')
        response = self.client.get(reverse(
            'books:edit_review',
            kwargs={'book_id': self.book.id, 'review_id': review.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/edit_review.html')
        self.assertEqual(response.context['book'], self.book)
        self.assertEqual(response.context['review'], review)
        self.assertIsInstance(response.context['review_form'], BookReviewForm)


    def test_edit_review_post(self):
        review = BookReview.objects.create(book=self.book, user=self.user, stars_given=5, comment='Nice book')
        response = self.client.post(reverse(
            'books:edit_review',
            kwargs={'book_id': self.book.id, 'review_id': review.id}),
            data={
                'stars_given': 4,
                'comment': 'New comment'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:detail', kwargs={'id': self.book.id}))
        review.refresh_from_db()
        self.assertEqual(review.comment, 'New comment')
        self.assertEqual(review.stars_given, 4)


    def test_confirm_delete_review(self):
        review = BookReview.objects.create(book=self.book, user=self.user, stars_given=5, comment='Nice book')
        response = self.client.get(reverse(
            'books:confirm_delete_review',
            kwargs={'book_id': self.book.id, 'review_id': review.id}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, review.comment)
        self.assertContains(response, 'Are your sure you want to delete this review?')


    def test_delete_review(self):
        review = BookReview.objects.create(book=self.book, user=self.user, stars_given=5, comment='Nice book')
        factory = RequestFactory()
        response = self.client.get(reverse(
            'books:delete_review',
            kwargs={'book_id': self.book.id, 'review_id': review.id}
        ))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:detail', kwargs={'id': self.book.id}))
        self.assertFalse(BookReview.objects.filter(id=review.id).exists())
