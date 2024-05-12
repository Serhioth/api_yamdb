from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, send_confirmation_code, get_token
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

router = SimpleRouter()

router.register(
    r'users',
    UserViewSet,
    basename='user-list'
)
router.register(
    r'users\/[\w.@+-]+',
    UserViewSet,
    basename='user-detail'
)
router.register('categories', CategoryViewSet, basename='сategories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_token),
]
