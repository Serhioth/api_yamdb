from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class BaseReviewSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели Review.
    Без дополнительных проверок.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)


class ReviewCreateSerializer(BaseReviewSerializer):
    """Сериализатор для модели Review, используемый при создании нового
    элемента.
    Запрещает создание автором более оного отзыва на произведение.
    """

    def validate(self, attr):
        view = self.context['view']
        if view.get_queryset().filter(author=view.request.user).exists():
            raise serializers.ValidationError(
                'Нельзя дать на произведение более одного отзыва.')

        return attr


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
