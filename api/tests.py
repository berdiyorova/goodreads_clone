from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCate(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(first_name='Rano', last_name='Berdiyorova', username='baxromovna',
                                              email='berdiyorova@gmail.com')
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='baxromovna', password='somepass')

    def test_review_detail(self):
        book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')

        response = self.client.get(reverse('api:review_detail', kwargs={'id': book_review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], book_review.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'Nice book')

        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], book.title)
        self.assertEqual(response.data['book']['description'], book.description)
        self.assertEqual(response.data['book']['isbn'], book.isbn)

        self.assertEqual(response.data['user']['first_name'], self.user.first_name)
        self.assertEqual(response.data['user']['last_name'], self.user.last_name)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['user']['email'], self.user.email)


    # def test_review_list(self):
    #     user_two = CustomUser.objects.create(first_name='Ramazon', last_name='Xurramov', username='ramazon90',
    #                                        email='rxurramov@gmail.com')
    #     book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
    #
    #     br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')
    #     br_two = BookReview.objects.create(book=book, user=user_two, stars_given=3, comment='Not Good')
    #
    #     response = self.client.get(reverse('api:review_list'))
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data['results']), 2)
    #     self.assertEqual(response.data['count'], 2)
    #
    #
    #     self.assertEqual(response.data['results'][0]['id'], br_two.id)
    #     self.assertEqual(response.data['results'][0]['stars_given'], 3)
    #     self.assertEqual(response.data['results'][0]['comment'], 'Not Good')
    #     self.assertIn('next', response.data)
    #     self.assertIn('previous', response.data)
    #
    #     self.assertEqual(response.data['results'][1]['id'], br.id)
    #     self.assertEqual(response.data['results'][1]['stars_given'], 5)
    #     self.assertEqual(response.data['results'][1]['comment'], 'Nice book')


    def test_delete_review(self):
        book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')

        response = self.client.delete(reverse('api:review_detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())


    def test_patch_review(self):
        book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')

        response = self.client.patch(reverse('api:review_detail', kwargs={'id': br.id}), data={'stars_given': 4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)


    def test_put_review(self):
        book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')

        response = self.client.put(reverse('api:review_detail', kwargs={'id': br.id}),
                                   data={'stars_given': 4, 'comment': 'Very good book', 'book_id': book.id, 'user_id': self.user.id}
                                   )
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'Very good book')
        self.assertEqual(br.book_id, book.id)
        self.assertEqual(br.user_id, self.user.id)


    def test_create_review(self):
        book = Book.objects.create(title='title1', description='s=description1', isbn='12345678')
        data = {
            'stars_given': 3,
            'comment': 'Not bad',
            'book_id': book.id,
            'user_id': self.user.id
        }
        response = self.client.post(reverse('api:review_list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 3)
        self.assertEqual(br.comment, 'Not bad')
