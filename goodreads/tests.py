from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        user = CustomUser.objects.create(
            first_name='Rano', last_name='Berdiyorova', username='baxromovna', email='berdiyorova@gmail.com'
        )
        user.set_password('somepass')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='Nice book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment='Useful book')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Very good book')

        response = self.client.get(reverse('home_page') + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
