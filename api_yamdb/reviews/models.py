from django.contrib import auth
from django.core import validators
from django.db import models

from .validators import validate_year

User = auth.get_user_model()


class Category(models.Model):
    """Модель категории."""

    name = models.CharField('Имя категории', max_length=200)
    slug = models.SlugField('Слаг категории', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField('Имя жанра', max_length=200)
    slug = models.SlugField('Слаг жанра', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название произведения', max_length=200, db_index=True
    )
    year = models.IntegerField('Год', validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        'Описание', max_length=255, null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        through='GenreTitle',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель взаимосвязи произведения и жанров."""

    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True
    )


class Published(models.Model):
    """Базовый класс для публикаций (отзывов, комментариев)."""

    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('Опубликовано', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(Published):
    """Отзыв на произведение."""

    score = models.SmallIntegerField(
        'Оценка',
        validators=[
            validators.MaxValueValidator(
                10, message='Оценка не может быть больше 10.'),
            validators.MinValueValidator(
                1, message='Оценка не может быть меньше 1.'),
        ]
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE,
    )

    class Meta(Published.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='only_one_review_per_author'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.pk} на "{self.title}"'


class Comment(Published):
    """Комментарий к отзыву на произведение."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta(Published.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.pk} на отзыв {self.review.pk}'
