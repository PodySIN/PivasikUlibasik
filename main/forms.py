from django import forms


class RegistrationForm(forms.Form):
    Username = forms.CharField(
        label="Имя пользователя",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Имя",
            }
        ),
    )
    Password = forms.CharField(
        label="Пароль",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль",
            }
        ),
    )
    RepeatPassword = forms.CharField(
        label="Повтор пароля",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Повтор пароля",
            }
        ),
    )


class LoginForm(forms.Form):
    """
    Форма для входа пользователя
    """

    username = forms.CharField(
        max_length=64,
        required=True,
        label="Логин",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Логин",
            }
        ),
    )
    password = forms.CharField(
        max_length=64,
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль",
            }
        ),
    )
