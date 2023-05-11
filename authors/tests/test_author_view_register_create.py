from django.test import TestCase
from django.urls import reverse


class AuthorRegiterCreateView(TestCase):
    def test_if_user_is_valid(self):
        user = {
            'username': 'zoro',
            'first_name': 'Roronoa',
            'last_name': 'Sola',
            'email': 'zoro@gmail.com',
            'password': '#Naruto123',
            'password2': '#Naruto123'
        }

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