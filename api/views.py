from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(GenericViewSet, CreateModelMixin, ListModelMixin,
                     RetrieveModelMixin, UpdateModelMixin):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
