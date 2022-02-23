# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_text, force_bytes
#
# from .serializers import (RegisterSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer,
#                           ForgotPasswordSerializer, ForgotPasswordCompleteSerializer)
# from .tasks import send_activation_email
# User = get_user_model()
#
#
# class RegistrationView(APIView):
#     # def post(self, request):
#     #     data = request.data
#     #     serializer = RegisterSerializer(data=data)
#     #     if serializer.is_valid(raise_exception=True):
#     #         serializer.save()
#     #         return Response("Вы успешно зарегистрированы!", status=status.HTTP_201_CREATED)
#
#
#     def post(self, request):
#         data = request.data
#         serializer = RegisterSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.create()
#             # print(user.pk)
#             message = f'Вы успешно зарегистрированы. ' \
#                       f'Вам отправлено письмо с активацией'
#             current_site = get_current_site(request)
#             email_message = render_to_string("account_activate_email.html", {
#                 "user": user,
#                 "domain": current_site.domain,
#                 "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                 "token": user.generate_activation_code()
#             })
#             send_activation_email.delay(user.email, email_message)
#
#             return Response(message, status=201)
#
# # class ActivateView(APIView):
# #     def get(self, request, activation_code):
# #         User = get_user_model()
# #         user = get_object_or_404(User, activation_code=activation_code)
# #         user.is_active = True
# #         user.activation_code = ''
# #         user.save()
# #         return Response("Активация прошла успешно!", status=status.HTTP_200_OK)
# def activate(request, uid, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uid))
#         user = User.objects.get(pk=uid)
#     except (ValueError, TypeError, OverflowError, User.DoesNotExist):
#         user = None
#     if user:
#         if user.check_token(token):
#             user.is_active = True
#             user.activation_code = ''
#             user.save()
#             return HttpResponse("Активация прошла успешно")
#     return HttpResponse("Ссылка для активации неправильная")
#
#
# class LoginView(ObtainAuthToken):
#     serializer_class = LoginSerializer
#
#
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]  # проверка на наличие права
#
#     def post(self, request):
#         user = request.user
#         Token.objects.filter(user=user).delete()
#         return Response('Вы успешно разлогинились')
#
#
# class ChangePasswordView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         data = request.data
#         serializer = ChangePasswordSerializer(data=data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.set_new_pass()
#         return Response('Пароль успешно обновлен')
#
#
# class ForgotPasswordView(APIView):
#
#     def post(self, request):
#         data = request.data
#         serializer = ForgotPasswordSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.send_code()
#         return Response('Вам отправлено письмо для восстановления пароля')
#
#
# class ForgotPasswordComlete(APIView):
#
#     def post(self, request):
#         data = request.data
#         serializer = ForgotPasswordCompleteSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.set_new_pass()
#         return Response('Пароль успешно обновлен')


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered', status=201)


class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Your account activated!', status=200)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = MyUser.objects.filter(phone_number=phone_number, activation_code=code).first()
        if not user:
            return Response('There is no such user', status=400)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('You activate your account', status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Logged out', status=200)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Пароль успешно обновлён')


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено письмо для восстановления пароля')


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Пароль успешно обновлён')