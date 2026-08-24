from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django_registration.backends.activation.views import ActivationView, RegistrationView
from django.urls import reverse_lazy


app_name = 'users'

urlpatterns = [
    path(
        '<int:user_id>', 
        views.profile, 
        name='profile'
    ),
    path(
        'favorites',
        views.favorites,
        name='favorites'
    ),
    path(
        'settings',
        views.settings,
        name='settings'
    ),
    path(
        'login',
        auth_views.LoginView.as_view(
            template_name='users/login.html'
        ),
        name='login'
    ),
    path(
        'logout',
        auth_views.LogoutView.as_view(
            next_page='poems:home'
        ),
        name='logout'
    ),
]

# При обновлении модуля django_registration перепроверить пути \/

# Важно: имена трогать не стоит!

django_registration_urlpatterns = [
    path(
        'activate/complete/',
        TemplateView.as_view(
            template_name='users/activation_complete.html',
        ),
        name='django_registration_activation_complete', 
    ),
    path(
        'activate/',
        ActivationView.as_view(
            template_name='users/activate.html',
            success_url=reverse_lazy('users:django_registration_activation_complete')
        ),
        name='django_registration_activate',
    ),
    path(
        'register/',
        RegistrationView.as_view(
            template_name='users/register.html',
            email_subject_template='users/activation_email_subject.txt',
            email_body_template='users/activation_email_body.txt',
            success_url=reverse_lazy('users:django_registration_complete'),
            disallowed_url=reverse_lazy('users:django_registration_disallowed'),
        ),
        name='django_registration_register',
    ),
    path(
        'register/complete/',
        TemplateView.as_view(
            template_name='users/registration_complete.html',
        ),
        name='django_registration_complete',
    ),
    path(
        'register/closed/',
        TemplateView.as_view(
            template_name='users/registration_closed.html',
        ),
        name='django_registration_disallowed',
    ),
]

urlpatterns += django_registration_urlpatterns

# Я впечатлен разработчиком, что создавал этот модуль, ведь он решил отойти от стандартных меодов активации с GET запросом и вставить в версиях 5.1+ POST!!!
# Около 3-4 часов ушло на то, чтобы понять в чем кроется проблема. Я успел за это время перелопатить все кишки этому модулю, везде вписывал принты, дебажил
# разобрался как работает механизм этой активации и шифрования, потратил ТОННУ нервов и все это из-за того, что я не изменения модуля относительно прошлых записей
# Пускай это тут лежит, обожаю django-registration. Лучший модуль, что я запомню на век. Мало того что он хардкодит пути к тэмплэйтам и не гибок, так он еще
# и шикарную инструкцию имеет