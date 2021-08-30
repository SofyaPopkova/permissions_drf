from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from models import Advertisement
from serializers import AdvertisementSerializer
from filters import AdvertisementFilter
from permissions import DefaultPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.queryset = Advertisement.objects.filter(~Q(status="OPEN"))
        elif request.user.is_superuser:
            self.queryset = Advertisement.objects.all()
        else:
            self.queryset = Advertisement.objects.filter(~Q(status="OPEN") | Q(creator=request.user))

        return super().list(self, request, *args, **kwargs)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [DefaultPermission]
        else:
            permissions = []
        return [permission() for permission in permissions]