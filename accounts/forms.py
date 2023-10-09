from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from allauth.account.forms import SignupForm
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, mail_admins


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name='common users')
        user.groups.add(common_users)

        # отправка электропочты
        # send_mail(
        #     subject='Добро пожаловать в наш интернет-магазин',
        #     message=f'{user.username}, Вы успешно зарегистрировались!',
        #     from_email=None,  # будет использоваться значение DEFAULT_FROM_EMAIL
        #     recipient_list=[user.email],
        # )
        # проверил, получилось

        # теперь отправка электропочты в HTML формате
        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, Вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        # # Рассылка менеджерам
        # mail_managers(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь {user.username} зарегистрировался на сайте.'
        # )
        #
        # # Рассылка админам
        # mail_admins(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь {user.username} зарегистрировался на сайте.'
        # )

        return user
