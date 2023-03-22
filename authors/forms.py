from django import forms
from django.contrib.auth.models import User


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):
    '''
    Essa função inicializadora permite sobreescrever
    auterações da classe Meta sem desabilitar 
    configurações já feitas
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')

    '''
    Podemos criar um novo campo dessa forma abaixo
    '''
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        })
    )

    '''
    Aqui estou sobreescrevendo as configurações do password 
    feitas na classe Meta. Essa forma de configurações
    desabilita todas auterações realizadas na classe Meta
    '''
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
        }),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={
            'required': 'Password must not be empty',
        }

    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }

        error_messages = {
            'username': {
                'required': 'This field must be not empty',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your username here',
            })
        }
