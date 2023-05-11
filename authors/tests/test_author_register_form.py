from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

'''
unittest.TestCase é uma classe genérica de teste unitário que pode ser
usada em qualquer projeto Python, enquanto django.test.TestCase é uma 
classe específica para testes em projetos Django que inclui recursos 
adicionais específicos do framework.
'''


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Type your first name'),
        ('last_name', 'Type your last name'),
        ('username', 'Your username'),
        ('email', 'Type your email'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        )),
        ('email', 'The e-mail must be valid'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_help_text_is_correct(self, field, needed):
        '''
        needed guarda os valores dos campos definidos em parameterized
        current captura os help text dos campos do form real
        '''
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Type your email'),
        ('password', 'Password must not be empty'),
        ('password2', 'Repeat your password')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

        '''
            - data=self_data encaminha o dado criado sem self.form_data para
            preencher o form chamado pelo self.client.post

            - follow=True é para a response continuar a execução, no caso
            ela para quando chega no redirec na view e é de nosso interesse
            que prossiga

            - msg é a mensagem definida no parameterized e também é a mensagem
            gerada no template quando tentamos enviar o forms com um campo 
            vazio
        '''

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'luc'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have less than 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_uper_caso_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_if_email_is_being_used_another_user(self):
        user1 = {
            'username': 'zoro',
            'first_name': 'Roronoa',
            'last_name': 'Sola',
            'email': 'zoro@gmail.com',
            'password': '#Naruto123',
            'password2': '#Naruto123'
        }

        user2 = user1
        user2['username'] = 'zorinho'

        url = reverse('authors:create')
        self.client.post(url, user1)
        response = self.client.post(url, user2, follow=True)
        self.assertIn('Email já em uso', response.context['form'].errors.get('email'))
        self.assertIn('Email já em uso', response.content.decode('utf-8'))
