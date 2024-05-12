from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.validators import check_username, check_user_is_not_registred

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def __init__(self, *args, **kwargs):
        """
        Переопределение свойства поля role,
        в зависимости от статуса пользователя
        """
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.is_admin:
            self.fields['role'].read_only = True

    def validate_username(self, value):
        """
        Проверка, что имя пользователя
        соответствует требованиям для регистрации
        """
        if not check_username(value):
            raise serializers.ValidationError(
                {'ошибка регистрации':
                    'Имя пользователя не может быть Me, '
                    'содержит недопустимые символы, '
                    'либо превышает допустимую длину в 150 символов'}
            )
        return value


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации новых пользователей"""
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        """
        Проверка, что имя пользователя
        соответствует требованиям для регистрации
        """
        if not check_username(value):
            raise serializers.ValidationError(
                {'ошибка регистрации':
                    'Имя пользователя не может быть Me, '
                    'содержит недопустимые символы, '
                    'либо превышает допустимую длину в 150 символов'}
            )
        return value

    def validate(self, attrs):
        """
        Проверка, что пользователь не регистрируется
        с занятым почтовым ящиком или юзернеймом
        """
        email = attrs.get('email')
        username = attrs.get('username')
        if not check_user_is_not_registred(
            email=email,
            username=username
        ):
            raise serializers.ValidationError(
                {'ошибка регистрации':
                 f'Пользователь с таким {username} '
                 f'или {email} уже зарегестрирован'}
            )
        return super().validate(attrs)


class UserGetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи токенов"""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
