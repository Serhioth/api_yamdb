from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter

from .permissions import IsAdminOrReadOnly


class CreateListDeleteModelMixin(CreateModelMixin, ListModelMixin,
                                 DestroyModelMixin, GenericViewSet):
    pass


class AttributesModelMixin(CreateListDeleteModelMixin):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
