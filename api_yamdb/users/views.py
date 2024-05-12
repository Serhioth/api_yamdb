from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api_yamdb.settings import HOST_EMAIL
from users.serializers import (SignUpSerializer, UserGetTokenSerializer,
                               UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели User,
    обрабатывает энд-пойнты users, users/<username> и /me
    """
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def edit_profile(self, request):
        """Действие для обработки эндпойнта /me"""
        if request.method == 'GET':
            serializer = UserSerializer(
                request.user,
                context={'request': request}
            )
            return Response(
                data=serializer.data,
                status=HTTPStatus.OK
            )
        serializer = UserSerializer(
            request.user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data
        )


def generate_confiramtion_code(signed_user, email):
    """Функция генерации и отправки верификационных кодов"""
    token = default_token_generator.make_token(signed_user)
    return send_mail(
        'Код авторизации для YAMDB',
        f'''
        {token}
        Ваш код авторизации, используйте его, чтобы получить свой токен
        ''',
        HOST_EMAIL,
        [email],
        fail_silently=False,
    )


@api_view(['POST'])
def send_confirmation_code(request):
    """
    Вью функция для создания нового пользователя,
    либо для отправки верификационного кода уже существующему
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    signed_user, created = User.objects.get_or_create(
        email=email,
        username=username
    )
    generate_confiramtion_code(
        signed_user=signed_user,
        email=email
    )
    return Response(
        data=serializer.data,
        status=HTTPStatus.OK
    )


@api_view(['POST'])
def get_token(request):
    """Вью-функция для генерации и отправки JWT-токенов"""
    serializer = UserGetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)},
            status=HTTPStatus.OK
        )
    return Response(
        {'ошибка верификационного кода': 'неверный верификационный код'},
        status=HTTPStatus.BAD_REQUEST
    )
