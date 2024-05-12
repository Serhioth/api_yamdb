from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title
from .filters import TitleFilter
from .mixins import AttributesModelMixin
from .permissions import ReviewCommentPermission, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadOnlySerializer,
    TitleWriteSerializer,
    BaseReviewSerializer,
    ReviewCreateSerializer,
    CommentSerializer,
)


class CategoryViewSet(AttributesModelMixin):
    """Возвращает список всех категорий. Доступно без токена."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AttributesModelMixin):
    """Возвращает список жанров. Доступно без токена."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Возвращает список произведений. Доступно без токена."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadOnlySerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """Обработчик CRUD-запросов к модели Review."""

    permission_classes = (ReviewCommentPermission,)

    def get_serializer_class(self):
        """Возвращает требуемый класс сериализатора в зависимости от
        исполняемой операции.
        """
        if self.action == 'create':
            return ReviewCreateSerializer
        return BaseReviewSerializer

    def get_queryset(self):
        """Возвращает кверисет, состоящий из отзывов к произведению,
        заданному в URL запроса.
        """
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создаёт объект модели (отзыв)."""
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        """Возвращает произведение, заданное в URL запроса."""
        return get_object_or_404(Title, pk=self.kwargs['title_id'])


class CommentViewSet(ModelViewSet):
    """Обработчик CRUD-запросов к модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        """Возвращает кверисет, состоящий из комментариев к отзыву,
        заданному в URL запроса.
        """
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создаёт объект модели (комментарий)."""
        serializer.save(author=self.request.user, review=self.get_review())

    def get_review(self):
        """Возвращает отзыв, заданный в URL запроса."""
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return get_object_or_404(title.reviews, pk=self.kwargs['review_id'])
