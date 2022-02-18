#Поместите модель конфигурации jiango в переменные окружения системы, celery может вызвать модуль django
from Booking.celery import app
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

#  Определить задачи


@app.task
def send_password_change_email(user_name, to_email):
    """Отправить письмо смены пароля"""
    subject = "Рекомендуем вам менять пароли кажды 3 месяца, для смены пароля перейдите по ссылке ниже"  #  Заголовок
    # сообщения
    body = ""  #  Тело почты
    sender = settings.EMAIL_FROM  #  отправитель
    receivers = ['aman.abdyldaev@gmail.com']  #  Получатели
    html_body = 'Уважаемый пользователь, нажмите эту ссылку, чтобы сменить пароль ' #  html mail body
    send_mail(subject, body, sender, receivers, html_message=html_body)


@app.task
def send_activation_email(to_email, message):
    email = EmailMessage("Активация аккаунта", message, to=[to_email])
    email.send()
