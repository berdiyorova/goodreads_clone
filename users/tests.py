from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):

    def test_user_account_is_created(self):
        self.client.post(  # client - so'rov yuborayotgan brauserni aniqlab beradi
            reverse('users:register'),  # url ko'rsatiladi
            data={  # forma fieldlaridan kelayotgan data
                'username': 'rano',
                'first_name': "Ra'no",
                'last_name': 'Berdiyorova',
                'email': 'berdiyorova@gmail.com',
                'password': 'rrshv1719'
            }
        )

        user = CustomUser.objects.get(username='rano')

        self.assertEqual(user.first_name, "Ra'no")
        self.assertEqual(user.last_name, "Berdiyorova")
        self.assertEqual(user.email, 'berdiyorova@gmail.com')
        self.assertNotEqual(user.password, 'rrshv1719')
        self.assertTrue(user.check_password('rrshv1719'))


    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': "Ra'no",
                'email': 'berdiyorova@gmail.com'
            }
        )
        user_count = CustomUser.objects.count()  # test funksiya ishlaganda userni saqlash uchun vaqtinchalik yangi
        # ma'lumotlar bazasini yaratadi bu holatda required
        # fieldlar to'ldirilmaganligi uchun user saqlanmasligi kk va
        self.assertEqual(user_count, 0)  # user_count=0 bo'lishi kk

        self.assertFormError(response, 'form', 'username', 'This field is required.')
        # fieldni backenddagi xatosini to'g'ri yozish kk
        # This field is required!  deb yozilsa ham test xato ishlaydi.
        self.assertFormError(response, 'form', 'password', 'This field is required.')


    def test_invalid_email(self):
        response = self.client.post(
                    reverse('users:register'),
                    data={
                        'username': 'rano',
                        'first_name': "Ra'no",
                        'last_name': 'Berdiyorova',
                        'email': 'berdiyorova@gmail',
                        'password': 'rrshv1719'
                    }
                )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


    def test_unique_username(self):
        # self.client.post(         # user client dan post() qilindi
        #     reverse('users:register'),
        #     data={
        #         'username': 'rano',
        #         'first_name': "Ra'no",
        #         'last_name': 'Berdiyorova',
        #         'email': 'berdiyorova@gmail.com',
        #         'password': 'rrshv1719'
        #     }
        # )

        # user Django ORM dan foydalanib yaratildi.
        user = CustomUser.objects.create(username='rano', first_name="Ra'no")
        user.set_password('rrshv1719')
        user.save()

        response = self.client.post(
                    reverse('users:register'),
                    data={
                        'username': 'rano',
                        'first_name': "Visola",
                        'last_name': 'Samadova',
                        'email': 'samadova@gmail.com',
                        'password': 'somepassword'
                    }
                )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')




class LoginTestCase(TestCase):

    def setUp(self):
        # setUp() funksiya har bitta test funksiya ishlashidan oldin chaqiriladi  (DRY -- Don't Repeat Yourself)
        self.db_user = CustomUser.objects.create(username='ramazon90')  # user bazada yaratilyapti
        self.db_user.set_password('Xurramov2604')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'ramazon90',
                'password': 'Xurramov2604'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong-username',
                'password': 'Xurramov2604'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'ramazon90',
                'password': 'wrong-password'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_successful_logout(self):
        self.client.login(username='ramazon90', password='Xurramov2604')

        self.client.get(reverse('users:logout'))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)




class ProfileTestCase(TestCase):

    def test_login_redirect(self):
        response = self.client.get(reverse('users:profile'))

        # login qilmagan userning login pagega redirect qilinganligini 2 xil usulda tekshirish mumkin:
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')
        self.assertEqual(response.status_code, 302)

    def test_profile_detatil(self):
        user = CustomUser.objects.create(first_name='Ramazon', last_name='Xurramov', username='ramazon90',
                                         email='xurramov@gmail.com')
        user.set_password('somepassword')
        user.save()

        self.client.login(username='ramazon90', password='somepassword')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.username)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(first_name='Ramazon', last_name='Xurramov', username='ramazon90',
                                         email='xurramov@gmail.com')
        user.set_password('somepassword')
        user.save()

        self.client.login(username='ramazon90', password='somepassword')

        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'first_name': 'Ramazon',
                'last_name': 'Xurramov',
                'username': 'ramazon2604',
                'email': 'xurramov90@mail.ru'
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.username, 'ramazon2604')
        self.assertEqual(user.email, 'xurramov90@mail.ru')
        self.assertEqual(response.url, reverse('users:profile'))
