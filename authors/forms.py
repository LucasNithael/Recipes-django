import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


'''def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()
'''

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    '''
    Essa função inicializadora permite sobreescrever
    auterações da classe Meta sem desabilitar 
    configurações já feitas

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.:Lucas')
        add_placeholder(self.fields['last_name'], 'Ex.: Nithael')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    '''
    '''
    Podemos criar um novo campo dessa forma abaixo
    '''
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        }),
        label='Password2'
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
        },
        validators=[strong_password]

    )

    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name',
        },
        label='First name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your first name',
        })
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name',
        },
        label='Last name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your last name'
        })
    )

    email = forms.CharField(
        error_messages={
            'required': 'E-mail is required',
        },
        label='Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your email'
        }),
        help_text='The e-mail must be valid',
    )

    username = forms.CharField(
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
        }),
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        min_length=4, max_length=150,
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

    '''    labels = {
            'username': 'Username',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            },
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Your username',
            }),
        }'''

    '''def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'Atenção' in data:
            raise ValidationError(
                'Não digite "Atenção"',
                code='invalid'
            )

        return data
    '''
    
    def clean(self):
        '''
        Método para pegar todos os campos da classe mãe
        cleaned_data = super().clean()
        '''
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            error = ValidationError(
                'Senhas não correspondem',
                code='invalid',
            )
            raise ValidationError({
                'password': error,
                # Posso mandar um dicionário com erros tbm
                'password2': [
                    error,
                    'Outro error'
                ],
                # 'password2': 'Não corresponde ao primeiro password'
            })
