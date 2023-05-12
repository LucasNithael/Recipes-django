from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


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

