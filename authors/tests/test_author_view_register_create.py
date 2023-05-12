from django.test import TestCase
from django.urls import reverse


class AuthorRegiterCreateView(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'ZoroSola',
            'first_name': 'Zoro',
            'last_name': 'Roronoa',
            'email': 'email@anyemail.com',
            'password': '#Zoro321',
            'password2': '#Zoro321',
        }
        return super().setUp(*args, **kwargs)

    def test_if_user_is_valid(self):
        user = self.form_data

        url_create = reverse('authors:create')
        response = self.client.post(url_create, user)

        url_register = reverse('authors:register')
        response = self.client.get(url_register)

        msg = 'Your use is created, you can login'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_if_register_create_is_not_post(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_can_login_system(self):
        user = self.form_data
        url = reverse('authors:create')
        self.client.post(url, user, follow=True)

        '''Variável booleana'''
        login = self.client.login(
            username='ZoroSola',
            password='#Zoro321'
        )

        '''Mesma assert'''
        self.assertIs(login, True)
        self.assertTrue(login)
